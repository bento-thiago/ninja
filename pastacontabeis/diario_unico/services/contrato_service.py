import uuid

from diario_unico.entity.contrato import Contrato
from diario_unico.enum.pessoas.pessoa_papel import PessoaPapel
from diario_unico.repository.contato_repository import ContatoRepository
from diario_unico.repository.contrato_repository import ContratoRepository
from diario_unico.repository.endereco_repository import EnderecoRepository
from diario_unico.repository.estabelecimento_repository import EstabelecimentoRepository
from diario_unico.repository.pessoas_repository import PessoasRepository
from diario_unico.repository.utilitario_repository import UtilitarioRepository
from diario_unico.services.pessoa_service import PessoaService
from diario_unico.services.utilitario_service import UtilitarioService


class ContratoService:
    def __init__(self, repository: ContratoRepository, utilitario_service: UtilitarioService,
                 estabelecimento_repository: EstabelecimentoRepository, pessoa_service: PessoaService) -> object:
        self.repository = repository
        self.utilitarioService = utilitario_service
        self.estabelecimentoRepository = estabelecimento_repository
        self.pessoa_service = pessoa_service

    def inserir_contrato(self, contrato: Contrato, tenant: int):
        if contrato.id_registro is not None:
            if self.utilitarioService.exists_pk(self.repository.table_name, 'id_registro', tenant,
                                                contrato.id_registro):
                raise Exception("Contrato ja cadastrado")
        else:
            contrato.id_registro = uuid.uuid4()
        if contrato.id_compartilhado is None:
            contrato.id_compartilhado = uuid.uuid4()

        if self.utilitarioService.exists(self.repository.table_name, 'codigo', tenant, contrato.codigo):
            raise Exception("Este código de contrato já está em uso")
        if not self.utilitarioService.exists_pk(self.estabelecimentoRepository.table_name, 'id_compartilhado', tenant,
                                                contrato.estabelecimento):
            raise Exception("Estabelecimento não encontrato")

        for item in contrato.itens:
            item.registro_contrato_id = contrato.id_registro
            if item.id is None:
                item.id = uuid.uuid4()
        try:
            self.repository.begin()
            contrato.participante.registro_papel = PessoaPapel.CLIENTE
            self.pessoa_service.inserir_pessoa(contrato.participante, tenant, contrato=contrato)
            self.repository.inserir_contrato(contrato, tenant)
            self.repository.commit()
        except Exception as e:
            self.repository.rollback()
            raise e
        return contrato

    def listar_contratos(self, tenant: int):
        dados_base = self.repository.listar_dados_base_contratos(tenant)
        if len(dados_base)==0:
            return []
        # Recupera participante
        participantes_id = [c["participante_id"] for c in dados_base]
        contratos_ids = [c["id_registro"] for c in dados_base]
        participantes = self.pessoa_service.listar_dados_completos_participantes(tenant, ids_registro=participantes_id)
        for contrato in dados_base:
            for participante in participantes:
                if  contrato["participante_id"] == participante["id_registro"]:
                    contrato["participante"] = participante

        # Recupera Itens
        itens = self.repository.listar_itens_varios_contratos(tenant, contratos_ids)
        for contrato in dados_base:
            contrato["itens"] = list()
            for item in itens:
                contrato["itens"].append(item)
        contratos_obj = list()
        for contrato in dados_base:
            contrato_obj = Contrato.parse_obj(contrato)
            contratos_obj.append(contrato_obj)
        return contratos_obj


if __name__ == '__main__':
    from diario_unico.services.contato_service import ContatoService
    from diario_unico.services.endereco_service import EnderecoService

    service = ContratoService(ContratoRepository(), UtilitarioService(UtilitarioRepository()),
                              EstabelecimentoRepository(),
                              PessoaService(PessoasRepository(), UtilitarioService(UtilitarioRepository()),
                                            ContatoService(ContatoRepository()), EnderecoService(EnderecoRepository())))
    d = service.listar_contratos(47)
    print(d)
