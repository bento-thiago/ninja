from diario_unico.repository.abstract_repository import AbstractRepository
import uuid
from django.db import connections, transaction
from nasajon.util.cursor_util import CursorUtil
from diario_unico.entity.info_cobranca import InfoCobranca


class CobrancasRepository(AbstractRepository):
    # Insere a cobranca no banco
    def inserir(self, cobranca: InfoCobranca):
        # query do insert a ser feito
        sql = """insert into info_cobranca (info_cobranca, documento, juros_mensal, multa_atraso, desconto, texto_instrucao, numero, nosso_numero, id_externo, 
                    banco_numero, uuid_externo, url_boleto, linha_digitavel, tentativas_registro, vencimento, situacao, mensagem_erro, nome_cliente, cpf_cliente, 
                    endereco_logradouro, endereco_numero, endereco_complemento, endereco_bairro, endereco_cidade, endereco_estado, endereco_cep, tenant)
             values ( :id_cobranca,:id_documento,:juros_mensal,:multa_atraso,:desconto,:texto_instrucao,:numero,:nosso_numero,
                        :id_externo,:banco_numero,:uuid_externo,:url_boleto,:linha_digitavel,:tentativas_registro,:vencimento,
                        :situacao,:mensagem_erro,:nome_cliente,:cpf_cliente,:endereco_logradouro,:endereco_numero,:endereco_complemento,
                        :endereco_bairro,:endereco_cidade,:endereco_estado,:endereco_cep,:tenant)"""
        # Gerando o ID
        cobranca.id_cobranca = uuid.uuid4()

        # Executa a query
        params = cobranca.__dict__
        self.execute(sql, params)

        # Retornando o resultado:
        result = {'id_cobranca': str(cobranca.id_cobranca)}

        return result

    # Coleta as cobrancas do tenant, podendo filtrar por situacao e vencimento
    def listar(self, tenant, situacao, vencimento_apos):
        # Monta query do select para listagem
        sql = "select ic.info_cobranca as id_cobranca, ic.documento as id_documento, SUM(du.valor) as valor, ic.juros_mensal, ic.multa_atraso, ic.desconto, ic.texto_instrucao, ic.numero, ic.nosso_numero, d.codigo_barras, ic.vencimento, ic.situacao, ic.mensagem_erro, p.codigo as estabelecimento, " \
            "ic.id_externo, ic.banco_numero, ic.url_boleto, ic.linha_digitavel, ic.tentativas_registro, ic.nome_cliente, ic.cpf_cliente, ic.endereco_logradouro, ic.endereco_numero, ic.endereco_complemento, ic.endereco_bairro, ic.endereco_cidade, ic.endereco_estado, ic.endereco_cep " \
            "from info_cobranca as ic "\
            "left join documento as d on ic.documento = d.documento " \
            "left join diario_unico as du on ic.info_cobranca = du.info_cobranca " \
            "left join pessoas as p on d.estabelecimento = p.pessoa " \
            "where ic.tenant = :tenant "

        params = dict()
        params["tenant"] = tenant

        # Adiciona filtro por situação se houver
        if situacao != None:
            sql += "and ic.situacao = :situacao "
            params["situacao"] = situacao

        # Adiciona filtro por para depois do vencimento se houver
        if vencimento_apos != None:
            sql += "and ic.vencimento >= :vencimento "
            params["vencimento"] = vencimento_apos

        sql += 'group by ic.info_cobranca, ic.documento, ic.juros_mensal, ic.multa_atraso, ic.desconto, ic.texto_instrucao,'\
            'ic.numero, ic.nosso_numero, ic.id_externo, ic.banco_numero,'\
            'ic.url_boleto, ic.linha_digitavel, ic.tentativas_registro, ic.vencimento,'\
            'ic.situacao, ic.mensagem_erro, d.codigo_barras, ic.nome_cliente, ic.cpf_cliente, ic.endereco_logradouro,'\
            'ic.endereco_numero, ic.endereco_complemento, ic.endereco_bairro, ic.endereco_cidade, ic.endereco_estado, ic.endereco_cep, p.codigo'

        # Executa a query
        result = self.fetchAll(sql, params)

        return result

    # Coleta a cobranca a partir do id do documento
    def getByIdDocumento(self, tenant, id_documento):
        # Monta query do select para listagem
        sql = "select ic.info_cobranca as id_cobranca, ic.documento as id_documento, SUM(du.valor) as valor, ic.juros_mensal, ic.multa_atraso, ic.desconto, ic.texto_instrucao, ic.numero, ic.nosso_numero, d.codigo_barras, ic.vencimento, ic.situacao, ic.mensagem_erro, p.codigo as estabelecimento, p.nomefantasia as condominio," \
            "ic.id_externo, ic.banco_numero, ic.url_boleto, ic.linha_digitavel, ic.tentativas_registro, ic.nome_cliente, ic.cpf_cliente, ic.endereco_logradouro, ic.endereco_numero, ic.endereco_complemento, ic.endereco_bairro, ic.endereco_cidade, ic.endereco_estado, ic.endereco_cep, p2.email, ic.cpf_cliente as participante, ic.tenant " \
            "from info_cobranca as ic "\
            "left join documento as d on ic.documento = d.documento " \
            "left join diario_unico as du on ic.info_cobranca = du.info_cobranca " \
            "left join pessoas as p on d.estabelecimento = p.pessoa " \
            "left join pessoas as p2 on d.participante = p2.pessoa " \
            "where ic.tenant = :tenant and ic.documento = :id_documento " \
            'group by ic.info_cobranca, ic.documento, ic.juros_mensal, ic.multa_atraso, ic.desconto, ic.texto_instrucao,'\
            'ic.numero, ic.nosso_numero, ic.id_externo, ic.banco_numero,'\
            'ic.url_boleto, ic.linha_digitavel, ic.tentativas_registro, ic.vencimento,'\
            'ic.situacao, ic.mensagem_erro, d.codigo_barras, ic.nome_cliente, ic.cpf_cliente, ic.endereco_logradouro,'\
            'ic.endereco_numero, ic.endereco_complemento, ic.endereco_bairro, ic.endereco_cidade, ic.endereco_estado, ic.endereco_cep, p.codigo, p2.email, p.nomefantasia'

        # Executa a query
        params = dict()
        params["tenant"] = tenant
        params["id_documento"] = id_documento
        result = self.fetchOne(sql, params)

        return result

    # Atualiza a cobranca no banco
    def atualizar(self, cobranca: InfoCobranca):
        # query do insert a ser feito
        sql = """update info_cobranca set documento=:id_documento, juros_mensal=juros_mensal, multa_atraso=multa_atraso, desconto=desconto, 
                    texto_instrucao=:texto_instrucao,numero=:numero,nosso_numero=:nosso_numero, id_externo=:id_externo, banco_numero=:banco_numero,
                    uuid_externo=:uuid_externo, url_boleto=:url_boleto,linha_digitavel=:linha_digitavel, tentativas_registro=tentativas_registro, 
                    vencimento=:vencimento,situacao=:situacao, mensagem_erro=:mensagem_erro, nome_cliente=:nome_cliente, cpf_cliente=:cpf_cliente,
                    endereco_logradouro=:endereco_logradouro, endereco_numero=:endereco_numero, endereco_complemento=:endereco_complemento,
                    endereco_bairro=:endereco_bairro, endereco_cidade=:endereco_cidade,endereco_estado=:endereco_estado,endereco_cep=:endereco_cep 
                where info_cobranca=:id_cobranca and tenant=:tenant"""

        params = cobranca.__dict__
        self.execute(sql, params)

    # Coleta a cobranca a partir do id do documento

    def getDadosCobranca(self, tenant, cpf_cnpj_pessoa):
        # Monta query do select para listagem
        sql = 'select p.pessoa, p.descricao as nome, p.cpf_cnpj, end.cidade, end.bairro, end.cep, end.tipologradouro, end.logradouro, ' \
            'end.numero, end.complemento, end.estado '\
            'from pessoas p '\
            'left join enderecos end on end.pessoa=p.pessoa '\
            'where p.tenant=:tenant and p.cpf_cnpj=:cpf_cnpj '\
            'order by end.cobranca desc '\
            'limit 1'

        # Executa a query
        params = dict()
        params["tenant"] = tenant
        params["cpf_cnpj"] = cpf_cnpj_pessoa

        # Retornando o resultado:
        return self.fetchOne(sql, params)
