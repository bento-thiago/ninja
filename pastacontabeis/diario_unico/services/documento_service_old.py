from diario_unico.repository.documento_repository_old import DocumentoRepository
from diario_unico.repository.estabelecimento_repository import EstabelecimentoRepository
from diario_unico.repository.pessoas_repository import PessoasRepository
from diario_unico.entity.documento import Documento
from diario_unico.enum.situacao import Situacao
from nasajon.util.objeto_util import ObjetosUtils
from nasajon.util.json_util import JsonUtil
from nasajon.helper.documento_helper import DocumentoHelper
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from typing import List
import uuid
from time_service.service.time_service import TimeService
from diario_unico.entity.informacoes_a_recuperar import InformacoesARecuperar
from diario_unico.entity.filtro import Filtro
from diario_unico.services.query_service import QueryEnum
from nasajon.util.log import Log


class DocumentoServiceOld:

    def __init__(self, repository: DocumentoRepository, estabelecimentoRepository: EstabelecimentoRepository, pessoasRepository: PessoasRepository):
        self.repository = repository
        self.estabelecimentoRepository = estabelecimentoRepository
        self.pessoasRepository = pessoasRepository
        self.log = Log("DIARIO_UNIFICADO")

    def insereDocumento(self, documento: Documento, tenant: int, campos_obrigatorios: list, campos_permitidos: list, permite_lancamento_em_caixa_no_passado: bool):
        self.log.info("Comecou a inserir documento")
        # Preencher campos auto-calculados
        if documento.documento == None:
            documento.documento = str(uuid.uuid4())

        if documento.data_criacao == None:
            documento.data_criacao = TimeService.now().date()

        for item in documento.itens:
            if item.item_documento == None:
                item.item_documento = str(uuid.uuid4())
            if item.documento == None:
                item.documento = documento.documento

        # Validacoes
        DocumentoHelper().validarCamposObrigatorios(documento, campos_obrigatorios)
        DocumentoHelper().validarCamposPermitidos(documento, campos_permitidos)
        DocumentoHelper().validarLancamentos(
            documento, permite_lancamento_em_caixa_no_passado)
        DocumentoHelper().validarTipos(documento)

        # Conversao CODIGO -> GUID
        documento.estabelecimento = self.estabelecimentoRepository.recuperarEstabelecimentoPeloCodigo(
            documento.estabelecimento, tenant)["pessoa"]
        documento.participante = self.pessoasRepository.recuperarPessoaPeloCPF_CNPJ(
            documento.participante, tenant)["pessoa"]

        # Cadastro
        doc = self.repository.documentoJaCadastrado(documento, tenant)

        self.log.info("Documento depois de tratamentos:")
        # Atualizar
        if (doc != None):
            id_documento = doc["documento"]
            situacao_anterior = doc["situacao"]
            if (Situacao(situacao_anterior) == Situacao.REALIZADO) and (Situacao(documento.situacao) == Situacao.PREVISTO):
                self.log.info(
                    "Não é permitido realizar a previsao de um documento ja realizado")
                return None
            self.log.info("Documento ja cadastrado, realizando atualizacao. Passando de " +
                          situacao_anterior+" para: "+str(documento.situacao))
            documento.documento = id_documento
            self.repository.begin()
            for item in documento.itens:
                for lancamento in item.lancamentos:
                    if lancamento.info_pagamento != None:
                        self.repository.inserir_ou_atualizarInfoPagamento(
                            lancamento.info_pagamento, id_documento, tenant)
                    if lancamento.info_cobranca != None:
                        self.log.info("Possui Info Cobranca")
                        self.repository.inserir_ou_atualizarInfoCobranca(
                            lancamento.info_cobranca, id_documento, tenant)
                    else:
                        self.log.info("NAO Possui Info Cobranca")

            self.repository.atualizarTodosLancamentos(
                documento, tenant)
            self.repository.atualizarDocumento(documento)
            self.repository.commit()

        # Cadastrar
        else:
            self.log.info(
                "Documento ainda nao cadastrado, Realizando cadastro")
            self.repository.begin()
            self.repository.insereDocumento(documento, tenant)
            self.repository.insereDiarioUnico(documento, tenant)
            self.repository.commit()

        return documento

    def listarDocumentos(self, filtro, informacoes_a_receber, tenant):

        # Ajustar o valor do estabelecimento para usar o ID em vez do código
        filtro = self.filtroAjustarEstabelecimento(filtro, tenant)

        # Consulta ao banco e conversao para objeto
        documentos: List[Documento] = self.repository.listarDocumentos(
            filtro, informacoes_a_receber, tenant)

        # LOOP de documento para preencher campos fazer conversao de GUID em CODIGO
        for documento in documentos:
            estabelecimento = self.estabelecimentoRepository.recuperarEstabelecimentoPeloID(
                documento.estabelecimento, tenant)
            participante = self.pessoasRepository.recuperarPessoaPeloID(
                documento.participante, tenant)
            if estabelecimento != None:
                documento.estabelecimento = estabelecimento['codigo']
            if participante != None:
                documento.participante = participante['cpf_cnpj']
                documento.participante_nome = participante['nomefantasia']
            if documento.situacao == Situacao.QUITADO.value:
                documento.data_pagamento = self.repository.getDataPagamento(
                    documento.documento)

        return documentos

    def filtroAjustarEstabelecimento(self, filtro: Filtro, tenant):
        _filtro = JsonUtil().toDict(filtro)
        if (not "campo" in _filtro) or (_filtro["campo"] == None):
            for index, parametro in enumerate(_filtro["parametros"]):
                _filtro["parametros"][index] = self.filtroAjustarEstabelecimento(
                    parametro, tenant)
        elif _filtro["campo"] == "estabelecimento":
            # TODO Rever abaixo, acho que não funcionaria para um filtro recebendo N estabelecimentos (N>1):
            _filtro["parametros"][0] = self.estabelecimentoRepository.recuperarEstabelecimentoPeloCodigo(
                _filtro["parametros"][0], tenant)['pessoa']

        return ObjetosUtils().dictToObject(_filtro, Filtro)

    def getDocumentoInteiro(self, id_documento, tenant):
        informacoes_a_receber = list()
        for entidade in QueryEnum.camposcorrespondentes:
            info = InformacoesARecuperar()
            info.entidade = entidade
            info.campos = [
                nome_campo for nome_campo in QueryEnum.camposcorrespondentes[entidade]]
            informacoes_a_receber.append(info)

        filtro = Filtro()
        filtro.operacao = "Igual"
        filtro.entidade = "Documento"
        filtro.campo = "documento"
        filtro.parametros = [id_documento]
        return self.listarDocumentos(filtro, informacoes_a_receber, tenant)[0]

    def atualizarDocumento(self, documento):
        self.repository.atualizarDocumento(documento)

    def cadastrarPessoa(self, cpf_cnpj, nome, tenant):
        self.pessoasRepository.cadastrarPessoa(cpf_cnpj,nome, tenant)
