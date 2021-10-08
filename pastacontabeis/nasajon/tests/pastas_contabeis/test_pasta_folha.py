import unittest
from nasajon.tests.pastas_contabeis.diario_util_mock import DiarioUtilMock
from nasajon.pastas_contabeis.pasta_folha import PastaFolha
from diario_unico.entity.documento import Documento
from diario_unico.enum.situacao import Situacao
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.enum.sinal import Sinal

from diario_unico.entity.item_documento import ItemDocumento
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
import os
from datetime import date, datetime
from diario_unico.entity.lancamento import Lancamento, SituacaoDiario
from diario_unico.entity.partida import Partida
from nasajon.util.json_util import JsonUtil
import copy
from dateutil.relativedelta import relativedelta
from diario_unico.util.date_util import ultimoDiaMes
from nasajon.entity.dados_integracao_pagamento_a_trabalhador import DadosIntegracaoPagamentoATrabalhador
from diario_unico.entity.estabelecimento import Estabelecimento
from nasajon.entity.departamento import Departamento
from nasajon.entity.lotacao import Lotacao
from nasajon.entity.rubrica import Rubrica
from nasajon.enum.folha.rubrica_tipo_valor import RubricaTipoValor
from nasajon.entity.trabalhador import Trabalhador
from nasajon.entity.calculo_trabalhador import CalculoTrabalhador
from nasajon.entity.mudanca_trabalhador import MudancaTrabalhador
from nasajon.util.objeto_util import ObjetosUtils


class TestPastaFolha(unittest.TestCase):
    def setUp(self):
        os.environ["usar_time_service"] = "False"

        self._diario_util_mock = DiarioUtilMock()
        self._pasta = PastaFolha(self._diario_util_mock)

    def test_get_dados_escrituracao_futura(self):
        dados = dict()
        dados["ano"] = 2020
        dados["mes"] = 3
        dados["estabelecimento"] = "01"
        dados["tenant"] = 25

        resultado = self._pasta.get_dados_escrituracao_futura(dados)
        print(resultado)

        self.assertIsInstance(resultado, dict)
        self.assertEqual(resultado["ano"], dados["ano"])
        self.assertEqual(resultado["mes"], dados["mes"])
        self.assertEqual(resultado["estabelecimento"],
                         dados["estabelecimento"])
        self.assertEqual(resultado["tenant"], dados["tenant"])
        self.assertIsInstance(resultado["documentos_anteriores"], list)
        self.assertEqual(len(resultado["documentos_anteriores"]), 3)

        self.assertEqual(resultado["documentos_anteriores"][0].numero, "03")
        self.assertEqual(resultado["documentos_anteriores"]
                         [0].estabelecimento, dados["estabelecimento"])
        self.assertEqual(resultado["documentos_anteriores"]
                         [0].data_lancamento, date(2020, 2, 29))

        self.assertEqual(resultado["documentos_anteriores"][1].numero, "02")
        self.assertEqual(resultado["documentos_anteriores"]
                         [1].data_lancamento, date(2020, 1, 31))

        self.assertEqual(resultado["documentos_anteriores"][2].numero, "01")
        self.assertEqual(resultado["documentos_anteriores"]
                         [2].data_lancamento, date(2019, 11, 1))

    def test_escriturar_futuro(self):
        self._diario_util_mock.documento_recebidos = list()
        dados = dict()
        dados["ano"] = 2020
        dados["mes"] = 3
        dados["estabelecimento"] = "Estab01"
        dados["tenant"] = 25

        doc1 = self.criar_documento(data=date(2020, 2, 29),
                                    valor_salario=1500,
                                    valor_faltas=500,
                                    id="1ecf08cf-992c-4866-80ea-0edaf48462f9",
                                    estab="Estab01",
                                    empresa="Empresa01",
                                    grupo="Grupo01",
                                    numero="01",
                                    trabalhador="34154735039")
        doc2 = self.criar_documento(data=date(2020, 1, 31),
                                    valor_salario=1500,
                                    valor_faltas=200,
                                    id="1ecf08cf-992c-4866-80ea-0edaf48462f9",
                                    estab="Estab01",
                                    empresa="Empresa01",
                                    grupo="Grupo01",
                                    numero="02",
                                    trabalhador="34154735039")
        doc3 = self.criar_documento(data=date(2019, 12, 31),
                                    valor_salario=1500,
                                    valor_faltas=0,
                                    id="1ecf08cf-992c-4866-80ea-0edaf48462f9",
                                    estab="Estab01",
                                    empresa="Empresa01",
                                    grupo="Grupo01",
                                    numero="03",
                                    trabalhador="34154735039")
        doc4 = self.criar_documento(data=date(2020, 2, 29),
                                    valor_salario=1200,
                                    valor_faltas=150,
                                    id="1ecf08cf-992c-4866-80ea-0edaf48462f9",
                                    estab="Estab01",
                                    empresa="Empresa01",
                                    grupo="Grupo01",
                                    numero="04",
                                    trabalhador="76845333041")
        doc5 = self.criar_documento(data=date(2020, 1, 31),
                                    valor_salario=1200,
                                    valor_faltas=0,
                                    id="1ecf08cf-992c-4866-80ea-0edaf48462f9",
                                    estab="Estab01",
                                    empresa="Empresa01",
                                    grupo="Grupo01",
                                    numero="05",
                                    trabalhador="76845333041")
        doc6 = self.criar_documento(data=date(2020, 1, 31),
                                    valor_salario=4500,
                                    valor_faltas=4000,
                                    id="1ecf08cf-992c-4866-80ea-0edaf48462f9",
                                    estab="Estab01",
                                    empresa="Empresa01",
                                    grupo="Grupo01",
                                    numero="06",
                                    trabalhador="53115601000")
        dados["documentos_anteriores"] = [doc1, doc4, doc2, doc5, doc6, doc3]

        self._pasta.escriturar_futuro(dados)
        # Começa Asserts
        documentos = self._diario_util_mock.documento_recebidos
        self.assertEqual(len(documentos), 36)

        documentos_marcos = [
            doc for doc in documentos if doc.itens[0].trabalhador == "34154735039"]
        documentos_Antonio = [
            doc for doc in documentos if doc.itens[0].trabalhador == "76845333041"]
        documentos_Francisco = [
            doc for doc in documentos if doc.itens[0].trabalhador == "53115601000"]
        documentos_marcos = sorted(
            documentos_marcos, key=lambda x: x.data_lancamento)
        documentos_Antonio = sorted(
            documentos_Antonio, key=lambda x: x.data_lancamento)
        documentos_Francisco = sorted(
            documentos_Francisco, key=lambda x: x.data_lancamento)

        self.assertEqual(len(documentos_marcos), 12)
        self.assertEqual(len(documentos_Antonio), 12)
        self.assertEqual(len(documentos_Francisco), 12)

        media_salario_marcos = 1500
        media_salario_antonio = 1200
        media_salario_francisco = 4500
        media_faltas_marcos = 233.33
        media_faltas_antonio = 75
        media_faltas_francisco = 4000

        for i in range(0, 12):
            # Verifica valores
            self.assertEqual(
                documentos_marcos[i].valor, media_salario_marcos-media_faltas_marcos)
            self.assertEqual(
                documentos_Antonio[i].valor, media_salario_antonio-media_faltas_antonio)
            self.assertEqual(
                documentos_Francisco[i].valor, media_salario_francisco-media_faltas_francisco)

            # verifica datas
            self.assertEqual(documentos_marcos[i].data_lancamento, ultimoDiaMes(
                date(2020, 3, 1)+relativedelta(months=i)))

    def test_escriturar_futuro_ajuste(self):
        self._diario_util_mock.documento_recebidos = list()
        dados = DadosIntegracaoPagamentoATrabalhador()
        dados.ano = 2020
        dados.mes = 3
        dados.tipo_calculo = "Fo"
        dados.tenant = "101"
        dados.estabelecimentos.append(Estabelecimento(
            "36e5d08d-7334-45d7-b660-644ea3b08aa2", "01"))
        dados.departamentos.append(Departamento(
            id="032457fd-e047-4987-b0c4-10fe7dadf4b9", codigo="DP01", nome="Departamento 1"))
        dados.departamentos.append(Departamento(
            id="2584a663-a643-49af-a2ad-db42211d7f06", codigo="DP02", nome="Departamento 2"))
        dados.lotacoes.append(Lotacao(
            id="0f21b2c1-4dcc-4cb0-9f73-199475e0cf0e", codigo="LOT01", nome="Lotacao01"))
        dados.rubricas.append(Rubrica(id="3f91d58f-77e1-46a9-8404-9f3c325ca47e", codigo="01",
                                      nome="01 - Salário, vencimento, soldo ou subsídio", tipovalor=RubricaTipoValor.RENDIMENTO, categoria="1000"))
        dados.rubricas.append(Rubrica(id="e196394e-79ea-4390-8eb3-f79d386bb86b", codigo="02",
                                      nome="02 - Falta", tipovalor=RubricaTipoValor.DESCONTO, categoria="9209"))
        dados.trabalhadores.append(Trabalhador(
            id="2cf1d734-1b65-4663-a12e-b10687e4afe0", codigo="MARCOS", nome="Marcos da Silva", cpf="74831768065"))
        dados.trabalhadores.append(Trabalhador(
            id="738cbe4c-9b4e-4d2a-b33b-f3c5b3fabb5a", codigo="RODRIGO", nome="Rodrigo Dias", cpf="72803243040"))
        dados.mudancas_trabalhadores.append(MudancaTrabalhador(data_inicial=date(2020, 1, 1),
                                                               data_final=None,
                                                               estabelecimento="36e5d08d-7334-45d7-b660-644ea3b08aa2",
                                                               departamento="032457fd-e047-4987-b0c4-10fe7dadf4b9",
                                                               lotacao="0f21b2c1-4dcc-4cb0-9f73-199475e0cf0e",
                                                               trabalhador="2cf1d734-1b65-4663-a12e-b10687e4afe0"))
        dados.mudancas_trabalhadores.append(MudancaTrabalhador(data_inicial=date(2020, 1, 1),
                                                               data_final=None,
                                                               estabelecimento="36e5d08d-7334-45d7-b660-644ea3b08aa2",
                                                               departamento="2584a663-a643-49af-a2ad-db42211d7f06",
                                                               lotacao="0f21b2c1-4dcc-4cb0-9f73-199475e0cf0e",
                                                               trabalhador="738cbe4c-9b4e-4d2a-b33b-f3c5b3fabb5a"))

        dados.calculos.append(CalculoTrabalhador(id="6bbe33a7-3e86-4f59-a00b-e78fd0f4c2bf",
                                                 data_de_pagamento=date(
                                                     2020, 3, 31),
                                                 valor=1500,
                                                 rubrica="3f91d58f-77e1-46a9-8404-9f3c325ca47e",
                                                 ano=2020,
                                                 mes=3,
                                                 trabalhador="2cf1d734-1b65-4663-a12e-b10687e4afe0",
                                                 ano_gerador=2020,
                                                 mes_gerador=3))
        dados.calculos.append(CalculoTrabalhador(id="12db6e9e-fd66-4d8a-9099-154182d803e0",
                                                 data_de_pagamento=date(
                                                     2020, 3, 31),
                                                 valor=350,
                                                 rubrica="e196394e-79ea-4390-8eb3-f79d386bb86b",
                                                 ano=2020,
                                                 mes=3,
                                                 trabalhador="2cf1d734-1b65-4663-a12e-b10687e4afe0",
                                                 ano_gerador=2020,
                                                 mes_gerador=3))
        dados.calculos.append(CalculoTrabalhador(id="d7b196d1-3991-4095-bbb9-717e39da406a",
                                                 data_de_pagamento=date(
                                                     2020, 3, 31),
                                                 valor=2500,
                                                 rubrica="3f91d58f-77e1-46a9-8404-9f3c325ca47e",
                                                 ano=2020,
                                                 mes=3,
                                                 trabalhador="738cbe4c-9b4e-4d2a-b33b-f3c5b3fabb5a",
                                                 ano_gerador=2020,
                                                 mes_gerador=3))
        self._pasta.escriturar_futuro_ajuste(JsonUtil().toDict(dados), False)

        self.assertEqual(len(self._diario_util_mock.documento_recebidos), 2)
        for documento in self._diario_util_mock.documento_recebidos:
            self.assertEqual(documento.ano, 2020)
            self.assertEqual(documento.competencia_inicial, date(2020, 3, 1))
            self.assertEqual(documento.competencia_final, date(2020, 3, 31))
            self.assertEqual(documento.data_lancamento, date(2020, 3, 31))
            self.assertEqual(documento.estabelecimento, "01")
            self.assertEqual(documento.situacao, Situacao.PREVISTO)
            self.assertEqual(documento.sinal, Sinal.SAIDA)
            if documento.itens[0].trabalhador == "74831768065":
                self.assertEqual(documento.valor, 1150)
                self.assertEqual(len(documento.itens), 2)
            else:
                self.assertEqual(documento.valor, 2500)

    def assertObjeto(self, objeto1, objeto2):
        d1 = JsonUtil().toDict(objeto1)
        d2 = JsonUtil().toDict(objeto2)
        self.assertDictEqual(d1, d2)

    def criar_documento(self, data: date, valor_salario, valor_faltas, id, estab, empresa, grupo, numero, trabalhador):
        doc1 = Documento()
        doc1.ano = data.year
        doc1.competencia_final = data
        doc1.competencia_inicial = data.replace(day=1)
        doc1.data_criacao = doc1.competencia_final
        doc1.data_entrada = doc1.competencia_final
        doc1.data_lancamento = doc1.competencia_final
        doc1.data_pagamento = doc1.competencia_final
        doc1.documento = id
        doc1.emissao = doc1.competencia_final
        doc1.empresa = empresa
        doc1.estabelecimento = estab
        doc1.grupo_empresarial = grupo
        doc1.numero = numero
        doc1.sinal = Sinal.SAIDA
        doc1.situacao = Situacao.REALIZADO
        doc1.tipo = DocumentoTipo.FOLHA
        doc1.valor = valor_salario - valor_faltas
        doc1.participante = trabalhador
        item1 = ItemDocumento()
        item1.codigo = "1000"
        item1.departamento = "DP1"
        item1.descricao = "01 - Salário, vencimento, soldo ou subsídio"
        item1.rubrica = "01 - Salário, vencimento, soldo ou subsídio"
        item1.rubrica_esocial = "1000"
        item1.tipo = ItemDocumentoTipo.DETALHE_FOLHA
        item1.trabalhador = trabalhador
        item1.valor = valor_salario
        lanc1 = Lancamento()
        lanc1.data = doc1.competencia_final
        lanc1.numero = 1
        lanc1.situacao = SituacaoDiario.REALIZADO
        lanc2 = Lancamento()
        lanc2.data = doc1.competencia_final
        lanc2.numero = 2
        lanc2.situacao = SituacaoDiario.PREVISTO
        partida1 = Partida()
        partida1.conta_contabil = "4.1.1.01.0015"
        partida1.natureza = "D"
        partida1.ordem = 1
        partida1.valor = valor_salario
        partida2 = Partida()
        partida2.conta_contabil = "2.1.2.03.0003"
        partida2.natureza = "C"
        partida2.ordem = 2
        partida2.valor = valor_salario
        partida3 = Partida()
        partida3.conta_contabil = "2.1.2.03.0003"
        partida3.natureza = "D"
        partida3.ordem = 3
        partida3.valor = valor_salario
        partida4 = Partida()
        partida4.conta_contabil = "1.1.1.01.0001"
        partida4.natureza = "C"
        partida4.ordem = 4
        partida4.valor = valor_salario
        lanc1.partidas.append(partida1)
        lanc1.partidas.append(partida2)
        lanc2.partidas.append(partida3)
        lanc2.partidas.append(partida4)
        item1.lancamentos.append(lanc1)
        item1.lancamentos.append(lanc2)
        doc1.itens.append(item1)

        if valor_faltas > 0:
            item2 = ItemDocumento()
            item2.codigo = "9209"
            item2.departamento = "DP1"
            item2.descricao = "02 - Faltas"
            item2.rubrica = "02 - Faltas"
            item2.rubrica_esocial = "9209"
            item2.tipo = ItemDocumentoTipo.DETALHE_FOLHA
            item2.trabalhador = trabalhador
            item2.valor = valor_faltas
            lanc1 = Lancamento()
            lanc1.data = doc1.competencia_final
            lanc1.numero = 1
            lanc1.situacao = SituacaoDiario.REALIZADO
            lanc2 = Lancamento()
            lanc2.data = doc1.competencia_final
            lanc2.numero = 2
            lanc2.situacao = SituacaoDiario.PREVISTO
            partida1 = Partida()
            partida1.conta_contabil = "2.1.2.03.0003"
            partida1.natureza = "D"
            partida1.ordem = 1
            partida1.valor = valor_faltas
            partida2 = Partida()
            partida2.conta_contabil = "4.1.1.01.0015"
            partida2.natureza = "C"
            partida2.ordem = 2
            partida2.valor = valor_faltas
            partida3 = Partida()
            partida3.conta_contabil = "1.1.1.01.0001"
            partida3.natureza = "D"
            partida3.ordem = 3
            partida3.valor = valor_faltas
            partida4 = Partida()
            partida4.conta_contabil = "2.1.2.03.0003"
            partida4.natureza = "C"
            partida4.ordem = 4
            partida4.valor = valor_faltas

            lanc1.partidas.append(partida1)
            lanc1.partidas.append(partida2)
            lanc2.partidas.append(partida3)
            lanc2.partidas.append(partida4)
            item2.lancamentos.append(lanc1)
            item2.lancamentos.append(lanc2)

            doc1.itens.append(item2)
        return doc1


if __name__ == "__main__":
    unittest.main()
