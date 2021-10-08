from diario_unico.entity.lancamento import SituacaoDiario
from diario_unico.enum.codigo_contabil_financeiro import CodigoContabilFinanceiro
from diario_unico.enum.pasta_contabil import PastaContabil
from nasajon.pastas_contabeis.pastas_router import MomentoContabil


class DefinicaoLancamento:
    def __init__(self, momento, tipo, numero, ordem, natureza, conta,
                 historico, formula, formula_data, situacao, pasta_contabil, codigo_contabil_financeiro):
        self.tipo: int = tipo
        self.numero: int = numero
        self.ordem: int = ordem
        self.natureza: str = natureza
        self.conta: str = conta
        self.historico: str = historico
        self.formula: str = formula
        self.formula_data: str = formula_data
        self.situacao: SituacaoDiario = SituacaoDiario(situacao)
        self.pasta_contabil: PastaContabil = PastaContabil(pasta_contabil)
        self.momento: MomentoContabil = MomentoContabil(momento)
        self.codigo_contabil_financeiro: CodigoContabilFinanceiro = CodigoContabilFinanceiro(codigo_contabil_financeiro)
