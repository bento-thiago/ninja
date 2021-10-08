from nasajon.pastas_contabeis.pastas_router import MomentoContabil
from nasajon.util.lancamento_util import LancamentosUtil
from diario_unico.entity.documento import Documento
from diario_unico.enum.situacao import Situacao
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.entity.imposto_retido_acumulado import ImpostoRetidoAcumulado
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from typing import List
from abc import ABC, abstractmethod
from nasajon.util.diario_util import DiarioUtil
from nasajon.entity.guia import Guia
from typing import Dict
from diario_unico.entity.lancamento import SituacaoDiario
from datetime import date
import calendar
from diario_unico.entity.item_documento import ItemDocumento
from diario_unico.enum.documentos.item_documento_tipo_imposto import ItemDocumentoTipoImposto
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from diario_unico.enum.sinal import Sinal



class PastaImpostoComRetencao(ABC):
    tipo_documento_retencao: DocumentoTipo
    imposto: ItemDocumentoTipoImposto

    def retencao_do_periodo(self, configuracoes: dict):
        """
        Método padrão para renteção de impostos de terceiros
        O dict configuracoes pode variar entre diferentes impostos. 
        """

        impostos: List[dict] = DiarioUtil().recuperar_impostos_diario(
            self.imposto,
            configuracoes["tenant"],
            configuracoes["ano"],
            configuracoes["mes"]
        )

        guias: Dict['estabelecimento:str', Guia] = dict()
        for imposto in impostos:
            if not imposto.estabelecimento in guias:
                guias[imposto.estabelecimento] = Guia()
                guias[imposto.estabelecimento].estabelecimento = imposto.estabelecimento

            dados_lancamentos = dict()

            guia = guias[imposto.estabelecimento]
            guia.ano = configuracoes["ano"]
            guia.mes = configuracoes["mes"]
            guia.estabelecimento = imposto.estabelecimento
            # TODO Esta situação fixa em previsto está correto?
            guia.situacao = Situacao.PREVISTO

            dados_lancamentos["valor_calculado"] = self.calcular_retencao(
                imposto, configuracoes)
            dados_lancamentos["competencia_inicial"] = guia.competencia_inicial
            dados_lancamentos["competencia_final"] = guia.competencia_final

            if SituacaoDiario(imposto.situacao) == SituacaoDiario.REALIZADO:
                def_lancamentos = self.get_definicoes_lancamentos_escrituracao_futura_parte_realizada(
                    configuracoes)
                lancamentos = LancamentosUtil().criar_lancamentos(
                    dados_lancamentos, def_lancamentos, None, None)
                guia.lancamentos_sobre_doc_realizados += lancamentos

                continue

            if SituacaoDiario(imposto.situacao) == SituacaoDiario.PREVISTO:
                def_lancamentos = self.get_definicoes_lancamentos_escrituracao_futura_parte_prevista(
                    configuracoes)
                lancamentos = LancamentosUtil().criar_lancamentos(
                    dados_lancamentos, def_lancamentos, None, None)
                guia.lancamentos_sobre_doc_previstos += lancamentos

                continue

        for guia in guias:
            documento = self.guia_para_documento(guias[guia])
            DiarioUtil().escriturar_antecipadamente_documento(
                configuracoes["tenant"], documento)

    @abstractmethod
    def calcular_retencao(self, imposto_acumulado: ImpostoRetidoAcumulado, configuracoes):
        pass

    @abstractmethod
    def get_definicoes_lancamentos_escrituracao_futura_parte_realizada(self, configuracoes) -> List[DefinicaoLancamento]:
        pass

    @abstractmethod
    def get_definicoes_lancamentos_escrituracao_futura_parte_prevista(self, configuracoes) -> List[DefinicaoLancamento]:
        pass

    def guia_para_documento(self, guia: Guia) -> Documento:
        saida = Documento()
        saida.ano = guia.ano
        saida.competencia_inicial = guia.competencia_inicial
        saida.competencia_final = guia.competencia_final
        saida.data_entrada = date.today()
        saida.data_lancamento = saida.competencia_final
        saida.emissao = date.today()
        saida.sinal = Sinal.ENTRADA
        saida.numero = str(1)
        saida.estabelecimento = guia.estabelecimento
        saida.participante = 'GOVERNO'
        saida.situacao = guia.situacao
        saida.tipo = self.tipo_documento_retencao
        saida.valor = guia.valor_total()
        item = ItemDocumento()
        item.codigo = self.imposto.value["codigo"]
        item.descricao = self.imposto.value["codigo"]
        item.tipo = ItemDocumentoTipo.GUIA_IMPOSTO_RETIDO
        item.valor = saida.valor
        item.lancamentos = list()
        item.lancamentos = item.lancamentos + guia.lancamentos_sobre_doc_previstos
        item.lancamentos = item.lancamentos + guia.lancamentos_sobre_doc_realizados
        saida.itens.append(item)
        return saida
