from enum import Enum

from diario_unico.entity.entity_codigo_contabil_financeiro import EntityCodigoContabilFinanceiro


class CodigoContabilFinanceiro(Enum):
    CLIENTES_A_RECEBER = "CLIENTES_A_RECEBER"
    ISS_RECUPERAR = "ISS_RECUPERAR"
    PIS_RECUPERAR = "PIS_RECUPERAR"
    COFINS_RECUPERAR = "COFINS_RECUPERAR"
    CSLL_RECUPERAR = "CSLL_RECUPERAR"
    IRRF_RECUPERAR = "IRRF_RECUPERAR"
    INSS_RECUPERAR = "INSS_RECUPERAR"
    RECEITA_PRESTACAO_SERVICO = "RECEITA_PRESTACAO_SERVICO"
    CAIXA = "CAIXA"

