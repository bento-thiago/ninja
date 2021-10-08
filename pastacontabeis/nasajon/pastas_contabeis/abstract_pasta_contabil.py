from abc import ABC, abstractmethod

from diario_unico.enum.pasta_contabil import PastaContabil
from nasajon.pastas_contabeis.pastas_router import MomentoContabil
from nasajon.pastas_contabeis.pastas_router import simular as task_simular
from nasajon.pastas_contabeis.pastas_router import faturar as task_faturar
from nasajon.pastas_contabeis.pastas_router import escriturar_futuro as task_escriturar_futuro
from nasajon.pastas_contabeis.pastas_router import apropriar as task_apropriar
from nasajon.pastas_contabeis.pastas_router import quitar as task_quitar
from nasajon.pastas_contabeis.pastas_router import cancelar as task_cancelar

from nasajon.util.diario_util import DiarioUtil
from nasajon.util.json_util import JsonUtil
from nasajon.util.jobs_util import JobsUtil
from nasajon.util.log import Log
from nasajon.util.projecao_util import ProjecaoUtil


class AbstractPastaContabil(ABC):

    def __init__(self, diario_util: DiarioUtil, nome: PastaContabil):
        self._projecao_util = ProjecaoUtil()
        self._diario_util = diario_util        
        self._log = Log(type(self).__name__)
        self.pasta_contabil:PastaContabil=nome

    def simular(self, dados):
        pass

    def faturar(self, dados):
        pass

    def escriturar_futuro(self, dados):
        pass

    def apropriar(self, dados):
        pass

    def quitar(self, dados):
        pass

    def cancelar(self, dados):
        pass

    def get_dados_simulacao(self, dados: dict):
        """
        Parâmetros:
        - dados: Informações repassadas pelo responsável do agendamento da simulação.

        Return:
        - Deve retornar dados suficientes para a simulação desta pasta contábil, sem necessidade de novas consultas ao diário ou ao banco de dados.
        """
        return dados

    def get_dados_faturamento(self, dados: dict):
        """
        Parâmetros:
        - dados: Informações repassadas pelo responsável do agendamento o faturamento.

        Return:
        - Deve retornar dados suficientes para a faturamento desta pasta contábil, sem necessidade de novas consultas ao diário ou ao banco de dados.
        """
        return dados

    def get_dados_escrituracao_futura(self, dados: dict):
        """
        Parâmetros:
        - dados: Informações repassadas pelo responsável do agendamento da escrituração futura (normalmente: job de previsão).

        Return:
        - Deve retornar dados suficientes para a escrituração futura desta pasta contábil, sem necessidade de novas consultas ao diário ou ao banco de dados.
        """
        return dados

    def get_dados_apropriacao(self, dados: dict):
        """
        Parâmetros:
        - dados: Informações repassadas pelo responsável do agendamento da apropriação.

        Return:
        - Deve retornar dados suficientes para a apropriação desta pasta contábil, sem necessidade de novas consultas ao diário ou ao banco de dados.
        """
        return dados

    def get_dados_quitacao(self, dados: dict):
        """
        Parâmetros:
        - dados: Informações repassadas pelo responsável da quitação.

        Return:
        - Deve retornar dados suficientes para a quitação desta pasta contábil, sem necessidade de novas consultas ao diário ou ao banco de dados.
        """
        return dados

    def get_dados_cancelamento(self, dados: dict):
        """
        Parâmetros:
        - dados: Informações repassadas pelo responsável do cancelamento.

        Return:
        - Deve retornar dados suficientes para o cancelamento desta pasta contábil, sem necessidade de novas consultas ao diário ou ao banco de dados.
        """
        return dados

    def notificar(self, id_pasta: str, momento: MomentoContabil, dados: dict, id_log_assincrono: str, tentativa: int):
        if (momento == MomentoContabil.SIMULACAO):
            task_simular.delay(id_pasta, JsonUtil().toDict(
                self.get_dados_simulacao(dados)), id_log_assincrono)
        elif (momento == MomentoContabil.ESCRITURACAO_FUTURA):
            task_escriturar_futuro.delay(
                id_pasta, JsonUtil().toDict(self.get_dados_escrituracao_futura(dados)), id_log_assincrono, tentativa)
        elif (momento == MomentoContabil.APROPRIACAO):
            task_apropriar.delay(id_pasta, JsonUtil().toDict(
                self.get_dados_apropriacao(dados)), id_log_assincrono, tentativa)
        elif (momento == MomentoContabil.QUITACAO):
            task_quitar.delay(id_pasta, JsonUtil().toDict(
                self.get_dados_quitacao(dados)), id_log_assincrono, tentativa)
        elif (momento == MomentoContabil.CANCELAMENTO):
            task_cancelar.delay(id_pasta, JsonUtil().toDict(
                self.get_dados_cancelamento(dados)), id_log_assincrono)
        elif (momento == MomentoContabil.FATURAMENTO):
            info = JsonUtil().toDict(self.get_dados_faturamento(dados))
            task_faturar.delay(id_pasta, info, id_log_assincrono, tentativa)
        else:
            raise Exception(
                "Momento contábil não implementado: "+str(momento.__class__))
