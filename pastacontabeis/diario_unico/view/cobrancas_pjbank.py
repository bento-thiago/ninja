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
from diario_unico.entity.info_cobranca import InfoCobranca
from diario_unico.enum.info_cobranca.situacao_info_cobranca import SituacaoInfoCobranca
from nasajon.util.objeto_util import ObjetosUtils
from django.utils.decorators import method_decorator
from nasajon.pastas_contabeis.pastas_router import get_pasta_obj, MomentoContabil, notificar as notificar_task
from nasajon.util.nasajon_factory import NasajonFactory
from nasajon.entity.log_assincrono import LogAssincrono
import datetime
from diario_unico.util.mala_direta import MalaDireta

from diario_unico.repository.util_repository import UtilRepository
import uuid
import os


@method_decorator(csrf_exempt, name='dispatch')
class CobrancasPJBankView(AbstractView):

    def __init__(self):
        self.http_method_names = ['put']
        self.service = DiarioUnicoFactory.getCobrancasService()
        self.documento_service = DiarioUnicoFactory.getDocumentoService()

    def do_put(self, request: HttpRequest, args, kwargs):

        # Tratando os parametros de entrada:
        tenant = kwargs["tenant"]
        dados = JsonUtil().decode(request.body.decode('utf-8'))

        cobranca = self.service.getByIdDocumento(
            tenant, kwargs["id_documento"])
        if not cobranca:
            return {"msg": 'Não existe cobrança para o id_documento informado.', "status": 400}

        cobranca = ObjetosUtils().dictToObject(cobranca, InfoCobranca)

        documento = self.documento_service.getDocumentoInteiro(
            cobranca.id_documento, tenant)

        if cobranca.situacao == SituacaoInfoCobranca.ABERTO.value and dados["registro_sistema_bancario"] == 'confirmado' and "data_pagamento" in dados:

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
            cobranca = {"data_pagamento": datetime.datetime.strptime(
                dados["data_pagamento"], '%m/%d/%Y'), "valor": dados["valor_pago"]}
            doc_pag["pagamento"] = cobranca
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

        elif cobranca.situacao == SituacaoInfoCobranca.AGENDADO.value and dados["registro_sistema_bancario"] == 'confirmado' and "data_pagamento" not in dados:

            mes = dados['data_vencimento'].split("/")
            mes = mes[0] + "/" + mes[2]

            dados_email = {'condominio': cobranca.condominio,
                           'cliente': cobranca.nome_cliente, 'mes': mes, 'link': cobranca.url_boleto}
            MalaDireta().enviarEmail(os.getenv("email_sender", ""),
                                     [cobranca.email], 'meucondominio_boleto', dados_email, tenant)

            cobranca.situacao = SituacaoInfoCobranca.ABERTO

            self.service.atualizar(cobranca)
        elif dados["registro_sistema_bancario"] == 'rejeitado':

            cobranca.situacao = SituacaoInfoCobranca.ERRO
            cobranca.mensagem_erro = dados['registro_rejeicao_motivo']

            self.service.atualizar(cobranca)
            documento.situacao = Situacao.REJEITADO
            self.documento_service.atualizarDocumento(documento)

        return {}
