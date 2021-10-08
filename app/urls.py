from django.urls import path

import app.view.pastas_contabeis

# TODO Adicionar aqui novos mapeamentos de URLs:
# Pode ver o exemplo PingPong
urlpatterns = [

    path('<str:id_pasta>/notificar/<str:momento_contabil>/',
         app.view.pastas_contabeis.notificar, name='pastas_contabeis'),
    path('<str:id_pasta>/apropriar/',
         app.view.pastas_contabeis.apropriar, name='pastas_contabeis_apropriar'),
    path('status/<str:token>',
         app.view.pastas_contabeis.status, name='pastas_contabeis_status'),
]
