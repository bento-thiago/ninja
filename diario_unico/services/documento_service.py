import uuid
from typing import List

from diario_unico.entity.documento import Documento
from diario_unico.entity.linha_diario_unico import LinhaDiarioUnico
from diario_unico.enum.codigo_contabil_financeiro import CodigoContabilFinanceiro
from diario_unico.enum.lancamento.lancamento_natureza import LancamentoNatureza
from diario_unico.repository.documento_repository import DocumentoRepository
from diario_unico.services.diario_unico_service import DiarioUnicoService
from diario_unico.services.info_cobranca_service import InfoCobrancaService
from diario_unico.services.utilitario_service import UtilitarioService
from nasajon.pastas_contabeis.pastas_router import MomentoContabil


class DocumentoService:
    def __init__(self, documentoRepository: DocumentoRepository, diarioUnicoService: DiarioUnicoService,
                 utilitarioService: UtilitarioService, infoCobrancaService: InfoCobrancaService):
        self.utilitarioService = None
        self.repository = documentoRepository
        self.diarioUnicoService = diarioUnicoService
        self.infoCobrancaService = infoCobrancaService

    def insere_documento(self, tenant: int, documento: Documento):
        if documento.id is not None:
            if self.utilitarioService.exists_pk(self.repository.table_name, 'id', tenant, documento.id):
                raise Exception("Documento ja cadastrado")
        else:
            documento.id = uuid.uuid4()

        for item in documento.itens:
            if item.id is not None:
                if self.utilitarioService.exists_pk(self.diarioUnicoRepository.table_name, 'item_id', tenant, item.id):
                    raise Exception("Item ja cadastrado")
            else:
                item.id = uuid.uuid4()

            for lancamento in item.lancamentos:
                if lancamento.id is not None:
                    if self.utilitarioService.exists_pk(self.diarioUnicoRepository.table_name, 'lancamento_id', tenant,
                                                        lancamento.id):
                        raise Exception("Lancamento ja cadastrado")
                else:
                    lancamento.id = uuid.uuid4()

        self.repository.begin()
        self.repository.insere_documento(tenant, documento)
        for info_cobranca in documento.infos_cobranca:
            info_cobranca.documento_id = documento.id
        self.infoCobrancaService.insere_info_cobranca(tenant, documento.infos_cobranca)
        self.diarioUnicoService.insere_diario(tenant,
                                              DocumentoService.documento_para_linhas_diario_unico(tenant, documento))
        self.repository.commit()
        return documento

    def listar_documentos(self, tenant: int) -> List[Documento]:
        headers = self.repository.listar_dados_documentos(tenant)
        ids = [d["id"] for d in headers]
        linhas_diario = self.diarioUnicoService.listar_linha_de_documentos(tenant, ids)
        infos_cobranca = self.infoCobrancaService.listar_de_documentos(tenant, ids)
        saida = list()
        for header in headers:
            documento: Documento = self.montar_documento(header,
                                                         [linha for linha in linhas_diario if
                                                          str(linha.documento_id) == header["id"]],
                                                         [info for info in infos_cobranca if
                                                          str(info.documento_id) == header["id"]])
            saida.append(documento)
        return saida

    @staticmethod
    def documento_para_linhas_diario_unico(tenant: int, documento: Documento) -> List[LinhaDiarioUnico]:
        saida = list()
        for item in documento.itens:
            for lancamento in item.lancamentos:
                for partida in lancamento.partidas:
                    linha = LinhaDiarioUnico(id=uuid.uuid4(),
                                             tenant=tenant,
                                             estabelecimento=documento.estabelecimento,
                                             participante=documento.participante,
                                             cnae=documento.cnae,
                                             documento_numero=documento.numero,
                                             documento_serie=documento.serie,
                                             documento_subserie=documento.subserie,
                                             documento_sinal=documento.sinal,
                                             documento_id=documento.id,
                                             documento_emissao=documento.emissao,
                                             documento_tipo=documento.tipo,
                                             documento_modelo=documento.modelo,
                                             item_id=item.id,
                                             item_ordem=item.ordem,
                                             item_codigo=item.codigo,
                                             item_descricao=item.descricao,
                                             data_registro=documento.data_registro,
                                             origem=documento.origem,
                                             tipo_tributacao_servico=documento.tipo_tributacao_servico,
                                             tipoIss=documento.tipoIss,
                                             tipo_tributacao_iss=item.tipo_tributacao_iss,
                                             recorrente=item.recorrente,
                                             situacao=lancamento.situacao,
                                             documento_situacao=documento.situacao,
                                             lancamento_ID=lancamento.id,
                                             lancamento_numero=lancamento.numero,
                                             lancamento_data=lancamento.data,
                                             lancamento_natureza=partida.natureza,
                                             lancamento_ordem=partida.ordem,
                                             conta_contabil=partida.conta_contabil,
                                             lancamento_historico=partida.historico,
                                             valor=partida.valor,
                                             base=partida.base,
                                             percentagem_sobre_base=partida.percentagem_sobre_base,
                                             momento=partida.momento,
                                             pasta_contabil=partida.pasta_contabil,
                                             codigo_contabil_financeiro=partida.codigo_contabil_financeiro
                                             )
                    if lancamento.info_cobranca is not None:
                        linha.info_cobranca = lancamento.info_cobranca
                    if partida.codigo_contabil_financeiro == CodigoContabilFinanceiro.CAIXA:
                        linha.base_iss = item.base_iss
                        linha.aliquota_iss = item.aliquota_iss
                        linha.iss_retido = item.iss_retido
                        linha.base_irrf = item.base_irrf
                        linha.aliquota_irrf = item.aliquota_irrf
                        linha.irrf_retido = item.irrf_retido
                        linha.base_inss = item.base_inss
                        linha.incidencia_inss = item.incidencia_inss
                        linha.inss_retido = item.inss_retido
                        linha.base_csll = item.base_csll
                        linha.aliquota_csll = item.aliquota_csll
                        linha.csll_retido = item.csll_retido
                        linha.base_pis = item.base_pis
                        linha.aliquota_pis = item.aliquota_pis
                        linha.pis_retido = item.pis_retido
                        linha.base_cofins = item.base_cofins
                        linha.aliquota_cofins = item.aliquota_cofins
                        linha.cofins_retido = item.cofins_retido
                    saida.append(linha)

        return saida

    def montar_documento(self, header: dict, linhas_diario: List[LinhaDiarioUnico],
                         infos_cobranca: List[dict]) -> Documento:
        doc = dict()
        for key in header.keys():
            doc[key] = header[key]
        itens_dict = dict()
        lancamentos_dict = dict()
        partidas_dict = dict()
        for linha in linhas_diario:
            # item
            item_dict = itens_dict.get(linha.item_id, dict())
            item_dict["codigo"] = linha.item_codigo
            item_dict["descricao"] = linha.item_descricao
            item_dict["tipo_tributacao_iss"] = linha.tipo_tributacao_iss
            if (linha.momento == MomentoContabil.APROPRIACAO) and (linha.lancamento_natureza == LancamentoNatureza.D):
                item_dict["valor"] = item_dict.get("valor", 0) + linha.valor
            if linha.codigo_contabil_financeiro == CodigoContabilFinanceiro.CAIXA:
                item_dict["base_iss"] = linha.base_iss
                item_dict["aliquota_iss"] = linha.aliquota_iss
                item_dict["iss_retido"] = linha.iss_retido
                item_dict["base_irrf"] = linha.base_irrf
                item_dict["aliquota_irrf"] = linha.aliquota_irrf
                item_dict["irrf_retido"] = linha.irrf_retido
                item_dict["base_inss"] = linha.base_inss
                item_dict["incidencia_inss"] = linha.incidencia_inss
                item_dict["inss_retido"] = linha.inss_retido
                item_dict["base_csll"] = linha.base_csll
                item_dict["aliquota_csll"] = linha.aliquota_csll
                item_dict["csll_retido"] = linha.csll_retido
                item_dict["base_pis"] = linha.base_pis
                item_dict["aliquota_pis"] = linha.aliquota_pis
                item_dict["pis_retido"] = linha.pis_retido
                item_dict["base_cofins"] = linha.base_cofins
                item_dict["aliquota_cofins"] = linha.aliquota_cofins
                item_dict["cofins_retido"] = linha.cofins_retido
            item_dict["recorrente"] = linha.recorrente
            item_dict["id"] = linha.item_id
            item_dict["documento_id"] = linha.documento_id
            item_dict["ordem"] = linha.item_ordem
            itens_dict[item_dict["id"]] = item_dict

            # lancamento
            lancamento_dict = lancamentos_dict.get(linha.lancamento_ID, dict())
            lancamento_dict["id"] = linha.lancamento_ID
            lancamento_dict["numero"] = linha.lancamento_numero
            lancamento_dict["info_cobranca"] = linha.info_cobranca
            lancamento_dict["data"] = linha.lancamento_data
            lancamento_dict["situacao"] = linha.situacao
            lancamentos_dict[lancamento_dict["id"]] = lancamento_dict

            # partidas
            partida_dict = dict()
            partida_dict["natureza"] = linha.lancamento_natureza
            partida_dict["ordem"] = linha.lancamento_ordem
            partida_dict["conta_contabil"] = linha.conta_contabil
            partida_dict["historico"] = linha.lancamento_historico
            partida_dict["valor"] = linha.valor
            partida_dict["base"] = linha.base
            partida_dict["momento"] = linha.momento
            partida_dict["pasta_contabil"] = linha.pasta_contabil
            partida_dict["codigo_contabil_financeiro"] = linha.codigo_contabil_financeiro
            partida_dict["percentagem_sobre_base"] = linha.percentagem_sobre_base

            # vincular partida com lancamento
            lista_partidas = lancamento_dict.get("partidas", list())
            lista_partidas.append(partida_dict)
            lista_partidas = sorted(lista_partidas, key=lambda i: i["ordem"])
            lancamento_dict["partidas"] = lista_partidas

            # vincular lancamento a item
            lista_lancamentos = item_dict.get("lancamentos", list())
            if lancamento_dict not in lista_lancamentos:
                lista_lancamentos.append(lancamento_dict)
            lista_lancamentos = sorted(lista_lancamentos, key=lambda i: i["numero"])
            item_dict["lancamentos"] = lista_lancamentos

        # vincular item a documento
        lista_itens = list(itens_dict.values())
        lista_itens = sorted(lista_itens, key=lambda i: i["ordem"])
        doc["itens"] = lista_itens
        doc["infos_cobranca"]=[info.dict() for info in infos_cobranca]
        documento = Documento.parse_obj(doc)
        return documento
