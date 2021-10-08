from django.http import HttpRequest
from django.shortcuts import render
from time_service.view.abstract_view import AbstractView


class DatasApresentacaoView(AbstractView):

    def __init__(self):
        super().__init__()
        self.http_method_names = ['get']

    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, 'datas_apresentacao.html', {})
