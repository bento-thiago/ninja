from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from nasajon.util.json_util import JsonUtil
from nasajon.util.objeto_util import ObjetosUtils
from diario_unico.util import date_util
from diario_unico.util.diario_factory import DiarioUnicoFactory
from diario_unico.view.abstract_view import AbstractView
from diario_unico.entity.info_cobranca import InfoCobranca
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class CobrancasIdView(AbstractView):

    def __init__(self):
        self.http_method_names = ['put']
        self.service = DiarioUnicoFactory.getCobrancasService()

    def do_put(self, request: HttpRequest, args, kwargs):

        # Recuperando o corpo da requisição:
        body_unicode = request.body.decode('utf-8')
        dados = JsonUtil().decode(body_unicode)
        cobranca = ObjetosUtils().dictToObject(dados, InfoCobranca)
        cobranca.tenant = kwargs["tenant"]
        cobranca.id_cobranca = kwargs["id_cobranca"]

        # Verificando se trata-se de uma inserção ou atualização, e chamando o service:
        resultado = self.service.atualizar(cobranca)

        return resultado
