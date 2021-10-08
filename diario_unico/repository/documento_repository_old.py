from diario_unico.entity.documento import Documento
from diario_unico.entity.info_pagamento import InfoPagamento
from diario_unico.entity.info_cobranca import InfoCobranca
from diario_unico.entity.lancamento import Lancamento
from diario_unico.repository.abstract_repository import AbstractRepository
from diario_unico.repository.util_repository import UtilRepository
from diario_unico.services.query_service import QueryService
from diario_unico.entity.item_documento import ItemDocumento
from diario_unico.entity.lancamento import Lancamento
from diario_unico.entity.partida import Partida
import uuid
from nasajon.util.log import Log


class DocumentoRepositoryOld(AbstractRepository):

    def __init__(self, util_repository: UtilRepository):
        super().__init__()
        self._util_repository = util_repository

    def documentoJaCadastrado(self, documento: Documento, tenant: int):
        sql = """select d.documento, d.situacao from documento d
                    where d.tipo=:tipo and d.tenant=:tenant and MONTH(d.data_lancamento)=:mes and YEAR(d.data_lancamento)=:ano and ((d.participante is null and :participante is null) or (d.participante=:participante)) and
                            d.estabelecimento=:estabelecimento"""

        params = dict()
        params["tipo"] = documento.tipo
        params["tenant"] = tenant
        params["mes"] = documento.data_lancamento.month
        params["ano"] = documento.data_lancamento.year
        params["participante"] = documento.participante
        params["estabelecimento"] = documento.estabelecimento

        result = self.fetchOne(sql, params)

        if (result != None):
            return result
        else:
            return None

    def listarDocumentos(self, filtro, informacoes_a_recuperar, tenant, dicionario: dict = dict()):
        queryService = QueryService()

        sql = "select documento.documento as documento___documento "

        # Obtem campos do header de documento e do diario unico solicitados
        campos_documento = queryService.recuperacamposSelectDocumento(
            informacoes_a_recuperar)
        campos_diario_unico = queryService.recuperacamposSelectDiarioUnico(
            informacoes_a_recuperar)

        if len(campos_documento) > 0:
            sql += "," + ", ".join(campos_documento)

        if len(campos_diario_unico) > 0:
            sql += "," + ", ".join(campos_diario_unico)

        sql += " from documento as documento "
        if (len(campos_diario_unico) > 0) or (queryService.filtroUsaDiarioUnico(filtro)):
            sql += " join diario_unico as diario_unico on diario_unico.documento=documento.documento "

        sql += ' where documento.tenant=:main___tenant and '

        sql_filtro, parametros_filtro = queryService.converteFiltroEmSQL(
            filtro, dicionario)
        sql += sql_filtro

        params = dict()
        params["main___tenant"] = tenant
        params.update(parametros_filtro)
        resultset = self.fetchAll(sql, params)
        return self.resultsetToDocumento(resultset)

    def resultsetToDocumento(self, resultset):
        mapaDocumentos = dict()
        saida = list()
        for linha in resultset:
            # =======DOCUMENTO===========

            if not linha['documento___documento'] in mapaDocumentos:
                mapaDocumentos[linha['documento___documento']] = Documento()
                saida.append(mapaDocumentos[linha['documento___documento']])

            documento: Documento = mapaDocumentos[linha['documento___documento']]
            documento.documento = (linha['documento___documento'])

            if 'documento___tipo' in linha:
                documento.tipo = (linha['documento___tipo'])

            if 'documento___numero' in linha:
                documento.numero = linha['documento___numero']

            if 'documento___ano' in linha:
                documento.ano = linha['documento___ano']

            if 'documento___sinal' in linha:
                documento.sinal = linha['documento___sinal']

            if 'documento___modelo' in linha:
                documento.modelo = linha['documento___modelo']

            if 'documento___data_lancamento' in linha:
                documento.data_lancamento = linha['documento___data_lancamento']

            if 'documento___emissao' in linha:
                documento.emissao = linha['documento___emissao']

            if 'documento___competencia_inicial' in linha:
                documento.competencia_inicial = linha['documento___competencia_inicial']

            if 'documento___competencia_final' in linha:
                documento.competencia_final = linha['documento___competencia_final']

            if 'documento___cfop' in linha:
                documento.cfop = linha['documento___cfop']

            if 'documento___situacao' in linha:
                documento.situacao = linha['documento___situacao']

            if 'documento___valor' in linha:
                documento.valor = linha['documento___valor']

            if 'documento___data_entrada' in linha:
                documento.data_entrada = linha['documento___data_entrada']

            if 'documento___tipo_ligacao' in linha:
                documento.tipo_ligacao = linha['documento___tipo_ligacao']

            if 'documento___origem' in linha:
                documento.origem = linha['documento___origem']

            if 'documento___codigo_consumo' in linha:
                documento.codigo_consumo = linha['documento___codigo_consumo']

            if 'documento___serie' in linha:
                documento.serie = linha['documento___serie']

            if 'documento___subserie' in linha:
                documento.subserie = linha['documento___subserie']

            if 'documento___grupo_tensao' in linha:
                documento.grupo_tensao = linha['documento___grupo_tensao']

            if 'documento___estabelecimento' in linha:
                documento.estabelecimento = linha['documento___estabelecimento']

            if 'documento___empresa' in linha:
                documento.empresa = linha['documento___empresa']

            if 'documento___grupo_empresarial' in linha:
                documento.grupo_empresarial = linha['documento___grupo_empresarial']

            if 'documento___participante' in linha:
                documento.participante = linha['documento___participante']

            if 'documento___usuario' in linha:
                documento.usuario = linha['documento___usuario']

            if 'documento___codigo_barras' in linha:
                documento.codigo_barras = linha['documento___codigo_barras']

            if 'documento___serie' in linha:
                documento.serie = linha['documento___serie']

            if 'documento___url_documento' in linha:
                documento.url_documento = linha['documento___url_documento']

            if 'documento___data_criacao' in linha:
                documento.data_criacao = linha['documento___data_criacao']

            if 'documento___codigo_transacao' in linha:
                documento.codigo_transacao = linha['documento___codigo_transacao']

            if 'documento___identificador_contrato' in linha:
                documento.identificadorContrato = linha['documento___identificador_contrato']

            # =======ITEM===========
            # verifica se item já está cadastrado
            if (not 'diario_unico___item_documento' in linha) or (linha['diario_unico___item_documento'] == None) or (linha['diario_unico___item_documento'] == 0):
                continue

            item = None
            for itemLoop in documento.itens:
                if itemLoop.item_documento == linha['diario_unico___item_documento']:
                    item = itemLoop
                    continue

            if (item == None):
                item = ItemDocumento()

                documento.itens.append(item)

            item.item_documento = linha['diario_unico___item_documento']
            item.documento = documento.documento

            if 'diario_unico___codigo' in linha:
                item.codigo = linha['diario_unico___codigo']

            if 'diario_unico___descricao' in linha:
                item.descricao = linha['diario_unico___descricao']

            if 'diario_unico___diario_unico_tipo' in linha:
                item.tipo = linha['diario_unico___diario_unico_tipo']
            
            if 'diario_unico___rubrica' in linha:
                item.rubrica = linha['diario_unico___rubrica']
            
            if 'diario_unico___rubrica_esocial' in linha:
                item.rubrica_esocial = linha['diario_unico___rubrica_esocial']
            
            if 'diario_unico___trabalhador' in linha:
                item.trabalhador = linha['diario_unico___trabalhador']
            
            if 'diario_unico___departamento' in linha:
                item.departamento = linha['diario_unico___departamento']

            if 'diario_unico___lotacao' in linha:
                item.lotacao = linha['diario_unico___lotacao']

            # =======Lancamento===========
            # verifica se lancamento já está na lista
            if (not 'diario_unico___numero_lancamento' in linha) or (linha['diario_unico___numero_lancamento'] == None) or (linha['diario_unico___numero_lancamento'] == 0):
                continue

            lancamento = None
            for lancamentoLoop in item.lancamentos:
                if (lancamentoLoop.numero == linha['diario_unico___numero_lancamento']):
                    lancamento = lancamentoLoop
                    continue

            if (lancamento == None):
                lancamento = Lancamento()
                item.lancamentos.append(lancamento)

            lancamento.numero = (linha['diario_unico___numero_lancamento'])

            lancamento.data = linha['diario_unico___data']
            lancamento.situacao = linha['diario_unico___situacao']

            partida = Partida()
            if 'diario_unico___ordem_lancamento' in linha:
                partida.ordem = (linha['diario_unico___ordem_lancamento'])

            if 'diario_unico___conta_contabil' in linha:
                partida.conta_contabil = (
                    linha['diario_unico___conta_contabil'])

            if 'diario_unico___historico_lancamento' in linha:
                partida.historico = (
                    linha['diario_unico___historico_lancamento'])

            if 'diario_unico___valor' in linha:
                partida.valor = (linha['diario_unico___valor'])

            if 'diario_unico___definicao_lancamento' in linha:
                partida.definicao = (
                    linha['diario_unico___definicao_lancamento'])

            if 'diario_unico___natureza_lancamento' in linha:
                partida.natureza = (
                    linha['diario_unico___natureza_lancamento'])

            lancamento.partidas.append(partida)

        return saida

    def insereDocumento(self, documento: Documento, tenant: int):
        sql = """
            insert into documento(
            documento, 
            tipo,  
            numero, 
            ano, 
            sinal, 
            modelo, 
            data_lancamento, 
            emissao, 
            competencia_inicial, 
            competencia_final, 
            cfop, 
            situacao, 
            valor, 
            data_entrada, 
            tipo_ligacao, 
            grupo_tensao, 
            origem, 
            codigo_consumo, 
            serie, 
            subserie, 
            estabelecimento, 
            empresa, 
            grupo_empresarial, 
            participante, 
            codigo_barras, 
            usuario, 
            url_documento, 
            data_criacao, 
            identificador_contrato, 
            tenant) 
        values (
            :documento, 
            :tipo,  
            :numero, 
            :ano, 
            :sinal, 
            :modelo, 
            :data_lancamento, 
            :emissao, 
            :competencia_inicial, 
            :competencia_final, 
            :cfop, 
            :situacao, 
            :valor, 
            :data_entrada, 
            :tipo_ligacao, 
            :grupo_tensao, 
            :origem, 
            :codigo_consumo, 
            :serie, 
            :subserie, 
            :estabelecimento, 
            :empresa, 
            :grupo_empresarial, 
            :participante, 
            :codigo_barras, 
            :usuario, 
            :url_documento, 
            :data_criacao, 
            :identificador_contrato, 
            :tenant)
        """

        params = dict()
        params["documento"] = documento.documento
        params["tipo"] = documento.tipo
        params["numero"] = documento.numero
        params["ano"] = documento.ano
        params["sinal"] = documento.sinal
        params["modelo"] = documento.modelo
        params["data_lancamento"] = documento.data_lancamento
        params["emissao"] = documento.emissao
        params["competencia_inicial"] = documento.competencia_inicial
        params["competencia_final"] = documento.competencia_final
        params["cfop"] = documento.cfop
        params["situacao"] = documento.situacao
        params["valor"] = documento.valor
        params["data_entrada"] = documento.data_entrada
        params["tipo_ligacao"] = documento.tipo_ligacao
        params["grupo_tensao"] = documento.grupo_tensao
        params["origem"] = documento.origem
        params["codigo_consumo"] = documento.codigo_consumo
        params["serie"] = documento.serie
        params["subserie"] = documento.subserie
        params["estabelecimento"] = documento.estabelecimento
        params["empresa"] = documento.empresa
        params["grupo_empresarial"] = documento.grupo_empresarial
        params["participante"] = documento.participante
        params["codigo_barras"] = documento.codigo_barras
        params["usuario"] = documento.usuario
        params["url_documento"] = documento.url_documento
        params["data_criacao"] = documento.data_criacao
        params["identificador_contrato"] = documento.identificador_contrato
        params["tenant"] = tenant
        self.execute(sql, params)

    def inserir_ou_atualizarInfoPagamento(self, info_pagamento: InfoPagamento, id_documento: str, tenant: int):
        if self.possuiInfoPagamento(id_documento, tenant):
            self.atualizarInfoPagamento(id_documento, info_pagamento, tenant)
        else:
            self.insereInfoPagamento(info_pagamento, id_documento, tenant)

    def possuiInfoPagamento(self, id_documento, tenant):
        sql = 'select 1 from info_pagamento where documento=:documento and tenant=:tenant'
        params = dict()
        params['documento'] = id_documento
        params['tenant'] = tenant
        if (self.fetchOne(sql, params) != None):
            return True
        else:
            return False

    def atualizarInfoPagamento(self, id_documento: str, info_pagamento: InfoPagamento, tenant: int):
        sql = 'update info_pagamento set tenant=tenant'
        params = dict()
        if info_pagamento.vencimento != None:
            params['vencimento'] = info_pagamento.vencimento
            sql = sql + ", vencimento=:vencimento"

        if info_pagamento.mensagem_erro != None:
            params['mensagem_erro'] = info_pagamento.mensagem_erro
            sql = sql + ', mensagem_erro=:mensagem_erro'

        if info_pagamento.situacao != None:
            params['situacao'] = info_pagamento.situacao
            sql = sql + ', situacao=:situacao'

        sql = sql + ' where documento=:documento and tenant=:tenant'
        params['documento'] = id_documento
        params["tenant"] = tenant
        self.execute(sql, params)

    def insereInfoPagamento(self, info_pagamento: InfoPagamento, id_documento: str, tenant: int):
        sql = """insert into info_pagamento (info_pagamento, vencimento, mensagem_erro, situacao, tenant, documento)
                values (:info_pagamento, :vencimento, :mensagem_erro, :situacao, :tenant, :documento)"""
        params = dict()
        params['info_pagamento'] = str(uuid.uuid4())
        if info_pagamento.vencimento != None:
            params['vencimento'] = info_pagamento.vencimento
        else:
            params['vencimento'] = None
        if info_pagamento.mensagem_erro != None:
            params['mensagem_erro'] = info_pagamento.mensagem_erro
        else:
            params['mensagem_erro'] = None
        if info_pagamento.situacao != None:
            params['situacao'] = info_pagamento.situacao
        else:
            params['situacao'] = None
        params["tenant"] = tenant
        params["documento"] = id_documento

        self.execute(sql, params)

        return params["info_pagamento"]

    def inserir_ou_atualizarInfoCobranca(self, info_cobranca: InfoCobranca, id_documento: str, tenant: int):
        if self.possuiInfoCobranca(id_documento, tenant):
            self.atualizarInfoCobranca(id_documento, info_cobranca, tenant)
        else:
            self.insereInfoCobranca(info_cobranca, id_documento, tenant)

    def possuiInfoCobranca(self, id_documento: str, tenant: int):
        sql = 'select 1 from info_cobranca where documento=:documento and tenant=:tenant'
        params = dict()
        params['documento'] = id_documento
        params['tenant'] = tenant
        if self.fetchOne(sql, params) != None:
            return True
        else:
            return False

    def atualizarInfoCobranca(self, id_documento: int, info_cobranca: InfoCobranca, tenant: int):
        sql = 'update info_cobranca set tenant=tenant'
        params = dict()
        if info_cobranca.situacao != None:
            params['situacao'] = info_cobranca.situacao
            sql = sql + ', situacao=:situacao'

        if info_cobranca.juros_mensal != None:
            params['juros_mensal'] = info_cobranca.juros_mensal
            sql = sql + ', juros_mensal=:juros_mensal'

        if info_cobranca.multa_atraso != None:
            params['multa_atraso'] = info_cobranca.multa_atraso
            sql = sql + ', multa_atraso=:multa_atraso'

        if info_cobranca.desconto != None:
            params['desconto'] = info_cobranca.desconto
            sql = sql + ', desconto=:desconto'

        if info_cobranca.texto_instrucao != None:
            params['texto_instrucao'] = info_cobranca.texto_instrucao
            sql = sql + ', texto_instrucao=:texto_instrucao'

        if info_cobranca.numero != None:
            params['numero'] = info_cobranca.numero
            sql = sql + ', numero=:numero'

        if info_cobranca.nosso_numero != None:
            params['nosso_numero'] = info_cobranca.nosso_numero
            sql = sql + ', nosso_numero=:nosso_numero'

        if info_cobranca.id_externo != None:
            params['id_externo'] = info_cobranca.id_externo
            sql = sql + ', id_externo=:id_externo'

        if info_cobranca.banco_numero != None:
            params['banco_numero'] = info_cobranca.banco_numero
            sql = sql + ', banco_numero=:banco_numero'

        if info_cobranca.uuid_externo != None:
            params['uuid_externo'] = info_cobranca.uuid_externo
            sql = sql + ', uuid_externo=:uuid_externo'

        if info_cobranca.url_boleto != None:
            params['url_boleto'] = info_cobranca.url_boleto
            sql = sql + ', url_boleto=:url_boleto'

        if info_cobranca.linha_digitavel != None:
            params['linha_digitavel'] = info_cobranca.linha_digitavel
            sql = sql + ' in linha_digitavel=:linha_digitavel'

        if info_cobranca.tentativas_registro != None:
            params['tentativas_registro'] = info_cobranca.tentativas_registro
            sql = sql + ', tentativas_registro=:tentativas_registro'

        if info_cobranca.vencimento != None:
            params['vencimento'] = info_cobranca.vencimento
            sql = sql + ', vencimento=:vencimento'

        if info_cobranca.nome_cliente != None:
            params['nome_cliente'] = info_cobranca.nome_cliente
            sql = sql + ', nome_cliente=:nome_cliente'

        if info_cobranca.cpf_cliente != None:
            params['cpf_cliente'] = info_cobranca.cpf_cliente
            sql = sql + ', cpf_cliente=:cpf_cliente'

        if info_cobranca.endereco_logradouro != None:
            params['endereco_logradouro'] = info_cobranca.endereco_logradouro
            sql = sql + ', endereco_logradouro=:endereco_logradouro'

        if info_cobranca.endereco_numero != None:
            params['endereco_numero'] = info_cobranca.endereco_numero
            sql = sql + ', endereco_numero=:endereco_numero'

        if info_cobranca.endereco_complemento != None:
            params['endereco_complemento'] = info_cobranca.endereco_complemento
            sql = sql + ', endereco_complemento=:endereco_complemento'

        if info_cobranca.endereco_bairro != None:
            params['endereco_bairro'] = info_cobranca.endereco_bairro
            sql = sql + ', endereco_bairro=:endereco_bairro'

        if info_cobranca.endereco_cidade != None:
            params['endereco_cidade'] = info_cobranca.endereco_cidade
            sql = sql + ', endereco_cidade=:endereco_cidade'

        if info_cobranca.endereco_estado != None:
            params['endereco_estado'] = info_cobranca.endereco_estado
            sql = sql + ', endereco_estado=:endereco_estado'

        if info_cobranca.endereco_cep != None:
            params['endereco_cep'] = info_cobranca.endereco_cep
            sql = sql + ', endereco_cep=:endereco_cep'

        sql = sql + ' where documento=:documento and tenant=:tenant'
        params['documento'] = id_documento
        params["tenant"] = tenant

        self.execute(sql, params)

    def insereInfoCobranca(self, info_cobranca: InfoCobranca, id_documento: str, tenant: int):
        sql = 'select info_cobranca from info_cobranca where documento=:documento'
        ja_cadastrado = self.fetchOne(sql, {"documento": id_documento})
        if ja_cadastrado != None:
            return ja_cadastrado['info_cobranca']

        sql = """insert into info_cobranca (info_cobranca, juros_mensal, multa_atraso, desconto, texto_instrucao,
                                            numero, nosso_numero, id_externo, banco_numero, uuid_externo,
                                            url_boleto, linha_digitavel, tentativas_registro, vencimento,
                                            situacao, mensagem_erro, tenant, nome_cliente, cpf_cliente,
                                            endereco_logradouro, endereco_numero, endereco_complemento,
                                            endereco_bairro, endereco_cidade, endereco_estado,
                                            endereco_cep, documento)
                values (:info_cobranca, :juros_mensal, :multa_atraso, :desconto, :texto_instrucao,
                        :numero, :nosso_numero, :id_externo, :banco_numero, :uuid_externo,
                        :url_boleto, :linha_digitavel, :tentativas_registro, :vencimento,
                        :situacao, :mensagem_erro, :tenant, :nome_cliente, :cpf_cliente,
                        :endereco_logradouro, :endereco_numero, :endereco_complemento,
                        :endereco_bairro, :endereco_cidade, :endereco_estado,
                        :endereco_cep, :documento)"""
        params = dict()
        params['info_cobranca'] = str(uuid.uuid4())
        params['tenant'] = tenant
        params['juros_mensal'] = info_cobranca.juros_mensal
        params['multa_atraso'] = info_cobranca.multa_atraso
        params['desconto'] = info_cobranca.desconto
        params['texto_instrucao'] = info_cobranca.texto_instrucao
        params['numero'] = info_cobranca.endereco_numero
        params['nosso_numero'] = info_cobranca.nosso_numero
        params['id_externo'] = info_cobranca.id_externo
        params['banco_numero'] = info_cobranca.banco_numero
        params['uuid_externo'] = info_cobranca.uuid_externo
        params['url_boleto'] = info_cobranca.url_boleto
        params['linha_digitavel'] = info_cobranca.linha_digitavel
        params['tentativas_registro'] = info_cobranca.tentativas_registro
        params['vencimento'] = info_cobranca.vencimento
        params['situacao'] = info_cobranca.situacao
        params['nome_cliente'] = info_cobranca.nome_cliente
        params['cpf_cliente'] = info_cobranca.cpf_cliente
        params['endereco_logradouro'] = info_cobranca.endereco_logradouro
        params['mensagem_erro'] = info_cobranca.mensagem_erro
        params['endereco_numero'] = info_cobranca.endereco_numero
        params['endereco_complemento'] = info_cobranca.endereco_complemento
        params['endereco_bairro'] = info_cobranca.endereco_bairro
        params['endereco_cidade'] = info_cobranca.endereco_cidade
        params['endereco_estado'] = info_cobranca.endereco_estado
        params['endereco_cep'] = info_cobranca.endereco_cep
        params['documento'] = id_documento

        self.execute(sql, params)
        return params['info_cobranca']

    def atualizarTodosLancamentos(self, documento: Documento, tenant: int, codigo: str = None, atualizar_valor: bool = True):
        if documento.itens != None:
            for item in documento.itens:
                if item.lancamentos != None:
                    for lancamento in item.lancamentos:
                        self.atualizarLancamento(
                            lancamento, item, documento.documento, tenant, codigo if codigo != None else item.codigo, atualizar_valor)

    def atualizarDocumento(self, documento: Documento):
        sql = """update documento set tipo=:tipo, numero=:numero, ano=:ano, sinal=:sinal, modelo=:modelo, data_lancamento=:data_lancamento,
                                                emissao=:emissao, competencia_inicial=:competencia_inicial, competencia_final=:competencia_final,
                                                cfop=:cfop, situacao=:situacao, valor=:valor, data_entrada=:data_entrada, tipo_ligacao=:tipo_ligacao,
                                                origem=:origem, codigo_consumo=:codigo_consumo, serie=:serie,
                                                subserie=:subserie, empresa=:empresa, grupo_empresarial=:grupo_empresarial, participante=:participante,
                                                codigo_barras=:codigo_barras, usuario=:usuario, url_documento=:url_documento, data_criacao=:data_criacao,
                                                identificador_contrato=:identificador_contrato
                    where documento=:documento"""

        params = documento.__dict__
        self.execute(sql, params)

    def insereDiarioUnico(self, documento: Documento, tenant: int):
        sql_insert_diario = """insert into diario_unico(diario_unico, 
            valor, 
            base, 
            percentagem_sobre_base, 
            natureza_lancamento, 
            ordem_lancamento, 
            historico_lancamento, 
            numero_lancamento, 
            indicador_lancamento_contabil, 
            definicao_lancamento, 
            conta_contabil, 
            centro_custo, 
            documento, 
            diario_unico_tipo, 
            indice_item, 
            estabelecimento, 
            empresa, 
            grupo_empresarial, 
            participante, 
            sinal, 
            origem, 
            descricao, 
            situacao, 
            codigo, 
            codigo_barras, 
            data, 
            tenant, 
            info_pagamento, 
            info_cobranca, 
            icms_retido_original, 
            icms_retido, 
            base_icms_retido_original, 
            base_icms_retido, 
            aliquota_icms_retido, 
            pis_retido_original, 
            pis_retido, 
            base_pis_retido_original, 
            base_pis_retido, 
            aliquota_pis_retido, 
            cofins_retido_original, 
            cofins_retido, 
            base_cofins_retido_original, 
            base_cofins_retido, 
            aliquota_cofins_retido, 
            csll_retido_original, 
            csll_retido, 
            base_csll_retido_original, 
            base_csll_retido, 
            aliquota_csll_retido, 
            irrf_retido_original, 
            irrf_retido, 
            base_irrf_retido_original, 
            base_irrf_retido, 
            aliquota_irrf_retido, 
            iss_retido_original, 
            iss_retido, 
            base_iss_retido_original, 
            base_iss_retido, 
            aliquota_iss_retido,
            rubrica,
            rubrica_esocial,
            trabalhador,
            departamento,
            lotacao,
            item_documento) values (

            :diario_unico,               
            :valor, 
            :base, 
            :percentagem_sobre_base, 
            :natureza_lancamento, 
            :ordem_lancamento, 
            :historico_lancamento, 
            :numero_lancamento, 
            :indicador_lancamento_contabil, 
            :definicao_lancamento, 
            :conta_contabil, 
            :centro_custo, 
            :documento, 
            :diario_unico_tipo, 
            :indice_item, 
            :estabelecimento, 
            :empresa, 
            :grupo_empresarial, 
            :participante, 
            :sinal, 
            :origem, 
            :descricao, 
            :situacao, 
            :codigo, 
            :codigo_barras, 
            :data, 
            :tenant, 
            :info_pagamento, 
            :info_cobranca, 
            :icms_retido_original, 
            :icms_retido, 
            :base_icms_retido_original, 
            :base_icms_retido, 
            :aliquota_icms_retido, 
            :pis_retido_original, 
            :pis_retido, 
            :base_pis_retido_original, 
            :base_pis_retido, 
            :aliquota_pis_retido, 
            :cofins_retido_original, 
            :cofins_retido, 
            :base_cofins_retido_original, 
            :base_cofins_retido, 
            :aliquota_cofins_retido, 
            :csll_retido_original, 
            :csll_retido, 
            :base_csll_retido_original, 
            :base_csll_retido, 
            :aliquota_csll_retido, 
            :irrf_retido_original, 
            :irrf_retido, 
            :base_irrf_retido_original, 
            :base_irrf_retido, 
            :aliquota_irrf_retido, 
            :iss_retido_original, 
            :iss_retido, 
            :base_iss_retido_original, 
            :base_iss_retido, 
            :aliquota_iss_retido,
            :rubrica,
            :rubrica_esocial,
            :trabalhador,
            :departamento,
            :lotacao, 
            :item_documento)"""

        indice_item = 0
        indice_lancamento = 0

        for item in documento.itens:
            indice_item = indice_item+1
            indice_lancamento = 0
            elementos_inseridos = list()

            # Insere lancamentos
            for lancamento_principal in item.lancamentos:
                ordem_ja_preenchida = False

                # Insere info pagamento e info cobranca
                id_info_pagamento = None
                id_info_cobranca = None
                if lancamento_principal.info_pagamento != None:
                    id_info_pagamento = self.insereInfoPagamento(
                        lancamento_principal.info_pagamento, documento.documento, tenant)
                if lancamento_principal.info_cobranca != None:
                    id_info_cobranca = self.insereInfoCobranca(
                        lancamento_principal.info_cobranca, documento.documento, tenant)

                # Obtem numero do lancamento
                lancamento_principal.numero = self.proximoNumeroLancamento(
                    documento.estabelecimento, documento.ano, tenant)

                for lancamento in lancamento_principal.partidas:
                    if lancamento.ordem:
                        if ordem_ja_preenchida == False:
                            indice_lancamento = indice_lancamento+1
                        else:
                            raise Exception(
                                'Algumas partidas estao com a ordem preenchida, outras não estão. Isso não é permitido')
                    else:
                        indice_lancamento = lancamento.ordem
                        ordem_ja_preenchida = True

                    sql = sql_insert_diario
                    params = dict()
                    params["diario_unico"] = str(uuid.uuid4())
                    params["valor"] = lancamento.valor
                    params["base"] = lancamento.base
                    params["percentagem_sobre_base"] = lancamento.percentagem_sobre_base
                    params["natureza_lancamento"] = lancamento.natureza
                    params["ordem_lancamento"] = indice_lancamento
                    params["historico_lancamento"] = lancamento.historico
                    params["numero_lancamento"] = lancamento_principal.numero
                    params["indicador_lancamento_contabil"] = True
                    params["definicao_lancamento"] = lancamento.definicao
                    params["conta_contabil"] = lancamento.conta_contabil
                    params["centro_custo"] = lancamento.centro_custo
                    params["documento"] = documento.documento
                    params["diario_unico_tipo"] = item.tipo
                    params["indice_item"] = indice_item
                    params["estabelecimento"] = documento.estabelecimento
                    params["empresa"] = documento.empresa
                    params["grupo_empresarial"] = documento.grupo_empresarial
                    params["participante"] = documento.participante
                    params["sinal"] = documento.sinal
                    params["origem"] = documento.origem
                    params["descricao"] = item.descricao
                    params["situacao"] = lancamento_principal.situacao.value
                    params["codigo"] = item.codigo
                    params["codigo_barras"] = documento.codigo_barras
                    params["data"] = lancamento_principal.data
                    params["tenant"] = tenant
                    params["info_pagamento"] = id_info_pagamento if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["info_cobranca"] = id_info_cobranca if (
                        lancamento.conta_contabil == '1.1.1.01') else None

                    params["icms_retido_original"] = item.icms_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["icms_retido"] = item.icms_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_icms_retido_original"] = item.base_icms_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_icms_retido"] = item.base_icms_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["aliquota_icms_retido"] = item.aliquota_icms_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["pis_retido_original"] = item.pis_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["pis_retido"] = item.pis_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_pis_retido_original"] = item.base_pis_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_pis_retido"] = item.base_pis_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["aliquota_pis_retido"] = item.aliquota_pis_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["cofins_retido_original"] = item.cofins_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["cofins_retido"] = item.cofins_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_cofins_retido_original"] = item.base_cofins_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_cofins_retido"] = item.base_cofins_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["aliquota_cofins_retido"] = item.aliquota_cofins_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["csll_retido"] = item.csll_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_csll_retido_original"] = item.base_csll_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_csll_retido"] = item.base_csll_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["csll_retido_original"] = item.csll_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["aliquota_csll_retido"] = item.aliquota_csll_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["irrf_retido_original"] = item.irrf_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["irrf_retido"] = item.irrf_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_irrf_retido_original"] = item.base_irrf_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_irrf_retido"] = item.base_irrf_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["aliquota_irrf_retido"] = item.aliquota_irrf_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["iss_retido_original"] = item.iss_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["iss_retido"] = item.iss_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_iss_retido_original"] = item.base_iss_retido_original if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["base_iss_retido"] = item.base_iss_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["aliquota_iss_retido"] = item.aliquota_iss_retido if (
                        lancamento.conta_contabil == '1.1.1.01') else None
                    params["item_documento"] = item.item_documento
                    params["rubrica"] = item.rubrica
                    params["rubrica_esocial"] = item.rubrica_esocial
                    params["trabalhador"] = item.trabalhador
                    params["departamento"] = item.departamento
                    params["lotacao"] = item.lotacao

                    self.execute(sql, params)

    def atualizarLancamento(self, lancamento: Lancamento, item, documento, tenant, codigo, atualizar_valor):
        partidas = lancamento.partidas
        situacao = lancamento.situacao
        data = lancamento.data

        info_pagamento = None

        # Info pagamento
        if lancamento.info_pagamento != None:
            sql = 'select info_pagamento from info_pagamento where documento=:documento limit 1'
            params = dict()
            params["documento"] = documento
            result = self.fetchOne(sql, params)
            if result != None:
                info_pagamento = result['info_pagamento']

        info_cobranca = None
        # Info cobranca
        if lancamento.info_cobranca != None:
            sql = 'select info_cobranca from info_cobranca where documento=:documento limit 1'
            params = dict()
            params["documento"] = documento
            result = self.fetchOne(sql, params)
            if result != None:
                info_cobranca = result['info_cobranca']

        # Obtem numero do proximo lancamento
        sql = "select estabelecimento, ano from documento where documento=:documento and tenant=:tenant limit 1"

        params = dict()
        params["documento"] = documento
        params["tenant"] = tenant
        result = self.fetchOne(sql, params)
        estabelecimento = result['estabelecimento']
        ano = result['ano']
        numero = self.proximoNumeroLancamento(estabelecimento, ano, tenant)

        # Insere/Atualiza partidas
        for partida in partidas:
            guid = str(uuid.uuid4())
            sql = """select diario_unico from diario_unico as du where documento=:documento and tenant=:tenant and conta_contabil=:conta_contabil
                     and natureza_lancamento=:natureza_lancamento"""

            if codigo != None:
                sql += " and codigo=:codigo"

            params = dict()
            params["documento"] = documento
            params["tenant"] = tenant
            params["conta_contabil"] = partida.conta_contabil
            params["natureza_lancamento"] = partida.natureza
            params["item_documento"] = item.item_documento
            if codigo != None:
                params["codigo"] = codigo

            result = self.fetchOne(sql, params)

            if result != None:  # UPDATE
                sql = """update diario_unico set data=:data, valor = :valor, info_cobranca=:info_cobranca, info_pagamento=:info_pagamento, 
                            situacao=:situacao"""
                if atualizar_valor:
                    sql = sql + ", valor=:valor"
                sql = sql + " where diario_unico=:diario_unico"

                params = dict()
                params["data"] = data
                params["info_cobranca"] = info_cobranca if partida.conta_contabil == '1.1.1.01' else None
                params["info_pagamento"] = info_pagamento if partida.conta_contabil == '1.1.1.01' else None
                params["situacao"] = situacao
                if atualizar_valor:
                    params["valor"] = partida.valor
                params["diario_unico"] = result["diario_unico"]

                self.execute(sql, params)

            else:  # INSERIR

                sql = """select :base as base, :percentagem_sobre_base as percentagem_sobre_base,
                :situacao as situacao, :valor as valor,:data as data, :natureza_lancamento as natureza_lancamento, :ordem_lancamento as ordem_lancamento,
                :historico_lancamento as historico_lancamento, :numero_lancamento as numero_lancamento, :indicador_lancamento_contabil as indicador_lancamento_contabil,
                :definicao_lancamento as definicao_lancamento, COALESCE(diario_unico, :diario_unico) as diario_unico, :conta_contabil as conta_contabil,
                documento, indice_item, estabelecimento, empresa, participante, grupo_empresarial,
                usuario, modulo, conta_financeira, forma_pagamento, projeto, renegociacao, item, pedido, tipo_forma_pagamento,
                sinal, origem, descricao, codigo, cancelado, valor_total_sem_rateio,
                codigo_barras, url_documento, lote_contabil, centro_custo,
                semana, tipo_calculo, avos_ferias, rubrica, movimento, trabalhador, lotacao, departamento,
                tenant, item_documento, codigo_transacao, diario_unico_tipo, :info_pagamento as info_pagamento, :info_cobranca as info_cobranca,

                coalesce(:icms_retido_original, icms_retido_original) as icms_retido_original, coalesce(:icms_retido, icms_retido) as icms_retido,
                coalesce(:base_icms_retido_original, base_icms_retido_original) as base_icms_retido_original, coalesce(:base_icms_retido, base_icms_retido) as base_icms_retido,
                coalesce(:aliquota_icms_retido, aliquota_icms_retido) as aliquota_icms_retido, coalesce(:pis_retido_original, pis_retido_original) as pis_retido_original,
                coalesce(:pis_retido, pis_retido) as pis_retido, coalesce(:base_pis_retido_original, base_pis_retido_original) as base_pis_retido_original,
                coalesce(:base_pis_retido, base_pis_retido) as base_pis_retido, coalesce(:aliquota_pis_retido, aliquota_pis_retido) as aliquota_pis_retido,
                coalesce(:cofins_retido_original, cofins_retido_original) as cofins_retido_original, coalesce(:cofins_retido, cofins_retido) as cofins_retido,
                coalesce(:base_cofins_retido_original, base_cofins_retido_original) as base_cofins_retido_original, coalesce(:base_cofins_retido, base_cofins_retido) as base_cofins_retido,
                coalesce(:aliquota_cofins_retido, aliquota_cofins_retido) as aliquota_cofins_retido, coalesce(:csll_retido_original, csll_retido_original) as csll_retido_original,
                coalesce(:csll_retido, csll_retido) as csll_retido, coalesce(:base_csll_retido_original, base_csll_retido_original) as base_csll_retido_original,
                coalesce(:base_csll_retido, base_csll_retido) as base_csll_retido, coalesce(:aliquota_csll_retido, aliquota_csll_retido) as aliquota_csll_retido ,
                coalesce(:irrf_retido_original, irrf_retido_original) as irrf_retido_original, coalesce(:irrf_retido, irrf_retido) as irrf_retido,
                coalesce(:base_irrf_retido_original, base_irrf_retido_original) as base_irrf_retido_original, coalesce(:base_irrf_retido, base_irrf_retido) as base_irrf_retido,
                coalesce(:aliquota_irrf_retido, aliquota_irrf_retido) as aliquota_irrf_retido, coalesce(:iss_retido_original, iss_retido_original) as iss_retido_original,
                coalesce(:iss_retido, iss_retido) as iss_retido, coalesce(:base_iss_retido_original, base_iss_retido_original) as base_iss_retido_original,
                coalesce(:base_iss_retido, base_iss_retido) as base_iss_retido, coalesce(:aliquota_iss_retido, aliquota_iss_retido) as aliquota_iss_retido,
                coalesce(:rubrica, rubrica) as rubrica,
                coalesce(:rubrica_esocial, rubrica_esocial) as rubrica_esocial,
                coalesce(:trabalhador, trabalhador) as trabalhador,
                coalesce(:departamento, departamento) as departamento,
                coalesce(:lotacao, lotacao) as lotacao

                from diario_unico
                where documento=:documento and tenant=:tenant order by numero_lancamento desc limit 1"""

                params = dict()
                params["base"] = partida.base
                params["percentagem_sobre_base"] = partida.percentagem_sobre_base
                params["situacao"] = situacao
                params["valor"] = partida.valor
                params["data"] = data
                params["natureza_lancamento"] = partida.natureza
                params["ordem_lancamento"] = partida.ordem
                params["historico_lancamento"] = partida.historico
                params["numero_lancamento"] = numero
                params["indicador_lancamento_contabil"] = 1
                params["definicao_lancamento"] = partida.definicao
                params["diario_unico"] = guid
                params["conta_contabil"] = partida.conta_contabil
                params["documento"] = documento
                params["tenant"] = tenant
                params["info_pagamento"] = info_pagamento if partida.conta_contabil == '1.1.1.01' else None
                params["info_cobranca"] = info_cobranca if partida.conta_contabil == '1.1.1.01' else None

                # IMPOSTOS
                params["icms_retido_original"] = item.icms_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["icms_retido"] = item.icms_retido if partida.conta_contabil == '1.1.1.01' else None
                params["base_icms_retido_original"] = item.base_icms_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["base_icms_retido"] = item.base_icms_retido if partida.conta_contabil == '1.1.1.01' else None
                params["aliquota_icms_retido"] = item.aliquota_icms_retido if partida.conta_contabil == '1.1.1.01' else None
                params["pis_retido_original"] = item.pis_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["pis_retido"] = item.pis_retido if partida.conta_contabil == '1.1.1.01' else None
                params["base_pis_retido_original"] = item.base_pis_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["base_pis_retido"] = item.base_pis_retido if partida.conta_contabil == '1.1.1.01' else None
                params["aliquota_pis_retido"] = item.aliquota_pis_retido if partida.conta_contabil == '1.1.1.01' else None
                params["cofins_retido_original"] = item.cofins_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["cofins_retido"] = item.cofins_retido if partida.conta_contabil == '1.1.1.01' else None
                params["base_cofins_retido_original"] = item.base_cofins_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["base_cofins_retido"] = item.base_cofins_retido if partida.conta_contabil == '1.1.1.01' else None
                params["aliquota_cofins_retido"] = item.aliquota_cofins_retido if partida.conta_contabil == '1.1.1.01' else None
                params["csll_retido_original"] = item.csll_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["csll_retido"] = item.csll_retido if partida.conta_contabil == '1.1.1.01' else None
                params["base_csll_retido_original"] = item.base_csll_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["base_csll_retido"] = item.base_csll_retido if partida.conta_contabil == '1.1.1.01' else None
                params["aliquota_csll_retido"] = item.aliquota_csll_retido if partida.conta_contabil == '1.1.1.01' else None
                params["irrf_retido_original"] = item.irrf_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["irrf_retido"] = item.irrf_retido if partida.conta_contabil == '1.1.1.01' else None
                params["base_irrf_retido_original"] = item.base_irrf_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["base_irrf_retido"] = item.base_irrf_retido if partida.conta_contabil == '1.1.1.01' else None
                params["aliquota_irrf_retido"] = item.aliquota_irrf_retido if partida.conta_contabil == '1.1.1.01' else None
                params["iss_retido_original"] = item.iss_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["iss_retido"] = item.iss_retido if partida.conta_contabil == '1.1.1.01' else None
                params["base_iss_retido_original"] = item.base_iss_retido_original if partida.conta_contabil == '1.1.1.01' else None
                params["base_iss_retido"] = item.base_iss_retido if partida.conta_contabil == '1.1.1.01' else None
                params["aliquota_iss_retido"] = item.aliquota_iss_retido if partida.conta_contabil == '1.1.1.01' else None

                params["rubrica"] = item.rubrica
                params["rubrica_esocial"] = item.rubrica_esocial
                params["trabalhador"] = item.trabalhador
                params["departamento"] = item.departamento
                params["lotacao"] = item.lotacao
                

                params = self.fetchOne(sql, params)
                if codigo != None:
                    params['codigo'] = codigo

                sql = """INSERT INTO diario_unico
                            (base, percentagem_sobre_base, situacao, valor,data, natureza_lancamento, ordem_lancamento,
                            historico_lancamento, numero_lancamento, indicador_lancamento_contabil, definicao_lancamento,
                            diario_unico,conta_contabil,
                            documento, indice_item, estabelecimento, empresa, participante, grupo_empresarial,
                            usuario, modulo, conta_financeira, forma_pagamento, projeto, renegociacao, item, pedido, tipo_forma_pagamento,
                            sinal, origem, descricao, codigo, cancelado, valor_total_sem_rateio,
                            codigo_barras, url_documento, lote_contabil, centro_custo,
                            semana, tipo_calculo, avos_ferias, rubrica, movimento, trabalhador, lotacao, departamento,
                            tenant, item_documento, diario_unico_tipo, info_pagamento, info_cobranca)
                        values (:base, :percentagem_sobre_base, :situacao, :valor,:data, :natureza_lancamento, :ordem_lancamento,
                            :historico_lancamento, :numero_lancamento, :indicador_lancamento_contabil, :definicao_lancamento,
                            :diario_unico, :conta_contabil,
                            :documento, :indice_item, :estabelecimento, :empresa, :participante, :grupo_empresarial,
                            :usuario, :modulo, :conta_financeira, :forma_pagamento, :projeto, :renegociacao, :item, :pedido, :tipo_forma_pagamento,
                            :sinal, :origem, :descricao, :codigo, :cancelado, :valor_total_sem_rateio,
                            :codigo_barras, :url_documento, :lote_contabil, :centro_custo,
                            :semana, :tipo_calculo, :avos_ferias, :rubrica, :movimento, :trabalhador, :lotacao, :departamento,
                            :tenant, :item_documento, :diario_unico_tipo, :info_pagamento, :info_cobranca)"""
                self.execute(sql, params)

    def proximoNumeroLancamento(self, estabelecimento: str, ano: int, tenant: int):

        chave_sequence = "{}-{}".format(estabelecimento, ano)
        return self._util_repository.getProximovalueCustomSequence(chave_sequence, tenant)

    def getDataPagamento(self, id_documento):
        sql = "select data from diario_unico where conta_contabil=:conta_contabil and documento = :documento"
        params = dict()
        params['conta_contabil'] = '1.1.1.01'
        params['documento'] = id_documento
        return self.fetchOne(sql, params)['data']
