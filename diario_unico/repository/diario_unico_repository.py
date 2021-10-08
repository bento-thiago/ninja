from typing import List
from uuid import UUID

from diario_unico.entity.linha_diario_unico import LinhaDiarioUnico
from diario_unico.repository.abstract_repository import AbstractRepository


class DiarioUnicoRepository(AbstractRepository):
    def insere_diario(self, tenant:int, linhas:List[LinhaDiarioUnico]):
        sql = """
            insert into diario_unico( id, tenant, estabelecimento, 
            participante, cnae, documento_numero, documento_serie, documento_subserie, documento_sinal, documento_id, 
            documento_emissao, documento_tipo, documento_modelo, documento_situacao, item_id, item_ordem,
            item_codigo, item_descricao, data_registro, origem, tipo_tributacao_servico, tipoIss, tipo_tributacao_iss,
            recorrente, situacao, base_iss, aliquota_iss, iss_retido, base_irrf, aliquota_irrf, irrf_retido, base_inss,
            incidencia_inss, inss_retido, base_csll, aliquota_csll, csll_retido, base_pis, aliquota_pis, pis_retido,
            base_cofins, aliquota_cofins, cofins_retido, info_pagamento, info_cobranca, lancamento_ID,
            lancamento_numero, lancamento_data, lancamento_natureza, lancamento_ordem, conta_contabil, 
            lancamento_historico, valor, base, percentagem_sobre_base, momento, pasta_contabil, 
            codigo_contabil_financeiro)
            values
            ( :id, :tenant, :estabelecimento,
            :participante, :cnae, :documento_numero, :documento_serie, :documento_subserie, :documento_sinal, 
            :documento_id, :documento_emissao, :documento_tipo, :documento_modelo, :documento_situacao, :item_id, 
            :item_ordem, :item_codigo, :item_descricao, :data_registro, :origem, :tipo_tributacao_servico, :tipoIss, 
            :tipo_tributacao_iss, :recorrente, :situacao, :base_iss, :aliquota_iss, :iss_retido, :base_irrf, 
            :aliquota_irrf, :irrf_retido, :base_inss, :incidencia_inss, :inss_retido, :base_csll, :aliquota_csll, 
            :csll_retido, :base_pis, :aliquota_pis, :pis_retido, :base_cofins, :aliquota_cofins, :cofins_retido, 
            :info_pagamento, :info_cobranca, :lancamento_ID, :lancamento_numero, :lancamento_data, :lancamento_natureza,
            :lancamento_ordem, :conta_contabil, :lancamento_historico, :valor, :base, :percentagem_sobre_base, 
            :momento, :pasta_contabil, :codigo_contabil_financeiro)
        """
        parametros = list()
        for linha in linhas:
            parametros.append(linha.dict())
        
        self.executeMany(sql, parametros)

    def listar_linha_de_documentos(self, tenant:int, documentos_ids:List[UUID]):
        sql = """
            select 
                id, 
                tenant, 
                estabelecimento, 
                participante, 
                cnae, 
                documento_numero, 
                documento_serie, 
                documento_subserie, 
                documento_sinal, 
                documento_id, 
                documento_emissao, 
                documento_tipo, 
                documento_modelo, 
                documento_situacao, 
                item_id, 
                item_ordem,
                item_codigo, 
                item_descricao, 
                data_registro, 
                origem, 
                tipo_tributacao_servico, 
                tipoIss, 
                tipo_tributacao_iss,
                recorrente, 
                situacao, 
                base_iss, 
                aliquota_iss, 
                iss_retido, 
                base_irrf, 
                aliquota_irrf, 
                irrf_retido, 
                base_inss,
                incidencia_inss, 
                inss_retido, 
                base_csll, 
                aliquota_csll, 
                csll_retido, 
                base_pis, 
                aliquota_pis, 
                pis_retido,
                base_cofins, 
                aliquota_cofins, 
                cofins_retido, 
                info_pagamento, 
                info_cobranca, 
                lancamento_ID,
                lancamento_numero, 
                lancamento_data, 
                lancamento_natureza, 
                lancamento_ordem, 
                conta_contabil, 
                lancamento_historico, 
                valor, 
                base, 
                percentagem_sobre_base, 
                momento, 
                pasta_contabil, 
                codigo_contabil_financeiro
        from diario_unico
        where tenant=:tenant
        and documento_id in :documentos_ids
        """
        parametros = {"tenant":tenant, "documentos_ids":documentos_ids}
        return self.fetchAll(sql, parametros)
        