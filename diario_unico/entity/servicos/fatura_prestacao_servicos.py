from datetime import datetime, date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, constr, Field

from diario_unico.entity.info_cobranca import InfoCobranca
from diario_unico.entity.pessoa import Pessoa
from diario_unico.entity.servicos.item_fatura_prestacao_servicos import ItemFaturaPrestacaoServicos
from diario_unico.enum.documentos.tipo_iss import TipoIss
from diario_unico.enum.documentos.tipo_tributacao_servico import TipoTributacaoServico
from diario_unico.enum.situacao import Situacao


class FaturaPrestacaoServicos(BaseModel):
    estabelecimento: UUID
    participante: Pessoa
    token_facilitador: Optional[UUID]
    cnae: constr(min_length=7, max_length=7, strip_whitespace=True)
    discriminacao: Optional[constr(min_length=1, max_length=500)]
    municipio_prestacao: constr(min_length=7, max_length=7, strip_whitespace=True)
    numero: Optional[constr(min_length=1, max_length=20, strip_whitespace=True)]
    serie: Optional[constr(min_length=1, max_length=3, strip_whitespace=True)]
    subserie: Optional[constr(min_length=1, max_length=3, strip_whitespace=True)]
    tipo_tributacao_servico: TipoTributacaoServico = TipoTributacaoServico.NENHUM
    tipoIss: TipoIss = TipoIss.RETIDO
    situacao: Optional[Situacao]
    id: Optional[UUID]
    infos_cobranca: List[InfoCobranca] = list()

    emissao: date = Field(default_factory=datetime.today)
    data_registro: datetime = Field(default_factory=datetime.now)
    itens: List[ItemFaturaPrestacaoServicos] = list()

    @property
    def valor_servicos(self):
        valor_servicos = 0
        for item in self.itens:
            valor_servicos += item.valor

        return valor_servicos

    @property
    def valor_liquido(self):
        valor_liquido = 0
        for item in self.itens:
            valor_liquido += item.valor_liquido

        return valor_liquido
