import enum


class ItemContratoSituacao(enum.Enum):
    ATIVO = 'ATIVO'
    INATIVO = 'INATIVO'
    AGUARDANDO_ATIVACAO = 'AGUARDANDO_ATIVACAO'
