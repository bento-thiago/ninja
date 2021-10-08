from diario_unico.enum.contas_contabeis.conta_contabil_natureza import ContaContabilNatureza
from diario_unico.enum.contas_contabeis.grupo_conta_contabil import GrupoContaContabil

class ContaContabil:
    """
    Classe que representa uma conta do plano de contas contábil.
    """

    def __init__(
        self,
        codigo: str = None,
        natureza: ContaContabilNatureza = None,
        nome: str = None,
        grupo: GrupoContaContabil = None,
        conta_pai: str = None
    ):
        self.codigo: str = codigo
        self.natureza: ContaContabilNatureza = natureza
        self.nome: str = nome
        self.grupo: GrupoContaContabil = grupo
        self.conta_pai: str = conta_pai
