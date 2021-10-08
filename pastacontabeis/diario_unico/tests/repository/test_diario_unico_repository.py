from diario_unico.enum.documentos.item_documento_tipo_imposto import ItemDocumentoTipoImposto
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from diario_unico.entity.plano_conta_condominio import PlanoContasCondominio

from diario_unico.repository.diario_unico_repository_old import DiarioUnicoRepository

import unittest


class MockCursor:

    def __init__(self):
        self.sqls = list()
        self.params = list()
        self.rowcount = 1
        self.description = [
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
        return [1]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


class MockConnection:

    def __init__(self):
        self._cursor = MockCursor()

    def cursor(self):
        return self._cursor


class TestDiarioUnicoRepository(unittest.TestCase):

    def test_get_imposto_acumulado(self):
        # Montando a conexão mock:
        conn = MockConnection()

        # Instanciando o repository
        repository = DiarioUnicoRepository()

        # Arbitrando a conexão mock:
        repository.set_connection(conn)

        # Executando o método a testar:
        repository.get_imposto_acumulado(
            ItemDocumentoTipoImposto.ICMS,
            [ItemDocumentoTipo.SERVICO],
            [PlanoContasCondominio.CC_1_1_1_01],
            2019,
            10,
            1
        )

        # Realizando as conferências:
        self.assertEqual(conn._cursor.sqls[0], """
            select
                sum(icms_retido_original) as icms_retido_original, sum(icms_retido) as icms_retido, sum(base_icms_retido_original) as base_icms_retido_original, sum(base_icms_retido) as base_icms_retido, sum(aliquota_icms_retido) as aliquota_icms_retido,
                p.codigo as estabelecimento,
                du.situacao
            from
                diario_unico as du join
                pessoas p on (p.pessoa = du.estabelecimento)
            where
                du.sinal = %s and
                du.diario_unico_tipo in (%s) and
                du.conta_contabil in (%s) and
                year(du.data) = %s and
                month(du.data) = %s and
                du.tenant = %s
            group by
                du.estabelecimento,
                du.situacao
        """)

        self.assertEqual(conn._cursor.params[0], [
                         "ENTRADA", "SERVICO", '1.1.1.01', 2019, 10, 1])


if __name__ == '__main__':
    unittest.main()
