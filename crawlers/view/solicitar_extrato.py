from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from nasajon.util.json_util import JsonUtil
from nasajon.util.objeto_util import ObjetosUtils
from crawlers.view.abstract_view import AbstractView
from django.utils.encoding import smart_str
from nasajon.util.nasajon_factory import NasajonFactory
from nasajon.entity.log_assincrono import LogAssincrono
import crawlers.celery.crawler_celery as crawler_celery
import uuid
import os
from crawlers.util.crawler_factory import CrawlerFactory


class SolicitarExtratoView(AbstractView):

    def __init__(self):
        super().__init__()
        self.http_method_names = ['get']

    def get(self, request: HttpRequest, *args, **kwargs):
        conta = CrawlerFactory.getFinanceiroService().getConta(
            kwargs["iban"], kwargs["tenant"])

        if conta == None:
            return HttpResponseBadRequest("Código Iban inválido para o tenant informado.")

        key = conta["api_key"]
        codigo = key["codigo"]
        senha = key["senha"]

        log_assincrono = LogAssincrono(
            uuid.uuid4(), "extratos_bancarios", "Aguardando", kwargs["tenant"])

        NasajonFactory.getLogAssincronoService().inserir(log_assincrono)

        crawler_celery.baixar_extrato.delay(
            codigo, senha, log_assincrono.token, kwargs["tenant"])

        response = HttpResponse(status=202)
        response['Location'] = "/extratos_bancarios/status/" + \
            str(log_assincrono.token)

        return response
