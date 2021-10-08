from dateutil import relativedelta

from nasajon.pastas_contabeis.abstract_pasta_contabil import AbstractPastaContabil
from nasajon.pastas_contabeis.abstract_pasta_contabil_composta import AbstractPastaContabilComposta
from nasajon.pastas_contabeis.pastas_router import MomentoContabil

from nasajon.entity.rpa import Rpa
from nasajon.entity.dados_escrituracao_futura import DadosEscrituracaoFutura, DadosItem, ValoresAnteriores
from nasajon.entity.definicao_info_pagamento import DefinicaoInfoPagamento
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from diario_unico.entity.documento import Documento
from diario_unico.enum.situacao import Situacao
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.entity.item_documento import ItemDocumento
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from diario_unico.entity.lancamento import Lancamento, SituacaoDiario
from nasajon.entity.dados_faturamento import DadosFaturamento
from nasajon.entity.definicao_info_cobranca import DefinicaoInfoCobranca
from nasajon.entity.dados_cobranca import Dados_Cobranca
from nasajon.pastas_contabeis.pasta_quitacao_padrao import PastaQuitacaoPadrao
from diario_unico.enum.sinal import Sinal

from diario_unico.enum.info_cobranca.situacao_info_cobranca import SituacaoInfoCobranca
from diario_unico.enum.info_pagamento.situacao_info_pagamento import SituacaoInfoPagamento

from nasajon.util.diario_util import DiarioUtil
from nasajon.util.json_util import JsonUtil
from nasajon.util.lancamento_util import LancamentosUtil
from nasajon.util.objeto_util import ObjetosUtils
from nasajon.util.jobs_util import JobsUtil


from abc import abstractmethod
from typing import List

import datetime
import enum


class PastaRpa(AbstractPastaContabil, PastaQuitacaoPadrao):

    def __init__(self, diario_util: DiarioUtil):
        super().__init__(diario_util)

        self.documento_tipo: enum.Enum = DocumentoTipo.RPA
        self.item_tipo = ItemDocumentoTipo.SERVICO
        self.item_descricao = 'Serviço'

    def simular(self, dados: dict):
        # TODO: O módulo de orçamentos será feito no futuro
        pass

    def escriturar_futuro(self, dados):
        """
        TODO: Ainda não há escrituração futura para RPA
        """
        pass

    def faturar(self, dados: DadosFaturamento):
        """
        Nao Aplicável
        """
        pass

    def get_dados_escrituracao_futura(self, dados: dict):
        """
        TODO: Ainda não há escrituração futura para RPA
        """
        pass

    def apropriar(self, dados: dict):
        """
        dados:
            dict com os campos da entity RPA + o campo tenant
        """
        # Primeiro, convertemos o dicionario de dados de entrada para uma RPA
        rpa: Rpa = ObjetosUtils().dictToObject(
            dados, Rpa)

        # Depois, buscamos as definicoes de lancamentos e de info pagamento referentes a apropriacao
        definicao_info_pagamento = self.get_definicao_info_pagamento_apropriacao()

        # Usa-se o LancamentosUtil() para criar um list de model de lancamentos a partir das definicoes
        definicoes_lancamentos = self.get_definicoes_lancamentos_apropriacao()
        rpa.lancamentos = LancamentosUtil().criar_lancamentos(
            rpa, definicoes_lancamentos, definicao_info_pagamento, None)

        # Criamos um model de Documento baseado na RPA e nos lancamentos. Passamos por parametros
        documento = self.rpa_para_documento(rpa)

        # Invoco o diário para persistir os dados
        self._diario_util.apropriar_documento(dados["tenant"], documento)
        return documento

    def quitar(self, dados: dict):
        """
        dados:
            informações suficientes para a quitação do documento
        """
        return self.quitar_padrao(dados)

    def cancelar(self, dados: dict):
        # TODO: O módulo de cancelamentos será feito no futuro
        pass

    def get_definicoes_lancamentos(self, momento: MomentoContabil):
        if momento == MomentoContabil.ESCRITURACAO_FUTURA.value:
            return self.get_definicoes_lancamentos_escrituracao_futura()
        elif momento == MomentoContabil.APROPRIACAO.value:
            return self.get_definicoes_lancamentos_apropriacao()
        elif momento == MomentoContabil.QUITACAO.value:
            return self.get_definicoes_lancamentos_quitacao()

    def get_dados_simulacao(self, dados: dict):
        # TODO
        pass

    def get_dados_faturamento(self, dados: dict):
        # Não há faturamento para rpa
        return dados

    def get_dados_apropriacao(self, dados: dict):
        return dados

    def get_dados_cancelamento(self, dados: dict):
        # TODO
        pass

    def get_dados_quitacao(self, dados: dict):
        # TODO
        return self.get_dados_quitacao_padrao(dados)

    def get_definicoes_lancamentos_apropriacao(self) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='4.1.1.03',
            historico='Despesa de aquisição de serviço',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='rpa.apropriacao.despesa'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='2.1.2.04',
            historico='Aquisição de serviço',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='rpa.apropriacao.provisao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=1,
            natureza='D',
            conta='2.1.2.04',
            historico='Pagamento de aquisição de serviço',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='rpa.apropriacao.conclusao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de aquisição de serviço',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='rpa.apropriacao.caixa'
        ))
        return saida

    def get_definicoes_lancamentos_escrituracao_futura(self) -> List[DefinicaoLancamento]:
        saida = list()
        return saida

    def get_definicoes_lancamentos_quitacao(self) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='2.1.2.04',
            historico='Pagamento de aquisição de serviço',
            formula='valor',
            formula_data='data_pagamento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='rpa.pagamento.conclusao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de aquisição de serviço',
            formula='valor',
            formula_data='data_pagamento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='rpa.pagamento.caixa'
        ))
        return saida

    def get_definicao_info_pagamento_apropriacao(self):
        return DefinicaoInfoPagamento(
            numero_lancamento=2,
            formula_vencimento="vencimento",
            situacao=SituacaoInfoPagamento.PENDENTE
        )

    def get_definicao_info_pagamento_quitacao(self):
        return DefinicaoInfoPagamento(
            numero_lancamento=1,
            formula_vencimento="data_pagamento",
            situacao=SituacaoInfoPagamento.QUITADO
        )

    def rpa_para_documento(self, rpa: Rpa) -> Documento:
        self.validar_percentagem_imposto(rpa)
        saida = Documento()
        saida.ano = rpa.data_lancamento.year
        saida.cfop = rpa.cfop
        saida.codigo_barras = rpa.codigo_barras
        saida.data_entrada = rpa.emissao
        saida.estabelecimento = rpa.estabelecimento
        saida.identificador_contrato = None
        saida.modelo = 'RPA'
        saida.numero = str(rpa.numero)
        saida.participante = rpa.fornecedor_cnpj
        saida.sinal = Sinal.ENTRADA
        saida.situacao = rpa.situacao
        saida.tipo = DocumentoTipo.RPA.value
        saida.token_facilitador = rpa.token_facilitador
        saida.url_documento = rpa.foto
        saida.valor = rpa.valor
        saida.data_lancamento = rpa.data_lancamento

        item = ItemDocumento()
        item.codigo = 'Servico'
        item.descricao = 'Aquisição de serviço'
        item.lancamentos = rpa.lancamentos
        item.tipo = ItemDocumentoTipo.SERVICO.value
        item.valor = rpa.valor
        item.irrf_retido = rpa.irrf_retido
        item.iss_retido = rpa.iss_retido
        saida.itens.append(item)

        return saida

    def validar_percentagem_imposto(self, nota: Rpa):
        ObjetosUtils().validar_range_percentagem(nota, "irrf_retido", "valor", 28, 0)
        ObjetosUtils().validar_range_percentagem(nota, "iss_retido", "valor", 15, 0)
