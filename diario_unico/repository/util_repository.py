from diario_unico.repository.abstract_repository import AbstractRepository


class UtilRepository(AbstractRepository):

    def __init__(self):
        super().__init__("default")

    def getProximovalueCustomSequence(self, chave_sequence: str, tenant: int):
        return 1

        """
        # Monta query
        sql = "insert into util.custom_sequence (chave, tenant, last_value) values (:chave, :tenant, 1)
                    on conflict (tenant, chave) do
                    update set last_value=util.custom_sequence.last_value+1 where util.custom_sequence.tenant=:tenant and util.custom_sequence.chave=:chave
                    returning last_value"

        params = dict()
        params["chave"] = chave_sequence
        params["tenant"] = tenant

        # Executa a query
        result = self.fetchOne(sql, params)

        # retorna o resultado
        if result == None:
            raise Exception(
                'Erro ao recuperar próximo valor da sequence de chave {} no tenant {}.'.format(chave_sequence, tenant))
        else:
            return result["last_value"]"""
