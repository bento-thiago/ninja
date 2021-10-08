from typing import List
from uuid import UUID

from diario_unico.entity.pessoa import Pessoa
from diario_unico.repository.abstract_repository import AbstractRepository


class PessoasRepository(AbstractRepository):
    table_name = 'pessoas'

    def inserir_pessoa(self, pessoa: Pessoa, tenant: int):
        # Verifica se precisa inserir linha base
        sql = f"""
            select 1
            from pessoas
            where tenant=:tenant
            and id_compartilhado=:valor
        """

        ja_existe = self.fetchOne(sql, {"tenant": tenant, "valor": pessoa.id_compartilhado}) != None

        if not ja_existe:
            # Insere a linha base
            sql = """
                insert into pessoas  (tenant, id_compartilhado, codigo, registro_principal)
                values (:tenant, :id_compartilhado, :codigo, :id_registro)
            """
            parametros = pessoa.dict()
            parametros["tenant"] = tenant
            self.execute(sql, parametros)

        # Insere o registro
        sql = """
            INSERT INTO pessoas_registros (tenant, id_compartilhado, id_registro, cpf_cnpj,
                        nome_fantasia, razao_social, qualificacao, inscricao_municipal, inscricao_estadual, 
                        origem_informacoes, tipo_simples_nacional, registro_papel, endereco_cobranca,
                        endereco_principal, contato_cobranca, contato_principal, contrato_id)
                VALUES(:tenant, :id_compartilhado, :id_registro, :cpf_cnpj,
                        :nome_fantasia, :razao_social, :qualificacao, :inscricao_municipal, :inscricao_estadual, 
                        :origem_informacoes, :tipo_simples_nacional, :registro_papel, :endereco_cobranca,
                        :endereco_principal, :contato_cobranca, :contato_principal, :contrato_id);

        """
        parametros = pessoa.dict()
        parametros["tenant"] = tenant
        if pessoa.endereco_cobranca is not None:
            parametros["endereco_cobranca"] = pessoa.endereco_cobranca.id
        if pessoa.endereco_principal is not None:
            parametros["endereco_principal"] = pessoa.endereco_principal.id
        if pessoa.contato_principal is not None:
            parametros["contato_principal"] = pessoa.contato_principal.id
        if pessoa.contato_cobranca is not None:
            parametros["contato_cobranca"] = pessoa.contato_cobranca.id

        self.execute(sql, parametros)

    def recuperar_dados_base_sem_complemento_pelo_id_compartilhado(self, tenant: int, id_compartilhado: UUID) -> dict:
        sql = """
            select id_compartilhado, codigo, registro_principal
            from pessoas
            where tenant=:tenant and id_compartilhado=:id_compartilhado    
        """
        parametros = {"tenant": tenant, "id_compartilhado": id_compartilhado}
        return self.fetchOne(sql, parametros)

    def recuperar_dados_base_sem_complemento_pelo_codigo(self, tenant: int, codigo: str) -> dict:
        sql = """
            select id_compartilhado, codigo, registro_principal
            from pessoas
            where tenant=:tenant and codigo=:codigo    
        """
        parametros: dict = {"tenant": tenant, "codigo": codigo}
        return self.fetchOne(sql, parametros)

    def listar_dados_base_e_registro_participantes(self, tenant, ids_registro) -> List[dict]:
        sql = f"""
            select
                p.tenant,
                p.id_compartilhado,
                p.codigo,
                pr.cpf_cnpj,
                pr.id_registro,
                pr.nome_fantasia,
                pr.razao_social,
                pr.qualificacao,
                pr.inscricao_municipal,
                pr.inscricao_estadual,
                pr.origem_informacoes,
                pr.tipo_simples_nacional,
                pr.endereco_cobranca,
                pr.endereco_principal,
                pr.contato_cobranca,
                pr.contato_principal,
                pr.contrato_id,
                pr.registro_papel
            from pessoas p
            join pessoas_registros pr on pr.id_compartilhado=p.id_compartilhado and p.tenant=pr.tenant
            where p.tenant=:tenant
            and pr.id_registro in :ids_registro
        """
        parametros = {"tenant":tenant, "ids_registro":ids_registro}
        return self.fetchAll(sql, parametros)