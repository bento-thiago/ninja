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
class DocumentosView(AbstractView):
    def __init__(self):
        self.service = DiarioUnicoFactory.getDocumentoService()

    def do_get(self, request: HttpRequest, args, kwargs):
        # Trata entrada
        body_unicode = request.body.decode('utf-8')
        dados = JsonUtil().decode(body_unicode)

        informacoes_a_recuperar = [ObjetosUtils().dictToObject(
            info, InformacoesARecuperar) for info in dados["InformacoesARecuperar"]]
        filtro = ObjetosUtils().dictToObject(dados["filtro"], Filtro)

        tenant = kwargs["tenant"]

        result = self.service.listarDocumentos(
            filtro, informacoes_a_recuperar, tenant)
        return result
