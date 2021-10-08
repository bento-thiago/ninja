from datetime import datetime
from django.db import connection, transaction

class JobsUtil:
    def registra_log(self, tenant:int, identificador_compromisso:str, participante:str, estabelecimento:str,
                    pasta_contabil:str, momento:str, etapa:str, referencia:str):
        sql = """ insert into log_auxiliar_job (tenant, identificador_compromisso, participante,
                                                estabelecimento, pasta_contabil, momento, etapa, referencia)
                                values (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = connection.cursor()
        cursor.execute(sql, [tenant, identificador_compromisso, participante, estabelecimento, pasta_contabil,momento, etapa, referencia ])
