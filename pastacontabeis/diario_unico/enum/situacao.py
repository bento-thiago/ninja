import enum

class Situacao(enum.Enum):
    # Situação
    REALIZADO = 'REALIZADO'
    QUITADO = 'QUITADO'
    PREVISTO = 'PREVISTO'
    REJEITADO = 'REJEITADO'