from dateutil import relativedelta

from nasajon.pastas_contabeis.abstract_pasta_contabil import AbstractPastaContabil
from nasajon.pastas_contabeis.abstract_pasta_contabil_composta import AbstractPastaContabilComposta
from nasajon.pastas_contabeis.pastas_router import MomentoContabil

from nasajon.entity.conta_consumo import ContaConsumo
from nasajon.entity.dados_escrituracao_futura import DadosEscrituracaoFutura, DadosItem, ValoresAnteriores
from nasajon.enum.heuristica_projecao import HeuristicaProjecao
from nasajon.entity.definicao_info_pagamento import DefinicaoInfoPagamento
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from diario_unico.entity.documento import Documento
from diario_unico.enum.situacao import Situacao
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.entity.item_documento import ItemDocumento
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from diario_unico.entity.lancamento import Lancamento
from diario_unico.enum.info_pagamento.situacao_info_pagamento import SituacaoInfoPagamento
from diario_unico.enum.info_cobranca.situacao_info_cobranca import SituacaoInfoCobranca

from nasajon.util.diario_util import DiarioUtil
from nasajon.util.json_util import JsonUtil
from nasajon.util.lancamento_util import LancamentosUtil
from nasajon.util.objeto_util import ObjetosUtils
from time_service.service.time_service import TimeService
from nasajon.pastas_contabeis.pasta_quitacao_padrao import PastaQuitacaoPadrao
from nasajon.pastas_contabeis.pasta_recorrente import PastaRecorrente
from abc import abstractmethod
from typing import List

import datetime
import enum
from diario_unico.entity.documento import Sinal


class PastaContaConsumo(PastaRecorrente, AbstractPastaContabilComposta, PastaQuitacaoPadrao):

    def __init__(self, diario_util: DiarioUtil):
        super().__init__(diario_util)

        self.documento_tipo = DocumentoTipo.CONTA_CONSUMO
        self.item_tipo = ItemDocumentoTipo.ITEM_CONTA_CONSUMO
        self.item_descricao = 'Conta de Consumo'

    def simular(self, dados: dict):
        # TODO: O módulo de orçamentos será feito no futuro
        pass

    def faturar(self, dados: dict):
        # TODO: O módulo de contas de consumo nao tem faturamento
        pass

    def escriturar_futuro(self, dados: DadosEscrituracaoFutura):
        """
        dados:
            Parâmetros para realizar a escrituração antecipada
        """
        dados = ObjetosUtils().dictToObject(dados, DadosEscrituracaoFutura)

        # Recuperando os lançamentos para os próximos 12 meses (por item):
        dict_lancamentos = self._projecao_util.gerar_lancamentos_projecao(
            dados, self)

        # Iterando os lançamentos por mês
        for data in dict_lancamentos:
            # Recuperando os lançamentos do mês em questão:
            lancamentos = dict_lancamentos[data][dados.itens[0].codigo]

            # Montando o objeto da conta de consumo:
            conta = ContaConsumo()
            conta.estabelecimento = dados.estabelecimento
            conta.vencimento = data.replace(day=dados.dia_vencimento)
            conta.valor = lancamentos.dados.valor
            conta.fornecedor_cnpj = dados.participante
            conta.emissao = data.replace(day=dados.dia_apropriacao)
            conta.situacao = Situacao.PREVISTO
            conta.numero = 1

            # Instanciando a entidade genérica de documento:
            documento = self.conta_consumo_para_documento(
                conta, lancamentos.vetor_lancamentos, self.item_tipo, self.item_descricao)

            # Inserindo a previsão no diário unico:
            self._diario_util.escriturar_antecipadamente_documento(
                dados.tenant, documento)
        return documento

    def get_dados_escrituracao_futura(self, dados: dict):
        """
        Parâmetros:
        - dados: Informações repassadas pelo responsável do agendamento da escrituração futura (normalmente: job de previsão).
            dia_apropriacao
            dia_vencimento
            estabelecimento
            fornecedor
            tenant
            heuristica_valor
            valor

        Return:
        - Deve retornar dados suficientes para a escrituração futura desta pasta contábil, sem necessidade de novas consultas ao diário ou ao banco de dados.
        """

        dados_previsao = DadosEscrituracaoFutura()
        dados_previsao.dia_apropriacao = dados["dia_apropriacao"]
        dados_previsao.dia_vencimento = dados["dia_vencimento"]
        dados_previsao.estabelecimento = dados["estabelecimento"]
        dados_previsao.participante = dados["fornecedor"]
        dados_previsao.tenant = dados["tenant"]

        item = DadosItem()
        item.valores_anteriores = self._diario_util.recuperar_ultimo_trimestre(
            dados["tenant"], dados, TimeService.now(), "Documento", self.documento_tipo)
        item.codigo = "1"
        item.heuristica_projecao = HeuristicaProjecao(
            dados["heuristica_valor"])
        item.tipo = "1"
        item.valor_medio_inicial = dados["valor"]

        dados_previsao.itens = list()
        dados_previsao.itens.append(item)

        return dados_previsao

    # @abstractmethod
    # def get_tipo_documento(self) -> DocumentoTipo:
    #     pass

    def apropriar(self, dados: dict):
        """
        dados:
            dict com os campos da entity conta_consumo + o campo tenant
        """
        # Primeiro, convertemos o dicionario de dados de entrada para uma Conta de Consumo
        conta_consumo: ContaConsumo = ObjetosUtils().dictToObject(
            dados, ContaConsumo)

        # Depois, buscamos as definicoes de lancamentos e de info pagamento referentes a apropriacao
        definicoes_lancamentos = self.get_definicoes_lancamentos_apropriacao()
        definicao_info_pagamento = self.get_definicao_info_pagamento_apropriacao()

        # Usa-se o LancamentosUtil() para criar um list de model de lancamentos a partir das definicoes
        lancamentos = LancamentosUtil().criar_lancamentos(
            conta_consumo, definicoes_lancamentos, definicao_info_pagamento)

        # Criamos um model de Documento baseado na conta de consumo e nos lancamentos. Passamos por parametros
        # enumerados sobre o tipo de documento(eletricidade, agua, gas) e a descricao
        documento = self.conta_consumo_para_documento(
            conta_consumo, lancamentos, self.item_tipo, self.item_descricao)

        # Invoco o diário para persistir os dados
        self._diario_util.apropriar_documento(dados["tenant"], documento)
        return documento

    def quitar(self, dados: dict):
        """
        dados:
            informações suficientes para a quitação do documento
        """
        return self.quitar_padrao(dados)

    def cancelar(self, dados: dict):
        # TODO: O módulo de cancelamentos será feito no futuro
        pass

    def get_definicoes_lancamentos(self, momento: MomentoContabil):
        if momento == MomentoContabil.ESCRITURACAO_FUTURA.value:
            return self.get_definicoes_lancamentos_escrituracao_futura()
        elif momento == MomentoContabil.APROPRIACAO.value:
            return self.get_definicoes_lancamentos_apropriacao()
        elif momento == MomentoContabil.QUITACAO.value:
            return self.get_definicoes_lancamentos_quitacao()

    def get_dados_simulacao(self, dados: dict):
        # TODO
        pass

    def get_dados_faturamento(self, dados: dict):
        # TODO
        pass

    def get_dados_apropriacao(self, dados: dict):
        return dados

    def get_dados_cancelamento(self, dados: dict):
        # TODO
        pass

    def get_dados_quitacao(self, dados: dict):
        return self.get_dados_quitacao_padrao(dados)

    def get_definicoes_lancamentos_escrituracao_futura_item(self, tipo_item):
        """
        A pasta de contas de consumo não é por item, mas se utiliza do utilitário de projeção, o qual trabalha por item.

        Assim, este método é implementado como um adpater, para transitar entre as realidades com e sem itens.
        """
        return self.get_definicoes_lancamentos_escrituracao_futura()

    @abstractmethod
    def get_definicoes_lancamentos_escrituracao_futura(self) -> List[DefinicaoLancamento]:
        pass

    @abstractmethod
    def get_definicoes_lancamentos_apropriacao(self) -> List[DefinicaoLancamento]:
        pass

    @abstractmethod
    def get_definicoes_lancamentos_quitacao(self) -> List[DefinicaoLancamento]:
        pass

    # def get_definicoes_info_pagamento_escrituracao_futura_item(self, tipo_item):
    #     """
    #     A pasta de contas de consumo não é por item, mas se utiliza do utilitário de projeção, o qual trabalha por item.

    #     Assim, este método é implementado como um adpater, para transitar entre as realidades com e sem itens.
    #     """
    #     return self.get_definicoes_info_pagamento_escrituracao_futura()

    def get_definicoes_info_pagamento_escrituracao_futura(self):
        return DefinicaoInfoPagamento(
            numero_lancamento=2,
            formula_vencimento="vencimento",
            situacao=SituacaoInfoPagamento.PREVISTO
        )

    def get_definicao_info_pagamento_apropriacao(self):
        return DefinicaoInfoPagamento(
            numero_lancamento=2,
            formula_vencimento="vencimento",
            situacao=SituacaoInfoPagamento.PENDENTE
        )

    def get_definicao_info_pagamento_quitacao(self):
        return DefinicaoInfoPagamento(
            numero_lancamento=1,
            formula_vencimento="data_pagamento",
            situacao=SituacaoInfoPagamento.QUITADO
        )

    def conta_consumo_para_documento(self, conta_consumo: ContaConsumo, lancamentos: List[Lancamento],
                                     item_tipo: int, descricao_item: str) -> Documento:
        saida = Documento()
        saida.estabelecimento = str(conta_consumo.estabelecimento)
        saida.numero = str(conta_consumo.numero)
        saida.sinal = Sinal.ENTRADA
        saida.data_lancamento = conta_consumo.vencimento
        saida.ano = conta_consumo.vencimento.year
        saida.codigo_barras = conta_consumo.codigo_barras
        saida.valor = conta_consumo.valor
        saida.participante = str(conta_consumo.fornecedor_cnpj)
        saida.emissao = conta_consumo.emissao
        if (conta_consumo.vencimento == None):
            saida.data_lancamento = conta_consumo.emissao
            saida.ano = conta_consumo.emissao.year
        saida.codigo_consumo = conta_consumo.codigo_consumo
        saida.url_documento = conta_consumo.url_documento
        saida.grupo_tensao = conta_consumo.grupo_tensao
        saida.situacao = conta_consumo.situacao
        saida.identificador_contrato = conta_consumo.identificador_contrato
        saida.tipo = self.documento_tipo.value

        item = ItemDocumento()
        item.codigo = '01'
        item.valor = conta_consumo.valor
        item.tipo = item_tipo
        item.descricao = descricao_item
        item.lancamentos = lancamentos
        saida.itens.append(item)
        return saida
