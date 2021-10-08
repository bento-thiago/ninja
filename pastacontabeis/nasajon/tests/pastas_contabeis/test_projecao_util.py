from nasajon.util.projecao_util import ProjecaoUtil

from nasajon.entity.dados_escrituracao_futura import DadosEscrituracaoFutura, DadosItem, ValoresAnteriores
from nasajon.enum.heuristica_projecao import HeuristicaProjecao
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.entity.lancamento import SituacaoDiario
from nasajon.pastas_contabeis.pastas_router import MomentoContabil
from nasajon.pastas_contabeis.pasta_conta_energia_eletrica import PastaContaEnergiaEletrica
from nasajon.util.diario_util import DiarioUtil

import datetime
import os
import unittest


class TestProjecaoUtil(unittest.TestCase):

    def setUp(self):
        self._proj_util = ProjecaoUtil()

        self.dados = DadosEscrituracaoFutura()
        self.make_dados_para_testes()

    def make_dados_para_testes(self):
        # Item projetado via média móvel:
        item0 = DadosItem()
        item0.codigo = "1"
        item0.heuristica_projecao = HeuristicaProjecao.MEDIA_MOVEL
        item0.tipo = "1"
        item0.valor_medio_inicial = 100.0

        valor_anterior0 = ValoresAnteriores()
        valor_anterior0.valor = 100.0

        valor_anterior1 = ValoresAnteriores()
        valor_anterior1.valor = 200.0

        item0.valores_anteriores = list()
        item0.valores_anteriores.append(valor_anterior0)
        item0.valores_anteriores.append(valor_anterior1)

        # Item projetado via valor fixo:
        item1 = DadosItem()
        item1.codigo = "2"
        item1.heuristica_projecao = HeuristicaProjecao.VALOR_FIXO
        item1.tipo = "1"
        item1.valor_medio_inicial = 500.0

        valor_anterior0 = ValoresAnteriores()
        valor_anterior0.valor = 100.0

        valor_anterior1 = ValoresAnteriores()
        valor_anterior1.valor = 200.0

        item1.valores_anteriores = list()
        item1.valores_anteriores.append(valor_anterior0)
        item1.valores_anteriores.append(valor_anterior1)

        # Item projetado via média móvel, porém sem histórico anterior:
        item2 = DadosItem()
        item2.codigo = "3"
        item2.heuristica_projecao = HeuristicaProjecao.MEDIA_MOVEL
        item2.tipo = "1"
        item2.valor_medio_inicial = 234.0

        item2.valores_anteriores = list()

        # Adicionando os itens nos dados:
        self.dados.itens = list()
        self.dados.itens.append(item0)
        self.dados.itens.append(item1)
        self.dados.itens.append(item2)

        # Preenchendo os dados básicos:
        self.dados.dia_apropriacao = 10
        self.dados.dia_vencimento = 15

    def test_calcular_valor_projetado(self):
        # Chanado o cálculo da projeção:
        valores_projetados = self._proj_util.calcular_valor_projetado(
            self.dados)

        # Testando os valores projetados:
        self.assertEqual(valores_projetados["1"], 150.0)
        self.assertEqual(valores_projetados["2"], 500.0)
        self.assertEqual(valores_projetados["3"], 234.0)

    def test_gerar_lancamentos_projecao_mes(self):

        # Gerando os valores projetados:
        valores_projetados = self._proj_util.calcular_valor_projetado(
            self.dados)

        # Gerando os lançamentos de projeção do mês:
        projecoes_mes = self._proj_util.gerar_lancamentos_projecao_mes(
            self.dados, datetime.date(2019, 10, 10), valores_projetados, PastaContaEnergiaEletrica(DiarioUtil()))

        # Testando os lancamentos gerados:
        self.assertEqual(len(projecoes_mes), 3)

        self.assertEqual(len(projecoes_mes["1"]), 2)

        self.assertEqual(
            len(projecoes_mes["1"].vetor_lancamentos[0].partidas), 2)
        self.assertEqual(
            len(projecoes_mes["1"].vetor_lancamentos[1].partidas), 2)
        self.assertEqual(
            projecoes_mes["1"].vetor_lancamentos[0].partidas[0].natureza, 'D')
        self.assertEqual(
            projecoes_mes["1"].vetor_lancamentos[0].partidas[0].conta_contabil, '4.1.1.08.0002')
        self.assertEqual(
            projecoes_mes["1"].vetor_lancamentos[0].partidas[0].valor, 150.0)
        self.assertEqual(projecoes_mes["1"].vetor_lancamentos[0].data,
                         datetime.date(2019, 10, 10))

    def test_gerar_lancamentos_projecao(self):

        # Gerando os lançamentos de projeção para os próximos meses:
        projecoes = self._proj_util.gerar_lancamentos_projecao(
            self.dados, PastaContaEnergiaEletrica(DiarioUtil()))

        # Testando o resultado gerado:
        self.assertEqual(len(projecoes), 12)

        self.assertEqual(
            len(projecoes[datetime.datetime.now().replace(day=1).date()]["1"].vetor_lancamentos[0].partidas), 2)
        self.assertEqual(
            len(projecoes[datetime.datetime.now().replace(day=1).date()]["1"].vetor_lancamentos[1].partidas), 2)
        self.assertEqual(projecoes[datetime.datetime.now().replace(
            day=1).date()]["1"].vetor_lancamentos[0].partidas[0].natureza, 'D')
        self.assertEqual(projecoes[datetime.datetime.now().replace(day=1).date(
        )]["1"].vetor_lancamentos[0].partidas[0].conta_contabil, '4.1.1.08.0002')
        self.assertEqual(projecoes[datetime.datetime.now().replace(
            day=1).date()]["1"].vetor_lancamentos[0].partidas[0].valor, 150.0)
        self.assertEqual(projecoes[datetime.datetime.now().replace(day=1).date()]["1"].vetor_lancamentos[0].data,
                         datetime.datetime.now().replace(day=10).date())


if __name__ == '__main__':
    unittest.main()
