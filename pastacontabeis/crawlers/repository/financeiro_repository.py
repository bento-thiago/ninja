from crawlers.repository.abstract_repository import AbstractRepository


class FinanceiroRepository(AbstractRepository):
    def getConta(self, iban: str, tenant: int):
        # Monta query
        sql = """select * 
                from financeiro.conta_financeira
                where tenant=:tenant
                and iban=:iban"""
        params = dict()
        params["tenant"] = tenant
        params["iban"] = iban
        result = self.fetchOne(sql, params)

        # retorna o resultado
        return result
