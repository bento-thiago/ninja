from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from nasajon.util.json_util import JsonUtil
from nasajon.util.objeto_util import ObjetosUtils
from crawlers.view.abstract_view import AbstractView
from django.utils.encoding import smart_str
from nasajon.util.nasajon_factory import NasajonFactory
import nasajon.pastas_contabeis.pastas_router as pastas_router
import uuid
import json


class StatusView(AbstractView):

    def __init__(self):
        super().__init__()
        self.http_method_names = ['get', 'delete']

    def get(self, request: HttpRequest, *args, **kwargs):

        status = NasajonFactory.getLogAssincronoService().getStatusLogAssincrono(
            kwargs["token"], kwargs["tenant"], "extratos_bancarios")

        if not status:
            return HttpResponseBadRequest("Token informado não existente no banco")

        if status == "Concluido":
            response = HttpResponse(status=303)
            response['Location'] = "/{}/extratos_bancarios/{}".format(
                kwargs["tenant"], kwargs["token"])

            return response
        else:
            return HttpResponse(json.dumps({"status": status, "link": {"rel": "cancelar", "method": "delete", "href": "{}/extratos_bancarios/status/{}".format(kwargs["tenant"], kwargs["token"])}}))
