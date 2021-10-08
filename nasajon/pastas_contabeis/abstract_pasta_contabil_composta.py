from abc import ABC, abstractmethod


class AbstractPastaContabilComposta(ABC):
    """
    Representa uma interface para pastas contábeis cuja escrituração futura seja projetada por item (e não pelo documento unicamente).
    """

    @abstractmethod
    def get_definicoes_lancamentos_escrituracao_futura_item(self, tipo_item):
        pass
