class EntityCodigoContabilFinanceiro:
    def __init__(self, codigo: str, descricao: str):
        self.codigo = codigo
        self.descricao = descricao

    def __str__(self):
        return self.codigo
