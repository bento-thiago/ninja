from diario_unico.repository.contato_repository import ContatoRepository
from diario_unico.entity.contato import Contato
from diario_unico.entity.pessoa import Pessoa
import uuid

class ContatoService:
    
    def __init__(self, repository: ContatoRepository):
        self.repository = repository
        
    def inserir_contato(self, contato:Contato, tenant:int, pessoa:Pessoa):
        if contato.id==None:
            contato.id=uuid.uuid4()
        self.repository.inserir_contato(contato,tenant, pessoa)

    def listar_dados_contatos_participantes(self, tenant, ids_registro):
        return self.repository.listar_dados_contatos_participantes(tenant, ids_registro)