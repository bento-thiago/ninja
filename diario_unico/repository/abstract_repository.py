import datetime
from enum import Enum
from typing import List

from django.db import connections, transaction

from nasajon.util.cursor_util import CursorUtil
from nasajon.util.repetir_exception import RepetirException


class AbstractRepository:
    def __init__(self, alias_banco: str = "default"):
        self.alias_banco = alias_banco
        self.__con = connections[self.alias_banco]

    def set_connection(self, connection):
        self.__con = connection

    def begin(self):
        transaction.set_autocommit(False, using=self.alias_banco)
        return

    def commit(self):
        transaction.commit(using=self.alias_banco)
        transaction.set_autocommit(True, using=self.alias_banco)

    def em_transacao(self):
        return not transaction.get_autocommit(using=self.alias_banco)

    def rollback(self):
        transaction.rollback(using=self.alias_banco)
        transaction.set_autocommit(True, using=self.alias_banco)

    def execute(self, sql: str, params: dict):
        try:
            cursor = None
            try:
                cursor = self.__con.cursor()
            except Exception as err:
                raise RepetirException(err)
            self.__execute_retornando_cursor(sql, params, cursor)
        finally:
            if cursor != None:
                cursor.close()

    def executeMany(self, sql: str, params: List[dict]):
        try:
            cursor = None
            try:
                cursor = self.__con.cursor()
            except Exception as err:
                raise RepetirException(err)
            self.__execute_many_retornando_cursor(sql, params, cursor)
        finally:
            if cursor != None:
                cursor.close()

    def fetchAll(self, sql: str, params: dict) -> List[dict]:
        try:
            cursor = None
            try:
                cursor = self.__con.cursor()
            except Exception as err:
                raise RepetirException(err)

            self.__execute_retornando_cursor(sql, params, cursor)
            retorno = CursorUtil().fetchall(cursor)
        finally:
            if cursor != None:
                cursor.close()

        return retorno

    def fetchOne(self, sql: str, params: dict) -> dict:
        try:
            cursor = None
            try:
                cursor = self.__con.cursor()
            except Exception as err:
                raise RepetirException(err)

            self.__execute_retornando_cursor(sql, params, cursor)
            retorno = CursorUtil().fetchone(cursor)
        finally:
            if cursor != None:
                cursor.close()

        return retorno

    def __execute_retornando_cursor(self, sql: str, params: dict, cursor):

        from sqlparams import SQLParams
        if not isinstance(params, dict):
            params = params.__dict__
        sql2, params2 = SQLParams('named', 'format').format(sql, params)
        params3 = list()
        for elem in params2:
            if isinstance(elem, Enum):
                params3.append(elem.value)
            elif isinstance(elem, str):
                try:
                    val = datetime.datetime.strptime(elem, '%d/%m/%Y').date()
                except:
                    try:
                        val = datetime.datetime.strptime(elem, '%d/%m/%Y %H:%M:%S')
                    except:
                        try:
                            val = datetime.datetime.strptime(elem, '%Y-%m-%dT%H:%M:%S')
                        except:
                            val = elem
                params3.append(val)
            else:
                params3.append(elem)

        cursor.execute(sql2, params3)
        return cursor

    def __execute_many_retornando_cursor(self, sql: str, params: List[dict], cursor):

        from sqlparams import SQLParams
        for i in range(len(params)):
            parametro = params[i]
            if not isinstance(parametro, dict):
                parametro = parametro.__dict__
            sql2, params2 = SQLParams('named', 'format').format(sql, parametro)
            params3 = list()
            for elem in params2:
                if isinstance(elem, Enum):
                    params3.append(elem.value)
                elif isinstance(elem, str):
                    try:
                        val = datetime.datetime.strptime(elem, '%d/%m/%Y').date()
                    except:
                        try:
                            val = datetime.datetime.strptime(elem, '%d/%m/%Y %H:%M:%S')
                        except:
                            try:
                                val = datetime.datetime.strptime(elem, '%Y-%m-%dT%H:%M:%S')
                            except:
                                val = elem
                    params3.append(val)
                else:
                    params3.append(elem)
            params[i] = params3


        cursor.executemany(sql2, params)
        return cursor
