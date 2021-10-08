from diario_unico.repository.abstract_repository import AbstractRepository
import uuid
from django.db import connections, transaction
from nasajon.util.cursor_util import CursorUtil
from diario_unico.entity.info_pagamento import InfoPagamento


class PagamentosRepository(AbstractRepository):
    # Insere o pagamento no banco
    def inserir(self, pagamento: InfoPagamento):
        # query do insert a ser feito
        sql = """insert into info_pagamento (info_pagamento,documento,id_operacao,vencimento,mensagem_erro,situacao,tenant) 
                    values (:id_pagamento,:documento,:id_operacao,:vencimento,:mensagem_erro,:situacao,:tenant)"""

        # Gerando o ID
        pagamento.id_pagamento = uuid.uuid4()

        # Executa a query
        params = pagamento.__dict__
        self.execute(sql, params)

        # Retornando o resultado:
        result = {'id_pagamento': str(pagamento.id_pagamento)}

        return result

    # Coleta os pagamentos do tenant, podendo filtrar por situacao
    def listar(self, tenant, situacao):
        # Monta query do select para listagem
        sql = "select ip.info_pagamento as id_pagamento, ip.documento as id_documento, SUM(du.valor) as valor, d.codigo_barras, ip.vencimento, ip.id_operacao, ip.situacao, ip.mensagem_erro " \
            "from info_pagamento as ip "\
            "left join documento as d on ip.documento = d.documento " \
            "left join diario_unico as du on ip.info_pagamento = du.info_pagamento " \
            "where ip.tenant = :tenant "

        params = dict()
        params["tenant"] = tenant

        # Adiciona filtro por situação se houver
        if situacao != None:
            sql += "and ip.situacao = :situacao "
            params["situacao"] = situacao

        sql += "group by ip.info_pagamento, ip.documento, d.codigo_barras, ip.vencimento, ip.id_operacao, ip.situacao, ip.mensagem_erro"

        # Retornando o resultado:
        result = self.fetchAll(sql, params)

        return result

    # Coleta o pagamento a partir do id de operacao
    def getPagamentoOperacao(self, tenant, id_operacao):
        # Monta query do select para listagem
        sql = "select ip.info_pagamento as id_pagamento, ip.documento as id_documento, SUM(du.valor) as valor, d.codigo_barras, ip.vencimento, ip.id_operacao, ip.situacao, ip.mensagem_erro, ip.tenant " \
            "from info_pagamento as ip "\
            "left join documento as d on ip.documento = d.documento " \
            "left join diario_unico as du on ip.info_pagamento = du.info_pagamento " \
            "where ip.tenant = :tenant " \
            "and  ip.id_operacao = :id_operacao " \
            "group by ip.info_pagamento, ip.documento, d.codigo_barras, ip.vencimento, ip.id_operacao, ip.situacao, ip.mensagem_erro, ip.tenant"

        params = dict()
        params["tenant"] = tenant
        params["id_operacao"] = id_operacao

        # Retornando o resultado:
        result = self.fetchOne(sql, params)

        return result

    # Atualiza o pagamento no banco
    def atualizar(self, pagamento: InfoPagamento):
        # query do insert a ser feito
        sql = "update info_pagamento set situacao=:situacao, id_operacao=:id_operacao, mensagem_erro=:mensagem_erro where info_pagamento=:info_pagamento and tenant=:tenant"

        params = dict()
        params["situacao"] = pagamento.situacao
        params["id_operacao"] = pagamento.id_operacao
        params["mensagem_erro"] = pagamento.mensagem_erro
        params["info_pagamento"] = pagamento.id_pagamento
        params["tenant"] = pagamento.tenant

        # Executa a query
        self.execute(sql, params)
