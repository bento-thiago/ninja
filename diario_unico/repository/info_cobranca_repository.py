from typing import List

from diario_unico.entity.info_cobranca import InfoCobranca
from diario_unico.repository.abstract_repository import AbstractRepository


class InfoCobrancaRepository(AbstractRepository):
    def insere_info_cobranca(self, tenant:int, infos_cobranca:List[InfoCobranca]):
        sql = """
            insert into infos_cobranca( id, vencimento, data_limite_desconto, data_inicio_multa, percentual_desconto,
                                        percentual_multa, percentual_juros_diario, valor_bruto, valor_liquido, 
                                        texto_instrucao, situacao, cpf_cnpj_cliente, nome_cliente,
                                        documento_id, numero, nosso_numero, endereco_cidade, email, tenant)
            values (:id, :vencimento, :data_limite_desconto, :data_inicio_multa, :percentual_desconto,
                                        :percentual_multa, :percentual_juros_diario, :valor_bruto, :valor_liquido, 
                                        :texto_instrucao, :situacao, :cpf_cnpj_cliente, :nome_cliente,
                                        :documento_id, :numero, :nosso_numero, :endereco_cidade, :email, :tenant);                
        """
        parametros = [info_cobranca.dict() for info_cobranca in infos_cobranca]
        self.executeMany(sql, parametros)

    def listar_de_documentos(self, tenant, ids):
        sql = """
            select 
                id, 
                vencimento, 
                data_limite_desconto, 
                data_inicio_multa, 
                percentual_desconto,
                percentual_multa,
                percentual_juros_diario, 
                valor_bruto, 
                valor_liquido, 
                texto_instrucao, 
                situacao, 
                cpf_cnpj_cliente, 
                nome_cliente,
                documento_id,
                tenant, 
                numero, 
                nosso_numero, 
                endereco_cidade, 
                email
            from infos_cobranca
            where tenant=:tenant
            and documento_id in :ids
        
                                        
        """
        return self.fetchAll(sql,{"tenant":tenant, "ids":ids})