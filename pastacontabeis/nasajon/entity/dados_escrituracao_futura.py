import datetime
from typing import List
from nasajon.enum.heuristica_projecao import HeuristicaProjecao


class ValoresAnteriores:
    def __init__(self):
        # self.vencimento: datetime.date = None
        # self.apropriacao: datetime.date = None
        self.valor: float = None


class DadosItem:
    valores_anteriores: List[ValoresAnteriores]
    
    def __init__(self):
        self.tipo: str = None
        self.codigo: str = None
        self.heuristica_projecao: HeuristicaProjecao = None
        self.valor_medio_inicial: float = None
        self.valores_anteriores: List[ValoresAnteriores] = list()
        self.valor_projetado : float = 0


class DadosEscrituracaoFutura:

    itens: List[DadosItem]
    def __init__(self):
        self.estabelecimento: str = None
        self.dia_vencimento: int = None
        self.dia_apropriacao: int = None
        self.participante: str = None
        self.itens: List[DadosItem] = list()
        self.tenant: int = None


class DocumentoRetornoProjecao:
    def __init__(self, data_apropriacao:datetime.date = None, data_pagamento:datetime.date = None):
        self.data_apropriacao: datetime.date = data_apropriacao
        self.data_pagamento: datetime.date = data_pagamento
        self.itens: List[ItemDocumentoRetornoProjecao] = list()
    
    @property
    def valor(self):
        return sum([item.valor for item in self.itens])

class ItemDocumentoRetornoProjecao:
    def __init__(self, valor:float = 0, codigo: str = None, tipo: str = None):
        self.valor: float = valor
        self.codigo: str = codigo
        self.tipo: str = tipo
        
