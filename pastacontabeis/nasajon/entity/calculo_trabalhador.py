from datetime import date, datetime

    
class CalculoTrabalhador:
    def __init__(self, id:str=None, data_de_pagamento:date=None, valor:float=None, 
                rubrica:str=None, ano:int=None, mes:int = None, 
                trabalhador:str = None, ano_gerador:int=None, mes_gerador:int = None, 
                invisivel:bool=False, tipo_recebimento_trabalhador:int = None):
        self.id:str=id
        self.data_de_pagamento:date = data_de_pagamento
        self.valor:float = valor
        self.rubrica:str = rubrica
        self.ano:int = ano
        self.mes:int = mes
        self.trabalhador:str = trabalhador
        self.ano_gerador:int = ano_gerador
        self.mes_gerador:int = mes_gerador
        self.invisivel:bool = invisivel
        self.tipo_recebimento_trabalhador:int = tipo_recebimento_trabalhador
