from django.db import connection, transaction
from nasajon.util.objeto_util import ObjetosUtils
from nasajon.entity.contrato_a_receber import ContratoReceber, ParticipantesContratoReceber, ItemContratoReceber
from typing import List


class ContratoAReceberRepository:

    def getContratoAReceberDoParticipante(self, tenant, contrato, participante) -> ContratoReceber:
        sql = """select contrato, codigo, tipo, tenant, pasta_contabil
                from faturamento.contrato
                where codigo=%s and tenant=%s
                """
        cursor = connection.cursor()
        cursor.execute(sql, [contrato, tenant])
        result = cursor.fetchone()
        if (result == None):
            raise Exception("Contrato nao encontrado:"+contrato)
        contrato: ContratoReceber = ObjetosUtils().dictToObject(result, ContratoReceber)

        sql = """select participante, participacao, dia_processamento, dia_vencimento
                from faturamento.contrato_participante
                where contrato=%s
                """
        cursor = connection.cursor()
        cursor.execute(sql, [contrato])
        result = cursor.fetchone()
        if (result == None):
            raise Exception(
                "Participante nao participante do contrato:"+participante)
        participante: ParticipantesContratoReceber = ObjetosUtils(
        ).dictToObject(result, ParticipantesContratoReceber)
        contrato.participantes.append(participante)

        sql = """select item_contrato, contrato, valor, tenant, heuristica_valor, codigo
                from faturamento.item_contrato
                where contrato=%s
                """
        cursor = connection.cursor()
        cursor.execute(sql, [contrato])
        for result in cursor.fetchall():
            item: ItemContratoReceber = ObjetosUtils().dictToObject(result, ItemContratoReceber)
            contrato.participantes.append(item)
        return contrato
