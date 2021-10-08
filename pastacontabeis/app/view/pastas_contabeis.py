from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from nasajon.pastas_contabeis.pastas_router import get_pasta_obj, MomentoContabil, notificar as notificar_task
from nasajon.util.nasajon_factory import NasajonFactory
from nasajon.entity.log_assincrono import LogAssincrono
from nasajon.util.jobs_util import JobsUtil
from nasajon.util.log import Log
import uuid
import json


@csrf_exempt
def apropriar(request: HttpRequest, tenant: int, id_pasta: str):
    log = Log("API_PASTAS_CONTABEIS")
    log.info("Entrando no método 'apropriar'...")

    # Recuperando o corpo da requisição:
    body_unicode = request.body.decode('utf-8')
    dados = json.loads(body_unicode)

    # TODO Implementar validação dos campos obrigatórios

    # Adcionando o tenant, nos dados da requisição:
    dados['tenant'] = tenant

    # Invocando o método de apropriação da pasta contábil:
    get_pasta_obj(id_pasta).apropriar(dados)

    # Gerando log:
    log = Log("API_PASTAS_CONTABEIS")
    log.info("Apropriando...  Pasta: {}  -  Dados: {}".format(id_pasta, dados))

    # Retornando ok:
    retorno = {'status': 200, 'msg': 'ok'}
    return HttpResponse(json.dumps(retorno))


@csrf_exempt
def notificar(request: HttpRequest, tenant: int, id_pasta: str, momento_contabil: str):
    log = Log("API_PASTAS_CONTABEIS")
    log.info("Entrando no método 'notificar'...")

    # Recuperando o corpo da requisição:
    body_unicode = request.body.decode('utf-8')
    dados = json.loads(body_unicode)
    # Adcionando o tenant, nos dados da requisição:
    dados['tenant'] = tenant

    # TODO Implementar validação dos campos obrigatórios

    # Tratando do momento contábil:
    momento = MomentoContabil(momento_contabil)

    # Criar a requisição
    log_assincrono = LogAssincrono(
        uuid.uuid4(), "pastas_contabeis", "Aguardando", tenant)

    # Salvar a requisição no banco
    NasajonFactory.getLogAssincronoService().inserir(log_assincrono)

    # Enfileirando a chamada para a pasta contábil:
    notificar_task.delay(id_pasta, momento.value, dados, log_assincrono.token)

    # Gerando log:
    log.info("Origem1: {}".format(request.META.get('HTTP_X_FORWARDED_FOR')))
    log.info("Origem2: {}".format(request.META.get('REMOTE_ADDR')))
    log.info("Origem3: {}".format(request.META.get('REMOTE_HOST')))
    log.info("Enfileirando...  Pasta: {}  -  Momento: {}  -  Dados: {}".format(
        id_pasta, momento.value, dados))

    response = HttpResponse(status=202)
    response['Location'] = "{}/pastas_contabeis/status/{}".format(
        tenant, str(log_assincrono.token))

    # Retornando ok:
    return response


@csrf_exempt
def status(request: HttpRequest, tenant: int, token: str):
    status = NasajonFactory.getLogAssincronoService().getStatusLogAssincrono(token,
                                                                             tenant, "pastas_contabeis")

    if not status:
        return HttpResponseBadRequest("Token informado não existente no banco")

    resposta = {"status": status}

    if status != "Concluido":
        resposta["link"] = {"rel": "cancelar", "method": "delete",
                            "href": "{}/pastas_contabeis/cancelar/{}".format(tenant, token)}

    return HttpResponse(json.dumps(resposta))
