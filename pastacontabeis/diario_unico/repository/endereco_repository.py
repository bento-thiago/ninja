from diario_unico.entity.endereco import Endereco
from diario_unico.entity.pessoa import Pessoa
from diario_unico.repository.abstract_repository import AbstractRepository


class EnderecoRepository(AbstractRepository):
    def inserir_endereco(self, endereco: Endereco, tenant: int, pessoa: Pessoa):
        sql = """
            insert into enderecos(tenant, id, pessoa_registro, tipo_logradouro,
                    cidade_ibge, logradouro, numero, complemento, bairro,
                     cep, uf, pais_codigo, referencia)
            values (:tenant, :id, :pessoa_registro, :tipo_logradouro,
                    :cidade_ibge, :logradouro, :numero, :complemento, :bairro,
                    :cep, :uf, :pais_codigo, :referencia)        
        """
        parametros = endereco.dict()
        parametros["tenant"] = tenant
        self.execute(sql, parametros)

    def listar_dados_enderecos_participantes(self, tenant, ids_registro):
        sql = """
            select
                tenant,
                id,
                pessoa_registro,
                tipo_logradouro,
                cidade_ibge,
                logradouro,
                numero,
                complemento,
                bairro,
                cep,
                uf,
                pais_codigo,
                referencia
            from enderecos
            where tenant=:tenant
            and pessoa_registro in :ids_registro            
        """
        parametros = {"tenant":tenant, "ids_registro":ids_registro}
        return self.fetchAll(sql, parametros)