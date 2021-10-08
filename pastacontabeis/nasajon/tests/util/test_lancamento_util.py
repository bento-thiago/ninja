import os
import unittest
from nasajon.util.lancamento_util import LancamentosUtil
from datetime import date
from typing import List
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from nasajon.pastas_contabeis.pastas_router import MomentoContabil
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from nasajon.entity.definicao_info_pagamento import DefinicaoInfoPagamento
from diario_unico.entity.lancamento import SituacaoDiario


class TestLancamentoUtil(unittest.TestCase):
    def setUp(self):
        self.__lancUtil = LancamentosUtil()

    def mock_parametros_criar_lancamentos(self) -> dict:
        dados: dict = dict()
        dados["valor"] = 100
        dados["data_lancamento"] = date(2019, 10, 1)
        dados["vencimento"] = date(2019, 10, 15)
        definicoes:  List[DefinicaoLancamento] = list()
        definicoes.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=DocumentoTipo.CONTA_AGUA_E_ESGOTO,
            numero=1,
            ordem=1,
            natureza='D',
            conta='4.1.1.08.0002',
            historico='Despesa com conta de água',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.REALIZADO
        ))
        definicoes.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=DocumentoTipo.CONTA_AGUA_E_ESGOTO,
            numero=1,
            ordem=2,
            natureza='C',
            conta='2.1.2.04',
            historico='Conta de água a pagar',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.REALIZADO
        ))
        definicoes.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=DocumentoTipo.CONTA_AGUA_E_ESGOTO,
            numero=2,
            ordem=1,
            natureza='D',
            conta='2.1.2.04',
            historico='Pagamento de conta de água',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO
        ))
        definicoes.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=DocumentoTipo.CONTA_AGUA_E_ESGOTO,
            numero=2,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de conta de água',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO
        ))

        definicao_info_pagamento: DefinicaoInfoPagamento = DefinicaoInfoPagamento(
            numero_lancamento=2,
            formula_vencimento="vencimento",
            situacao=1
        )
        params = dict()
        params["dados"] = dados
        params["definicoes"] = definicoes
        params["definicao_info_pagamento"] = definicao_info_pagamento
        return params

    def test_criar_info_pagamento(self):
        params = self.mock_parametros_criar_lancamentos()
        resultado = self.__lancUtil.criar_lancamentos(
            params["dados"], params["definicoes"], params["definicao_info_pagamento"])
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0].data, date(2019, 10, 1))
        self.assertIsNone(resultado[0].info_cobranca)
        self.assertIsNone(resultado[0].info_pagamento)
        self.assertEqual(resultado[0].numero, 1)
        self.assertEqual(resultado[0].situacao.value,
                         SituacaoDiario.REALIZADO.value)
        self.assertEqual(len(resultado[0].partidas), 2)
        self.assertEqual(
            resultado[0].partidas[0].conta_contabil, '4.1.1.08.0002')
        self.assertEqual(
            resultado[0].partidas[0].historico, 'Despesa com conta de água')
        self.assertEqual(resultado[0].partidas[0].natureza, 'D')
        self.assertEqual(resultado[0].partidas[0].ordem, 1)
        self.assertEqual(resultado[0].partidas[0].valor, 100)
        self.assertEqual(resultado[0].partidas[1].conta_contabil, '2.1.2.04')
        self.assertEqual(
            resultado[0].partidas[1].historico, 'Conta de água a pagar')
        self.assertEqual(resultado[0].partidas[1].natureza, 'C')
        self.assertEqual(resultado[0].partidas[1].ordem, 2)
        self.assertEqual(resultado[0].partidas[1].valor, 100)

        self.assertEqual(resultado[1].data, date(2019, 10, 15))
        self.assertIsNone(resultado[1].info_cobranca)
        self.assertIsNotNone(resultado[1].info_pagamento)
        self.assertEqual(resultado[1].numero, 2)
        self.assertEqual(resultado[1].situacao.value,
                         SituacaoDiario.PREVISTO.value)
        self.assertEqual(len(resultado[1].partidas), 2)
        self.assertEqual(resultado[1].partidas[0].conta_contabil, '2.1.2.04')
        self.assertEqual(
            resultado[1].partidas[0].historico, 'Pagamento de conta de água')
        self.assertEqual(resultado[1].partidas[0].natureza, 'D')
        self.assertEqual(resultado[1].partidas[0].ordem, 1)
        self.assertEqual(resultado[1].partidas[0].valor, 100)
        self.assertEqual(resultado[1].partidas[1].conta_contabil, '1.1.1.01')
        self.assertEqual(
            resultado[1].partidas[1].historico, 'Pagamento de conta de água')
        self.assertEqual(resultado[1].partidas[1].natureza, 'C')
        self.assertEqual(resultado[1].partidas[1].ordem, 2)
        self.assertEqual(resultado[1].partidas[1].valor, 100)
