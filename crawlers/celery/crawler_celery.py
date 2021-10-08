from __future__ import absolute_import, unicode_literals
from celery import shared_task

from nasajon.util.log import Log
from nasajon.util.repetir_exception import RepetirException

import os
import shutil
from crawlers.services.itau_service import ItauService
from nasajon.util.nasajon_factory import NasajonFactory
from nasajon.entity.log_assincrono import LogAssincrono

log = Log("PASTAS_ROUTER")


def inserirLogAssincrono(id_log_assincrono, recurso, status, tenant):
    log_assincrono = LogAssincrono(
        id_log_assincrono, recurso, status, tenant)
    NasajonFactory.getLogAssincronoService().inserir(log_assincrono)


@shared_task
def baixar_extrato(codigo, senha, id_log_assincrono, tenant, tentativa: int = 1):
    log.info("Baixando extrato do operador {}".format(codigo))
    try:
        inserirLogAssincrono(
            id_log_assincrono, "extratos_bancarios", "Baixando extrato", tenant)

        caminho_extrato = ItauService(
            codigo, senha).baixar_extrato(id_log_assincrono)

        if not os.path.isdir(os.path.join(os.path.dirname(
                __file__), "../../crawlers/requisicoes")):
            os.mkdir(os.path.join(os.path.dirname(
                __file__), "../../crawlers/requisicoes"))

        shutil.copy(caminho_extrato, os.path.join(os.path.dirname(
            __file__), "../../crawlers/requisicoes/{}.ofx".format(id_log_assincrono)))
        inserirLogAssincrono(
            id_log_assincrono, "extratos_bancarios", "Concluido", tenant)
    except RepetirException as err:
        if tentativa < 5:
            baixar_extrato.delay(
                codigo, senha, id_log_assincrono, tenant, tentativa + 1)
        else:
            log.info(str(err))
            inserirLogAssincrono(
                id_log_assincrono, "extratos_bancarios", "Erro ao baixar extrato depois de 5 tentativas: " + str(err), tenant)
            raise err
    except Exception as err:
        log.info(str(err))
        inserirLogAssincrono(
            id_log_assincrono, "extratos_bancarios", "Erro ao baixar extrato: " + str(err), tenant)
        raise err
