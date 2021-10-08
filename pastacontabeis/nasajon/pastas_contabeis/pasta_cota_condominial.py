from dateutil import relativedelta

from nasajon.pastas_contabeis.abstract_pasta_contabil import AbstractPastaContabil
from nasajon.pastas_contabeis.abstract_pasta_contabil_composta import AbstractPastaContabilComposta
from nasajon.pastas_contabeis.pastas_router import MomentoContabil
from nasajon.pastas_contabeis.pasta_recorrente import PastaRecorrente

from nasajon.entity.cota_condominial import CotaCondominial
from nasajon.entity.dados_escrituracao_futura import DadosEscrituracaoFutura, DadosItem, ValoresAnteriores
from nasajon.enum.heuristica_projecao import HeuristicaProjecao
from nasajon.entity.definicao_info_pagamento import DefinicaoInfoPagamento
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from diario_unico.entity.documento import Documento
from diario_unico.enum.situacao import Situacao
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.enum.sinal import Sinal

from diario_unico.entity.item_documento import ItemDocumento
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from diario_unico.entity.lancamento import Lancamento, SituacaoDiario
from nasajon.entity.item_cota_condominial import ItemCotaCondominial
from nasajon.enum.condominios.tipo_item_cota_condominial import TipoItemCotaCondominial
from nasajon.entity.dados_faturamento import DadosFaturamento
from nasajon.entity.definicao_info_cobranca import DefinicaoInfoCobranca
from nasajon.entity.dados_cobranca import Dados_Cobranca
from nasajon.pastas_contabeis.pasta_quitacao_padrao import PastaQuitacaoPadrao
from diario_unico.enum.info_cobranca.situacao_info_cobranca import SituacaoInfoCobranca
from diario_unico.enum.info_pagamento.situacao_info_pagamento import SituacaoInfoPagamento
from diario_unico.util.diario_factory import DiarioUnicoFactory

from nasajon.util.diario_util import DiarioUtil
from nasajon.util.json_util import JsonUtil
from nasajon.util.lancamento_util import LancamentosUtil
from nasajon.util.objeto_util import ObjetosUtils
from time_service.service.time_service import TimeService
from nasajon.util.jobs_util import JobsUtil

from dateutil import relativedelta

from abc import abstractmethod
from typing import List
import datetime
import enum


class PastaCotaCondominial(PastaRecorrente, PastaQuitacaoPadrao):

    def __init__(self, diario_util: DiarioUtil):
        super().__init__(diario_util)

        self.documento_tipo: enum.Enum = DocumentoTipo.COTA_CONDOMINIAL
        self.item_tipo = ItemDocumentoTipo.COTA_CONDOMINIAL
        self.item_descricao = 'Cota Condominial'
        self.cobrancas_service = DiarioUnicoFactory.getCobrancasService()

    def simular(self, dados: dict):
        # TODO: O módulo de orçamentos será feito no futuro
        pass

    def escriturar_futuro(self, dados: DadosEscrituracaoFutura):
        """
        dados:
            Parâmetros para realizar a escrituração antecipada
        """

        self._log.info("Iniciando escrituração futura.")

        dados = ObjetosUtils().dictToObject(dados, DadosEscrituracaoFutura)
        # Recuperando os lançamentos para os próximos 12 meses (por item):
        projecao = self._projecao_util.realizar_projecao(dados)

        # Monta documentos de cota condominal a partir do resultado da projeção
        for projecao_mes in projecao:
            cota = CotaCondominial()
            cota.competencia_inicial = projecao_mes.data_apropriacao.replace(
                day=1)
            cota.competencia_final = cota.competencia_inicial + \
                relativedelta.relativedelta(
                    months=1)-relativedelta.relativedelta(day=1)
            cota.emissao = projecao_mes.data_apropriacao
            cota.estabelecimento = dados.estabelecimento
            cota.participante = dados.participante
            cota.situacao = Situacao.PREVISTO.value
            cota.tipo = DocumentoTipo.COTA_CONDOMINIAL
            cota.valor = projecao_mes.valor
            cota.vencimento = projecao_mes.data_pagamento
            cota.tenant = dados.tenant
            cota.dados_cobranca = self.cobrancas_service.getDadosCobranca(
                dados.tenant, cota.participante)
            for projecao_item in projecao_mes.itens:
                item = ItemCotaCondominial()
                item.codigo = projecao_item.codigo
                item.descricao = projecao_item.codigo
                item.texto_instrucao = ''
                item.tipo = TipoItemCotaCondominial(projecao_item.tipo)
                item.valor = projecao_item.valor
                item.data_apropriacao = cota.emissao
                item.vencimento = cota.vencimento
                definicoes = self.get_definicoes_lancamentos_escrituracao_futura(
                    item.tipo)
                item.dados_cobranca = cota.dados_cobranca
                item.participante = cota.participante
                item.lancamentos = LancamentosUtil().criar_lancamentos(
                    item, definicoes, None, self.get_definicao_info_cobranca_escrituracao_futura())
                cota.itens.append(item)

            # Converte para documentos genéricos e envia para o diário
            documento = self.cota_condominial_para_documento(cota)
            self._diario_util.escriturar_antecipadamente_documento(
                cota.tenant, documento)

        self._log.info("Finalizada escrituração futura.")

    def faturar(self, dados: DadosFaturamento):
        """
        Realiza o faturamento dos contratos de cota condominiais

        parametros:
            dados: Dados necessários para realizar o faturamento. O valor do contrato já está proporcionalizado para o participante
        """

        self._log.info("Iniciando faturamento.")

        agora = TimeService.now()
        dados: DadosFaturamento = ObjetosUtils().dictToObject(dados, DadosFaturamento)

        JobsUtil().registra_log(dados.tenant, dados.contrato_codigo, dados.participante, dados.contrato_estabelecimento,
                                'COTA_CONDOMINIAL', 'FATURAMENTO', 'INICIO', str(agora.month)+"/"+str(agora.year))
        cota = CotaCondominial()
        cota.competencia_inicial = agora.replace(day=1)
        cota.competencia_final = cota.competencia_inicial + \
            relativedelta.relativedelta(
                months=1)-relativedelta.relativedelta(day=1)
        cota.emissao = TimeService.now()
        cota.estabelecimento = dados.contrato_estabelecimento
        cota.identificador_contrato = dados.contrato_codigo
        cota.participante = dados.participante
        cota.situacao = Situacao.REALIZADO
        cota.tipo = DocumentoTipo.COTA_CONDOMINIAL
        cota.numero = 1
        cota.vencimento = TimeService.now().replace(day=dados.contrato_dia_vencimento)
        cota.valor = sum([item.valor for item in dados.itens])
        cota.dados_cobranca = self.cobrancas_service.getDadosCobranca(
            dados.tenant, cota.participante)
        for _item in dados.itens:
            item = ItemCotaCondominial()
            item.codigo = _item.codigo
            item.descricao = _item.codigo
            item.tipo = TipoItemCotaCondominial(_item.tipo)
            item.valor = _item.valor
            item.data_apropriacao = cota.emissao
            item.vencimento = cota.vencimento
            item.texto_instrucao = ''
            definicoes = self.get_definicoes_lancamentos_apropriacao(item.tipo)
            definicoes_info = self.get_definicao_info_cobranca_apropriacao()
            item.participante = cota.participante
            item.dados_cobranca = cota.dados_cobranca
            item.lancamentos = LancamentosUtil().criar_lancamentos(
                item, definicoes, None, definicoes_info)
            cota.itens.append(item)
        documento = self.cota_condominial_para_documento(cota)
        self._diario_util.apropriar_documento(dados.tenant, documento)
        JobsUtil().registra_log(dados.tenant, dados.contrato_codigo, dados.participante, dados.contrato_estabelecimento,
                                'COTA_CONDOMINIAL', 'FATURAMENTO', 'FIM', str(agora.month)+"/"+str(agora.year))

        self._log.info("Finalizando faturamento.")

        return documento

    def get_dados_escrituracao_futura(self, dados: dict):
        """
        Parâmetros:
        - dados: Informações repassadas pelo responsável do agendamento da escrituração futura (normalmente: job de previsão).
            dia_apropriacao
            dia_vencimento
            estabelecimento
            participante
            tenant
            heuristica_valor
            itens[]
                codigo
                tipo
                valor   

        Return:
        - Deve retornar dados suficientes para a escrituração futura desta pasta contábil, sem necessidade de novas consultas ao diário ou ao banco de dados.
        """

        self._log.info("Recuperando dados para escrituracao futura.")

        dados_previsao = DadosEscrituracaoFutura()
        dados_previsao.dia_apropriacao = dados["dia_apropriacao"]
        dados_previsao.dia_vencimento = dados["dia_vencimento"]
        dados_previsao.estabelecimento = dados["estabelecimento"]
        dados_previsao.participante = dados["participante"]
        dados_previsao.tenant = dados["tenant"]
        dados_previsao.itens = list()

        for _item in dados["itens"]:

            item = DadosItem()
            item.codigo = _item["codigo"]
            item.tipo = _item["tipo"]
            item.valor = _item["valor"]
            item.valores_anteriores = self._diario_util.recuperar_ultimo_trimestre(
                dados["tenant"], dados, TimeService.now(), "Documento", self.documento_tipo, item.codigo)
            item.heuristica_projecao = HeuristicaProjecao(
                dados["heuristica_valor"])
            item.valor_medio_inicial = _item["valor"]
            dados_previsao.itens.append(item)

        self._log.info("Dados recuperados para escrituracao futura.")

        return dados_previsao

    def apropriar(self, dados: dict):
        """
        dados:
            dict com os campos da entity cota + o campo tenant
        """

        self._log.info("Iniciando apropriação.")

        # Primeiro, convertemos o dicionario de dados de entrada para uma Cota Condominial
        cota_condominial: CotaCondominial = ObjetosUtils().dictToObject(
            dados, CotaCondominial)

        # Depois, buscamos as definicoes de lancamentos e de info pagamento referentes a apropriacao
        definicao_info_cobranca = self.get_definicao_info_cobranca_apropriacao()

        # Usa-se o LancamentosUtil() para criar um list de model de lancamentos a partir das definicoes
        for item in cota_condominial.itens:
            item.data_apropriacao=cota_condominial.competencia_final
            item.vencimento=cota_condominial.vencimento
            definicoes_lancamentos = self.get_definicoes_lancamentos_apropriacao(
                TipoItemCotaCondominial(item.tipo))
            item.lancamentos = LancamentosUtil().criar_lancamentos(
                item, definicoes_lancamentos, None, definicao_info_cobranca)

        # Criamos um model de Documento baseado na cota condominial e nos lancamentos. Passamos por parametros
        documento = self.cota_condominial_para_documento(cota_condominial)

        # Invoco o diário para persistir os dados
        self._diario_util.apropriar_documento(dados["tenant"], documento)

        self._log.info("Finalizando apropriação.")

        return documento

    def quitar(self, dados: dict):
        """
        dados:
            informações suficientes para a quitação do documento
        """

        self._log.info("Iniciando quitação.")

        resultado = self.quitar_padrao(dados)

        self._log.info("Finalizando quitação.")

        return resultado

    def cancelar(self, dados: dict):
        # TODO: O módulo de cancelamentos será feito no futuro
        self._log.info("Cancelamento não implementado.")
        pass

    def get_definicoes_lancamentos(self, momento: MomentoContabil, tipo: TipoItemCotaCondominial):
        if momento == MomentoContabil.ESCRITURACAO_FUTURA.value:
            return self.get_definicoes_lancamentos_escrituracao_futura(tipo)
        elif momento == MomentoContabil.APROPRIACAO.value:
            return self.get_definicoes_lancamentos_apropriacao(tipo)
        elif momento == MomentoContabil.QUITACAO.value:
            return self.get_definicoes_lancamentos_quitacao()

    def get_dados_simulacao(self, dados: dict):
        # TODO
        pass

    def get_dados_faturamento(self, dados: dict):
        # TODO
        agora = TimeService.now()
        JobsUtil().registra_log(dados["tenant"], dados["contrato_codigo"], dados["participante"], dados["contrato_estabelecimento"],
                                'COTA_CONDOMINIAL', 'FATURAMENTO', 'GET_DADOS_INICIO', str(agora.month)+"/"+str(agora.year))
        dados_faturamento: DadosFaturamento = ObjetosUtils().dictToObject(dados,
                                                                          DadosFaturamento)
        dados_cobranca = self.cobrancas_service.getDadosCobranca(
            dados_faturamento.tenant, dados_faturamento.participante)
        dados_faturamento.dados_cobranca = ObjetosUtils(
        ).dictToObject(dados_cobranca, Dados_Cobranca)
        JobsUtil().registra_log(dados["tenant"], dados["contrato_codigo"], dados["participante"], dados["contrato_estabelecimento"],
                                'COTA_CONDOMINIAL', 'FATURAMENTO', 'GET_DADOS_FIM', str(agora.month)+"/"+str(agora.year))
        return dados_faturamento

    def get_dados_apropriacao(self, dados: dict):
        return dados

    def get_dados_cancelamento(self, dados: dict):
        # TODO
        pass

    def get_dados_quitacao(self, dados: dict):
        # TODO
        return self.get_dados_quitacao_padrao(dados)

    def get_definicoes_lancamentos_escrituracao_futura_item(self, tipo_item):
        pass
        # return self.get_definicoes_lancamentos_escrituracao_futura()

    def get_definicoes_lancamentos_apropriacao(self, tipo: TipoItemCotaCondominial) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='1.1.2.01',
            historico='Cotas Condominiais a receber',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__comum.apropriacao.provisao'
        ))
        if tipo == TipoItemCotaCondominial.COTA_CONDOMINIAL:
            saida.append(self.get_definicoes_lancamentos_apropriacao_cota())
        if tipo == TipoItemCotaCondominial.AGUA:
            saida.append(self.get_definicoes_lancamentos_apropriacao_agua())
        if tipo == TipoItemCotaCondominial.ENERGIA_ELETRICA:
            saida.append(self.get_definicoes_lancamentos_apropriacao_energia())
        if tipo == TipoItemCotaCondominial.GARAGEM:
            saida.append(self.get_definicoes_lancamentos_apropriacao_garagem())
        if tipo == TipoItemCotaCondominial.GAS:

            saida.append(self.get_definicoes_lancamentos_apropriacao_gas())
        if tipo == TipoItemCotaCondominial.MULTAS:
            saida.append(self.get_definicoes_lancamentos_apropriacao_multas())
        if tipo == TipoItemCotaCondominial.FUNDO_OBRAS:
            saida.append(self.get_definicoes_lancamentos_apropriacao_obras())
        if tipo == TipoItemCotaCondominial.OUTROS:
            saida.append(self.get_definicoes_lancamentos_apropriacao_outros())
        if tipo == TipoItemCotaCondominial.FUNDO_RESERVA:
            saida.append(self.get_definicoes_lancamentos_apropriacao_reserva())
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=1,
            natureza='D',
            conta='1.1.1.01',
            historico='Recebimento de cotas condominiais',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__comum.apropriacao.caixa'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=2,
            natureza='C',
            conta='1.1.2.01',
            historico='Recebimento de cotas condominiais',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__comum.apropriacao.conclusao'
        ))
        return saida

    def get_definicoes_lancamentos_apropriacao_cota(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.01',
            historico='Receita de cotas condominiais - cota',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__cota.apropriacao.receita'
        )

    def get_definicoes_lancamentos_apropriacao_agua(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.03',
            historico='Receita de cotas condominiais - água',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__agua.apropriacao.receita'
        )

    def get_definicoes_lancamentos_apropriacao_energia(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.02',
            historico='Receita de cotas condominiais - energia elétrica',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__energia.apropriacao.receita'
        )

    def get_definicoes_lancamentos_apropriacao_garagem(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.08',
            historico='Receita de cotas condominiais - garagem',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__garagem.apropriacao.receita'
        )

    def get_definicoes_lancamentos_apropriacao_gas(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.04',
            historico='Receita de cotas condominiais - gás',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__gas.apropriacao.receita'
        )

    def get_definicoes_lancamentos_apropriacao_multas(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.05',
            historico='Receita de cotas condominiais - multas',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__multa.apropriacao.receita'
        )

    def get_definicoes_lancamentos_apropriacao_obras(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.06',
            historico='Receita de cotas condominiais - fundo de obras',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__obras.apropriacao.receita'
        )

    def get_definicoes_lancamentos_apropriacao_outros(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.09',
            historico='Receita de cotas condominiais - outros',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__outros.apropriacao.receita'
        )

    def get_definicoes_lancamentos_apropriacao_reserva(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.07',
            historico='Receita de cotas condominiais - fundo de reserva',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__reserva.apropriacao.receita'
        )

    def get_definicoes_lancamentos_escrituracao_futura(self, tipo: TipoItemCotaCondominial) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='1.1.2.01',
            historico='Cotas Condominiais a receber',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__comum.esc_futura.provisao'
        ))
        if tipo == TipoItemCotaCondominial.COTA_CONDOMINIAL:
            saida.append(
                self.get_definicoes_lancamentos_escrituracao_futura_cota())
        if tipo == TipoItemCotaCondominial.AGUA:
            saida.append(
                self.get_definicoes_lancamentos_escrituracao_futura_agua())
        if tipo == TipoItemCotaCondominial.ENERGIA_ELETRICA:
            saida.append(
                self.get_definicoes_lancamentos_escrituracao_futura_energia())
        if tipo == TipoItemCotaCondominial.GARAGEM:
            saida.append(
                self.get_definicoes_lancamentos_escrituracao_futura_garagem())
        if tipo == TipoItemCotaCondominial.GAS:
            saida.append(
                self.get_definicoes_lancamentos_escrituracao_futura_gas())
        if tipo == TipoItemCotaCondominial.MULTAS:
            saida.append(
                self.get_definicoes_lancamentos_escrituracao_futura_multas())
        if tipo == TipoItemCotaCondominial.FUNDO_OBRAS:
            saida.append(
                self.get_definicoes_lancamentos_escrituracao_futura_obras())
        if tipo == TipoItemCotaCondominial.OUTROS:
            saida.append(
                self.get_definicoes_lancamentos_escrituracao_futura_outros())
        if tipo == TipoItemCotaCondominial.FUNDO_RESERVA:
            saida.append(
                self.get_definicoes_lancamentos_escrituracao_futura_reserva())
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=2,
            ordem=1,
            natureza='D',
            conta='1.1.1.01',
            historico='Recebimento de cotas condominiais',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__comum.esc_futura.caixa'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=2,
            ordem=2,
            natureza='C',
            conta='1.1.2.01',
            historico='Recebimento de cotas condominiais',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__comum.esc_futura.conclusao'
        ))
        return saida

    def get_definicoes_lancamentos_escrituracao_futura_cota(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.01',
            historico='Receita de cotas condominiais - cota',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__cota.esc_futura.receita'
        )

    def get_definicoes_lancamentos_escrituracao_futura_agua(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.03',
            historico='Receita de cotas condominiais - água',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__agua.esc_futura.receita'
        )

    def get_definicoes_lancamentos_escrituracao_futura_energia(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.02',
            historico='Receita de cotas condominiais - energia elétrica',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__energia.esc_futura.receita'
        )

    def get_definicoes_lancamentos_escrituracao_futura_garagem(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.08',
            historico='Receita de cotas condominiais - garagem',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__garagem.esc_futura.receita'
        )

    def get_definicoes_lancamentos_escrituracao_futura_gas(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.04',
            historico='Receita de cotas condominiais - gás',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__gas.esc_futura.receita'
        )

    def get_definicoes_lancamentos_escrituracao_futura_multas(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.05',
            historico='Receita de cotas condominiais - multas',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__multa.esc_futura.receita'
        )

    def get_definicoes_lancamentos_escrituracao_futura_obras(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.06',
            historico='Receita de cotas condominiais - fundo de obras',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__obras.esc_futura.receita'
        )

    def get_definicoes_lancamentos_escrituracao_futura_outros(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.09',
            historico='Receita de cotas condominiais - outros',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__outros.esc_futura.receita'
        )

    def get_definicoes_lancamentos_escrituracao_futura_reserva(self):
        return DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='3.1.1.07',
            historico='Receita de cotas condominiais - fundo de reserva',
            formula='valor',
            formula_data='data_apropriacao',
            situacao=SituacaoDiario.PREVISTO,
            definicao='cota__reserva.esc_futura.receita'
        )

    def get_definicoes_lancamentos_quitacao(self) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.QUITACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='1.1.1.01',
            historico='Recebimento de pagamento de cota condominial',
            formula='valor',
            formula_data='data_pagamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__comum.pagamento.caixa'
        ))

        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.QUITACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='1.1.2.01',
            historico='Recebimento de pagamento de cota condominial',
            formula='valor',
            formula_data='data_pagamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='cota__comum.pagamento.conclusao'
        ))
        return saida

    def get_definicao_info_cobranca_escrituracao_futura(self) -> DefinicaoInfoCobranca:
        return DefinicaoInfoCobranca(
            lancamento_numero=2,
            formula_juros_mensal='juros_mensal',
            formula_multa_atraso='multa_atraso',
            formula_desconto='desconto',
            formula_texto_instrucao='texto_instrucao',
            formula_vencimento='vencimento',
            formula_participante='participante',
            situacao=SituacaoInfoCobranca.PREVISTO
        )

    def get_definicao_info_cobranca_apropriacao(self) -> DefinicaoInfoCobranca:
        return DefinicaoInfoCobranca(
            lancamento_numero=2,
            formula_juros_mensal='juros_mensal',
            formula_multa_atraso='multa_atraso',
            formula_desconto='desconto',
            formula_texto_instrucao='texto_instrucao',
            formula_vencimento='vencimento',
            formula_participante='participante',
            situacao=SituacaoInfoCobranca.PENDENTE
        )

    def get_definicao_info_cobranca_quitacao(self):
        return DefinicaoInfoCobranca(
            lancamento_numero=1,
            formula_juros_mensal='juros_mensal',
            formula_multa_atraso='multa_atraso',
            formula_desconto='desconto',
            formula_texto_instrucao='texto_instrucao',
            formula_vencimento='data_pagamento',
            formula_participante='participante',
            situacao=SituacaoInfoCobranca.QUITADO
        )

    def cota_condominial_para_documento(self, cota: CotaCondominial) -> Documento:
        saida = Documento()
        saida.estabelecimento = str(cota.estabelecimento)
        saida.numero = str(1)
        saida.sinal = Sinal.SAIDA
        saida.data_lancamento = cota.emissao
        saida.ano = cota.emissao.year
        saida.codigo_barras = cota.codigo_barras
        saida.valor = cota.valor
        saida.participante = str(cota.participante)
        saida.emissao = cota.emissao
        saida.url_documento = cota.url_documento
        saida.situacao = cota.situacao
        saida.identificador_contrato = cota.identificador_contrato
        saida.tipo = self.documento_tipo.value

        for itemc in cota.itens:
            item = ItemDocumento()
            item.codigo = str(itemc.codigo)
            item.valor = itemc.valor
            item.tipo = ItemDocumentoTipo.COTA_CONDOMINIAL
            item.descricao = str(itemc.descricao)
            item.lancamentos = itemc.lancamentos
            saida.itens.append(item)
        return saida


""" 
if __name__ == '__main__':
    pasta = PastaCotaCondominial(DiarioUtil())
    j=  {"contrato_codigo": "implantacao",    "contrato_dia_processamento": 5,    "contrato_dia_vencimento": 15,    "contrato_estabelecimento": "743",    "dados_cobranca": null,    "itens": [        {            "codigo": null,            "tipo": null,            "valor": 600.0        },        {            "codigo": null,            "tipo": null,            "valor": 800.0        },        {            "codigo": null,            "tipo": null,            "valor": 6.0        },        {            "codigo": null,            "tipo": null,            "valor": 40.0        },        {            "codigo": null,            "tipo": null,            "valor": 60.0        }    ],    "participante": "02579981101",    "tenant": 47}
    
    dados_tratados = pasta.get_dados_faturamento(JsonUtil().decode(j))


    pasta.faturar(dados_tratados)    
    
    exit()
    
    dados = dict()
    dados["dia_apropriacao"] = 15
    dados["dia_vencimento"] = 20
    dados["estabelecimento"] = "743"
    dados["participante"] = "02579981101"
    dados["tenant"] = 47
    dados["heuristica_valor"] = 1
    item1 = dict()
    item1["codigo"] = TipoItemCotaCondominial.ENERGIA_ELETRICA.value
    item1["tipo"] = TipoItemCotaCondominial.ENERGIA_ELETRICA.value
    item1["valor"] = 100

    item2 = dict()
    item2["codigo"] = TipoItemCotaCondominial.FUNDO_OBRAS.value
    item2["tipo"] = TipoItemCotaCondominial.FUNDO_OBRAS.value
    item2["valor"] = 200

    dados["itens"] = list()
    dados["itens"].append(item1)
    dados["itens"].append(item2)

    novos_dados = pasta.get_dados_escrituracao_futura(dados)
    pasta.escriturar_futuro(novos_dados) """
