from nasajon.pastas_contabeis.abstract_pasta_contabil import AbstractPastaContabil
from nasajon.pastas_contabeis.pasta_imposto_com_retencao import PastaImpostoComRetencao
from nasajon.util.diario_util import DiarioUtil
from nasajon.util.projecao_util import ProjecaoUtil
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.entity.imposto_retido_acumulado import ImpostoRetidoAcumulado
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from nasajon.pastas_contabeis.pastas_router import MomentoContabil
from diario_unico.entity.lancamento import SituacaoDiario
from diario_unico.enum.documentos.item_documento_tipo_imposto import ItemDocumentoTipoImposto
from typing import List


class PastaCsll(AbstractPastaContabil, PastaImpostoComRetencao):
    tipo_documento_retencao: DocumentoTipo = DocumentoTipo.GUIA_RETENCAO_CSLL
    imposto: str = ItemDocumentoTipoImposto.CSLL

    def __init__(self, diario_util: DiarioUtil):
        self._diario_util = diario_util

    def escriturar_futuro(self, dados: dict):
        """
        dados: Dicionário com os seguintes campos:
            tenant
            ano
            mês
        """
        self.retencao_do_periodo(dados)

    def get_dados_escrituracao_futura(self, dados: dict):
        """
        dados: Dicionário com os seguintes campos:
            tenant
            ano
            mês
        """
        return dados

    def get_definicoes_lancamentos_escrituracao_futura_parte_realizada(self, configuracoes: dict) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.tipo_documento_retencao,
            numero=1,
            ordem=1,
            natureza='D',
            conta='2.1.2.02.0007',
            historico='Csll retido recolhido',
            formula='valor_calculado',
            formula_data='competencia_final',
            situacao=SituacaoDiario.PREVISTO,
            definicao='csll__retido.esc_futura.conclusao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.tipo_documento_retencao,
            numero=1,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de guia de CSLL retido',
            formula='valor_calculado',
            formula_data='competencia_final',
            situacao=SituacaoDiario.PREVISTO,
            definicao='csll__retido.esc_futura.conclusao'
        ))
        return saida

    def calcular_retencao(self, imposto_acumulado: ImpostoRetidoAcumulado, configuracoes):
        return imposto_acumulado.valor_retido

    def get_definicoes_lancamentos_escrituracao_futura_parte_prevista(self, configuracoes):
        return self.get_definicoes_lancamentos_escrituracao_futura_parte_realizada(configuracoes)
