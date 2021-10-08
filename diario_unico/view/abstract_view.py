from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from nasajon.util.json_util import JsonUtil
from nasajon.util.log import Log

# O decorator abaixo desabilita uma segurança padrão do django. Ver: https://docs.djangoproject.com/pt-br/2.2/ref/csrf/
@method_decorator(csrf_exempt, name='dispatch')
class AbstractView(View):

    def obtemMetodosPermitidos(self):
        metodosPermitidos = list()
        if self.__class__.do_get != AbstractView.do_get:
            metodosPermitidos.append('GET')
        if self.__class__.do_post != AbstractView.do_post:
            metodosPermitidos.append('POST')
        if self.__class__.do_put != AbstractView.do_put:
            metodosPermitidos.append('PUT')
        return metodosPermitidos

    def __init__(self):
        self.http_method_names = []
        

    def get(self, request: HttpRequest, *args, **kwargs):
        self.log = Log("REST_diario_unico")
        self.log.debug("GET Recebido: "+JsonUtil().encode(args))
        retorno = self.do_get(request, args, kwargs)

        return self.tratarRetorno(retorno)

    def do_get(self, request: HttpRequest, args, kwargs):
        return HttpResponseNotAllowed(self.obtemMetodosPermitidos(), "Method not allowed")

    def post(self, request: HttpRequest, *args, **kwargs):
        self.log = Log("REST_diario_unico")
        self.log.debug("POST Recebido: "+JsonUtil().encode(args))
        retorno = self.do_post(request, args, kwargs)

        return self.tratarRetorno(retorno)

    def do_post(self, request: HttpRequest, args, kwargs):
        return HttpResponseNotAllowed(self.obtemMetodosPermitidos(), "Method not allowed")

    def put(self, request: HttpRequest, *args, **kwargs):
        self.log = Log("REST_diario_unico")
        self.log.debug("PUT Recebido: "+JsonUtil().encode(args))
        retorno = self.do_put(request, args, kwargs)

        return self.tratarRetorno(retorno)

    def do_put(self, request: HttpRequest, args, kwargs):
        return HttpResponseNotAllowed(self.obtemMetodosPermitidos(), "Method not allowed")

    def tratarRetorno(self, retorno):
        if isinstance(retorno, HttpResponse):
            return retorno
        elif not isinstance(retorno, dict):
             return HttpResponse(JsonUtil().encode(retorno))
        elif  'status' not in retorno:
            return HttpResponse(JsonUtil().encode(retorno))
        elif retorno['status'] == 400:
            return HttpResponseBadRequest(retorno['msg'])
        else:
            return HttpResponse(JsonUtil().encode(retorno))
