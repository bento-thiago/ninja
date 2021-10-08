from django.urls import path

from . import views

from app.view.ping import PingView

import diario_unico.view.documentos
import diario_unico.view.pagamentos
from diario_unico.view.pagamentos import PagamentosView
from diario_unico.view.pagamentos_id import PagamentosIdView
from diario_unico.view.cobrancas import CobrancasView
from diario_unico.view.cobrancas_id import CobrancasIdView
from diario_unico.view.documentos import DocumentosView
from diario_unico.view.documentos_id import DocumentosIdView
from diario_unico.view.plano_contas import PlanoContasView
from diario_unico.view.estabelecimentos import EstabelecimentoView
from diario_unico.view.pagamentos_pjbank import PagamentosPJBankView
from diario_unico.view.cobrancas_pjbank import CobrancasPJBankView

# from diario_unico.view.exec_query import ExecQueryView

import os

# TODO Adicionar aqui novos mapeamentos de URLs:
from .view.contratos_view import ContratosView

urlpatterns = [
    path('documentos',
         DocumentosView.as_view(), name='documentos_requests'),
    path('documentos/<str:id_documento>',
         DocumentosIdView.as_view(), name='documentos_requests_id'),
    path('pagamentos',
         PagamentosView.as_view(), name='pagamentos_requests'),
    path('pagamentos/<str:id_pagamento>',
         PagamentosIdView.as_view(), name='pagamentos_requests_id'),
    path('cobrancas',
         CobrancasView.as_view(), name='cobrancas_requests'),
    path('cobrancas/<str:id_cobranca>',
         CobrancasIdView.as_view(), name='cobrancas_requests_id'),
    path('plano_contas/reconstruir/<str:empresa>',
         PlanoContasView.as_view(), name='plano_contas_requests'),
    path('estabelecimentos',
         EstabelecimentoView.as_view(), name='estabelecimentos_requests'),
    path('contratos',
         ContratosView.as_view(), name='contratos_requests'),
    path('pjbank/conta_digital',
         PagamentosPJBankView.as_view(), name='pagamentos_pjbank_requests'),
    path('pjbank/boleto/<str:id_documento>',
         CobrancasPJBankView.as_view(), name='cobrancas_pjbank_requests'),
]

# if (bool(os.getenv("permite_sql", False))):
#     urlpatterns.append(
#         path('sql', ExecQueryView.as_view(), name='exec_query')
#     )
