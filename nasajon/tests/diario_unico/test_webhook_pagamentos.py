import unittest
from unittest import mock
import json
import datetime
import os
from diario_unico.view.pagamentos_pjbank import PagamentosPJBankView, InfoPagamento
from diario_unico.enum.info_pagamento.situacao_info_pagamento import SituacaoInfoPagamento
from diario_unico.entity.documento import Documento
from diario_unico.enum.situacao import Situacao
from django.http import HttpRequest


def mocked_service_get_pagamento_agendado(tenant, operacao):

    return {"situacao": SituacaoInfoPagamento.AGENDADO.value, "id_documento": 1}


def mocked_service_get_pagamento_pendente_autorizacao(tenant, operacao):

    return {"situacao": SituacaoInfoPagamento.PENDENTE_AUTORIZACAO.value, "id_documento": 1}


def mocked_service_get_documento(documento, tenant):

    return Documento()


def mocked_service_atualizar_pagamento(pagamento: InfoPagamento):
    pass


def mocked_service_atualizar_documento(documento: Documento):
    pass


def mocked_service_notificar(pasta_contabil, momento, dados, token):
    pass


def mocked_log_assincrono(log):
    pass


class TestWebhookPagamentos(unittest.TestCase):

    """
    Teste de pagamento com erro
    """
    @mock.patch('diario_unico.services.documento_service.DocumentoService.atualizarDocumento', side_effect=mocked_service_atualizar_documento)
    @mock.patch('diario_unico.services.pagamentos_service.PagamentosService.atualizar', side_effect=mocked_service_atualizar_pagamento)
    @mock.patch('diario_unico.services.documento_service.DocumentoService.getDocumentoInteiro', side_effect=mocked_service_get_documento)
    @mock.patch('diario_unico.services.pagamentos_service.PagamentosService.getPagamentoOperacao', side_effect=mocked_service_get_pagamento_agendado)
    def test_webhook_pagamento_com_erro(self, mock_get_pagamento, mock_get_documento, mock_atualizar_pagamento, mock_atualizar_documento):
        kwargs = {"tenant": 47}
        body = {"id_operacao": 1,
                "status_pagamento": "com_erro", "mensagem": "teste"}
        request = type('obj', (object,), {
                       'body': json.dumps(body).encode(encoding='utf-8')})
        PagamentosPJBankView().do_put(request, [], kwargs)
        pagamento = mock_atualizar_pagamento.call_args[0][0]
        self.assertEqual(pagamento.situacao, SituacaoInfoPagamento.ERRO)
        self.assertEqual(pagamento.mensagem_erro, body["mensagem"])

        documento = mock_atualizar_documento.call_args[0][0]
        self.assertEqual(documento.situacao, Situacao.REJEITADO)

    """
    Teste de pagamento rejeitado
    """
    @mock.patch('diario_unico.services.documento_service.DocumentoService.atualizarDocumento', side_effect=mocked_service_atualizar_documento)
    @mock.patch('diario_unico.services.pagamentos_service.PagamentosService.atualizar', side_effect=mocked_service_atualizar_pagamento)
    @mock.patch('diario_unico.services.documento_service.DocumentoService.getDocumentoInteiro', side_effect=mocked_service_get_documento)
    @mock.patch('diario_unico.services.pagamentos_service.PagamentosService.getPagamentoOperacao', side_effect=mocked_service_get_pagamento_agendado)
    def test_webhook_pagamento_rejeitada(self, mock_get_pagamento, mock_get_documento, mock_atualizar_pagamento, mock_atualizar_documento):
        kwargs = {"tenant": 47}
        body = {"id_operacao": 1,
                "status_pagamento": "rejeitada", "mensagem": "teste"}
        request = type('obj', (object,), {
                       'body': json.dumps(body).encode(encoding='utf-8')})
        PagamentosPJBankView().do_put(request, [], kwargs)
        pagamento = mock_atualizar_pagamento.call_args[0][0]
        self.assertEqual(pagamento.situacao, SituacaoInfoPagamento.REJEITADO)
        self.assertEqual(pagamento.mensagem_erro, body["mensagem"])

        documento = mock_atualizar_documento.call_args[0][0]
        self.assertEqual(documento.situacao, Situacao.REJEITADO)

    """
    Teste de pagamento pendente de autorização
    """
    @mock.patch('diario_unico.services.pagamentos_service.PagamentosService.atualizar', side_effect=mocked_service_atualizar_pagamento)
    @mock.patch('diario_unico.services.documento_service.DocumentoService.getDocumentoInteiro', side_effect=mocked_service_get_documento)
    @mock.patch('diario_unico.services.pagamentos_service.PagamentosService.getPagamentoOperacao', side_effect=mocked_service_get_pagamento_agendado)
    def test_webhook_pagamento_autorizacao(self, mock_get_pagamento, mock_get_documento, mock_atualizar_pagamento):
        kwargs = {"tenant": 47}
        body = {"id_operacao": 1,
                "status_pagamento": "pendente_autorizacao"}
        request = type('obj', (object,), {
                       'body': json.dumps(body).encode(encoding='utf-8')})
        PagamentosPJBankView().do_put(request, [], kwargs)
        pagamento = mock_atualizar_pagamento.call_args[0][0]
        self.assertEqual(pagamento.situacao,
                         SituacaoInfoPagamento.PENDENTE_AUTORIZACAO)

    """
    Teste de pagamento realizado
    """
    @mock.patch('services.log_assincrono_service.LogAssincronoService.inserir', side_effect=mocked_log_assincrono)
    @mock.patch('pastas_contabeis.pastas_router.notificar.delay', side_effect=mocked_service_notificar)
    @mock.patch('diario_unico.services.documento_service.DocumentoService.getDocumentoInteiro', side_effect=mocked_service_get_documento)
    @mock.patch('diario_unico.services.pagamentos_service.PagamentosService.getPagamentoOperacao', side_effect=mocked_service_get_pagamento_pendente_autorizacao)
    def test_webhook_pagamento_realizada(self, mock_get_pagamento, mock_get_documento, mock_notificar: mock.MagicMock, mock_log_assincrono):
        kwargs = {"tenant": 47}
        body = {"id_operacao": 1,
                "status_pagamento": "realizada", "data_pagamento": "12/31/2019", "valor": 10.0}
        request = type('obj', (object,), {
                       'body': json.dumps(body).encode(encoding='utf-8')})
        PagamentosPJBankView().do_put(request, [], kwargs)
        mock_notificar.assert_called_once()
        args = mock_notificar.call_args[0]
        self.assertEqual(args[0], "desconhecida")
        self.assertEqual(args[1], "quitacao")

        pagamento = args[2]["pagamento"]

        self.assertEqual(pagamento["valor"], 10.0)
        self.assertEqual(pagamento["data_pagamento"],
                         datetime.datetime(2019, 12, 31))


if __name__ == '__main__':
    unittest.main()
