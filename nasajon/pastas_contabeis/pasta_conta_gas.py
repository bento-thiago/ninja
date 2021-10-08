from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo

from nasajon.pastas_contabeis.pasta_conta_consumo import PastaContaConsumo
from nasajon.pastas_contabeis.pastas_router import MomentoContabil
from diario_unico.entity.lancamento import SituacaoDiario
from nasajon.util.diario_util import DiarioUtil

from typing import List

import enum


class PastaContaGas(PastaContaConsumo):

    def __init__(self, diario_util: DiarioUtil):
        super().__init__(diario_util)

        self.documento_tipo = DocumentoTipo.CONTA_GAS
        self.item_descricao = 'Gás'

    def get_definicoes_lancamentos_escrituracao_futura(self) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='4.1.1.08.0003',
            historico='Despesa com conta de gás',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_gas.esc_futura.despesa'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='2.1.2.04',
            historico='Conta de gás a pagar',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_gas.esc_futura.provisao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=2,
            ordem=1,
            natureza='D',
            conta='2.1.2.04',
            historico='Pagamento de conta de gás',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_gas.esc_futura.conclusao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=2,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de conta de gás',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_gas.esc_futura.caixa'
        ))
        return saida

    def get_definicoes_lancamentos_apropriacao(self) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='4.1.1.08.0003',
            historico='Despesa com conta de gás',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='conta_gas.apropriacao.despesa'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='2.1.2.04',
            historico='Conta de gás a pagar',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='conta_gas.apropriacao.provisao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=1,
            natureza='D',
            conta='2.1.2.04',
            historico='Pagamento de conta de gás',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_gas.apropriacao.conclusao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de conta de gás',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_gas.apropriacao.caixa'
        ))
        return saida

    def get_definicoes_lancamentos_quitacao(self) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.QUITACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='2.1.2.04',
            historico='Pagamento de conta de gás',
            formula='valor',
            formula_data='data_pagamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='conta_gas.pagamento.conclusao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.QUITACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de conta de gás',
            formula='valor',
            formula_data='data_pagamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='conta_gas.pagamento.caixa'
        ))
        return saida
