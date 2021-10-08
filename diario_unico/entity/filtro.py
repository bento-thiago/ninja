from typing import List
class Filtro:
    parametros:List[str]
    def __init__(self):
        self.operacao:str = None
        self.entidade:str = None
        self.campo:str = None
        self.parametros:list = list()