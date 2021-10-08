
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, constr, Field

from diario_unico.entity.info_cobranca import InfoCobranca
from diario_unico.entity.info_pagamento import InfoPagamento
from diario_unico.entity.lancamento import SituacaoDiario
from diario_unico.entity.partida import Partida
from diario_unico.enum.codigo_contabil_financeiro import CodigoContabilFinanceiro
from diario_unico.enum.documentos.documento_origem import DocumentoOrigem
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.enum.documentos.item_documento_tipo_tributacao_iss import ItemDocumentoTipoTributacaoIss
from diario_unico.enum.documentos.tipo_iss import TipoIss
from diario_unico.enum.documentos.tipo_tributacao_servico import TipoTributacaoServico
from diario_unico.enum.lancamento.lancamento_natureza import LancamentoNatureza
from diario_unico.enum.pasta_contabil import PastaContabil
from diario_unico.enum.sinal import Sinal
from diario_unico.enum.situacao import Situacao
from nasajon.pastas_contabeis.pastas_router import MomentoContabil


class LinhaDiarioUnico(BaseModel):
    # ID
    id: UUID
    tenant: int

    # Partes envolvidas
    estabelecimento: UUID
    participante: UUID
    cnae: Optional[constr(min_length=7, max_length=7, strip_whitespace=True)]

    # Documento
    documento_numero: Optional[constr(min_length=1, max_length=20, strip_whitespace=True)]
    documento_serie: Optional[constr(min_length=1, max_length=3, strip_whitespace=True)]
    documento_subserie: Optional[constr(min_length=1, max_length=3, strip_whitespace=True)]
    documento_sinal: Optional[Sinal]
    documento_id: Optional[UUID]
    documento_emissao: Optional[date]
    documento_tipo: Optional[DocumentoTipo]
    documento_modelo: Optional[constr(min_length=1, max_length=10, strip_whitespace=True)]
    documento_situacao: Optional[Situacao]

    # Item de documento
    item_id: Optional[UUID]
    item_ordem: Optional[int]
    item_codigo: Optional[constr(min_length=1, max_length=40, strip_whitespace=True)]
    item_descricao: Optional[constr(min_length=1, max_length=200, strip_whitespace=True)]

    # auditoria
    data_registro: datetime = Field(default_factory=datetime.now)
    origem: Optional[DocumentoOrigem]

    #servicos
    tipo_tributacao_servico: Optional[TipoTributacaoServico]
    tipoIss: Optional[TipoIss]
    tipo_tributacao_iss: Optional[ItemDocumentoTipoTributacaoIss]
    recorrente: Optional[bool]

    #Diario Unico
    situacao: SituacaoDiario

    #impostos
    base_iss: Optional[Decimal]
    aliquota_iss: Optional[Decimal]
    iss_retido: Optional[Decimal]
    base_irrf: Optional[Decimal]
    aliquota_irrf: Optional[Decimal]
    irrf_retido: Optional[Decimal]
    base_inss: Optional[Decimal]
    incidencia_inss: Optional[Decimal]
    inss_retido: Optional[Decimal]
    base_csll: Optional[Decimal]
    aliquota_csll: Optional[Decimal]
    csll_retido: Optional[Decimal]
    base_pis: Optional[Decimal]
    aliquota_pis: Optional[Decimal]
    pis_retido: Optional[Decimal]
    base_cofins: Optional[Decimal]
    aliquota_cofins: Optional[Decimal]
    cofins_retido: Optional[Decimal]

    #titulos
    info_pagamento: Optional[UUID]
    info_cobranca: Optional[UUID]

    #lancamento
    lancamento_ID: UUID
    lancamento_numero: int
    lancamento_data: date
    lancamento_natureza: LancamentoNatureza
    lancamento_ordem: int
    conta_contabil: str
    lancamento_historico: str
    valor: Decimal
    base: Optional[Decimal]
    percentagem_sobre_base: Optional[float]
    momento: MomentoContabil
    pasta_contabil: PastaContabil
    codigo_contabil_financeiro: CodigoContabilFinanceiro
