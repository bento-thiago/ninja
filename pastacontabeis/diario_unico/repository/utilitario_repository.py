from diario_unico.repository.abstract_repository import AbstractRepository

class UtilitarioRepository(AbstractRepository):
    def exists_pk(self, table_name, nome_campo_pk, tenant, valor_pk):
        sql=f"""
            select 1
            from {table_name}
            where tenant=:tenant
            and {nome_campo_pk}=:valor
        """
        
        return self.fetchOne(sql,{"tenant":tenant, "valor":valor_pk})!=None
        
        
    def exists(self, table_name, nome_campo, tenant, valor):
        sql=f"""
            select 1
            from {table_name}
            where tenant=:tenant
            and {nome_campo}=:valor
        """
        
        return self.fetchOne(sql,{"tenant":tenant, "valor":valor})!=None