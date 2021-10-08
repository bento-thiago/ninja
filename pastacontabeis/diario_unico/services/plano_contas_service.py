from diario_unico.repository.plano_contas_repository import PlanoContasRepository

class PlanoContasService:
    def __init__(self, repository: PlanoContasRepository):
        self.repository = repository

    def reconstruir_plano_contas(self, empresa, tenant):
        self.repository.reconstroi_plano_contas(empresa, tenant)