from datetime import date, datetime

class MudancaTrabalhador:
    def __init__(self, data_inicial:date=None, data_final:date = None, 
                tipo:int = None,estabelecimento:str = None, departamento:str = None,  
                lotacao:str = None, trabalhador:str = None):
        self.data_inicial: date = data_inicial
        self.data_final:date = data_final
        self.tipo:int = tipo
        self.estabelecimento:str = estabelecimento
        self.departamento:str = departamento
        self.lotacao:str = lotacao
        self.trabalhador:str = trabalhador
