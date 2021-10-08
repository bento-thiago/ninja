from diario_unico.enum.situacao import Situacao
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from typing import List
from diario_unico.entity.lancamento import Lancamento, SituacaoDiario   
from datetime import date
import calendar

class Guia:   
    def __init__(self):
        self.tipo_documento : DocumentoTipo = None
        self.ano : int = None
        self.mes :  int = None
        self.estabelecimento :str = None
        self.situacao : Situacao = None        
        self.lancamentos_sobre_doc_previstos: List[Lancamento] = list()
        self.lancamentos_sobre_doc_realizados: List[Lancamento] = list()        
            
    def valor_previsao(self):
        return sum([lancamento.valor() for lancamento in self.lancamentos_sobre_doc_previstos if lancamento.situacao==SituacaoDiario.REALIZADO])

    def valor_realizado(self):
        return sum([lancamento.valor() for lancamento in self.lancamentos_sobre_doc_realizados if lancamento.situacao==SituacaoDiario.REALIZADO])

    def valor_total(self):
        return self.valor_previsao() + self.valor_realizado()

    @property
    def competencia_inicial(self):
        return date(self.ano,self.mes,1)

    @property
    def competencia_final(self):
        return date(self.ano,self.mes, calendar.monthrange(self.ano,self.mes)[1])
            

        
