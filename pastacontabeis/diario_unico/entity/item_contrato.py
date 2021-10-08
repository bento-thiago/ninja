from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, PositiveInt, constr

from diario_unico.enum.contratos.contrato_tipo_cobranca import ContratoTipoCobranca
from diario_unico.enum.contratos.contrato_tipo_recorrencia import ContratoTipoRecorrencia
from diario_unico.enum.contratos.item_contrato_situacao import ItemContratoSituacao


class ItemContrato(BaseModel):
    id: Optional[UUID]
    id_servico: UUID
    valor_unitario: Decimal
    quantidade: Decimal
    valor_total: Decimal
    recorrente: bool
    registro_contrato_id: Optional[UUID]
    codigo_item_contrato: constr(min_length=1, max_length=40, strip_whitespace=True)
    codigo_servico: constr(min_length=1, max_length=40, strip_whitespace=True)
    descricao: constr(min_length=1, max_length=200, strip_whitespace=True)
    situacao: ItemContratoSituacao

    competencia_inicio: date
    competencia_final: Optional[date]
    dia_processamento: PositiveInt
    tipo_recorrencia: ContratoTipoRecorrencia
    tipo_cobranca: ContratoTipoCobranca
    dia_vencimento: PositiveInt
    dias_antes_vencimento_para_desconto: int = 0
    dias_apos_vencimento_para_multa: int = 0
    dias_apos_vencimento_para_juros: int = 0

    incidencia_inss: Decimal
    aliquota_inss: Decimal
    aliquota_ir: Decimal
    aliquota_pis: Decimal
    aliquota_cofins: Decimal
    aliquota_csll: Decimal
