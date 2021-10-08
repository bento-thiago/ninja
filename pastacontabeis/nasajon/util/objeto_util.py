from typing import get_type_hints, List, Dict
import importlib
from datetime import date, datetime


class ObjetosUtils:

    def dictToObject(self, dados: dict, classe: type):
        nome_modulo = classe.__module__
        nome_classe = classe.__name__
        modulo = importlib.import_module(nome_modulo)
        saida = getattr(modulo, nome_classe)()
        if not isinstance(dados, dict):
            dados = dados.__dict__
        for key in dados:
            if hasattr(saida, key):
                # Tratamento de datas
                if (isinstance(dados[key], str)):
                    try:
                        data = datetime.strptime(dados[key], '%d/%m/%Y').date()
                        setattr(saida, key, data)
                    except:
                        try:
                            datahora = datetime.strptime(
                            dados[key], '%d/%m/%Y %H:%M:%S')
                            setattr(saida, key, datahora)
                        except:
                            try:
                                data = datetime.strptime(
                                    dados[key], '%Y-%m-%dT%H:%M:%S')
                                setattr(saida, key, data)
                            except:
                                setattr(saida, key, dados[key])
                 # Verifica se esse atributo eh outro objeto, criado pela nasajon, e que tambem devera ser convertido
                elif (isinstance(dados[key], dict)):
                    if (key in get_type_hints(saida.__class__)):
                        if('nasajon' in get_type_hints(saida.__class__)[key].__module__) or ('diario_unico' in get_type_hints(saida.__class__)[key].__module__):
                            setattr(saida, key, self.dictToObject(
                                dados[key], get_type_hints(saida)[key]))
                        else:
                            setattr(saida, key, dados[key])
                    else:
                        raise Exception(
                            "Erro interno: "+nome_classe+"."+key+" precisa ter Type Hint")
                elif isinstance(dados[key], list):
                    if (key in get_type_hints(saida.__class__)):
                        if('nasajon' in get_type_hints(saida.__class__)[key].__args__[0].__module__) or ('diario_unico' in get_type_hints(saida.__class__)[key].__args__[0].__module__):
                            nova_lista = list()
                            for elem in dados[key]:
                                nova_lista.append(self.dictToObject(
                                    elem, get_type_hints(saida)[key].__args__[0]))
                            setattr(saida, key, nova_lista)
                        else:
                            setattr(saida, key, dados[key])
                    else:
                        raise Exception(
                            "Erro interno: "+nome_classe+"."+key+" precisa ter Type Hint")
                else:
                    setattr(saida, key, dados[key])
        return saida

    def validar_range_percentagem(self, dados: dict, campo, campo_referencia, percentagem_superior, percentagem_inferior):
        if not isinstance(dados, dict):
            dados: dict = dados.__dict__
        if not campo in dados:
            return
        valor = dados[campo]
        if valor == None:
            return
        if valor == 0:
            return

        if not campo_referencia in dados:
            return
        valor_referencia = dados[campo_referencia]
        if valor_referencia == None:
            return
        if valor_referencia == 0:
            return

        percentagem = (valor*100)/valor_referencia

        if percentagem > percentagem_superior:
            raise Exception("Percentagem de "+campo +
                            " é maior do que o limite superior permitido de "+percentagem_superior)
        if percentagem < percentagem_inferior:
            raise Exception("Percentagem de "+campo +
                            " é maior do que o limite superior permitido de "+percentagem_inferior)
