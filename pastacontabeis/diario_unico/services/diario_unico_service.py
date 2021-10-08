from typing import List

from diario_unico.entity.linha_diario_unico import LinhaDiarioUnico
from diario_unico.repository.diario_unico_repository import DiarioUnicoRepository


class DiarioUnicoService:

    def __init__(self, repository: DiarioUnicoRepository):
        self.repository = repository

    def insere_diario(self, tenant: int, linhas: List[LinhaDiarioUnico]):
        self.repository.insere_diario(tenant, linhas)

    def listar_linha_de_documentos(self, tenant, documentos_ids) -> List[LinhaDiarioUnico]:
        linhas= self.repository.listar_linha_de_documentos(tenant, documentos_ids)
        linhas_obj = [LinhaDiarioUnico.parse_obj(linha) for linha in linhas]
        return linhas_obj
