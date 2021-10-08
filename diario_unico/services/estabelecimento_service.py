from diario_unico.repository.estabelecimento_repository import EstabelecimentoRepository

class EstabelecimentoService:
    def __init__(self, estabelecimentorepository: EstabelecimentoRepository):
        self.estabelecimentorepository = estabelecimentorepository

    def getEstabelecimentos(self, tenant):
        return self.estabelecimentorepository.getEstabelecimentos(tenant)