from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, constr

from diario_unico.entity.lancamento import Lancamento
from diario_unico.enum.documentos.item_documento_tipo_tributacao_iss import ItemDocumentoTipoTributacaoIss


class ItemFaturaPrestacaoServicos(BaseModel):
    id: Optional[UUID]
    ordem:int
    documento_id: Optional[UUID]
    codigo: constr(min_length=1, max_length=40, strip_whitespace=True)
    descricao: constr(min_length=1, max_length=200, strip_whitespace=True)
    tipo_tributacao_iss: ItemDocumentoTipoTributacaoIss
    valor: Decimal
    base_iss: Decimal
    aliquota_iss: Decimal
    iss_retido: Decimal
    base_irrf: Decimal
    aliquota_irrf: Decimal
    irrf_retido: Decimal
    base_inss: Decimal
    incidencia_inss: Decimal
    inss_retido: Decimal
    base_csll: Decimal
    aliquota_csll: Decimal
    csll_retido: Decimal
    base_pis: Decimal
    aliquota_pis: Decimal
    pis_retido: Decimal
    base_cofins: Decimal
    aliquota_cofins: Decimal
    cofins_retido: Decimal
    recorrente: bool
    lancamentos: Optional[List[Lancamento]] = list()

    @property
    def valor_deducoes(self):
        valor = self.iss_retido + self.irrf_retido + self.inss_retido + self.pis_retido + self.cofins_retido + self.csll_retido

        return valor

    @property
    def valor_liquido(self):
        valor = self.valor - self.valor_deducoes
        return valor
