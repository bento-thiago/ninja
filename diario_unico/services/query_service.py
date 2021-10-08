from typing import List, Dict
from diario_unico.entity.informacoes_a_recuperar import InformacoesARecuperar
from diario_unico.entity.filtro import Filtro
from nasajon.util.objeto_util import ObjetosUtils
from nasajon.util.json_util import JsonUtil


class QueryService():

    def __init__(self):
        self.list_alias: List[str] = []
        self.dict_alias_count: Dict[str, int] = {}

    def recuperacamposSelectDocumento(self, array_informacoes_a_recuperar: List[InformacoesARecuperar]) -> list:
        saida = list()
        for informacoes_a_recuperar in array_informacoes_a_recuperar:

            if (informacoes_a_recuperar.entidade == 'Documento'):
                for campo in informacoes_a_recuperar.campos:
                    saida = self.adicionaEmVetorComAlias(
                        saida, QueryEnum.camposcorrespondentes["Documento"][campo], 'documento')

            if (informacoes_a_recuperar.entidade == 'Item'):
                saida = self.adicionaEmVetorComAlias(
                    saida, QueryEnum.camposcorrespondentes["Documento"]["documento"], 'documento')

        return saida

    def recuperacamposSelectDiarioUnico(self, array_informacoes_a_recuperar) -> list:
        saida = list()

        for informacoes_a_recuperar in array_informacoes_a_recuperar:
            if (informacoes_a_recuperar.entidade == 'Documento'):
                for campo in informacoes_a_recuperar.campos:
                    saida = self.adicionaEmVetorComAlias(
                        saida, QueryEnum.camposcorrespondentes["Documento"][campo], 'diario_unico')

            if (informacoes_a_recuperar.entidade == 'Item'):
                saida = self.adicionaEmVetorComAlias(
                    saida, QueryEnum.camposcorrespondentes["Item"]["item_documento"], 'diario_unico')

                for campo in informacoes_a_recuperar.campos:
                    saida = self.adicionaEmVetorComAlias(
                        saida, QueryEnum.camposcorrespondentes["Item"][campo], 'diario_unico')

            if (informacoes_a_recuperar.entidade == 'Lancamento'):
                saida = self.adicionaEmVetorComAlias(
                    saida, QueryEnum.camposcorrespondentes["Item"]["item_documento"], 'diario_unico')
                saida = self.adicionaEmVetorComAlias(
                    saida, QueryEnum.camposcorrespondentes["Lancamento"]["numero"], 'diario_unico')

                for campo in informacoes_a_recuperar.campos:
                    saida = self.adicionaEmVetorComAlias(
                        saida, QueryEnum.camposcorrespondentes["Lancamento"][campo], 'diario_unico')

        return saida

    def filtroUsaDiarioUnico(self, filtro: Filtro):
        _filtro = JsonUtil().toDict(filtro)
        if (not "campo" in _filtro) or (_filtro["campo"] == None):
            for parametro in _filtro["parametros"]:
                if (self.filtroUsaDiarioUnico(parametro)):
                    return True
        else:
            return _filtro["entidade"] == "Item" or _filtro["entidade"] == "Lancamento"
        return False

    def converteFiltroEmSQL(self, filtro: Filtro, dicionario: dict) -> tuple([str, dict]):
        if filtro == None:
            return '(true)', dict()

        if filtro.entidade != None:
            alias = self.obtemAlias(
                (QueryEnum.camposcorrespondentes[filtro.entidade][filtro.campo]))

        if (filtro.operacao == "Igual"):
            sql = "( " + \
                (QueryEnum.camposcorrespondentes[filtro.entidade][filtro.campo])
            sql += " = "
            sql += ":" + alias+")"
            params = dict()
            params[alias] = self.consomeDicionario(
                filtro.entidade, filtro.campo, filtro.parametros[0], dicionario)
            return sql, params

        if (filtro.operacao == "Maior"):
            sql = "( " + \
                (QueryEnum.camposcorrespondentes[filtro.entidade][filtro.campo])
            sql += " > "
            sql += ":" + alias+")"
            params = dict()
            params[alias] = self.consomeDicionario(
                filtro.entidade, filtro.campo, filtro.parametros[0], dicionario)
            return sql, params

        if (filtro.operacao == "Menor"):
            sql = "( " + \
                (QueryEnum.camposcorrespondentes[filtro.entidade][filtro.campo])
            sql += " < "
            sql += ":" + alias+")"
            params = dict()
            params[alias] = self.consomeDicionario(
                filtro.entidade, filtro.campo, filtro.parametros[0], dicionario)
            return sql, params

        if (filtro.operacao == "Maior_Ou_Igual"):
            sql = "( " + \
                (QueryEnum.camposcorrespondentes[filtro.entidade][filtro.campo])
            sql += " >= "
            sql += ":" + alias+")"
            params = dict()
            params[alias] = self.consomeDicionario(
                filtro.entidade, filtro.campo, filtro.parametros[0], dicionario)
            return sql, params

        if (filtro.operacao == "Menor_Ou_Igual"):
            sql = "( " + \
                (QueryEnum.camposcorrespondentes[filtro.entidade][filtro.campo])
            sql += " <= "
            sql += ":" + alias+")"
            params = dict()
            params[alias] = self.consomeDicionario(
                filtro.entidade, filtro.campo, filtro.parametros[0], dicionario)
            return sql, params

        if (filtro.operacao == "Diferente"):
            sql = "( " + \
                (QueryEnum.camposcorrespondentes[filtro.entidade][filtro.campo])
            sql += " <> "
            sql += ":" + alias+")"
            return sql, self.consomeDicionario(filtro.entidade, filtro.campo, filtro.parametros[0], dicionario)

        if (filtro.operacao == "Entre"):
            sql = "( " + \
                (QueryEnum.camposcorrespondentes[filtro.entidade][filtro.campo])
            sql += " between  "
            sql += ":" + alias+"_menor"
            sql += " and "
            sql += ":" + alias+"_maior"+")"

            params = dict()
            params[alias +
                   "_menor"] = self.consomeDicionario(filtro.entidade, filtro.campo, filtro.parametros[0], dicionario)
            params[alias +
                   "_maior"] = self.consomeDicionario(filtro.entidade, filtro.campo, filtro.parametros[1], dicionario)
            return sql, params

        if (filtro.operacao == "Esta_Contido_Em"):
            sql = "(" + \
                QueryEnum.camposcorrespondentes[filtro.entidade][filtro.campo]
            sql += " in "
            sql += alias+" )"
            params = dict()
            params[alias] = tuple(filtro.parametros)
            return sql, params

        if (filtro.operacao == "And"):
            filtro.parametros = [ObjetosUtils().dictToObject(
                parametro, Filtro) for parametro in filtro.parametros]
            sql = "( "
            subFiltros = list()
            params = dict()
            for parametro in filtro.parametros:
                subFiltro, subParams = self.converteFiltroEmSQL(
                    parametro, dicionario)
                subFiltros.append(subFiltro)
                params.update(subParams)

            sql += " and ".join(subFiltros) + " )"
            return sql, params

        if (filtro.operacao == "Or"):
            filtro.parametros = [ObjetosUtils().dictToObject(
                parametro, Filtro) for parametro in filtro.parametros]
            sql = "( "
            subFiltros = list()
            params = dict()
            for parametro in filtro.parametros:
                subFiltro, subParams = self.converteFiltroEmSQL(
                    parametro, dicionario)
                subFiltros.append(subFiltro)
                params.update(subParams)

            sql += " or ".join(subFiltros) + " )"
            return sql, params

        return " True ", []

    def adicionaEmVetorComAlias(self, array, elemento, tabela):
        # recebe como parâmetro o campo a ser adicionado, e o nome de uma tabela cujos campos estao sendo adicionados
        # Só adiciona o campo no array se esse campo for dessa tabela específica
        if tabela in elemento:
            return self.adicionaEmVetor(array, elemento + ' as ' + self.obtemAlias(elemento))
        else:
            return array

    def consomeDicionario(self, entidade, campo, parametro, dicionario: dict):
        """
        Essa funcao serve para resolver a conversao entre GUID <--> Codigo
        Por exemplo, usar um filtro do tipo Estabelecimento = 'NASAJON'.
        Como a query deve ser realizada usando o GUID, será consumido um dicionário, a ser recebido por parâmetro, haverá a conversão
        Caso não seja um campo que deve ser tratado assim (Ex: ano = 2020), então a função retornará exatamente o que recebeu
        params:
            entidade: Entidade a ser filtrada. Exemplo: Para o Estabelecimento de um Documento, será 'Documento'
            campo: Campo da entidade que contém a informação a ser convertida. Para Estabelecimento de um Documento, será 'Estabelecimento'.
            parametro: O valor em sí da informação. no exemplo acima, será 'NASAJON'
            dicionario: Dicionario de dados para o de-para
            Exemplo de dicionario:
                {
                    "Documento":{
                                    "Estabelecimento": {
                                                            "Nasajon" : "GUID1"
                                                            "SUPORTEK": "GUID2"
                                                        },
                                    "Participante": {
                                                        "Pessoa 1": "GUID3"
                                                        "Pessoa 2": "GUID4"
                                                    }
                                    }
                                }
                }
        """
        valor = parametro
        # Remove áspas em volta. Feito por retro-compatibilidade com rotas que precisavam colocar áspas em volta de Strings no Filtro
        if (isinstance(parametro, str)):
            if parametro.startswith("'") and parametro.endswith("'"):
                valor = parametro[1:len(parametro)-1]
        if entidade in dicionario:
            if campo in dicionario[entidade]:
                if (valor in dicionario[entidade][campo]):
                    return dicionario[entidade][campo][valor]
        return valor

    def obtemAlias(self, campo: str):
        alias = campo.replace(".", "___")

        if alias in self.list_alias:
            self.list_alias.append(str(alias))

            if alias in self.dict_alias_count:
                self.dict_alias_count[alias] += 1
                alias = alias + "_" + str(self.dict_alias_count[alias])
            else:
                self.dict_alias_count[alias] = 1
                alias = alias + "_" + str(1)
        else:
            self.list_alias.append(str(alias))

        return alias

    def adicionaEmVetor(self, vetor, elemento):
        if not elemento in vetor:
            vetor.append(elemento)
        return vetor


class QueryEnum:
    camposcorrespondentes = {
        "Documento": {
            "documento": "documento.documento",
            "tipo": "documento.tipo",
            "numero": "documento.numero",
            "ano": "documento.ano",
            "sinal": "documento.sinal",
            "modelo": "documento.modelo",
            "data_lancamento": "documento.data_lancamento",
            "emissao": "documento.emissao",
            "competencia_inicial": "documento.competencia_inicial",
            "competencia_final": "documento.competencia_final",
            "cfop": "documento.cfop",
            "situacao": "documento.situacao",
            "valor": "documento.valor",
            "data_entrada": "documento.data_entrada",
            "tipo_ligacao": "documento.tipo_ligacao",
            "origem": "documento.origem",
            "codigo_consumo": "documento.codigo_consumo",
            "serie": "documento.serie",
            "subserie": "documento.subserie",
            "grupo_tensao": "documento.grupo_tensao",
            "estabelecimento": "documento.estabelecimento",
            "empresa": "documento.empresa",
            "grupo_empresarial": "documento.grupo_empresarial",
            "participante": "documento.participante",
            "usuario": "documento.usuario",
            "codigo_barras": "diario_unico.codigo_barras",
            "data_criacao": "documento.data_criacao",
            "url_documento": "documento.url_documento",
            "identificador_contrato": "documento.identificador_contrato",
        },
        "Item": {
            "item_documento": "diario_unico.item_documento",
            "documento": "diario_unico.documento",
            "codigo": "diario_unico.codigo",
            "descricao": "diario_unico.descricao",
            "tipo": "diario_unico.diario_unico_tipo",
            "valor": "diario_unico.valor",
            "valor_icms": "diario_unico.valor",
            "base_icms": "diario_unico.base",
            "aliquota_icms": "diario_unico.percentagem_sobre_base",
            "valor_pis": "diario_unico.valor",
            "base_pis": "diario_unico.base",
            "aliquota_pis": "diario_unico.percentagem_sobre_base",
            "valor_cofins": "diario_unico.valor",
            "base_cofins": "diario_unico.base",
            "aliquota_cofins": "diario_unico.percentagem_sobre_base",
            "valor_desconto": "diario_unico.valor",
            "valor_icms_st": "diario_unico.valor",
            "base_icms_st": "diario_unico.base",
            "aliquota_icms_st": "diario_unico.percentagem_sobre_base",
            "valor_consumo": "diario_unico.valor",
            "rubrica": "diario_unico.rubrica",
            "rubrica_esocial": "diario_unico.rubrica_esocial",
            "trabalhador": "diario_unico.trabalhador",
            "departamento": "diario_unico.departamento",
            "lotacao": "diario_unico.lotacao",
        },
        "Lancamento": {
            "numero": "diario_unico.numero_lancamento",
            "ordem": "diario_unico.ordem_lancamento",
            "conta_contabil": "diario_unico.conta_contabil",
            "historico": "diario_unico.historico_lancamento",
            "valor": "diario_unico.valor",
            "definicao": "diario_unico.definicao_lancamento",
            "natureza": "diario_unico.natureza_lancamento",
            "data": "diario_unico.data",
            "situacao": "diario_unico.situacao",
        }
    }
