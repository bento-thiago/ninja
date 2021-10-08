import enum


class TipoItemCotaCondominial(enum.Enum):
    AGUA: enum.Enum = 'ÁGUA'
    COTA_CONDOMINIAL: enum.Enum = 'COTA_CONDOMINIAL'
    ENERGIA_ELETRICA: enum.Enum = 'ENERGIA_ELÉTRICA'
    GAS: enum.Enum = 'GÁS'
    FUNDO_OBRAS: enum.Enum = 'FUNDO_DE_OBRAS'
    FUNDO_RESERVA: enum.Enum = 'FUNDO_DE_RESERVA'
    MULTAS: enum.Enum = 'MULTAS'
    GARAGEM: enum.Enum = 'GARAGEM'
    OUTROS: enum.Enum = 'OUTROS'