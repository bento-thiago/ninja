from dateutil import relativedelta

from nasajon.entity.dados_escrituracao_futura import ValoresAnteriores
from nasajon.enum.heuristica_projecao import HeuristicaProjecao

from diario_unico.enum.documentos.item_documento_tipo_imposto import ItemDocumentoTipoImposto
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from diario_unico.entity.informacoes_a_recuperar import InformacoesARecuperar
from diario_unico.entity.filtro import Filtro


from diario_unico.util.diario_factory import DiarioUnicoFactory
from diario_unico.repository.util_repository import UtilRepository

from nasajon.util.json_util import JsonUtil
from nasajon.util.objeto_util import ObjetosUtils
from typing import List

from nasajon.util.log import Log

import datetime
import json
import os
import requests


class DiarioUtil:

    def __init__(self):
        # URL base do diário unico
        self.url_diario = os.getenv(
            "url_diario_unico", "http://localhost:81")

    def escriturar_antecipadamente_documento(self, tenant: int, conteudo: object):
        return DiarioUnicoFactory.getDocumentoService().insereDocumento(conteudo, tenant, None, None, True)

    def apropriar_documento(self, tenant: int, conteudo: object):
        return DiarioUnicoFactory.getDocumentoService().insereDocumento(conteudo, tenant, None, None, True)
    
    def apropriar_fatura_prestacao_servicos(self, tenant:int, conteudo: object):
        return DiarioUnicoFactory.getFaturaPrestacaoServicosService().inserir_fatura_prestacao_servicos(tenant, conteudo)

    def listar_fatura_prestacao_servicos(self, tenant:int):
        return DiarioUnicoFactory.getFaturaPrestacaoServicosService().listar(tenant)

    def quitar_documento(self, tenant: int, conteudo: object):
        return DiarioUnicoFactory.getDocumentoService().insereDocumento(conteudo, tenant, None, None, True)

    def getDadosCobranca(self, tenant: int, participante: str):
        # Rota
        from nasajon.entity.dados_cobranca import Dados_Cobranca

        url = self.url_diario + \
            "/api/{tenant}/dados_cobranca/{participante}".format(
                tenant=tenant, participante=participante)

        response = requests.get(url)
        response.raise_for_status()
        return ObjetosUtils().dictToObject(json.loads(response.text), Dados_Cobranca)

    def notifica_erro_um_documento(self, dados: dict):
        doc = dados[0]
        if doc["erro_msg"] != None:
            raise Exception(doc["erro_msg"])

    def recuperar_impostos_diario(self, imposto: ItemDocumentoTipoImposto, tenant: int, ano, mes):
        return DiarioUnicoFactory.getDiarioUnicoService().get_imposto_acumulado_aquisicao_servico(
            imposto,
            ano,
            mes,
            tenant
        )

    def recuperar_ultimo_trimestre(self, tenant: int, dados: dict, data: datetime.date, entidade_negocio: str, tipo_documento: int, item_codigo: str = None) -> List[ValoresAnteriores]:
        valores_anteriores = list()

        if (dados["heuristica_valor"] == HeuristicaProjecao.MEDIA_MOVEL.value):
            tres_meses_atras = data.replace(
                day=dados["dia_vencimento"]) - relativedelta.relativedelta(months=3)

            # "Informacoes_A_Recuperar"
            informacoes = list()
            info = InformacoesARecuperar()
            info.entidade = entidade_negocio
            info.campos = ["valor"]
            informacoes.append(info)

            filtro = Filtro()
            filtro.operacao = "And"
            filtro.parametros = list()
            filtro2 = Filtro()
            filtro2.operacao = "Entre"
            filtro2.entidade = entidade_negocio
            filtro2.campo = "data_lancamento"
            filtro2.parametros = [tres_meses_atras, data]
            filtro.parametros.append(filtro2)

            filtro3 = Filtro()
            filtro3.operacao = "Igual"
            filtro3.entidade = entidade_negocio
            filtro3.campo = "estabelecimento"
            filtro3.parametros = [dados["estabelecimento"]]
            filtro.parametros.append(filtro3)

            filtro4 = Filtro()
            filtro4.operacao = "Igual"
            filtro4.entidade = entidade_negocio
            filtro4.campo = "tipo"
            filtro4.parametros = [tipo_documento]
            filtro.parametros.append(filtro4)

            if item_codigo != None:
                filtro5 = Filtro()
                filtro5.operacao = "Igual"
                filtro5.entidade = "Item"
                filtro5.campo = "codigo"
                filtro5.parametros = [str(item_codigo)]
                filtro.parametros.append(filtro5)

            valores = DiarioUnicoFactory.getDocumentoService(
            ).listarDocumentos(filtro, informacoes, tenant)

            for val in valores:
                valor_anterior = ValoresAnteriores()
                valor_anterior.valor = val["valor"]
                valores_anteriores.append(valor_anterior)

        return valores_anteriores


    def recuperar_documentos_por_estabelecimento_tipo_data(self, tenant: int, estabelecimento: str, data_inicial: datetime.date, data_final: datetime.date, tipo_documento: int):
        from  diario_unico.services.query_service import QueryEnum   
        informacoes = list()
        for entidade in QueryEnum.camposcorrespondentes.keys():
            info = InformacoesARecuperar()
            info.entidade = entidade
            info.campos = QueryEnum.camposcorrespondentes[entidade].keys()
            informacoes.append(info)

        filtro = Filtro()
        filtro.operacao = "And"
        filtro.parametros = list()
        filtro2 = Filtro()
        filtro2.operacao = "Entre"
        filtro2.entidade = "Documento"
        filtro2.campo = "data_lancamento"
        filtro2.parametros = [data_inicial, data_final]
        filtro.parametros.append(filtro2)

        filtro3 = Filtro()
        filtro3.operacao = "Igual"
        filtro3.entidade = "Documento"
        filtro3.campo = "estabelecimento"
        filtro3.parametros = [estabelecimento]
        filtro.parametros.append(filtro3)

        filtro4 = Filtro()
        filtro4.operacao = "Igual"
        filtro4.entidade = "Documento"
        filtro4.campo = "tipo"
        filtro4.parametros = [tipo_documento]
        filtro.parametros.append(filtro4)            

        return DiarioUnicoFactory.getDocumentoService(
        ).listarDocumentos(filtro, informacoes, tenant)

    def cadastrarPessoa(self, cpf_cnpj, nome, tenant):
        return DiarioUnicoFactory.getDocumentoService(
                ).cadastrarPessoa( cpf_cnpj, nome, tenant)

    