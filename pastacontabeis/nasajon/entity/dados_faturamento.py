from typing import List
from nasajon.entity.dados_cobranca import Dados_Cobranca

class ItemFaturamento:
    def __init__(self):
        self.valor:float = None
        self.codigo:str = None
        self.tipo:str = None

class DadosFaturamento:
    dados_cobranca : Dados_Cobranca
    itens:List[ItemFaturamento]

    def __init__(self):
        self.contrato_codigo:str = None
        self.contrato_estabelecimento: str = None
        self.contrato_dia_processamento:int = None
        self.contrato_dia_vencimento:int=None
        self.itens:List[ItemFaturamento] = list()
        self.participante:str = None
        self.dados_cobranca:Dados_Cobranca = None
        self.tenant:int = None