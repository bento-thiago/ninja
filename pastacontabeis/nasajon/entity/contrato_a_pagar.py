class ContratoAPagar:
    def __init__(self):
        self.contrato: str = None
        self.codigo:str  = None
        self.tipo:int = None
        self.codigo_transacao:str = None
        self.estabelecimento:str = None
        self.fornecedor:str = None
        self.tenant:int = None
        self.heuristica_valor : int = None
        self.valor:float = None
        self.dia_vencimento:int = None
        self.dia_apropriacao:int = None
        