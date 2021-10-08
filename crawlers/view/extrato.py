from django.http import HttpRequest, HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from nasajon.util.json_util import JsonUtil
from nasajon.util.objeto_util import ObjetosUtils
from crawlers.view.abstract_view import AbstractView
from django.utils.encoding import smart_str
import os


class ExtratoView(AbstractView):

    def __init__(self):
        super().__init__()
        self.http_method_names = ['get']

    def get(self, request: HttpRequest, *args, **kwargs):

        file_path = os.path.join(os.path.dirname(
            __file__), "../requisicoes/{}.ofx".format(kwargs["token"]))

        if not os.path.isfile(file_path):
            raise Http404()

        response = HttpResponse(open(file_path, "r"),
                                content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % (
            'extrato.ofx')

        return response
