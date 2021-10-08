from nasajon.entity.dados_escrituracao_futura import DadosEscrituracaoFutura, DadosItem, ValoresAnteriores
from nasajon.enum.heuristica_projecao import HeuristicaProjecao
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo

from nasajon.tests.pastas_contabeis.pasta_conta_consumo_mock import PastaContaConsumoMock

from nasajon.tests.pastas_contabeis.diario_util_mock import DiarioUtilMock

import datetime
import os
import unittest


class TestPastaContaConsumo(unittest.TestCase):

    def setUp(self):
        self._diario_util_mock = DiarioUtilMock()
        self._pasta = PastaContaConsumoMock(self._diario_util_mock)

        self._dados = DadosEscrituracaoFutura()
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
        self._dados.itens = list()
        self._dados.itens.append(item0)
        self._dados.itens.append(item1)
        self._dados.itens.append(item2)

        # Preenchendo os dados básicos:
        self._dados.dia_apropriacao = 10
        self._dados.dia_vencimento = 15
        self._dados.estabelecimento = "123456"
        self._dados.participante = "654321"
        self._dados.tenant = 47

    def test_get_dados_escrituracao_futura(self):

        dados = dict()
        dados["dia_apropriacao"] = 10
        dados["dia_vencimento"] = 15
        dados["estabelecimento"] = "123456"
        dados["fornecedor"] = "654321"
        dados["tenant"] = 47
        dados["heuristica_valor"] = 1
        dados["valor"] = 100.0

        dados_escrituracao = self._pasta.get_dados_escrituracao_futura(dados)

        # Testando os dados básicos:
        self.assertEqual(dados_escrituracao.dia_apropriacao, 10)
        self.assertEqual(dados_escrituracao.dia_vencimento, 15)
        self.assertEqual(dados_escrituracao.estabelecimento, "123456")
        self.assertEqual(dados_escrituracao.participante, "654321")
        self.assertEqual(dados_escrituracao.tenant, 47)

        # Testando os dados dos itens:
        self.assertEqual(len(dados_escrituracao.itens), 1)
        self.assertEqual(dados_escrituracao.itens[0].codigo, "1")
        self.assertEqual(
            dados_escrituracao.itens[0].heuristica_projecao, HeuristicaProjecao.MEDIA_MOVEL)
        self.assertEqual(dados_escrituracao.itens[0].tipo, "1")
        self.assertEqual(
            dados_escrituracao.itens[0].valor_medio_inicial, 100.0)

        # Testando os dados dos valroes anteriores dos itens:
        self.assertEqual(
            len(dados_escrituracao.itens[0].valores_anteriores), 1)
        self.assertEqual(
            dados_escrituracao.itens[0].valores_anteriores[0].valor, 134.0)

    def test_escriturar_futuro(self):
        # Chamando a escrituração futura:
        self._pasta.escriturar_futuro(self._dados)

        # Validando o resultado gerado:

        # Testando os dados básicos:
        self.assertEqual(
            self._diario_util_mock.documento_recebidos[0].emissao, datetime.datetime.now().replace(day=10).date())
        self.assertEqual(
            self._diario_util_mock.documento_recebidos[0].estabelecimento, "123456")
        self.assertEqual(
            self._diario_util_mock.documento_recebidos[0].participante, "654321")
        self.assertEqual(self._diario_util_mock.tenant_recebidos[0], 47)

        # Testando os dados dos itens:
        self.assertEqual(
            len(self._diario_util_mock.documento_recebidos[0].itens), 1)
        self.assertEqual(
            self._diario_util_mock.documento_recebidos[0].itens[0].codigo, "01")
        self.assertEqual(
            self._diario_util_mock.documento_recebidos[0].itens[0].tipo, ItemDocumentoTipo.ITEM_CONTA_CONSUMO)
        self.assertEqual(
            self._diario_util_mock.documento_recebidos[0].itens[0].valor, 150.0)


if __name__ == '__main__':
    unittest.main()
