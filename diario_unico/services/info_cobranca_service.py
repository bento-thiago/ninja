import uuid
from typing import List

from diario_unico.entity.info_cobranca import InfoCobranca
from diario_unico.repository.info_cobranca_repository import InfoCobrancaRepository


class InfoCobrancaService:
    def __init__(self, infoCobrancaRepository: InfoCobrancaRepository):
        self.repository = infoCobrancaRepository

    def insere_info_cobranca(self, tenant: int, infos_cobranca:List[InfoCobranca]):
        for info_cobranca in infos_cobranca:
            if info_cobranca.id is None:
                info_cobranca = uuid.uuid4()
        self.repository.insere_info_cobranca(tenant, infos_cobranca)

    def listar_de_documentos(self, tenant, ids):
        return [InfoCobranca.parse_obj(info) for info in  self.repository.listar_de_documentos(tenant, ids)]
