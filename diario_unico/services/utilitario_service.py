from diario_unico.repository.utilitario_repository import UtilitarioRepository

class UtilitarioService:
    def __init__(self, repository:UtilitarioRepository):
        self.repository = repository
        
    def exists_pk(self, table_name, nome_campo_pk, tenant, valor_pk):
        #TODO: remover este mock
        if table_name=="estabelecimentos":
            return True
        return self.repository.exists_pk( table_name, nome_campo_pk, tenant, valor_pk)
        
    def exists(self, table_name, nome_campo, tenant, valor):
        return self.repository.exists( table_name, nome_campo, tenant, valor)