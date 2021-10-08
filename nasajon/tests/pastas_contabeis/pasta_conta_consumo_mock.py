from nasajon.pastas_contabeis.pasta_conta_consumo import PastaContaConsumo

from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.entity.lancamento import SituacaoDiario

from nasajon.pastas_contabeis.pastas_router import MomentoContabil

from typing import List


class PastaContaConsumoMock(PastaContaConsumo):

    # def get_tipo_documento(self) -> DocumentoTipo:
    #     pass

    def get_definicoes_lancamentos_escrituracao_futura(self) -> List[DefinicaoLancamento]:
        pass

    def get_definicoes_lancamentos_apropriacao(self) -> List[DefinicaoLancamento]:
        pass

    def get_definicoes_lancamentos_quitacao(self) -> List[DefinicaoLancamento]:
        pass

    def get_definicoes_lancamentos_escrituracao_futura_item(self, tipo_item):
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=DocumentoTipo.CONTA_ENERGIA,
            numero=1,
            ordem=1,
            natureza='D',
            conta='4.1.1.08.0002',
            historico='Despesa com conta de energia elétrica',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.PREVISTO
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=DocumentoTipo.CONTA_ENERGIA,
            numero=1,
            ordem=2,
            natureza='C',
            conta='2.1.2.04',
            historico='Conta de energia elétrica a pagar',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.PREVISTO
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=DocumentoTipo.CONTA_ENERGIA,
            numero=2,
            ordem=1,
            natureza='D',
            conta='2.1.2.04',
            historico='Pagamento de conta de energia elétrica',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=DocumentoTipo.CONTA_ENERGIA,
            numero=2,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de conta de energia elétrica',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO
        ))
        return saida
