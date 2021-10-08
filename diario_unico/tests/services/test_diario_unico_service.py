from diario_unico.enum.documentos.item_documento_tipo_imposto import ItemDocumentoTipoImposto
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from diario_unico.entity.plano_conta_condominio import PlanoContasCondominio

from diario_unico.entity.icms_retido_acumulado import ICMSRetidoAcumulado

from diario_unico.repository.diario_unico_repository_old import DiarioUnicoRepository

from diario_unico.services.diario_unico_service_old import DiarioUnicoService

import unittest


class MockCursor:

    def __init__(self):
        self.sqls = list()
        self.params = list()
        self.rowcount = 1
        self.description = [
            ["estabelecimento"],
            ["situacao"],
            ["icms_retido_original"],
            ["icms_retido"],
            ["base_icms_retido_original"],
            ["base_icms_retido"],
            ["aliquota_icms_retido"]
        ]

    def execute(self, sql, params):
        self.sqls.append(sql)
        self.params.append(params)

    def fetchone(self):
        return (
            "20",
            "PREVISTO",
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
        )

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


class MockConnection:

    def __init__(self):
        self._cursor = MockCursor()

    def cursor(self):
        return self._cursor


class TestDiarioUnicoService(unittest.TestCase):

    def test_get_imposto_acumulado(self):
        # Montando a conexão mock:
        conn = MockConnection()

        # Instanciando o repository
        repository = DiarioUnicoRepository()

        # Arbitrando a conexão mock:
        repository.set_connection(conn)

        # Construindo o service:
        service = DiarioUnicoService(repository)

        # Executando o método a testar:
        retorno = service.get_imposto_acumulado(
            ItemDocumentoTipoImposto.ICMS,
            [ItemDocumentoTipo.SERVICO],
            [PlanoContasCondominio.CC_1_1_1_01],
            2019,
            10,
            1
        )

        # Realizando as conferências:
        self.assertEqual(type(retorno), ICMSRetidoAcumulado)
        self.assertEqual(retorno.valor_retido_original, 1.0)
        self.assertEqual(retorno.valor_retido, 2.0)
        self.assertEqual(retorno.base_original, 3.0)
        self.assertEqual(retorno.base, 4.0)
        self.assertEqual(retorno.aliquota, 5.0)


if __name__ == '__main__':
    unittest.main()
