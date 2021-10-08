from dateutil import relativedelta

from nasajon.pastas_contabeis.abstract_pasta_contabil_composta import AbstractPastaContabilComposta

from nasajon.entity.dados_escrituracao_futura import DadosEscrituracaoFutura, DocumentoRetornoProjecao, ItemDocumentoRetornoProjecao
from nasajon.enum.heuristica_projecao import HeuristicaProjecao
from diario_unico.entity.lancamento import Lancamento

from nasajon.util.lancamento_util import LancamentosUtil
from time_service.service.time_service import TimeService

from typing import Dict, List

from collections import namedtuple
import datetime


class DadosLancamentos:
    def __init__(self):
        self.valor: float = None
        self.data_lancamento: datetime.date = None
        self.vencimento: datetime.date = None


class ProjecaoUtil:

    def __init__(self):
        self.hoje = TimeService.now().date()
        self.addMonth = relativedelta.relativedelta(months=1)

    def realizar_projecao(self, dados: DadosEscrituracaoFutura) -> List[DocumentoRetornoProjecao]:
        """
        Gera os documentos projetados, por item da escrituração futura sendo efetuada, para os próximos 12 meses.

        Return:
            Dicionário com os lançamentos calculados para a projeção, o qual é indexado pela data base do mês projetado
            (sendo que cada mes conterá um dict indexado pelos códigos dos itens).
        """
        data_temp = self.hoje.replace(day=1)
        retorno = list()
        for _ in range(12):
            # Calculando o valor projetado por item:
            self.calcular_valor_projetado(dados)
            novo = DocumentoRetornoProjecao()
            novo.data_apropriacao = data_temp.replace(
                day=dados.dia_apropriacao)
            novo.data_pagamento = data_temp.replace(day=dados.dia_vencimento)
            novo.itens = [ItemDocumentoRetornoProjecao(
                item.valor_projetado, item.codigo, item.tipo) for item in dados.itens]

            # Incrementando um mês na data base:
            data_temp = data_temp + self.addMonth
            retorno.append(novo)

        return retorno

    def gerar_lancamentos_projecao(self, dados: DadosEscrituracaoFutura, pasta_contabil: AbstractPastaContabilComposta) -> Dict[datetime.date, Dict[str, List[Lancamento]]]:
        """
        Gera os lançamentos projetados, por item da escrituração futura sendo efetuada, para os próximos 12 meses.

        Return:
            Dicionário com os lançamentos calculados para a projeção, o qual é indexado pela data base do mês projetado
            (sendo que cada mes conterá um dict indexado pelos códigos dos itens).
        """

        data_temp = self.hoje.replace(day=1)
        valores_projetados = None
        dict_lancamentos = dict()

        # Projetando para os próximos 12 meses:
        for _ in range(12):
            # Calculando o valor projetado por item:
            if (valores_projetados == None):
                valores_projetados = self.calcular_valor_projetado(dados)

            # Gerando os lancamentos de projeção para o mês em questão:
            lancamentos = self.gerar_lancamentos_projecao_mes(
                dados, data_temp, valores_projetados, pasta_contabil)

            # Guardando os lançamentos gerados:
            dict_lancamentos[data_temp] = lancamentos

            # Incrementando um mês na data base:
            data_temp = data_temp + self.addMonth

        return dict_lancamentos

    def gerar_lancamentos_projecao_mes(self, dados: DadosEscrituracaoFutura, data_base_mes_projecao: datetime.date, valores_projetados: Dict[str, float], pasta_contabil: AbstractPastaContabilComposta) -> Dict[str, List[Lancamento]]:
        """
        Gera os lançamentos projetados, por item da escrituração futura sendo efetuada, para o mês indicado pelo parâmetro data_base_mes_projecao.

        Return:
            Dicionário com os lançamentos calculados para a projeção, o qual é indexado pelo código dos itens contidos no
            parâmetro dados (tipo: DadosEscrituracaoFutura).
        """

        # Gerando os lançamentos por item:
        lancamentos = dict()
        for item in dados.itens:
            dados_lancamentos = DadosLancamentos()

            # Preenchendo o dict necessário ao processamento dos lançamentos:
            dados_lancamentos.valor = valores_projetados[item.codigo]
            dados_lancamentos.data_lancamento = data_base_mes_projecao.replace(
                day=dados.dia_apropriacao)
            dados_lancamentos.vencimento = data_base_mes_projecao.replace(
                day=dados.dia_vencimento)

            # Recuperando as definições dos lançamentos:
            definicoes_lancamentos = pasta_contabil.get_definicoes_lancamentos_escrituracao_futura_item(
                item.tipo)

            # Recuperando as definições dos info pagamentos:
            definicao_info_pagamento = pasta_contabil.get_definicoes_info_pagamento_escrituracao_futura()

            # Gerando os lancamentos:
            CalculoLancamento = namedtuple(
                'CalculoLancamento', ['dados', 'vetor_lancamentos'])
            vetor_lancamentos = LancamentosUtil().criar_lancamentos(
                dados_lancamentos, definicoes_lancamentos, definicao_info_pagamento)
            lancamentos[item.codigo] = CalculoLancamento(
                dados=dados_lancamentos, vetor_lancamentos=vetor_lancamentos)

        return lancamentos

    def calcular_valor_projetado(self, dados: DadosEscrituracaoFutura) -> Dict[str, float]:
        """
        Calcula o valor projetado para cada item contido nos dados da escrituração futura, respeitando a heurística de projeção
        configurada por item.

        Return:
            Retorna um dict com os valores projetados, indexados pelo código do item.
        """

        retorno = dict()

        for item in dados.itens:
            if (HeuristicaProjecao(item.heuristica_projecao) == HeuristicaProjecao.VALOR_FIXO):
                retorno[item.codigo] = item.valor_medio_inicial
            elif (HeuristicaProjecao(item.heuristica_projecao) == HeuristicaProjecao.MEDIA_MOVEL):
                # O valor médio inicial é utilizado automaticamente, no caso da não existência de histórico anterior:
                if len(item.valores_anteriores) <= 0:
                    retorno[item.codigo] = item.valor_medio_inicial
                else:
                    novo_valor = sum(
                        [val.valor for val in item.valores_anteriores]) / len(item.valores_anteriores)
                    retorno[item.codigo] = round(novo_valor, 2)
            else:
                raise Exception("Tipo de heurística de projeção não identificado: {}".format(
                    item.heuristica_projecao))
            item.valor_projetado = retorno[item.codigo]

        return retorno
