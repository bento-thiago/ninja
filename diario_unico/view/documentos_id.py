from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from diario_unico.util.diario_factory import DiarioUnicoFactory
import json
from nasajon.util.json_util import JsonUtil
from nasajon.util.objeto_util import ObjetosUtils
from diario_unico.entity.informacoes_a_recuperar import InformacoesARecuperar
from diario_unico.entity.filtro import Filtro
from diario_unico.view.abstract_view import AbstractView
from django.utils.decorators import method_decorator

from diario_unico.repository.util_repository import UtilRepository


@method_decorator(csrf_exempt, name='dispatch')
class DocumentosIdView(AbstractView):
    def __init__(self):
        self.service = DiarioUnicoFactory.getDocumentoService()

    def do_get(self, request: HttpRequest, args, kwargs):

        # Trata entrada
        id_documento = kwargs["id_documento"]

        tenant = kwargs["tenant"]

        result = self.service.getDocumentoInteiro(id_documento, tenant)
        return result
