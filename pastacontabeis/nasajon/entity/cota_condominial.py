from datetime import date
from typing import List
from nasajon.entity.item_cota_condominial import ItemCotaCondominial
from diario_unico.enum.situacao import Situacao

class CotaCondominial:
    itens : List[ItemCotaCondominial]
    
    def __init__(self):
        self.token_facilitador : str = None
        self.tipo : int = None
        self.vencimento : date = None
        self.emissao : date = None
        self.competencia_inicial : date = None
        self.competencia_final : date = None
        self.situacao : Situacao = None
        self.valor : float = None
        self.origem : int = None
        self.estabelecimento : str = None
        self.participante : str = None
        self.usuario : str = None
        self.codigo_barras : str = None
        self.url_documento : str = None
        self.identificador_contrato: str = None
        self.itens : List[ItemCotaCondominial] = list()
