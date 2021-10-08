from diario_unico.repository.abstract_repository import AbstractRepository


class EstabelecimentoRepository(AbstractRepository):
    table_name = "estabelecimentos"
    
    def recuperarEstabelecimentoPeloCodigo(self, estabelecimento: str, tenant: int):
        # Monta query
        sql = """select * 
                from estabelecimentos e
                join pessoas p on p.pessoa=e.pessoa
                where e.tenant=:tenant
                      and codigo=:codigo"""
        params = dict()
        params["tenant"] = tenant
        params["codigo"] = estabelecimento
        result = self.fetchOne(sql, params)

        # retorna o resultado
        if result == None:
            raise Exception('Estabelecimento nao encontrado: {}. Tenant: {}'.format(
                estabelecimento, tenant))
        else:
            return result

    def recuperarEstabelecimentoPeloID(self, identificador, tenant):
        if (identificador == None):
            return None

        # Monta query
        sql = """select * 
                from estabelecimentos e 
                join pessoas p on p.pessoa=e.pessoa
                where e.tenant=:tenant
                      and e.pessoa=:id"""

        params = dict()
        params["tenant"] = tenant
        params["id"] = identificador
        # Executa a query
        result = self.fetchOne(sql, params)

        # retorna o resultado
        if result == None:
            raise Exception('Estabelecimento nao encontrado: '+identificador)
        else:
            return result

    def getEstabelecimentos(self, tenant):
        # Monta query
        sql = """select e.pessoa, p.codigo, p.nomefantasia
                from estabelecimentos e 
                join pessoas p on e.pessoa=p.pessoa and e.tenant=p.tenant
                where e.tenant=:tenant"""
        params = dict()
        params["tenant"] = tenant
        return self.fetchAll(sql, params)
