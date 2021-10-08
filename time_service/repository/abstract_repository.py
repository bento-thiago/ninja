from typing import List
from django.db import connections, transaction, connection
from nasajon.util.cursor_util import CursorUtil
from enum import Enum


class AbstractRepository:
    def __init__(self):
        self.alias_banco = "default"
        self.__con = connections[self.alias_banco]

    def set_connection(self, connection):
        self.__con = connection

    def begin(self):
        transaction.set_autocommit(False, using=self.alias_banco)

    def commit(self):
        transaction.commit(using=self.alias_banco)
        transaction.set_autocommit(True, using=self.alias_banco)

    def rollback(self):
        transaction.rollback(using=self.alias_banco)
        transaction.set_autocommit(True, using=self.alias_banco)

    def execute(self, sql: str, params: dict):
        with self.__con.cursor() as cursor:
            self.__execute_retornando_cursor(sql, params, cursor)

    def fetchAll(self, sql: str, params: dict) -> List[dict]:
        with self.__con.cursor() as cursor:
            self.__execute_retornando_cursor(sql, params, cursor)
            retorno = CursorUtil().fetchall(cursor)
        return retorno

    def fetchOne(self, sql: str, params: dict) -> List[dict]:
        with self.__con.cursor() as cursor:
            self.__execute_retornando_cursor(sql, params, cursor)
            retorno = CursorUtil().fetchone(cursor)
        return retorno

    def __execute_retornando_cursor(self, sql: str, params: dict, cursor):

        from sqlparams import SQLParams
        if not isinstance(params, dict):
            params = params.__dict__
        sql2, params2 = SQLParams('named', 'format').format(sql, params)
        params2 = [elem.value if isinstance(
            elem, Enum) else elem for elem in params2]
        cursor.execute(sql2, params2)
        return cursor
