from diario_unico.repository.endereco_repository import EnderecoRepository
from diario_unico.entity.endereco import Endereco
from diario_unico.entity.pessoa import Pessoa
import uuid

class EnderecoService:
    
    def __init__(self, repository: EnderecoRepository):
        self.repository = repository
        
    def inserir_endereco(self, endereco:Endereco, tenant:int, pessoa:Pessoa):
        if endereco.id==None:
            endereco.id=uuid.uuid4()
        self.repository.inserir_endereco(endereco,tenant,pessoa)

    def listar_dados_enderecos_participantes(self, tenant, ids_registro):
        return self.repository.listar_dados_enderecos_participantes(tenant, ids_registro)