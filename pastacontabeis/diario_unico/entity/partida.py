from decimal import Decimal

from pydantic import BaseModel, constr
from typing import List, Optional

from diario_unico.enum.codigo_contabil_financeiro import CodigoContabilFinanceiro
from diario_unico.enum.lancamento.lancamento_natureza import LancamentoNatureza
from diario_unico.enum.pasta_contabil import PastaContabil
from nasajon.pastas_contabeis.pastas_router import MomentoContabil


class Partida(BaseModel):
    natureza: LancamentoNatureza
    ordem: int
    conta_contabil: str
    historico: str
    valor: Decimal
    base: Optional[Decimal]
    percentagem_sobre_base: Optional[float]
    momento: MomentoContabil
    pasta_contabil: PastaContabil
    codigo_contabil_financeiro: CodigoContabilFinanceiro
