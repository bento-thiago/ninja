from diario_unico.entity.documento import Documento
from diario_unico.repository.abstract_repository import AbstractRepository


class DocumentoRepository(AbstractRepository):
    def insere_documento(self, tenant:int, documento:Documento):
        sql = """
            insert into documentos(id, estabelecimento, participante, token_facilitador, cnae, discriminacao, 
                municipio_prestacao, numero, serie, subserie, tipo_tributacao_servico, tipoIss, emissao,
                data_registro, modelo, tenant, sinal, situacao, origem, tipo)
            values (:id, :estabelecimento, :participante, :token_facilitador, :cnae, :discriminacao, 
                :municipio_prestacao, :numero, :serie, :subserie, :tipo_tributacao_servico, :tipoIss, :emissao,
                :data_registro, :modelo, :tenant, :sinal, :situacao, :origem, :tipo)
        """
        parametros = documento.dict()
        self.execute(sql, parametros)

    def listar_dados_documentos(self, tenant):
        sql = """
        select id, 
                estabelecimento, 
                participante, 
                token_facilitador, 
                cnae, 
                discriminacao, 
                municipio_prestacao, 
                numero, 
                serie, 
                subserie, 
                tipo_tributacao_servico, 
                tipoIss, 
                emissao,
                data_registro, 
                modelo, 
                tenant, 
                sinal, 
                situacao, 
                origem, 
                tipo
        from documentos
        where tenant=:tenant
        """
        parametros = {"tenant":tenant}
        return self.fetchAll(sql, parametros)