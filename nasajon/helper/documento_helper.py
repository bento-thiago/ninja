from diario_unico.entity.documento import Documento
from diario_unico.enum.lancamento.lancamento_natureza import LancamentoNatureza
from time_service.service.time_service import TimeService
from typing import List
from datetime import date
from diario_unico.entity.lancamento import Lancamento
from diario_unico.entity.lancamento import SituacaoDiario
from diario_unico.entity.partida import Partida
from diario_unico.entity.info_cobranca import InfoCobranca
from diario_unico.entity.info_pagamento import InfoPagamento
from enum import Enum
import numbers


class DocumentoHelper:

    def validarLancamentos(self, documento: Documento, permite_lancamento_em_caixa_no_passado: bool):
        for item in documento.itens:
            for lancamento in item.lancamentos:
                valor_total = 0
                for partida in lancamento.partidas:
                    if partida.natureza == LancamentoNatureza.C:
                        valor_total = valor_total + partida.valor
                    else:
                        valor_total = valor_total + ((-1) * partida.valor)

                    if (partida.conta_contabil == '1.1.1.01') and (not permite_lancamento_em_caixa_no_passado) and (lancamento.data < TimeService.now().date()):
                        raise Exception(
                            'Nao sao permitidos lancamentos em caixa no passado')

                if (valor_total != 0):
                    raise Exception(
                        'lancamento aberto com diferenca de: R$ ' + str(valor_total))

    def validarCamposObrigatorios(self, dados: dict, campos_obrigatorios: List[str]):
        if campos_obrigatorios == None:
            campos_obrigatorios = Documento.campos_obrigatorios

        subcampos_de_atributos = dict()
        campos_da_propria_entidade = list()
        if not isinstance(dados, dict):
            dados = dados.__dict__

        # Alguns objetos podem ter atributos que sao outros objetos. Essa função irá separar essas informações
        # para posteriormente chamar a si mesma de forma recursiva para esses objetos filhos
        for campo in campos_obrigatorios:
            if "." in campo:
                atributo = campo.split(".")[0]
                subcampo = campo.split(".")[1]
                if not atributo in subcampos_de_atributos:
                    subcampos_de_atributos[atributo] = list()
                subcampos_de_atributos[atributo].append(subcampo)
            else:
                campos_da_propria_entidade.append(campo)

        # Valida campos da propria entidade
        for campo in campos_da_propria_entidade:
            if not((campo in dados) and (dados[campo] != None)):
                raise Exception(
                    'Informacao obrigatoria nao preenchida: '+campo)

        # Recursao para atributos que sao classes
        for atributo in subcampos_de_atributos:
            if (atributo in dados) and (dados[atributo] != None):
                if isinstance(dados[atributo], list):
                    for elem in dados[atributo]:
                        self.validarCamposObrigatorios(
                            elem, subcampos_de_atributos[atributo])
                else:
                    self.validarCamposObrigatorios(
                        dados[atributo], subcampos_de_atributos[atributo])

    def validarCamposPermitidos(self, dados: dict, campos_permitidos: list):
        if campos_permitidos == None:
            return

        subcampos_de_atributos = dict()
        campos_da_propria_entidade = list()
        if not isinstance(dados, dict):
            dados = dados.__dict__

        # Alguns objetos podem ter atributos que sao outros objetos. Essa função irá separar essas informações
        # para posteriormente chamar a si mesma de forma recursiva para esses objetos filhos
        for campo in campos_permitidos:
            if "." in campo:
                atributo = campo.split(".")[0]
                subcampo = campo.split(".")[1]
                if not atributo in subcampos_de_atributos:
                    subcampos_de_atributos[atributo] = list()
                subcampos_de_atributos[atributo].append(subcampo)
            else:
                campos_da_propria_entidade.append(campo)

        # Valida campos da propria entidade
        for campo in dados:
            if (not campo in campos_da_propria_entidade) and (dados[campo] != None):
                raise Exception('Informacao nao permitida: '+campo)

        # Recursao para atributos que sao classes
        for atributo in subcampos_de_atributos:
            if (atributo in dados) and (dados[atributo] != None):
                if isinstance(dados[atributo], list):
                    for elem in dados[atributo]:
                        self.validarCamposPermitidos(
                            elem, subcampos_de_atributos[atributo])
                else:
                    self.validarCamposPermitidos(
                        dados[atributo], subcampos_de_atributos[atributo])

    def validarTipo(self, entidade, campo, tipo_esperado):
        if (entidade == None) or (getattr(entidade, campo) == None):
            return
        elif isinstance(getattr(entidade, campo), Enum):
            if not isinstance(getattr(entidade, campo).value, tipo_esperado):
                raise Exception("ERRO: "+campo+" deve ser do tipo "+str(tipo_esperado) +
                                ". Contudo o tipo recebido foi "+str(campo.__class__)+" com o valor: "+str(campo))
        elif not isinstance(getattr(entidade, campo), tipo_esperado):
            raise Exception("ERRO: "+campo+" deve ser do tipo "+str(tipo_esperado)+". Contudo o tipo recebido foi " +
                            str(getattr(entidade, campo).__class__)+" com o valor: "+str(getattr(entidade, campo)))

    def validarTipos(self, documento: Documento):
        import decimal
        NumberTypes = (int, float, complex, numbers.Real, decimal.Decimal)
        self.validarTipo(documento, "token_facilitador", str)
        self.validarTipo(documento, "tipo", str)
        self.validarTipo(documento, "documento", str)
        self.validarTipo(documento, "numero", str)
        self.validarTipo(documento, "ano", int)
        self.validarTipo(documento, "modelo", str)
        self.validarTipo(documento, "data_lancamento", date)
        self.validarTipo(documento, "emissao", date)
        self.validarTipo(documento, "competencia_inicial", date)
        self.validarTipo(documento, "competencia_final", date)
        self.validarTipo(documento, "cfop", str)
        self.validarTipo(documento, "situacao", str)
        self.validarTipo(documento, "data_entrada", date)
        self.validarTipo(documento, "tipo_ligacao", int)
        self.validarTipo(documento, "grupo_tensao", str)
        self.validarTipo(documento, "origem", str)
        self.validarTipo(documento, "codigo_consumo", int)
        self.validarTipo(documento, "serie", str)
        self.validarTipo(documento, "subserie", str)
        self.validarTipo(documento, "estabelecimento", str)
        self.validarTipo(documento, "empresa", str)
        self.validarTipo(documento, "grupo_empresarial", str)
        self.validarTipo(documento, "participante", str)
        self.validarTipo(documento, "usuario", str)
        self.validarTipo(documento, "codigo_barras", str)
        self.validarTipo(documento, "url_documento", str)
        self.validarTipo(documento, "data_criacao", date)
        self.validarTipo(documento, "identificador_contrato", str)
        self.validarTipo(documento, "itens", list)
        for item in documento.itens:
            self.validarTipo(item, "item_documento", str)
            self.validarTipo(item, "documento", str)
            self.validarTipo(item, "codigo", str)
            self.validarTipo(item, "descricao", str)
            self.validarTipo(item, "tipo", str)
            self.validarTipo(item, "valor", NumberTypes)
            self.validarTipo(item, "valor_consumo", NumberTypes)
            self.validarTipo(item, "icms_retido_original", NumberTypes)
            self.validarTipo(item, "icms_retido", NumberTypes)
            self.validarTipo(item, "base_icms_retido_original", NumberTypes)
            self.validarTipo(item, "base_icms_retido", NumberTypes)
            self.validarTipo(item, "aliquota_icms_retido", NumberTypes)
            self.validarTipo(item, "pis_retido_original", NumberTypes)
            self.validarTipo(item, "pis_retido", NumberTypes)
            self.validarTipo(item, "base_pis_retido_original", NumberTypes)
            self.validarTipo(item, "base_pis_retido", NumberTypes)
            self.validarTipo(item, "aliquota_pis_retido", NumberTypes)
            self.validarTipo(item, "cofins_retido_original", NumberTypes)
            self.validarTipo(item, "cofins_retido", NumberTypes)
            self.validarTipo(item, "base_cofins_retido_original", NumberTypes)
            self.validarTipo(item, "base_cofins_retido", NumberTypes)
            self.validarTipo(item, "aliquota_cofins_retido", NumberTypes)
            self.validarTipo(item, "csll_retido_original", NumberTypes)
            self.validarTipo(item, "csll_retido", NumberTypes)
            self.validarTipo(item, "base_csll_retido_original", NumberTypes)
            self.validarTipo(item, "base_csll_retido", NumberTypes)
            self.validarTipo(item, "aliquota_csll_retido", NumberTypes)
            self.validarTipo(item, "irrf_retido_original", NumberTypes)
            self.validarTipo(item, "irrf_retido", NumberTypes)
            self.validarTipo(item, "base_irrf_retido_original", NumberTypes)
            self.validarTipo(item, "base_irrf_retido", NumberTypes)
            self.validarTipo(item, "aliquota_irrf_retido", NumberTypes)
            self.validarTipo(item, "iss_retido_original", NumberTypes)
            self.validarTipo(item, "iss_retido", NumberTypes)
            self.validarTipo(item, "base_iss_retido_original", NumberTypes)
            self.validarTipo(item, "base_iss_retido", NumberTypes)
            self.validarTipo(item, "aliquota_iss_retido", NumberTypes)
            self.validarTipo(item, "lancamentos", list)
            self.validarTipo(item, "rubrica", str)
            self.validarTipo(item, "rubrica_esocial", str)
            self.validarTipo(item, "trabalhador", str)
            self.validarTipo(item, "departamento", str)
            self.validarTipo(item, "lotacao", str)
            for lancamento in item.lancamentos:
                self.validarTipo(lancamento, "numero", int)
                self.validarTipo(lancamento, "data", date)
                self.validarTipo(lancamento, "situacao", str)
                self.validarTipo(lancamento, "info_pagamento", InfoPagamento)
                self.validarTipo(lancamento, "info_cobranca", InfoCobranca)
                self.validarTipo(lancamento, "partidas", list)
                for partida in lancamento.partidas:
                    self.validarTipo(partida, "natureza", str)
                    self.validarTipo(partida, "ordem", int)
                    self.validarTipo(partida, "conta_contabil", str)
                    self.validarTipo(partida, "historico", str)
                    self.validarTipo(partida, "valor", NumberTypes)
                    self.validarTipo(partida, "base", NumberTypes)
                    self.validarTipo(
                        partida, "percentagem_sobre_base", NumberTypes)
                    self.validarTipo(partida, "definicao", str)
                    self.validarTipo(partida, "centro_custo", int)
