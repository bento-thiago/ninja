import uuid
from typing import Dict, List

from diario_unico.entity.contrato import Contrato
from diario_unico.entity.pessoa import Pessoa
from diario_unico.repository.pessoas_repository import PessoasRepository
from diario_unico.services.contato_service import ContatoService
from diario_unico.services.endereco_service import EnderecoService
from diario_unico.services.utilitario_service import UtilitarioService


class PessoaService:

    def __init__(self, repository: PessoasRepository, utilitario_service: UtilitarioService,
                 contato_service: ContatoService, endereco_service: EnderecoService):
        self.repository = repository
        self.utilitarios_banco = utilitario_service
        self.endereco_service = endereco_service
        self.contato_service = contato_service

    def inserir_pessoa(self, pessoa: Pessoa, tenant: int, contrato: Contrato = None):
        if pessoa.id_registro is not None:
            if self.utilitarios_banco.exists_pk(self.repository.table_name, 'id_registro', tenant, pessoa.id_registro):
                raise Exception("Pessoa ja cadastrada")
        if (pessoa.codigo is not None) and (pessoa.id_compartilhado is not None):
            pessoa_base = self.recuperar_dados_base_sem_complemento_pelo_id_compartilhado(tenant,
                                                                                          pessoa.id_compartilhado)
            if pessoa_base is not None:
                if pessoa_base["codigo"] != pessoa.codigo:
                    raise Exception("O participante indicado pelo ID possui um código diferente do informado")
            pessoa_base = self.recuperar_dados_base_sem_complemento_pelo_codigo(tenant, pessoa.codigo)
            if pessoa_base is not None:
                if pessoa_base["id_compartilhado"] != pessoa.id_compartilhado:
                    raise Exception("O participante indicado pelo codigo possui um ID diferente do informado")

        elif (pessoa.codigo is not None) and (pessoa.id_compartilhado is None):
            pessoa_base = self.recuperar_dados_base_sem_complemento_pelo_codigo(tenant, pessoa.codigo)
            if pessoa_base is not None:
                pessoa.id_compartilhado=pessoa_base["id_compartilhado"]

        elif (pessoa.codigo is  None) and (pessoa.id_compartilhado is not None):
            pessoa_base = self.recuperar_dados_base_sem_complemento_pelo_id_compartilhado(tenant,
                                                                                          pessoa.id_compartilhado)
            if pessoa_base is not None:
                pessoa.codigo = pessoa_base["codigo"]


        if (pessoa.endereco_cobranca is not None) and (pessoa.endereco_cobranca.id is None):
            pessoa.endereco_cobranca.id = uuid.uuid4()
        if (pessoa.endereco_principal is not None) and (pessoa.endereco_principal.id is None):
            pessoa.endereco_principal.id = uuid.uuid4()
        if (pessoa.contato_cobranca is not None) and (pessoa.contato_cobranca.id is None):
            pessoa.contato_cobranca.id = uuid.uuid4()
        if (pessoa.contato_principal is not None) and (pessoa.contato_principal.id is None):
            pessoa.contato_principal.id = uuid.uuid4()

        if pessoa.id_compartilhado is None:
            pessoa.id_compartilhado = uuid.uuid4()
        if pessoa.id_registro is None:
            pessoa.id_registro = uuid.uuid4()

        if contrato is not None:
            pessoa.contrato_id = contrato.id_compartilhado

        estava_em_transacao_anteriormente = self.repository.em_transacao()

        if not estava_em_transacao_anteriormente:
            self.repository.begin()

        self.repository.inserir_pessoa(pessoa, tenant)

        if pessoa.endereco_principal is not None:
            pessoa.endereco_principal.pessoa_registro = pessoa.id_registro
            self.endereco_service.inserir_endereco(pessoa.endereco_principal, tenant, pessoa)

        if pessoa.endereco_cobranca is not None:
            pessoa.endereco_cobranca.pessoa_registro = pessoa.id_registro
            self.endereco_service.inserir_endereco(pessoa.endereco_cobranca, tenant, pessoa)

        for endereco in pessoa.enderecos_outros:
            endereco.pessoa_registro = pessoa.id_registro
            self.endereco_service.inserir_endereco(endereco, tenant, pessoa)

        if pessoa.contato_principal is not None:
            pessoa.contato_principal.pessoa_registro = pessoa.id_registro
            self.contato_service.inserir_contato(pessoa.contato_principal, tenant, pessoa)

        if pessoa.contato_cobranca is not None:
            pessoa.contato_cobranca.pessoa_registro = pessoa.id_registro
            self.contato_service.inserir_contato(pessoa.contato_cobranca, tenant, pessoa)

        for contato in pessoa.contatos_outros:
            contato.pessoa_registro = pessoa.id_registro
            self.contato_service.inserir_contato(contato, tenant, pessoa)

        if not estava_em_transacao_anteriormente:
            self.repository.commit()
        return pessoa

    def recuperar_dados_base_sem_complemento_pelo_id_compartilhado(self, tenant: int, id_compartilhado: uuid.UUID):
        return self.repository.recuperar_dados_base_sem_complemento_pelo_id_compartilhado(tenant, id_compartilhado)

    def recuperar_dados_base_sem_complemento_pelo_codigo(self, tenant, codigo):
        return self.repository.recuperar_dados_base_sem_complemento_pelo_codigo(tenant, codigo)

    def listar_dados_completos_participantes(self, tenant: int, ids_registro: List[uuid.UUID]) -> List[Dict]:
        pessoas = self.repository.listar_dados_base_e_registro_participantes(tenant, ids_registro)
        enderecos = self.endereco_service.listar_dados_enderecos_participantes(tenant, ids_registro)
        contatos = self.contato_service.listar_dados_contatos_participantes(tenant, ids_registro)

        for pessoa in pessoas:
            pessoa["outros_enderecos"] = list()
            pessoa["outros_contatos"] = list()
            for endereco in enderecos:
                if endereco["id"] == pessoa["endereco_cobranca"]:
                    pessoa["endereco_cobranca"] = endereco
                if endereco["id"] == pessoa["endereco_principal"]:
                    pessoa["endereco_principal"] = endereco
                if endereco["pessoa_registro"] == pessoa["id_registro"] and not (
                        endereco["id"] in [pessoa["endereco_cobranca"], pessoa["endereco_principal"]]):
                    pessoa["outros_enderecos"].append(endereco)

            for contato in contatos:
                if contato["id"] == pessoa["contato_cobranca"]:
                    pessoa["contato_cobranca"] = contato
                if contato["id"] == pessoa["contato_principal"]:
                    pessoa["contato_principal"] = contato
                if contato["pessoa_registro"] == pessoa["id_registro"] and not (
                        contato["id"] in [pessoa["contato_cobranca"], pessoa["contato_principal"]]):
                    pessoa["outros_contatos"].append(contato)

        return pessoas
