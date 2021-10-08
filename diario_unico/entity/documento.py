from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import constr, Field, BaseModel

from diario_unico.entity.info_cobranca import InfoCobranca
from diario_unico.entity.item_documento import ItemDocumento
from diario_unico.enum.documentos.documento_origem import DocumentoOrigem
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.enum.documentos.tipo_iss import TipoIss
from diario_unico.enum.documentos.tipo_tributacao_servico import TipoTributacaoServico
from diario_unico.enum.sinal import Sinal
from diario_unico.enum.situacao import Situacao


class Documento(BaseModel):
    id: Optional[UUID]
    estabelecimento: UUID
    participante: UUID
    token_facilitador: Optional[UUID]
    cnae: constr(min_length=7, max_length=7, strip_whitespace=True)
    discriminacao: Optional[constr(min_length=1, max_length=200)]
    municipio_prestacao: Optional[constr(min_length=7, max_length=7, strip_whitespace=True)]
    numero: constr(min_length=1, max_length=20, strip_whitespace=True)
    serie: Optional[constr(min_length=1, max_length=3, strip_whitespace=True)]
    subserie: Optional[constr(min_length=1, max_length=3, strip_whitespace=True)]
    tipo_tributacao_servico: TipoTributacaoServico = TipoTributacaoServico.NENHUM
    tipoIss: TipoIss = TipoIss.RETIDO
    emissao: date
    data_registro: datetime = Field(default_factory=datetime.now)
    modelo: constr(min_length=1, max_length=10, strip_whitespace=True)
    tenant: int
    sinal: Sinal
    situacao: Situacao
    origem: DocumentoOrigem
    tipo: DocumentoTipo
    infos_cobranca : List[Optional[InfoCobranca]]

    itens: List[ItemDocumento] = list()
