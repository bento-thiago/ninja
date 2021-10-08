from enum import Enum
from nasajon.enum.folha.rubrica_tipo_valor import RubricaTipoValor
class Rubrica:
    def __init__(self, id:str = None, codigo:str = None, nome:str = None, tipovalor:str=None, categoria:str = None, unidade:str = None):
        self.id:str = id
        self.codigo:str = codigo
        self.nome:str = nome
        self.tipovalor:RubricaTipoValor = tipovalor
        self.categoria:str = categoria
        self.unidade:str = unidade

 

