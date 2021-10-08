from typing import List

from diario_unico.entity.documento import Documento
from diario_unico.entity.servicos.fatura_prestacao_servicos import FaturaPrestacaoServicos
from diario_unico.enum.documentos.documento_origem import DocumentoOrigem
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.enum.sinal import Sinal
from diario_unico.services.documento_service import DocumentoService
from diario_unico.services.pessoa_service import PessoaService


class FaturaPrestacaoServicosService:
    def __init__(self, documentoService: DocumentoService, pessoaService: PessoaService):
        self.documentoService = documentoService
        self.pessoaService = pessoaService

    def inserir_fatura_prestacao_servicos(self, tenant: int, fatura: FaturaPrestacaoServicos):
        if fatura.situacao is None:
            raise Exception("A situacao da fatura de prestacao de servicos deve ser informada")
        fatura.participante = self.pessoaService.inserir_pessoa(fatura.participante, tenant)
        documento: Documento = self.para_documento(tenant, fatura)
        self.documentoService.insere_documento(tenant, documento)
        return documento

    def listar(self, tenant: int):
        documentos: List[Documento] = self.documentoService.listar_documentos(tenant)
        pessoas = {p["id_registro"]: p
                   for p in
                   self.pessoaService.listar_dados_completos_participantes(tenant,
                                                                           [
                                                                               doc.participante
                                                                               for
                                                                               doc
                                                                               in
                                                                               documentos])}
        saida = list()
        for documento in documentos:
            fatura: FaturaPrestacaoServicos = self.documento_para_fatura(tenant, documento,
                                                                         pessoas[str(documento.participante)])
            saida.append(fatura)
        return saida

    @staticmethod
    def para_documento(tenant: int, fatura: FaturaPrestacaoServicos) -> Documento:
        dados = dict()
        dados["id"] = fatura.id
        dados["emissao"] = fatura.emissao
        dados["cnae"] = fatura.cnae
        dados["estabelecimento"] = fatura.estabelecimento
        dados["participante"] = fatura.participante.id_registro
        dados["token_facilitador"] = fatura.token_facilitador
        dados["discriminacao"] = fatura.discriminacao
        dados["municipio_prestacao"] = fatura.municipio_prestacao
        dados["numero"] = fatura.numero
        dados["serie"] = fatura.serie
        dados["subserie"] = fatura.subserie
        dados["tipo_tributacao_servico"] = fatura.tipo_tributacao_servico
        dados["tipoIss"] = fatura.tipoIss
        dados["emissao:"] = fatura.emissao
        dados["data_registro"] = fatura.data_registro
        dados["modelo"] = "NFSE"
        dados["tenant"] = tenant
        dados["sinal"] = Sinal.SAIDA
        dados["situacao"] = fatura.situacao
        dados["origem"] = DocumentoOrigem.PROCESSAMENTO_CONTRATOS
        dados["tipo"] = DocumentoTipo.FATURA_PRESTACAO_SERVICOS
        dados["valor"] = fatura.valor_servicos
        dados["infos_cobranca"] = [info.dict() for info in fatura.infos_cobranca]
        dados["itens"] = list()

        for item in fatura.itens:
            d_item = dict()
            d_item["codigo"] = item.codigo
            d_item["ordem"] = item.ordem
            d_item["descricao"] = item.descricao
            d_item["tipo_tributacao_iss"] = item.tipo_tributacao_iss
            d_item["valor"] = item.valor
            d_item["base_iss"] = item.base_iss
            d_item["aliquota_iss"] = item.aliquota_iss
            d_item["iss_retido"] = item.iss_retido
            d_item["base_irrf"] = item.base_irrf
            d_item["aliquota_irrf"] = item.aliquota_irrf
            d_item["irrf_retido"] = item.irrf_retido
            d_item["base_inss"] = item.base_inss
            d_item["incidencia_inss"] = item.incidencia_inss
            d_item["inss_retido"] = item.inss_retido
            d_item["base_csll"] = item.base_csll
            d_item["aliquota_csll"] = item.aliquota_csll
            d_item["csll_retido"] = item.csll_retido
            d_item["base_pis"] = item.base_pis
            d_item["aliquota_pis"] = item.aliquota_pis
            d_item["pis_retido"] = item.pis_retido
            d_item["base_cofins"] = item.base_cofins
            d_item["aliquota_cofins"] = item.aliquota_cofins
            d_item["cofins_retido"] = item.cofins_retido
            d_item["recorrente"] = item.recorrente
            d_item["documento_id"] = item.documento_id
            d_item["id"] = item.id
            d_item["lancamentos"] = list()
            for lancamento in item.lancamentos:
                d_item["lancamentos"].append(lancamento.dict())
            dados["itens"].append(d_item)

        return Documento.parse_obj(dados)

    def documento_para_fatura(self, tenant: int, documento: Documento, participante: dict) -> FaturaPrestacaoServicos:
        saida = dict()
        saida["estabelecimento"] = documento.estabelecimento
        saida["participante"] = participante
        saida["token_facilitador"] = documento.token_facilitador
        saida["cnae"] = documento.cnae
        saida["discriminacao"] = documento.discriminacao
        saida["municipio_prestacao"] = documento.municipio_prestacao
        saida["numero"] = documento.numero
        saida["emissao"] = documento.emissao
        saida["serie"] = documento.serie
        saida["subserie"] = documento.subserie
        saida["tipo_tributacao_servico"] = documento.tipo_tributacao_servico
        saida["tipoIss"] = documento.tipoIss
        saida["situacao"] = documento.situacao
        saida["id"] = documento.id
        saida["infos_cobranca"] = [info.dict() for info in documento.infos_cobranca]
        saida["itens"] = list()

        for item in documento.itens:
            item_fatura = dict()
            item_fatura["codigo"] = item.codigo
            item_fatura["descricao"] = item.descricao
            item_fatura["tipo_tributacao_iss"] = item.tipo_tributacao_iss
            item_fatura["valor"] = item.valor
            item_fatura["base_iss"] = item.base_iss
            item_fatura["aliquota_iss"] = item.aliquota_iss
            item_fatura["iss_retido"] = item.iss_retido
            item_fatura["base_irrf"] = item.base_irrf
            item_fatura["aliquota_irrf"] = item.aliquota_irrf
            item_fatura["irrf_retido"] = item.irrf_retido
            item_fatura["base_inss"] = item.base_inss
            item_fatura["incidencia_inss"] = item.incidencia_inss
            item_fatura["inss_retido"] = item.inss_retido
            item_fatura["base_csll"] = item.base_csll
            item_fatura["aliquota_csll"] = item.aliquota_csll
            item_fatura["csll_retido"] = item.csll_retido
            item_fatura["base_pis"] = item.base_pis
            item_fatura["aliquota_pis"] = item.aliquota_pis
            item_fatura["pis_retido"] = item.pis_retido
            item_fatura["base_cofins"] = item.base_cofins
            item_fatura["aliquota_cofins"] = item.aliquota_cofins
            item_fatura["cofins_retido"] = item.cofins_retido
            item_fatura["recorrente"] = item.recorrente
            item_fatura["id"] = item.id
            item_fatura["documento_id"] = item.documento_id
            item_fatura["ordem"] = item.ordem
            item_fatura["lancamentos"] = [l.dict() for l in item.lancamentos]
            saida["itens"].append(item_fatura)
        return FaturaPrestacaoServicos.parse_obj(saida)
