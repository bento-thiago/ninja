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
class CobrancasView(AbstractView):

    def __init__(self):
        super().__init__()
        self.http_method_names = ['get', 'post']
        self.service = DiarioUnicoFactory.getCobrancasService()

    def do_post(self, request: HttpRequest, args, kwargs):

        # Recuperando o corpo da requisição:
        body_unicode = request.body.decode('utf-8')
        dados = JsonUtil().decode(body_unicode)
        cobranca = ObjetosUtils().dictToObject(dados, InfoCobranca)
        cobranca.tenant = kwargs["tenant"]

        # Inserindo o pagamento
        resultado = self.service.inserir(cobranca)

        return resultado

    def do_get(self, request: HttpRequest, args, kwargs):

        # Recuperando filtros da requisição:
        situacao = request.GET.get('situacao')
        vencimento_apos = request.GET.get('vencimento_apos')

        # Listando os pagamentos
        resultados = self.service.listar(
            kwargs["tenant"], situacao, vencimento_apos)

        return resultados
