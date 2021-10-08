from nasajon.pastas_contabeis.abstract_pasta_contabil import AbstractPastaContabil
from diario_unico.entity.documento import Documento
from diario_unico.enum.situacao import Situacao
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.enum.sinal import Sinal

from diario_unico.entity.item_documento import ItemDocumento
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from nasajon.entity.dados_integracao_pagamento_a_trabalhador import DadosIntegracaoPagamentoATrabalhador
from nasajon.util.objeto_util import ObjetosUtils
from nasajon.entity.pagamento_a_trabalhador import PagamentoATrabalhador, ItemPagamentoTrabalhador
from time_service.service.time_service import TimeService
from diario_unico.util.date_util import ultimoDiaMes
from datetime import date, datetime
from nasajon.entity.rubrica import Rubrica
from nasajon.enum.folha.rubrica_tipo_valor import RubricaTipoValor
from nasajon.util.lancamento_util import LancamentosUtil
from dateutil import relativedelta
from typing import List
import copy
from nasajon.util.diario_util import DiarioUtil
from diario_unico.entity.lancamento import Lancamento, SituacaoDiario
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from nasajon.pastas_contabeis.pastas_router import MomentoContabil
from nasajon.util.json_util import JsonUtil
from nasajon.util.repetir_exception import RepetirException
from nasajon.util.log import Log
from nasajon.entity.log_assincrono import LogAssincrono
import uuid
from nasajon.util.nasajon_factory import NasajonFactory
import re


class PastaFolha(AbstractPastaContabil):
    def __init__(self, diario_util: DiarioUtil):
        super().__init__(diario_util)
        self.documento_tipo: enum.Enum = DocumentoTipo.FOLHA
        self.item_tipo = ItemDocumentoTipo.DETALHE_FOLHA
        self.item_descricao = 'Detalhe de Folha de Pagamento'

    def simular(self, dados: dict):
        # TODO: O módulo de orçamentos será feito no futuro
        pass

    def get_dados_escrituracao_futura(self, _dados: dict):
        """
        Escrituação Futura da Folha de Pagamento baseada no histórico da folha
        Parametro:
            dados:
                estabelecimento: <str> Código do estabelecimento
                mes: <int> Mês de competencia
                ano: <int> Ano de competencia
                tenant: <int> Tenant
        """
        dados = _dados
        if "calculos" in _dados.keys():
            return _dados

        # Preparamos consulta ao diário
        data_final_consulta = ultimoDiaMes(
            date(_dados["ano"], _dados["mes"], 1) - relativedelta.relativedelta(months=1))
        data_inicial_consulta = (
            data_final_consulta - relativedelta.relativedelta(months=3)).replace(day=1)
        documentos_anteriores: List[Documento] = self._diario_util.recuperar_documentos_por_estabelecimento_tipo_data(
            _dados["tenant"], _dados["estabelecimento"], data_inicial_consulta, data_final_consulta, DocumentoTipo.FOLHA.value)
        documentos_anteriores = sorted(
            documentos_anteriores, key=lambda x: x.data_lancamento)
        documentos_anteriores.reverse()
        dados["documentos_anteriores"] = documentos_anteriores
        return dados

    def escriturar_futuro(self, _dados: dict):
        """
        Escrituação Futura da Folha de Pagamento baseada no histórico da folha
        Parametro:
            dados:
                estabelecimento: <str> Código do estabelecimento
                mes: <int> Mês de competencia
                ano: <int> Ano de competencia
                tenant: <int> Tenant
                documentos_anteriores: vetor de documentos
        """
        dados = _dados
        if "calculos" in dados.keys():
            return self.escriturar_futuro_ajuste(_dados)

        documentos_anteriores = [ObjetosUtils().dictToObject(
            d, Documento) for d in dados["documentos_anteriores"]]

        # Preparamos documentos a serem inseridos em formato de previsao
        docs = dict()
        for doc_anterior in documentos_anteriores:
            trabalhador = doc_anterior.participante  # Obtem o trabalhador
            if not trabalhador in docs.keys():  # Se o trabalhador ainda nao foi processado, entao processe
                doc = copy.deepcopy(doc_anterior)
                doc.itens = list()
                docs[trabalhador] = doc
            doc: Documento = docs[trabalhador]
            for item_anterior in doc_anterior.itens:
                # Se a rubrica nao foi processada, entao processe.
                if (not item_anterior.rubrica in [item2.rubrica for item2 in doc.itens]):
                    item = copy.deepcopy(item_anterior)
                    # Valor pela média
                    item.valor = sum([
                        item2.valor for doc2 in documentos_anteriores
                        for item2 in doc2.itens
                        if item2.trabalhador == item_anterior.trabalhador and item2.rubrica == item_anterior.rubrica
                    ]) / len([d for d in documentos_anteriores if d.itens[0].trabalhador == trabalhador])
                    item.valor = round(item.valor, 2)

                    for lanc in item.lancamentos:
                        for partida in lanc.partidas:
                            partida.valor = item.valor
                    doc.itens.append(item)

        # Repete a previsao para 12 meses
        data_base = date(_dados["ano"], _dados["mes"], 1)
        for i in range(0, 12):
            for doc in docs.values():
                doc = copy.deepcopy(doc)
                doc.data_lancamento = ultimoDiaMes(
                    data_base + relativedelta.relativedelta(months=i))
                doc.emissao = TimeService.now()
                doc.competencia_inicial = data_base + \
                    relativedelta.relativedelta(months=i)
                doc.competencia_final = doc.data_lancamento
                doc.data_pagamento = doc.data_lancamento
                doc.situacao = Situacao.PREVISTO
                doc.valor = sum([p.valor for i in doc.itens
                                 for l in i.lancamentos
                                 for p in l.partidas
                                 if p.conta_contabil == "1.1.1.01.0001" and p.natureza == "C"]) - sum(
                    [p.valor for i in doc.itens
                     for l in i.lancamentos
                     for p in l.partidas
                     if p.conta_contabil == "1.1.1.01.0001" and p.natureza == "D"])
                for item in doc.itens:
                    for lancamento in item.lancamentos:
                        lancamento.data = doc.data_lancamento
                        lancamento.situacao = SituacaoDiario.PREVISTO
                doc.documento = None
                self._diario_util.escriturar_antecipadamente_documento(
                    _dados["tenant"], doc)

    def escriturar_futuro_ajuste(self, _dados: DadosIntegracaoPagamentoATrabalhador, _escriturar_meses_futuros: bool = True):
        """
        Escrituação Futura da Folha de Pagamento baseada no cálculo da folha
        """
        dados = _dados

        if not isinstance(dados, DadosIntegracaoPagamentoATrabalhador):
            dados: DadosIntegracaoPagamentoATrabalhador = ObjetosUtils(
            ).dictToObject(dados, DadosIntegracaoPagamentoATrabalhador)
        if dados.verificarSeFaltaDadosAuxiliares() != None:
            raise Exception(dados.verificarSeFaltaDadosAuxiliares())

        for trabalhador in dados.trabalhadores:
            self._diario_util.cadastrarPessoa(
                trabalhador.cpf, trabalhador.nome, dados.tenant)
        pagamentos_por_trabalhador = dict()
        for c in dados.calculos:
            if not c.trabalhador in pagamentos_por_trabalhador.keys():
                pag: PagamentoATrabalhador = PagamentoATrabalhador()
                pag.tipo = self.documento_tipo
                pag.ano_competencia = dados.ano
                pag.mes_competencia = dados.mes
                pag.data_geracao = TimeService.now().date()
                data_ultima_mudanca = ultimoDiaMes(
                    date(pag.ano_competencia, pag.mes_competencia, 1))
                ultima_mudanca = dados.obtemMudanca(
                    c.trabalhador, data_ultima_mudanca)
                pag.estabelecimento = next(
                    e for e in dados.estabelecimentos if e.id == ultima_mudanca.estabelecimento).codigo
                pag.departamento = ultima_mudanca.departamento
                pag.lotacao = ultima_mudanca.lotacao
                pag.trabalhador = next(
                    t for t in dados.trabalhadores if t.id == c.trabalhador).cpf
                pag.trabalhador = re.sub("[^0-9]", '', pag.trabalhador)
                pag.data_pagamento = c.data_de_pagamento
                pagamentos_por_trabalhador[c.trabalhador] = pag

            pag = pagamentos_por_trabalhador[c.trabalhador]
            item = ItemPagamentoTrabalhador()
            item.rubrica = c.rubrica
            rubrica: Rubrica = next(
                r for r in dados.rubricas if r.id == c.rubrica)
            if RubricaTipoValor(rubrica.tipovalor) == RubricaTipoValor.RENDIMENTO:
                item.tipovalor = RubricaTipoValor.RENDIMENTO
            if RubricaTipoValor(rubrica.tipovalor) == RubricaTipoValor.DESCONTO:
                item.tipovalor = RubricaTipoValor.DESCONTO
            if RubricaTipoValor(rubrica.tipovalor) == RubricaTipoValor.BASE:
                continue
            item.descricao_rubrica = rubrica.nome

            item.dados_gerais = pag
            item.rubrica_esocial = rubrica.categoria
            definicoes = self.get_definicoes_lancamentos_escrituracao_futura_ajustes(
                item)
            item.valor = c.valor
            item.lancamentos = LancamentosUtil().criar_lancamentos(item, definicoes, None, None)
            item.dados_gerais = None
            pag.itens.append(item)

        for pag in pagamentos_por_trabalhador.values():
            doc = self.pagamentoATrabalhadorParaDocumento(pag)
            self._diario_util.escriturar_antecipadamente_documento(
                _dados["tenant"], doc)

        # previsao de meses futuros
        if _escriturar_meses_futuros:
            for e in dados.estabelecimentos:
                params = dict()
                params["estabelecimento"] = e.codigo
                if dados.mes == 12:
                    params["ano"] = dados.ano+1
                    params["mes"] = 1
                else:
                    params["ano"] = dados.ano
                    params["mes"] = dados.mes+1
                params["tenant"] = dados.tenant
                dados_escrituracao_futura = JsonUtil().toDict(
                    self.get_dados_escrituracao_futura(params))
                self.escriturar_futuro(dados_escrituracao_futura)


    def apropriar(self, dados):
        """
        Apropriação da Folha de Pagamento. Cuja única função é mudar o Status dos lançamentos
        Parametro:
            dados:
                estabelecimento: <str> Código do estabelecimento
                mes: <int> Mês de competencia
                ano: <int> Ano de competencia
                tenant: <int> Tenant
        """
        data_inicial = date(dados["ano"], dados["mes"], 1)
        data_final = ultimoDiaMes(data_inicial)
        documentos = self._diario_util.recuperar_documentos_por_estabelecimento_tipo_data(
            dados["tenant"], dados["estabelecimento"], data_inicial, data_final, DocumentoTipo.FOLHA)
        for doc in documentos:
            doc.situacao = Situacao.REALIZADO
            for item in doc.itens:
                for lancamento in item.lancamentos:
                    for partida in lancamento.partidas:
                        if partida.definicao in ['FOLHA.APROPRIACAO.PASSIVO', 'FOLHA.APROPRIACAO.DESPESA']:
                            lancamento.situacao = SituacaoDiario.REALIZADO
            self._diario_util.apropriar_documento(dados["tenant"], doc)

    def pagamentoATrabalhadorParaDocumento(self, pag: PagamentoATrabalhador):
        doc = Documento()
        doc.ano = pag.ano_competencia
        doc.competencia_inicial = date(
            pag.ano_competencia, pag.mes_competencia, 1)
        doc.competencia_final = ultimoDiaMes(doc.competencia_inicial)
        doc.data_criacao = TimeService.now()
        doc.data_entrada = pag.data_geracao
        doc.data_lancamento = doc.competencia_final
        doc.emissao = doc.data_criacao
        doc.estabelecimento = pag.estabelecimento
        doc.participante = pag.trabalhador
        doc.numero = "01"
        doc.sinal = Sinal.SAIDA
        doc.situacao = Situacao.PREVISTO
        doc.tipo = DocumentoTipo.FOLHA
        doc.valor = sum([i.valor if RubricaTipoValor(
            i.tipovalor) == RubricaTipoValor.RENDIMENTO else i.valor*(-1) for i in pag.itens])
        for item in pag.itens:
            itemc = ItemDocumento()
            itemc.codigo = item.rubrica_esocial
            itemc.descricao = item.rubrica_esocial
            itemc.rubrica = item.rubrica
            itemc.rubrica_esocial = item.rubrica_esocial
            itemc.lancamentos = item.lancamentos
            itemc.tipo = self.item_tipo
            itemc.valor = item.valor
            itemc.trabalhador = pag.trabalhador
            itemc.departamento = pag.departamento
            itemc.lotacao = pag.lotacao
            doc.itens.append(itemc)
        return doc

    def get_definicoes_lancamentos_escrituracao_futura_ajustes(self, item: ItemPagamentoTrabalhador):
        saida = list()
        definicao_generica = DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=0,
            ordem=0,
            natureza='',
            conta='',
            historico='',
            formula='valor',
            formula_data='dados_gerais.data_pagamento',
            situacao=SituacaoDiario.PREVISTO,
            definicao=''
        )
        apropriacao_passivo = copy.deepcopy(definicao_generica)
        apropriacao_passivo.numero = 1
        apropriacao_passivo.conta = self.depara_rubrica_conta_passivo[item.rubrica_esocial]
        apropriacao_passivo.historico = item.descricao_rubrica
        apropriacao_passivo.definicao = 'FOLHA.APROPRIACAO.PASSIVO'

        apropriacao_despesa = copy.deepcopy(definicao_generica)
        apropriacao_despesa.numero = 1
        apropriacao_despesa.conta = self.depara_rubrica_conta_despesa[item.rubrica_esocial]
        apropriacao_despesa.historico = item.descricao_rubrica
        apropriacao_despesa.definicao = 'FOLHA.APROPRIACAO.DESPESA'

        pagamento_passivo = copy.deepcopy(definicao_generica)
        pagamento_passivo.numero = 2
        pagamento_passivo.conta = apropriacao_passivo.conta
        pagamento_passivo.historico = apropriacao_passivo.historico
        pagamento_passivo.definicao = 'FOLHA.PAGAMENTO.PASSIVO'

        pagamento_caixa = copy.deepcopy(definicao_generica)
        pagamento_caixa.numero = 2
        pagamento_caixa.conta = '1.1.1.01'
        pagamento_caixa.historico = 'Folha de Pagamento'
        pagamento_caixa.definicao = 'FOLHA.PAGAMENTO.PASSIVO'

        if item.tipovalor == RubricaTipoValor.RENDIMENTO:
            apropriacao_passivo.natureza = 'C'
            apropriacao_passivo.ordem = 2
            apropriacao_despesa.natureza = 'D'
            apropriacao_despesa.ordem = 1
            pagamento_caixa.ordem = 2
            pagamento_caixa.natureza = 'C'
            pagamento_passivo.ordem = 1
            pagamento_passivo.natureza = 'D'
            saida.append(apropriacao_despesa)
            saida.append(apropriacao_passivo)
            saida.append(pagamento_passivo)
            saida.append(pagamento_caixa)
        else:
            apropriacao_passivo.natureza = 'D'
            apropriacao_passivo.ordem = 1
            apropriacao_despesa.natureza = 'C'
            apropriacao_despesa.ordem = 2
            pagamento_caixa.ordem = 1
            pagamento_caixa.natureza = 'D'
            pagamento_passivo.ordem = 2
            pagamento_passivo.natureza = 'C'
            saida.append(apropriacao_passivo)
            saida.append(apropriacao_despesa)
            saida.append(pagamento_caixa)
            saida.append(pagamento_passivo)

        return saida

    depara_rubrica_conta_despesa = {
        "1000": "4.1.1.01.0015",
        "1002": "4.1.1.01.0006",
        "1003": "4.1.1.01.0012",
        "1004": "4.1.1.01.0012",
        "1005": "4.1.1.01.0015",
        "1007": "4.1.1.01.0015",
        "1009": "4.1.1.01.0015",
        "1010": "4.1.1.01.0015",
        "1011": "4.1.1.01.0015",
        "1020": "4.1.1.01.0009",
        "1021": "4.1.1.01.0009",
        "1022": "4.1.1.01.0009",
        "1023": "4.1.1.01.0009",
        "1024": "4.1.1.01.0009",
        "1040": "4.1.1.01.0015",
        "1041": "4.1.1.01.0015",
        "1099": "4.1.1.01.0015",
        "1201": "4.1.1.01.0015",
        "1202": "4.1.1.01.0015",
        "1203": "4.1.1.01.0015",
        "1204": "4.1.1.01.0015",
        "1205": "4.1.1.01.0015",
        "1206": "4.1.1.01.0015",
        "1207": "4.1.1.01.0015",
        "1208": "4.1.1.01.0015",
        "1209": "4.1.1.01.0015",
        "1210": "4.1.1.01.0015",
        "1211": "4.1.1.01.0015",
        "1213": "4.1.1.01.0015",
        "1215": "4.1.1.01.0015",
        "1230": "4.1.1.01.0015",
        "1299": "4.1.1.01.0015",
        "1300": "4.1.1.01.0015",
        "1350": "4.1.1.01.0015",
        "1351": "4.1.1.01.0015",
        "1352": "4.1.1.01.0015",
        "1401": "4.1.1.01.0015",
        "1402": "4.1.1.01.0015",
        "1403": "4.1.1.01.0015",
        "1404": "4.1.1.01.0015",
        "1405": "4.1.1.01.0003",
        "1406": "4.1.1.01.0003",
        "1407": "4.1.1.01.0003",
        "1409": "4.1.1.01.0015",
        "1410": "4.1.1.01.0015",
        "1601": "4.1.1.01.0015",
        "1602": "4.1.1.01.0015",
        "1620": "4.1.1.02",
        "1621": "4.1.1.02",
        "1629": "4.1.1.02",
        "1651": "4.1.1.01.0015",
        "1652": "4.1.1.01.0015",
        "1801": "4.1.1.01.0014",
        "1802": "4.1.1.01.0015",
        "1805": "4.1.1.02",
        "1810": "4.1.1.01.0017",
        "2501": "4.1.1.01.0015",
        "2510": "4.1.1.01.0015",
        "2901": "4.1.1.01.0015",
        "2902": "4.1.1.01.0016",
        "2920": "4.1.1.02",
        "2930": "4.1.1.01.0015",
        "3501": "4.1.1.03",
        "3505": "4.1.1.01.0015",
        "3506": "4.1.1.01.0015",
        "3508": "4.1.1.01.0015",
        "3509": "4.1.1.01.0015",
        "3520": "4.1.1.01.0015",
        "4010": "4.1.1.01.0015",
        "4050": "4.1.1.01.0015",
        "4051": "4.1.1.01.0011",
        "5001": "4.1.1.01.0011",
        "5005": "4.1.1.01.0011",
        "5501": "4.1.1.01.0011",
        "5504": "4.1.1.01.0011",
        "5510": "4.1.1.01.0013",
        "6000": "4.1.1.01.0005",
        "6001": "4.1.1.01.0011",
        "6002": "4.1.1.01.0011",
        "6003": "4.1.1.01.0005",
        "6004": "4.1.1.01.0005",
        "6006": "4.1.1.01.0009",
        "6007": "4.1.1.01.0009",
        "6101": "4.1.1.01.0005",
        "6102": "4.1.1.01.0005",
        "6103": "4.1.1.01.0005",
        "6104": "4.1.1.01.0005",
        "6105": "4.1.1.01.0005",
        "6106": "4.1.1.01.0005",
        "6107": "4.1.1.01.0005",
        "6129": "4.1.1.01.0005",
        "6901": "4.1.1.01.0005",
        "6904": "4.1.1.01.0005",
        "7001": "4.1.1.01.0015",
        "9200": "4.1.1.01.0015",
        "9201": "4.1.1.01.0015",
        "9203": "4.1.1.01.0015",
        "9208": "4.1.1.01.0015",
        "9209": "4.1.1.01.0015",
        "9210": "4.1.1.01.0015",
        "9211": "4.1.1.01.0015",
        "9213": "4.1.1.01.0015",
        "9214": "4.1.1.01.0011",
        "9216": "4.1.1.01.0017",
        "9217": "4.1.1.01.0015",
        "9218": "4.1.1.01.0015",
        "9219": "4.1.1.01.0003",
        "9220": "4.1.1.01.0014",
        "9221": "4.1.1.01.0009",
        "9222": "4.1.1.01.0015",
        "9226": "4.1.1.01.0009",
        "9230": "4.1.1.01.0015",
        "9231": "4.1.1.01.0015",
        "9232": "4.1.1.01.0015",
        "9233": "4.1.1.01.0015",
        "9250": "4.1.1.01.0015",
        "9254": "4.1.1.01.0015",
        "9255": "4.1.1.01.0015",
        "9258": "4.1.1.01.0015",
        "9260": "4.1.1.01.0015",
        "9270": "4.1.1.01.0005",
        "9290": "4.1.1.01.0015",
        "9299": "4.1.1.01.0015",
        "9901": "",
        "9902": "",
        "9903": "",
        "9904": "",
        "9905": "4.1.1.01.0015",
        "9906": "4.1.1.01.0015",
        "9908": "4.1.1.01.0010",
        "9910": "4.1.1.01.0015",
        "9911": "4.1.1.01.0003",
        "9930": "4.1.1.01.0015",
        "9931": "4.1.1.01.0015",
        "9932": "4.1.1.01.0015",
        "9933": "4.1.1.01.0015",
        "9938": "4.1.1.01.0015",
        "9939": "4.1.1.01.0015",
        "9950": "4.1.1.01.0012",
        "9951": "4.1.1.01.0012",
        "9989": "4.1.1.01.0015"
    }

    depara_rubrica_conta_passivo = {
        "1000": "2.1.2.03.0003",
        "1002": "2.1.2.03.0003",
        "1003": "2.1.2.03.0003",
        "1004": "2.1.2.03.0003",
        "1005": "2.1.2.03.0003",
        "1007": "2.1.2.03.0003",
        "1009": "2.1.2.03.0003",
        "1010": "2.1.2.03.0003",
        "1011": "2.1.2.03.0003",
        "1020": "2.1.2.03.0001",
        "1021": "2.1.2.03.0001",
        "1022": "2.1.2.03.0001",
        "1023": "2.1.2.03.0001",
        "1024": "2.1.2.03.0001",
        "1040": "2.1.2.03.0003",
        "1041": "2.1.2.03.0003",
        "1099": "2.1.2.03.0003",
        "1201": "2.1.2.03.0003",
        "1202": "2.1.2.03.0003",
        "1203": "2.1.2.03.0003",
        "1204": "2.1.2.03.0003",
        "1205": "2.1.2.03.0003",
        "1206": "2.1.2.03.0003",
        "1207": "2.1.2.03.0003",
        "1208": "2.1.2.03.0003",
        "1209": "2.1.2.03.0003",
        "1210": "2.1.2.03.0003",
        "1211": "2.1.2.03.0003",
        "1213": "2.1.2.03.0003",
        "1215": "2.1.2.03.0003",
        "1230": "2.1.2.03.0003",
        "1299": "2.1.2.03.0003",
        "1300": "2.1.2.03.0003",
        "1350": "2.1.2.03.0003",
        "1351": "2.1.2.03.0003",
        "1352": "2.1.2.03.0003",
        "1401": "2.1.2.03.0003",
        "1402": "2.1.2.03.0003",
        "1403": "2.1.2.03.0003",
        "1404": "2.1.2.03.0003",
        "1405": "2.1.2.03.0003",
        "1406": "2.1.2.03.0003",
        "1407": "2.1.2.03.0003",
        "1409": "2.1.2.03.0003",
        "1410": "2.1.2.03.0003",
        "1601": "2.1.2.03.0003",
        "1602": "2.1.2.03.0003",
        "1620": "2.1.2.03.0003",
        "1621": "2.1.2.03.0003",
        "1629": "2.1.2.03.0003",
        "1651": "2.1.2.03.0003",
        "1652": "2.1.2.03.0003",
        "1801": "2.1.2.03.0003",
        "1802": "2.1.2.03.0003",
        "1805": "2.1.2.03.0003",
        "1810": "2.1.2.03.0003",
        "2501": "2.1.2.03.0003",
        "2510": "2.1.2.03.0003",
        "2901": "2.1.2.03.0003",
        "2902": "2.1.2.03.0003",
        "2920": "2.1.2.03.0003",
        "2930": "2.1.2.03.0003",
        "3501": "2.1.2.03.0003",
        "3505": "2.1.2.03.0003",
        "3506": "2.1.2.03.0003",
        "3508": "2.1.2.03.0003",
        "3509": "2.1.2.03.0003",
        "3520": "2.1.2.03.0003",
        "4010": "2.1.2.03.0003",
        "4050": "2.1.2.03.0003",
        "4051": "2.1.2.03.0003",
        "5001": "2.1.2.03.0001",
        "5005": "2.1.2.03.0001",
        "5501": "2.1.2.03.0003",
        "5504": "2.1.2.03.0001",
        "5510": "2.1.2.01.0001",
        "6000": "2.1.2.03.0003",
        "6001": "2.1.2.03.0001",
        "6002": "2.1.2.03.0003",
        "6003": "2.1.2.03.0003",
        "6004": "2.1.2.03.0003",
        "6006": "2.1.2.03.0002",
        "6007": "2.1.2.03.0003",
        "6101": "2.1.2.03.0003",
        "6102": "2.1.2.03.0003",
        "6103": "2.1.2.03.0003",
        "6104": "2.1.2.03.0003",
        "6105": "2.1.2.03.0003",
        "6106": "2.1.2.03.0003",
        "6107": "2.1.2.03.0003",
        "6129": "2.1.2.03.0003",
        "6901": "2.1.2.03.0003",
        "6904": "2.1.2.03.0003",
        "7001": "2.1.2.03.0003",
        "9200": "2.1.2.03.0003",
        "9201": "2.1.2.01.0001",
        "9203": "2.1.2.02.0003",
        "9208": "2.1.2.03.0003",
        "9209": "2.1.2.03.0003",
        "9210": "2.1.2.03.0003",
        "9211": "2.1.2.03.0003",
        "9213": "2.1.2.03.0003",
        "9214": "2.1.2.03.0001",
        "9216": "2.1.2.03.0003",
        "9217": "2.1.2.03.0003",
        "9218": "2.1.2.03.0003",
        "9219": "2.1.2.03.0003",
        "9220": "2.1.2.03.0003",
        "9221": "2.1.2.03.0002",
        "9222": "2.1.2.03.0003",
        "9226": "2.1.2.03.0002",
        "9230": "2.1.2.03.0002",
        "9231": "2.1.2.03.0002",
        "9232": "2.1.2.03.0002",
        "9233": "2.1.2.03.0002",
        "9250": "2.1.2.03.0003",
        "9254": "2.1.2.03.0003",
        "9255": "2.1.2.03.0003",
        "9258": "2.1.2.03.0003",
        "9260": "2.1.2.03.0003",
        "9270": "2.1.2.03.0003",
        "9290": "2.1.2.03.0003",
        "9299": "2.1.2.03.0003",
        "9901": "",
        "9902": "",
        "9903": "",
        "9904": "",
        "9905": "2.1.2.03.0003",
        "9906": "2.1.2.03.0003",
        "9908": "2.1.2.01.0002",
        "9910": "2.1.2.03.0003",
        "9911": "2.1.2.03.0003",
        "9930": "2.1.2.03.0003",
        "9931": "2.1.2.03.0003",
        "9932": "2.1.2.03.0003",
        "9933": "2.1.2.03.0003",
        "9938": "2.1.2.02.0003",
        "9939": "2.1.2.03.0003",
        "9950": "2.1.2.03.0003",
        "9951": "2.1.2.03.0003",
        "9989": "2.1.2.03.0003"
    }

