import hashlib
from diario_unico.enum.info_pagamento.situacao_info_pagamento import SituacaoInfoPagamento

class DefinicaoInfoPagamento:
    def __init__(self, numero_lancamento=None, formula_vencimento=None, situacao=None):
        self.numero_lancamento: int = numero_lancamento
        self.formula_vencimento: str = formula_vencimento
        self.situacao: SituacaoInfoPagamento = situacao
