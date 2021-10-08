from typing import List
from nasajon.entity.trabalhador import Trabalhador
from nasajon.entity.departamento import Departamento
from nasajon.entity.lotacao import Lotacao
from nasajon.entity.rubrica import Rubrica
from nasajon.entity.calculo_trabalhador import CalculoTrabalhador
from nasajon.entity.mudanca_trabalhador import MudancaTrabalhador
from diario_unico.entity.estabelecimento import Estabelecimento
from datetime import date, datetime
from nasajon.util.json_util import JsonUtil

class DadosIntegracaoPagamentoATrabalhador:
    trabalhadores:List[Trabalhador]
    departamentos:List[Departamento]
    lotacoes:List[Lotacao]
    rubricas:List[Rubrica]
    calculos:List[CalculoTrabalhador]
    mudancas_trabalhadores:List[MudancaTrabalhador]
    estabelecimentos:List[Estabelecimento]

    def __init__(self):
        self.ano:int = None
        self.mes:int = None
        self.tipo_calculo:str = None
        self.trabalhadores:List[Trabalhador] = list()
        self.departamentos:List[Departamento] = list()
        self.lotacoes:List[Lotacao] = list()
        self.rubricas:List[Rubrica] = list()
        self.calculos:List[CalculoTrabalhador] = list()
        self.estabelecimentos:List[Estabelecimento] = list()
        self.mudancas_trabalhadores:List[MudancaTrabalhador] = list()
        self.tenant:str = None

    def verificarSeFaltaDadosAuxiliares(self):
        for calculo in self.calculos:
            if not calculo.trabalhador in [t.id for t in self.trabalhadores]:
                return "Informações do trabalhador {} não fornecidas".format(calculo.trabalhador)
            if not calculo.rubrica in [r.id for r in self.rubricas]:
                return "Informações da rubrica {} não fornecidas".format(calculo.rubrica)
            if not calculo.trabalhador in [m.trabalhador for m in self.mudancas_trabalhadores]:
                return "Informações de 'Mudanças Trabalhadores' do trabalhador {} não fornecidas".format(calculo.trabalhador)
            for mudanca in [mudanca for mudanca in self.mudancas_trabalhadores if mudanca.trabalhador==calculo.trabalhador]:
                if not mudanca.lotacao in [l.id for l in self.lotacoes]:
                    return "Informações da Lotação {} não fornecidas".format(mudanca.lotacao)
                if not mudanca.departamento in [d.id for d in self.departamentos]:
                    return "Informações da Departamento {} não fornecidas".format(mudanca.departamento)
        return None
    
    def obtemMudanca(self, trabalhador:str, data:date)->MudancaTrabalhador:
        maior_data = None
        saida=None
        for m in [m for m in self.mudancas_trabalhadores if m.trabalhador==trabalhador and m.data_inicial<=data]:
            if (maior_data==None) or (m.data_final==None) or (m.data_final=="") or (maior_data<m.data_final):
                saida = m
                maior_data=saida.data_final
        return saida



