import unittest
from unittest import mock
import json
import datetime
import os
from diario_unico.view.cobrancas_pjbank import CobrancasPJBankView, InfoCobranca
from diario_unico.enum.info_cobranca.situacao_info_cobranca import SituacaoInfoCobranca
from diario_unico.entity.documento import Documento
from diario_unico.enum.situacao import Situacao
from django.http import HttpRequest


def mocked_service_get_cobranca_agendado(tenant, id_documento):

    return {"situacao": SituacaoInfoCobranca.AGENDADO.value, "id_documento": id_documento}


def mocked_service_get_cobranca_aberto(tenant, id_documento):

    return {"situacao": SituacaoInfoCobranca.ABERTO.value, "id_documento": id_documento}


def mocked_service_get_documento(documento, tenant):

    return Documento()


def mocked_service_atualizar_cobranca(cobranca: InfoCobranca):
    pass


def mocked_service_atualizar_documento(documento: Documento):
    pass


def mocked_service_notificar(pasta_contabil, momento, dados, token):
    pass


def mocked_service_enviar_email(de, para, template, dados_email, tenant):
    pass


def mocked_log_assincrono(log):
    pass


class TestWebhookCobrancas(unittest.TestCase):

    """
    Teste de cobranca rejeitada
    """
    @mock.patch('diario_unico.services.documento_service.DocumentoService.atualizarDocumento', side_effect=mocked_service_atualizar_documento)
    @mock.patch('diario_unico.services.cobrancas_service.CobrancasService.atualizar', side_effect=mocked_service_atualizar_cobranca)
    @mock.patch('diario_unico.services.documento_service.DocumentoService.getDocumentoInteiro', side_effect=mocked_service_get_documento)
    @mock.patch('diario_unico.services.cobrancas_service.CobrancasService.getByIdDocumento', side_effect=mocked_service_get_cobranca_agendado)
    def test_webhook_cobranca_rejeitado(self, mock_get_cobranca, mock_get_documento, mock_atualizar_cobranca, mock_atualizar_documento):
        kwargs = {"tenant": 47, "id_documento": 1}
        body = {"registro_sistema_bancario": "rejeitado",
                "registro_rejeicao_motivo": "teste"}
        request = type('obj', (object,), {
                       'body': json.dumps(body).encode(encoding='utf-8')})
        CobrancasPJBankView().do_put(request, [], kwargs)
        cobranca = mock_atualizar_cobranca.call_args[0][0]
        self.assertEqual(cobranca.situacao, SituacaoInfoCobranca.ERRO)
        self.assertEqual(cobranca.mensagem_erro,
                         body["registro_rejeicao_motivo"])

        documento = mock_atualizar_documento.call_args[0][0]
        self.assertEqual(documento.situacao, Situacao.REJEITADO)

    """
    Teste de cobranca aberto
    """
    @mock.patch('diario_unico.util.mala_direta.MalaDireta.enviarEmail', side_effect=mocked_service_enviar_email)
    @mock.patch('diario_unico.services.cobrancas_service.CobrancasService.atualizar', side_effect=mocked_service_atualizar_cobranca)
    @mock.patch('diario_unico.services.documento_service.DocumentoService.getDocumentoInteiro', side_effect=mocked_service_get_documento)
    @mock.patch('diario_unico.services.cobrancas_service.CobrancasService.getByIdDocumento', side_effect=mocked_service_get_cobranca_agendado)
    def test_webhook_cobranca_aberto(self, mock_get_cobranca, mock_get_documento, mock_atualizar_cobranca, mock_enviar_email):
        kwargs = {"tenant": 47, "id_documento": 1}
        body = {"registro_sistema_bancario": "confirmado",
                "data_vencimento": "12/31/2019"}
        request = type('obj', (object,), {
                       'body': json.dumps(body).encode(encoding='utf-8')})
        CobrancasPJBankView().do_put(request, [], kwargs)
        cobranca = mock_atualizar_cobranca.call_args[0][0]
        self.assertEqual(cobranca.situacao,
                         SituacaoInfoCobranca.ABERTO)

    @mock.patch('services.log_assincrono_service.LogAssincronoService.inserir', side_effect=mocked_log_assincrono)
    @mock.patch('pastas_contabeis.pastas_router.notificar.delay', side_effect=mocked_service_notificar)
    @mock.patch('diario_unico.services.documento_service.DocumentoService.getDocumentoInteiro', side_effect=mocked_service_get_documento)
    @mock.patch('diario_unico.services.cobrancas_service.CobrancasService.getByIdDocumento', side_effect=mocked_service_get_cobranca_aberto)
    def test_webhook_cobranca_quitado(self, mock_get_cobranca, mock_get_documento, mock_notificar: mock.MagicMock, mock_log_assincrono):
        kwargs = {"tenant": 47, "id_documento": 1}
        body = {"registro_sistema_bancario": "confirmado",
                "data_pagamento": "12/31/2019", "valor_pago": 10.0}
        request = type('obj', (object,), {
                       'body': json.dumps(body).encode(encoding='utf-8')})
        CobrancasPJBankView().do_put(request, [], kwargs)
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
