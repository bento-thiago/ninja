from typing import List

from diario_unico.entity.contrato import Contrato
from diario_unico.repository.abstract_repository import AbstractRepository


class ContratoRepository(AbstractRepository):
    table_name = 'contratos'

    def inserir_contrato(self, contrato: Contrato, tenant: int):
        sql = """
            select 1
            from contratos
            where tenant=:tenant
            and id_compartilhado=:id_compartilhado
        """
        parametros = {"tenant": tenant, "id_compartilhado": contrato.id_compartilhado}
        contrato_base = self.fetchOne(sql, parametros)

        if contrato_base is None:
            sql = """insert into contratos (tenant, id_compartilhado, codigo, descricao, participante_id, 
            estabelecimento, ultimo_registro) values (:tenant, :id_compartilhado, :codigo, :descricao, 
            :participante_id, :estabelecimento, :id_registro) """
            parametros = contrato.dict()
            parametros["tenant"] = tenant
            parametros["participante_id"] = contrato.participante.id_registro
            self.execute(sql, parametros)

        sql = """insert into ordens_registro_contrato (tenant, id_compartilhado, data_registro,
         id_registro) 
        values (:tenant, :id_compartilhado, :data_registro,
         :id_registro); """
        parametros = contrato.dict()
        parametros["tenant"] = tenant
        parametros["participante_id"] = contrato.participante.id_registro
        self.execute(sql, parametros)

        sql = """
            insert into itens_contrato(tenant, id, id_servico, registro_contrato_id,	valor_unitario,
                    quantidade, valor_total,  recorrente, codigo_item_contrato,  codigo_servico,
                    descricao, incidencia_inss, aliquota_inss, aliquota_ir,
                    aliquota_pis,  aliquota_cofins,  aliquota_csll, competencia_inicio, competencia_final, 
                    dia_processamento, tipo_recorrencia, tipo_cobranca, dia_vencimento, 
                    dias_antes_vencimento_para_desconto, dias_apos_vencimento_para_multa, 
                    dias_apos_vencimento_para_juros, situacao)
            values (:tenant, :id, :id_servico, :registro_contrato_id,	:valor_unitario,
                    :quantidade, :valor_total,  :recorrente, :codigo_item_contrato,  :codigo_servico,
                    :descricao, :incidencia_inss, :aliquota_inss, :aliquota_ir,
                    :aliquota_pis,  :aliquota_cofins,  :aliquota_csll, :competencia_inicio, :competencia_final, 
                    :dia_processamento, :tipo_recorrencia, :tipo_cobranca, :dia_vencimento, 
                    :dias_antes_vencimento_para_desconto, :dias_apos_vencimento_para_multa, 
                    :dias_apos_vencimento_para_juros, :situacao)
        
        """
        for item in contrato.itens:
            parametros = item.dict()
            parametros["tenant"] = tenant
            self.execute(sql, parametros)

    def listar_dados_base_contratos(self, tenant: int) -> List[dict]:
        sql = """
            select c.tenant,
                c.id_compartilhado,
                c.codigo,
                c.participante_id,
                c.descricao,
                c.estabelecimento,
                orc.id_registro,
                orc.data_registro
        from contratos c
        join ordens_registro_contrato orc on orc.tenant=c.tenant and orc.id_registro=c.ultimo_registro
        where c.tenant=:tenant
        """

        parametros = {"tenant": tenant}
        contratos_dict = self.fetchAll(sql, parametros)
        return contratos_dict

    def listar_itens_varios_contratos(self, tenant, ids_registro):
        sql = """
            select
                tenant,
                id,
                id_servico,
                registro_contrato_id,
                valor_unitario,
                quantidade,
                valor_total,
                recorrente,
                codigo_item_contrato,
                codigo_servico,
                descricao,
                incidencia_inss,
                aliquota_ir,
                aliquota_inss,
                aliquota_pis,
                aliquota_cofins,
                aliquota_csll,
                competencia_inicio,
                competencia_final,
                dia_processamento,
                tipo_recorrencia,
                tipo_cobranca,
                dia_vencimento,
                dias_antes_vencimento_para_desconto,
                dias_apos_vencimento_para_multa,
                dias_apos_vencimento_para_juros,
                situacao
            from itens_contrato
            where registro_contrato_id in :ids_registro
        """
        parametros = {"tenant": tenant, "ids_registro": ids_registro}
        return self.fetchAll(sql, parametros)
