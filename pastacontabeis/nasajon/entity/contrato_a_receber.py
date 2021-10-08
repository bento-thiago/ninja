from typing import List

class ItemContratoReceber:
    def __init__(self):
        self.item_contrato:str = None
        self.contrato:str = None
        self.valor:float = None
        self.tenant:int = None
        self.heuristica_valor:int = None
        self.codigo: str = None

class ParticipantesContratoReceber:
    def __init__(self):
        self.participante:str = None
        self.participacao:float = None
        self.dia_processamento:int = None
        self.dia_vencimento:int = None

class ContratoReceber:
    itens : List[ItemContratoReceber]
    participantes : List[ParticipantesContratoReceber]

    def __init__(self):
        self.contrato:str = None
        self.tipo:int = None
        self.codigo:str = None
        self.tenant:int = None
        self.pasta_contabil:str = None
        self.itens : List[ItemContratoReceber] = list()
        self.participantes : List[ParticipantesContratoReceber] = list()
        