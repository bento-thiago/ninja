from __future__ import absolute_import, unicode_literals
import re

from celery import shared_task

from nasajon.pastas_contabeis.abstract_pasta_contabil import AbstractPastaContabil
from nasajon.pastas_contabeis.pastas_router import MomentoContabil
from nasajon.pastas_contabeis.pastas_router import apropriar as task_apropriar_e_antecipar

from nasajon.entity.dados_escrituracao_futura import DadosEscrituracaoFutura, DadosItem
from diario_unico.entity.documento import Documento
from diario_unico.enum.sinal import Sinal


from nasajon.pastas_contabeis.pastas_router import get_pasta_obj

from nasajon.repository.contratos_a_receber_repository import ContratoAReceberRepository
from nasajon.repository.contratos_a_pagar_repository import ContratosAPagarRepository

from nasajon.util.diario_util import DiarioUtil
from nasajon.util.json_util import JsonUtil


class PastaRecorrente(AbstractPastaContabil):

    def __init__(self, diario_util: DiarioUtil):
        super().__init__(diario_util)

    def notificar(self, id_pasta: str, momento: MomentoContabil, dados: dict, id_log_assincrono: str, tentativa: int):
        if (MomentoContabil(momento) == MomentoContabil.APROPRIACAO):
            task_apropriar_e_antecipar.delay(
                id_pasta, JsonUtil().toDict(self.get_dados_apropriacao(dados)), id_log_assincrono, tentativa)
        else:
            super().notificar(id_pasta, momento, dados, id_log_assincrono, tentativa)

    def documento_para_dados_escrituracao_futura(self, documento: Documento, dados: dict):

        # Contratos a Receber
        if (documento.sinal == Sinal.SAIDA):
            # TODO Refatorar abaixo para usar um service, e não um repository diretamente
            contrato = ContratoAReceberRepository().getContratoAReceberDoParticipante(
                dados["tenant"], documento.identificador_contrato, documento.participante)
            saida = DadosEscrituracaoFutura()
            saida.dia_apropriacao = contrato.participantes[0].dia_processamento
            saida.dia_vencimento = contrato.participantes[0].dia_vencimento
            saida.estabelecimento = documento.estabelecimento
            saida.participante = documento.participante
            saida.tenant = dados["tenant"]
            for _item in contrato.itens:
                item = DadosItem()
                item.codigo = _item.codigo
                item.heuristica_projecao = _item.heuristica_valor
                item.tipo = _item.codigo
                item.valor_medio_inicial = _item.valor
                saida.itens.append(item)

            return saida

        else:
            # Contrato a pagar
            # TODO Refatorar abaixo para usar um service, e não um repository diretamente
            contrato = ContratosAPagarRepository().getContratoAPagar(
                dados["tenant"], documento.identificador_contrato)
            saida = DadosEscrituracaoFutura()
            saida.dia_apropriacao = contrato.dia_apropriacao
            saida.dia_vencimento = contrato.dia_vencimento
            saida.estabelecimento = contrato.estabelecimento
            saida.participante = contrato.fornecedor
            saida.tenant = dados["tenant"]
            item = DadosItem()
            item.codigo = "1"
            item.heuristica_projecao = contrato.heuristica_valor
            item.tipo = contrato.tipo
            item.valor_medio_inicial = contrato.valor
            saida.itens.append(item)
            return saida
