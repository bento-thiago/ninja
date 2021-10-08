from diario_unico.entity.conta_contabil import ContaContabil
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo

from diario_unico.repository.abstract_repository import AbstractRepository

from typing import List
from diario_unico.enum.sinal import Sinal


class PlanoContasRepository(AbstractRepository):

    def __init__(self):
        super().__init__()

    def reconstroi_plano_contas(self, empresa: str, tenant: int):
        # Obtem ID e máscara da empresa
        params = dict()
        params["empresa"] = empresa
        params["tenant"] = tenant
        sql = 'select empresa, mascara_contabil from empresas where codigo=:empresa and tenant=:tenant'
        result = self.fetchOne(sql, params)
        empresa_id = result['empresa']

        params = dict()
        params['empresa'] = empresa_id
        params['tenant'] = tenant

        # Depara direto, Tipo de associação 1
        sql = """insert into contas_personalizadas_cache (empresa, ano, codigo, nome, conta_contabil, participante, rateio, tenant)
                select :empresa, cp.exercicio, cp.codigo, cp.nome, cc.conta_contabil, null, 1, cp.tenant
                from  contas_personalizadas cp
                join associacao_contas_personalizadas acp on acp.conta_personalizada=cp.conta_personalizada and acp.empresa=:empresa and acp.tipo_associacao=1
                join conta_contabil cc on cc.conta_contabil=acp.conta_contabil
                where cp.tenant=:tenant"""
        self.execute(sql, params)

        # Filtro, Tipo de associação 2
        sql = """insert into contas_personalizadas_cache (empresa, ano, codigo, nome, conta_contabil, participante, rateio, tenant)
        select :empresa, cp.exercicio, cp.codigo, cp.nome, cc.conta_contabil, fac.valor, 1, cp.tenant
        from  contas_personalizadas cp
        join associacao_contas_personalizadas acp on acp.conta_personalizada=cp.conta_personalizada and acp.empresa=:empresa and acp.tipo_associacao=2
        join conta_contabil cc on cc.conta_contabil=acp.conta_contabil and cp.tenant=:tenant
        join filtro_associacao_contas fac on fac.conta_personalizada=acp.conta_personalizada and fac.conta_contabil=cc.conta_contabil and dimensao=1 and tipo_filtro=1"""
        self.execute(sql, params)

        # Resto de filtro, Tipo de associacao 3 (Parte 1, removendo saldo para os filtros em uso)
        sql = """insert into contas_personalizadas_cache (empresa, ano, codigo, nome, conta_contabil, participante, rateio, tenant)
                select cpc.empresa, cpc.ano, cpc.codigo, cpc.nome, cpc.conta_contabil, cpc.participante, -1, cpc.tenant
                from contas_personalizadas_cache cpc
                join conta_contabil cc on cc.conta_contabil=cpc.conta_contabil
                join associacao_contas_personalizadas acp on acp.conta_contabil=cc.conta_contabil and acp.tipo_associacao=3
                
                where cpc.empresa=:empresa and participante is not null"""
        self.execute(sql, params)

        # Resto de filtro, Tipo de associacao 3 (Parte 2, adicionando vinculo sem participante)
        sql = """insert into contas_personalizadas_cache (empresa, ano, codigo, nome, conta_contabil, participante, rateio, tenant)
                select :empresa, cp.exercicio, cp.codigo, cp.nome, cc.conta_contabil, null, 1, cp.tenant
                from  contas_personalizadas cp
                join associacao_contas_personalizadas acp on acp.conta_personalizada=cp.conta_personalizada and acp.empresa=:empresa and acp.tipo_associacao=3
                join conta_contabil cc on cc.conta_contabil=acp.conta_contabil and cp.tenant=:tenant"""
        self.execute(sql, params)

        # Rateio, Tipo de associacao 4
        sql = """insert into contas_personalizadas_cache (empresa, ano, codigo, nome, conta_contabil, participante, rateio, tenant)
                select :empresa, cp.exercicio, cp.codigo, cp.nome, cc.conta_contabil, null, convert(fac.valor, decimal(5,4)), cp.tenant
                from  contas_personalizadas cp
                join associacao_contas_personalizadas acp on acp.conta_personalizada=cp.conta_personalizada and acp.empresa=:empresa and acp.tipo_associacao=4
                join conta_contabil cc on cc.conta_contabil=acp.conta_contabil and cp.tenant=:tenant
                join filtro_associacao_contas fac on fac.conta_personalizada=acp.conta_personalizada and fac.conta_contabil=cc.conta_contabil"""
        self.execute(sql, params)

        # Abertura automática, Tipo de associacao 5
        sql = """insert into contas_personalizadas_cache (empresa, ano, codigo, nome, conta_contabil, participante, rateio, tenant)
        select :empresa, cp.exercicio, colocar_mascara(cp.codigo,emp.mascara_contabil,coalesce(p.indice_contabil,count(1) over ( ROWS UNBOUNDED PRECEDING))) , p.nomefantasia, cc.conta_contabil, p.pessoa, 1, cp.tenant
        from  contas_personalizadas cp
        join associacao_contas_personalizadas acp on acp.conta_personalizada=cp.conta_personalizada and acp.empresa=:empresa and acp.tipo_associacao=5
        join conta_contabil cc on cc.conta_contabil=acp.conta_contabil
        join empresas emp on emp.empresa=:empresa and cp.tenant=:tenant
        join pessoas p on p.tenant=cp.tenant and p.ativo_fornecedor=1"""
        self.execute(sql, params)

        # Contas sintéticas
        sql = """insert into contas_personalizadas_cache (empresa, ano, codigo, nome, conta_contabil, participante, rateio, tenant)
        select :empresa, cp.exercicio, cp.codigo, cp.nome, 'conta_sintetica', null, 1, cp.tenant
        from  contas_personalizadas cp
        where not exists (select * from contas_personalizadas_cache cpc where cpc.codigo=cp.codigo)
        and cp.tenant=:tenant"""
        self.execute(sql, params)
