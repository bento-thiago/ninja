class ImpostoRetidoAcumulado:

    def __init__(self):
        self.estabelecimento: str = None
        self.situacao: str = None
        self.valor_retido_original: float = None
        self.valor_retido: float = None
        self.base_original: float = None
        self.base: float = None
        self.aliquota: float = None
