from __future__ import absolute_import, unicode_literals
from celery import shared_task

from nasajon.util.json_util import JsonUtil
from nasajon.util.log import Log
from nasajon.util.repetir_exception import RepetirException

import enum
import importlib
import nasajon.pastas_contabeis
import re
import os
import shutil
import time
from crawlers.services.itau_service import ItauService
from nasajon.util.nasajon_factory import NasajonFactory
from nasajon.entity.log_assincrono import LogAssincrono


class MomentoContabil(enum.Enum):
    SIMULACAO = 'simulacao'
    ESCRITURACAO_FUTURA = 'escrituracao_futura'
    APROPRIACAO = 'apropriacao'
    QUITACAO = 'quitacao'
    CANCELAMENTO = 'cancelamento'
    FATURAMENTO = 'faturamento'


log = Log("PASTAS_ROUTER")


@shared_task
def simular(id_pasta: str, dados: dict, id_log_assincrono: str = None):
    log.info("Simulando pasta: {}".format(id_pasta))
    try:
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Processando simulação", dados["tenant"])

        get_pasta_obj(id_pasta).simular(dados)

        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Concluido", dados["tenant"])
    except Exception as err:
        log.info(str(err))
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Erro ao simular: " + str(err), dados["tenant"])
        raise err


@shared_task
def faturar(id_pasta: str, dados: dict, id_log_assincrono: str = None, tentativa: int = 1):
    log.info("Faturando pasta: {}".format(id_pasta))
    try:
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Processando faturamento", dados["tenant"])

        get_pasta_obj(id_pasta).faturar(dados)

        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Concluido", dados["tenant"])
    except RepetirException as err:
        if tentativa < 5:
            time.sleep(15)
            faturar.delay(id_pasta, dados, id_log_assincrono, tentativa + 1)
        else:
            log.info(str(err))
            inserirLogAssincrono(
                id_log_assincrono, "pastas_contabeis", "Erro ao faturar depois de 5 tentativas: " + str(err), dados["tenant"])
            raise err
    except Exception as err:
        log.info(str(err))
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Erro ao faturar: " + str(err), dados["tenant"])
        raise err


@shared_task
def escriturar_futuro(id_pasta: str, dados: dict, id_log_assincrono: str = None, tentativa: int = 1):
    log.info("Escriturando futuro. Pasta: {}".format(id_pasta))
    try:
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Processando escrituração", dados["tenant"])

        get_pasta_obj(id_pasta).escriturar_futuro(dados)

        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Concluido", dados["tenant"])
    except RepetirException as err:
        if tentativa < 5:
            time.sleep(15)
            escriturar_futuro.delay(
                id_pasta, dados, id_log_assincrono, tentativa + 1)
        else:
            log.info(str(err))
            inserirLogAssincrono(
                id_log_assincrono, "pastas_contabeis", "Erro ao escriturar depois de 5 tentativas: " + str(err), dados["tenant"])
            raise err
    except Exception as err:
        log.info(str(err))
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Erro ao escriturar: " + str(err), dados["tenant"])
        raise err


@shared_task
def apropriar(id_pasta: str, dados: dict, id_log_assincrono: str = None, tentativa: int = 1):
    log.info("Apropriando pasta: {}".format(id_pasta))
    try:
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Processando apropriação", dados["tenant"])

        get_pasta_obj(id_pasta).apropriar(dados)

        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Concluido", dados["tenant"])
    except RepetirException as err:
        if tentativa < 5:
            time.sleep(15)
            apropriar.delay(id_pasta, dados, id_log_assincrono, tentativa + 1)
        else:
            log.info(str(err))
            inserirLogAssincrono(
                id_log_assincrono, "pastas_contabeis", "Erro ao apropriar depois de 5 tentativas: " + str(err), dados["tenant"])
            raise err
    except Exception as err:
        log.info(str(err))
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Erro ao apropriar: " + str(err), dados["tenant"])
        raise err


@shared_task
def quitar(id_pasta: str, dados: dict, id_log_assincrono: str = None, tentativa: int = 1):
    log.info("Quitando pasta: {}".format(id_pasta))
    try:
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Processando quitação", dados["tenant"])

        get_pasta_obj(id_pasta).quitar(dados)

        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Concluido", dados["tenant"])
    except RepetirException as err:
        if tentativa < 5:
            time.sleep(15)
            quitar.delay(id_pasta, dados, id_log_assincrono, tentativa + 1)
        else:
            log.info(str(err))
            inserirLogAssincrono(
                id_log_assincrono, "pastas_contabeis", "Erro ao quitar depois de 5 tentativas: " + str(err), dados["tenant"])
            raise err
    except Exception as err:
        log.info(str(err))
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Erro ao quitar: " + str(err), dados["tenant"])
        raise err


@shared_task
def cancelar(id_pasta: str, dados: dict, id_log_assincrono: str = None):
    log.info("Cancelando pasta: {}".format(id_pasta))
    try:
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Processando cancelamento", dados["tenant"])

        get_pasta_obj(id_pasta).cancelar(dados)

        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Cancelado", dados["tenant"])
    except Exception as err:
        log.info(str(err))
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Erro ao cancelar: " + str(err), dados["tenant"])
        raise err


@shared_task
def notificar(id_pasta: str, momento: str, dados: dict, id_log_assincrono: str = None, tentativa: int = 1):
    log.info("Notificando pasta: {}".format(id_pasta))
    try:
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Processando notificação", dados["tenant"])

        get_pasta_obj(id_pasta).notificar(
            id_pasta, MomentoContabil(momento), dados, id_log_assincrono, tentativa)
    except RepetirException as err:
        if tentativa < 5:
            time.sleep(15)
            notificar.delay(id_pasta, momento, dados,
                            id_log_assincrono, tentativa + 1)
        else:
            log.info(str(err))
            inserirLogAssincrono(
                id_log_assincrono, "pastas_contabeis", "Erro ao notificar depois de 5 tentativas: " + str(err), dados["tenant"])
            raise err
    except Exception as err:
        log.info(str(err))
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Erro ao notificar: " + str(err), dados["tenant"])
        raise err


@shared_task
def task_apropriar_e_antecipar(id_pasta: str, dados: dict, id_log_assincrono: str = None, tentativa: int = 1):
    log.info("Apropriando e antecipando pasta: {}".format(id_pasta))
    try:
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Processando apropriação", dados["tenant"])

        # Apropriacao
        pasta = get_pasta_obj(id_pasta)
        documento = pasta.apropriar(dados)
        dados_escrituracao_futura = pasta.documento_para_dados_escrituracao_futura(
            documento, dados)

        # Enfileira futuro
        escriturar_futuro.delay(
            id_pasta, JsonUtil().toDict(dados_escrituracao_futura), tentativa)

    except RepetirException as err:
        if tentativa < 5:
            time.sleep(15)
            task_apropriar_e_antecipar.delay(
                id_pasta, dados, id_log_assincrono, tentativa + 1)
        else:
            log.info(str(err))
            inserirLogAssincrono(
                id_log_assincrono, "pastas_contabeis", "Erro ao apropriar depois de 5 tentativas: " + str(err), dados["tenant"])
            raise err
    except Exception as err:
        log.info(str(err))
        inserirLogAssincrono(
            id_log_assincrono, "pastas_contabeis", "Erro ao apropriar: " + str(err), dados["tenant"])
        raise err


def inserirLogAssincrono(id_log_assincrono, recurso, status, tenant):
    log_assincrono = LogAssincrono(
        id_log_assincrono, recurso, status, tenant)
    NasajonFactory.getLogAssincronoService().inserir(log_assincrono)


def get_pasta_obj(id_pasta: str):
    # A convencao para nomes de pastas é:
    # O nome do arquivo deve sergui o modelo snake-case, começando com 'pasta_'
    # O nome da classe deve seguir o modelo CamelCase, comecando com 'Pasta'
    # O nome da pasta exposto para o mundo deverá seguir o modelo snake_case e omitir a palavra Pasta
    # Exemplo de nome de arquivo: pasta_conta_energia_eletrica
    # Exemplo de nome de classe: PastaContaEnergiaEletrica
    # Exemplo de nome da pasta a ser exposto externamente: conta_energia_eletrica

    # Passando o id_pasta para minúsculo:
    id_pasta = id_pasta.lower()

    # Resolvendo o nome do arquivo:
    nome_arquivo = "pasta_"+id_pasta

    # Resolvendo o nome do módulo:
    nome_modulo = "pastas_contabeis."+nome_arquivo

    # Resolvendo o nome da classe:
    nome_classe = "Pasta_"+id_pasta
    nome_classe = ''.join(x.title() for x in nome_classe.split('_'))

    try:
        from nasajon.util.diario_util import DiarioUtil

        modulo = importlib.import_module(nome_modulo)
        pasta = getattr(modulo, nome_classe)(DiarioUtil())
        log.info("Pasta instanciada: {}".format(type(pasta)))

        return pasta
    except ModuleNotFoundError:
        log.info("Pasta contábil não encontrada: "+id_pasta)
        raise Exception("Pasta contábil não encontrada: "+id_pasta)
    except AttributeError:
        log.info("Pasta contábil não encontrada: "+id_pasta)
        raise Exception("Pasta contábil não encontrada: "+id_pasta)
