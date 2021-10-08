from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
from nasajon.util.json_util import JsonUtil
from nasajon.util.objeto_util import ObjetosUtils
from diario_unico.entity.informacoes_a_recuperar import InformacoesARecuperar
from diario_unico.entity.filtro import Filtro
from diario_unico.view.abstract_view import AbstractView
from django.utils.decorators import method_decorator
from diario_unico.util.diario_factory import DiarioUnicoFactory


@method_decorator(csrf_exempt, name='dispatch')
class PlanoContasView(AbstractView):
    def __init__(self):
        self.service = DiarioUnicoFactory.getPlanoContasService()

    def do_post(self, request: HttpRequest, args, kwargs):
        empresa = kwargs["empresa"]
        tenant = kwargs["tenant"]

        self.service.reconstruir_plano_contas(empresa, tenant)
        return {"status": "OK"}
