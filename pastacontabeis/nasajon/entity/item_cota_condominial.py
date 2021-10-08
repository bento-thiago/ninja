import enum
from nasajon.enum.condominios.tipo_item_cota_condominial import TipoItemCotaCondominial

class ItemCotaCondominial:
    def __init__(self):
        self.codigo: str = None
        self.descricao: str = None
        self.tipo: TipoItemCotaCondominial = None
        self.valor: float = None

