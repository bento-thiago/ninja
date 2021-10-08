from decimal import Decimal
from uuid import UUID

from pydantic import constr, BaseModel

from diario_unico.entity.lancamento import Lancamento

from diario_unico.entity.confins_retido_acumulado import CONFINSRetidoAcumulado
from diario_unico.entity.csll_retido_acumulado import CSLLRetidoAcumulado
from diario_unico.entity.icms_retido_acumulado import ICMSRetidoAcumulado
from diario_unico.entity.irrf_retido_acumulado import IRRFRetidoAcumulado
from diario_unico.entity.iss_retido_acumulado import ISSRetidoAcumulado
from diario_unico.entity.pis_retido_acumulado import PISRetidoAcumulado

from typing import List, Optional

from diario_unico.enum.documentos.item_documento_tipo_tributacao_iss import ItemDocumentoTipoTributacaoIss


class ItemDocumento(BaseModel):
    codigo: constr(min_length=1, max_length=40, strip_whitespace=True)
    descricao: constr(min_length=1, max_length=200, strip_whitespace=True)
    tipo_tributacao_iss: ItemDocumentoTipoTributacaoIss
    valor: Decimal
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
    recorrente: Optional[bool]
    id: Optional[UUID]
    documento_id: Optional[UUID]
    lancamentos: Optional[List[Lancamento]] = list()
    ordem: int
