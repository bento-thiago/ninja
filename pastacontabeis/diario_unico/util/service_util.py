def verificaPropriedadesObjetoEntrada(campos_obrigatorios: list, dados: dict):
    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] == None:
            return [False, "Propriedade faltando no objeto: " + campo]
    return [True, '']
