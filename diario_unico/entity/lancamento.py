from datetime import date
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from diario_unico.entity.info_cobranca import InfoCobranca
from diario_unico.entity.info_pagamento import InfoPagamento
from diario_unico.entity.partida import Partida
from diario_unico.enum.lancamento.lancamento_natureza import LancamentoNatureza


class SituacaoDiario(Enum):
    REALIZADO = 'REALIZADO'
    PREVISTO = 'PREVISTO'
    REJEITADO = 'REJEITADO'


class Lancamento(BaseModel):
    id: Optional[UUID]
    numero: Optional[int]
    data: Optional[date]
    situacao: Optional[SituacaoDiario]
    partidas: Optional[List[Partida]] = list()
    info_cobranca: Optional[UUID]

    def valor(self):
        return sum([partida.valor for partida in self.partidas if partida.natureza == LancamentoNatureza.D])
