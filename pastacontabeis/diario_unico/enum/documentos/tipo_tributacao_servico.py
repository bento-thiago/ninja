from enum import Enum

class TipoTributacaoServico(Enum):
    NENHUM = "NENHUM"
    TRIBUTACAO_NO_MUNICIPIO = "TRIBUTACAO_NO_MUNICIPIO"
    TRIBUTACAO_FORA_DO_MUNICIPIO = "TRIBUTACAO_FORA_DO_MUNICIPIO"
    OPERACAO_ISENTA = "OPERACAO_ISENTA"
    OPERACAO_IMUNE = "OPERACAO_IMUNE"
    OPERACAO_SUSPENSA_POR_DECISAO_JUDICIAL = "OPERACAO_SUSPENSA_POR_DECISAO_JUDICIAL"
    OPERACAO_SUSPENSA_POR_DECISAO_ADMINISTRATIVA = "OPERACAO_SUSPENSA_POR_DECISAO_ADMINISTRATIVA"