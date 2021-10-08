from django.urls import path

from . import views

from app.view.ping import PingView

from crawlers.view.solicitar_extrato import SolicitarExtratoView
from crawlers.view.status import StatusView
from crawlers.view.extrato import ExtratoView

# TODO Adicionar aqui novos mapeamentos de URLs:
urlpatterns = [
    path('solicitar/<str:iban>',
         SolicitarExtratoView.as_view(), name='solicitar_requests'),
    path('status/<str:token>',
         StatusView.as_view(), name='status_requests'),
    path('<str:token>',
         ExtratoView.as_view(), name='extrato_requests'),
]
