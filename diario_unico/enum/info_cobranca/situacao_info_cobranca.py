from enum import Enum

class SituacaoInfoCobranca(Enum):
    PREVISTO = "PREVISTO"
    PENDENTE = "PENDENTE"
    AGENDADO = "AGENDADO"
    ABERTO = "ABERTO"
    QUITADO = "QUITADO"
    ERRO = "ERRO"
    REJEITADO = "REJEITADO"