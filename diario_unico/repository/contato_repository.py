from diario_unico.repository.abstract_repository import AbstractRepository
from diario_unico.entity.contato import Contato
from diario_unico.entity.pessoa import Pessoa

class ContatoRepository(AbstractRepository):
    def inserir_contato(self, contato:Contato, tenant:int, pessoa:Pessoa):
        sql = """
            insert into contatos(tenant, id, nome_ou_descricao, telefone, pessoa_registro, email)
            values (:tenant, :id, :nome_ou_descricao, :telefone, :pessoa_registro, :email)        
        """
        parametros = contato.dict()
        parametros["tenant"] = tenant
        self.execute(sql,parametros)

    def listar_dados_contatos_participantes(self, tenant, ids_registro):
        sql = """
            select
                tenant,
                id,
                pessoa_registro,
                nome_ou_descricao,
                telefone,
                email
            from contatos
            where tenant=:tenant and pessoa_registro in :ids_registro
        """
        parametros = {"tenant": tenant, "ids_registro": ids_registro}
        return self.fetchAll(sql, parametros)