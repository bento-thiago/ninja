from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.enum.sinal import Sinal

from datetime import date
from diario_unico.entity.lancamento import Lancamento
from typing import List
from nasajon.enum.folha.rubrica_tipo_valor import RubricaTipoValor

class ItemPagamentoTrabalhador:
    def __init__(self):
        self.valor:float = None
        self.rubrica:str = None
        self.rubrica_esocial:str = None
        self.tipovalor:RubricaTipoValor = None
        self.lancamentos = list()
        self.descricao_rubrica:str = None
        
class PagamentoATrabalhador:
    lancamentos : List[Lancamento]
    itens :List[ItemPagamentoTrabalhador]

    def __init__(self):
        self.token_facilitador : str=  None #Equivalente ao guid do Documento
        self.tipo :DocumentoTipo = None
        self.ano_competencia:int = None
        self.mes_competencia:int = None
        self.estabelecimento:str = None
        self.departamento:str = None
        self.lotacao:str = None
        self.trabalhador:str = None
        self.data_geracao:date=None
        self.data_pagamento:date=None
        self.itens :List[ItemPagamentoTrabalhador]= list()



