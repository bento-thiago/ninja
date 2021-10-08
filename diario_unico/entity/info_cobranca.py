from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from diario_unico.entity.endereco import Endereco
from diario_unico.enum.info_cobranca.situacao_info_cobranca import SituacaoInfoCobranca


class InfoCobranca(BaseModel):
    id: Optional[UUID]
    vencimento: Optional[date]
    data_limite_desconto: Optional[date]
    data_inicio_multa: Optional[date]
    percentual_desconto: Optional[float]
    percentual_multa: Optional[float]
    percentual_juros_diario: Optional[float]
    valor_bruto: Optional[float]
    valor_liquido: Optional[float]
    texto_instrucao: Optional[str]
    situacao: Optional[SituacaoInfoCobranca]
    cpf_cnpj_cliente: Optional[str]
    nome_cliente: Optional[str]
    documento_id: Optional[UUID]
    numero: Optional[int]
    nosso_numero: Optional[str]
    endereco_cidade: Optional[str]
    email: Optional[str]
    tenant:int
