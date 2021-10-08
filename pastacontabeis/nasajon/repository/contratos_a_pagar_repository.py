from django.db import connection, transaction
from nasajon.entity.contrato_a_pagar import ContratoAPagar
from nasajon.util.objeto_util import ObjetosUtils
from typing import List
from nasajon.util.cursor_util import CursorUtil
from nasajon.util.json_util import JsonUtil

class ContratosAPagarRepository:
    def getContratoAPagar(self, tenant, contrato) -> ContratoAPagar:
        sql = """select contrato, codigo, tipo, codigo_transacao, estabelecimento, fornecedor,
                        tenant, heuristica_valor, valor, dia_vencimento, dia_apropriacao
                from contratos_pagamentos.contrato
                where codigo=%s and tenant=%s
                """
        cursor = connection.cursor()
        cursor.execute(sql, [contrato,tenant])
        result = CursorUtil.fetchone(cursor)
        if (result==None):
            raise Exception("Contrato nao encontrado:"+contrato)
        return ObjetosUtils().dictToObject(result,ContratoAPagar)
