from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from diario_unico.util import date_util
from nasajon.util.json_util import JsonUtil
from diario_unico.util.diario_factory import DiarioUnicoFactory
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.enum.situacao import Situacao
from diario_unico.view.abstract_view import AbstractView
from diario_unico.entity.info_pagamento import InfoPagamento
from diario_unico.enum.info_pagamento.situacao_info_pagamento import SituacaoInfoPagamento
from nasajon.util.objeto_util import ObjetosUtils
from django.utils.decorators import method_decorator
from nasajon.pastas_contabeis.pastas_router import get_pasta_obj, MomentoContabil, notificar as notificar_task
from nasajon.util.nasajon_factory import NasajonFactory
from nasajon.entity.log_assincrono import LogAssincrono
import datetime
import uuid
from diario_unico.repository.util_repository import UtilRepository


@method_decorator(csrf_exempt, name='dispatch')
class PagamentosPJBankView(AbstractView):

    def __init__(self):
        self.http_method_names = ['put']
        self.service = DiarioUnicoFactory.getPagamentosService()
        self.documento_service = DiarioUnicoFactory.getDocumentoService()

    def do_put(self, request: HttpRequest, args, kwargs):

        # Tratando os parametros de entrada:
        tenant = kwargs["tenant"]
        dados = JsonUtil().decode(request.body.decode('utf-8'))

        pagamento = self.service.getPagamentoOperacao(
            tenant, dados["id_operacao"])
        if not pagamento:
            return {"msg": 'Não existe pagamento para o id_operacao informado.', "status": 400}

        pagamento = ObjetosUtils().dictToObject(pagamento, InfoPagamento)

        documento = self.documento_service.getDocumentoInteiro(
            pagamento.id_documento, tenant)

        if pagamento.situacao == SituacaoInfoPagamento.PENDENTE_AUTORIZACAO.value and dados["status_pagamento"] == 'realizada':

            if documento.tipo == DocumentoTipo.CONTA_ENERGIA.value:
                pasta_contabil = 'conta_energia_eletrica'
            elif documento.tipo == DocumentoTipo.CONTA_AGUA_E_ESGOTO.value:
                pasta_contabil = 'conta_agua'
            elif documento.tipo == DocumentoTipo.CONTA_GAS.value:
                pasta_contabil = 'conta_gas'
            elif documento.tipo == DocumentoTipo.COTA_CONDOMINIAL.value:
                pasta_contabil = 'cota_condominial'
            else:
                pasta_contabil = 'desconhecida'

            doc_pag = {"documento": JsonUtil().toDict(documento)}
            pagamento = {"data_pagamento": datetime.datetime.strptime(
                dados["data_pagamento"], '%m/%d/%Y'), "valor": dados["valor"]}
            doc_pag["pagamento"] = pagamento
            doc_pag["tenant"] = tenant

            # Criar a requisição
            log_assincrono = LogAssincrono(
                uuid.uuid4(), "pastas_contabeis", "Aguardando", tenant)

            # Salvar a requisição no banco
            NasajonFactory.getLogAssincronoService().inserir(log_assincrono)

            # Enfileirando a chamada para a pasta contábil:
            notificar_task.delay(
                pasta_contabil, MomentoContabil.QUITACAO.value, doc_pag, log_assincrono.token)

            response = HttpResponse(status=202)
            response['Location'] = "{}/pastas_contabeis/status/{}".format(
                tenant, str(log_assincrono.token))

            # Retornando ok:
            return response
        elif dados["status_pagamento"] == 'com_erro' or dados["status_pagamento"] == 'nao_realizada':

            pagamento.situacao = SituacaoInfoPagamento.ERRO
            pagamento.mensagem_erro = dados['mensagem']

            self.service.atualizar(pagamento)
            documento.situacao = Situacao.REJEITADO
            self.documento_service.atualizarDocumento(documento)

        elif pagamento.situacao == SituacaoInfoPagamento.AGENDADO.value and dados["status_pagamento"] == 'pendente_autorizacao':

            pagamento.situacao = SituacaoInfoPagamento.PENDENTE_AUTORIZACAO

            self.service.atualizar(pagamento)

        elif dados["status_pagamento"] == 'rejeitada':

            pagamento.situacao = SituacaoInfoPagamento.REJEITADO
            pagamento.mensagem_erro = dados['mensagem']

            self.service.atualizar(pagamento)
            documento.situacao = Situacao.REJEITADO
            self.documento_service.atualizarDocumento(documento)

        return {}
