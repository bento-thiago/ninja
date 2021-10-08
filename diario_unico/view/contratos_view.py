from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from diario_unico.services.contato_service import ContatoService
from diario_unico.services.contrato_service import ContratoService
from diario_unico.util.diario_factory import DiarioUnicoFactory
from diario_unico.view.abstract_view import AbstractView
from nasajon.util.json_util import JsonUtil


@method_decorator(csrf_exempt, name='dispatch')
class ContratosView(AbstractView):

    def __init__(self):
        super().__init__()
        self.http_method_names = ['get', 'post']
        self.service :ContratoService= DiarioUnicoFactory.getContratosService()

    def do_get(self, request: HttpRequest, args, kwargs):
        resultados = self.service.listar_contratos(
            kwargs["tenant"])

        return JsonUtil().toDict(resultados)
