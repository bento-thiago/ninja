from nasajon.repository.abstract_repository import AbstractRepository
from nasajon.entity.log_assincrono import LogAssincrono
import datetime
import uuid


class LogAssincronoRepository(AbstractRepository):
    # Insere uma requisição no banco
    def inserir(self, log_assincrono: LogAssincrono):
        # query do insert a ser feito
        sql = """insert into util.log_assincrono (token, datahora, recurso, status, tenant)
             values ( :token,:datahora,:recurso,:status, :tenant)"""

        # Executa a query
        params = dict()
        params["token"] = log_assincrono.token
        params["datahora"] = datetime.datetime.now()
        params["recurso"] = log_assincrono.recurso
        params["status"] = log_assincrono.status
        params["tenant"] = log_assincrono.tenant

        self.execute(sql, params)

    # Atualiza uma requisição no banco
    def atualizar(self, log_assincrono: LogAssincrono):
        # query do insert a ser feito
        sql = """ update util.log_assincrono set datahora=:datahora,  recurso=:recurso, status=:status
             where token=:token"""

        # Executa a query
        params = dict()
        params["token"] = log_assincrono.token
        params["datahora"] = datetime.datetime.now()
        params["recurso"] = log_assincrono.recurso
        params["status"] = log_assincrono.status

        self.execute(sql, params)

    def getStatusLogAssincrono(self, token, tenant, recurso=None):
        # Monta query do select para listagem
        sql = 'select status '\
            'from util.log_assincrono '\
            'where token=:token '\
            'and tenant=:tenant'

        # Executa a query
        params = dict()
        params["token"] = token
        params["tenant"] = tenant

        if recurso != None:
            sql += ' and recurso=:recurso'
            params["recurso"] = recurso

        sql += ' order by datahora desc limit 1'

        # Retornando o resultado:

        result = self.fetchOne(sql, params)

        if result == None:
            status = None
        else:
            status = result["status"]

        return status
