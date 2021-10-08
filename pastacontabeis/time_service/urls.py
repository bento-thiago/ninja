from django.urls import path

from . import views

from time_service.view.time import TimeView
from time_service.view.time_page import TimePageView
from time_service.view.datas_apresentacao import DatasApresentacaoView

# TODO Adicionar aqui novos mapeamentos de URLs:
urlpatterns = [
    path('api/time',
         TimeView.as_view(), name='time_requests'),
    path('time',
         TimePageView.as_view(), name='time_page'),
    path('datas_apresentacao',
         DatasApresentacaoView.as_view(), name='datas_apresentacao_page')
]
