from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from nasajon.util.json_util import JsonUtil


# O decorator abaixo desabilita uma segurança padrão do django. Ver: https://docs.djangoproject.com/pt-br/2.2/ref/csrf/
@method_decorator(csrf_exempt, name='dispatch')
class AbstractView(View):

    def __init__(self):
        self.http_method_names = []

    def get(self, request: HttpRequest, *args, **kwargs):
        retorno = self.do_get(request, args, kwargs)

        return self.tratarRetorno(retorno)

    def do_get(self, request: HttpRequest, args, kwargs):
        return {"msg": "Método não implementado ainda"}

    def post(self, request: HttpRequest, *args, **kwargs):
        retorno = self.do_post(request, args, kwargs)

        return self.tratarRetorno(retorno)

    def do_post(self, request: HttpRequest, args, kwargs):
        return {"msg": "Método não implementado ainda"}

    def tratarRetorno(self, retorno):
        if type(retorno) is list or 'status' not in retorno:
            return HttpResponse(JsonUtil().encode(retorno))
        elif retorno['status'] == 400:
            return HttpResponseBadRequest(retorno['msg'])
        else:
            return HttpResponse(JsonUtil().encode(retorno))
