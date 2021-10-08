import uuid
from decimal import Decimal
from typing import List

from diario_unico.entity.info_cobranca import InfoCobranca
from diario_unico.entity.info_pagamento import InfoPagamento
from diario_unico.entity.lancamento import Lancamento
from diario_unico.entity.partida import Partida
from nasajon.entity.dados_cobranca import Dados_Cobranca
from nasajon.entity.definicao_info_cobranca import DefinicaoInfoCobranca
from nasajon.entity.definicao_info_pagamento import DefinicaoInfoPagamento
from nasajon.entity.definicao_lancamento import DefinicaoLancamento


class LancamentosUtil():

    def criar_lancamentos(self, dados: object, definicoes: List[DefinicaoLancamento],
                          definicao_info_pagamento: DefinicaoInfoPagamento = None,
                          definicao_info_cobranca: DefinicaoInfoCobranca = None) -> List[Lancamento]:
        if not isinstance(dados, dict):
            dados = dados.__dict__
        saida = list()
        dict_lancamentos = dict()
        for definicao_lancamento in definicoes:
            lancamento: Lancamento = dict_lancamentos.setdefault(
                definicao_lancamento.numero, self.criar_lancamento(dados, definicao_lancamento))

            lancamento.partidas.append(
                self.criar_partida(dados, definicao_lancamento))

            if (definicao_info_pagamento != None) and (definicao_info_pagamento.numero_lancamento == lancamento.numero):
                lancamento.info_pagamento = self.criar_info_pagamento(
                    dados, definicao_info_pagamento)



        for key in dict_lancamentos.keys():
            saida.append(dict_lancamentos[key])

        return saida

    def criar_partida(self, dados: object, definicao: DefinicaoLancamento) -> Partida:
        saida = dict()
        saida["conta_contabil"] = definicao.conta
        saida["historico"] = eval(f'f"{definicao.historico}"', dados)
        saida["natureza"] = definicao.natureza
        saida["ordem"] = definicao.ordem
        saida["valor"] = Decimal(eval(definicao.formula, dados))
        saida["momento"] = definicao.momento
        saida["pasta_contabil"] = definicao.pasta_contabil
        saida["codigo_contabil_financeiro"] = definicao.codigo_contabil_financeiro
        return Partida.parse_obj(saida)
        return saida

    def criar_lancamento(self, dados: object, definicao: DefinicaoLancamento) -> Lancamento:
        saida = Lancamento()
        saida.data = eval(definicao.formula_data, dados)
        saida.numero = definicao.numero
        saida.situacao = definicao.situacao
        return saida

    def criar_info_pagamento(self, dados: object, definicao_info_pagamento: DefinicaoInfoPagamento) -> InfoPagamento:
        saida = InfoPagamento()
        saida.situacao = definicao_info_pagamento.situacao
        saida.vencimento = eval(
            definicao_info_pagamento.formula_vencimento, dados)
        return saida

    def criar_info_cobranca(self, dados: object, definicao_info_cobranca: DefinicaoInfoCobranca,
                            dados_cobranca: Dados_Cobranca, tenant:int) -> InfoCobranca:
        if not isinstance(dados_cobranca, dict):
            dados_cobranca = dados_cobranca.__dict__

        saida = InfoCobranca(tenant=tenant)
        saida.vencimento = eval(definicao_info_cobranca.origem_vencimento, dados)
        saida.data_inicio_multa = eval(definicao_info_cobranca.origem_data_inicio_multa, dados)
        saida.data_limite_desconto = eval(definicao_info_cobranca.origem_data_limite_desconto, dados)
        saida.percentual_juros_diario = eval(definicao_info_cobranca.origem_percentual_juros_diario, dados)
        saida.percentual_desconto = eval(definicao_info_cobranca.origem_percentual_desconto, dados)
        saida.percentual_multa = eval(definicao_info_cobranca.origem_percentual_multa, dados)
        saida.valor_bruto = eval(definicao_info_cobranca.origem_valor_bruto, dados)
        saida.valor_liquido = eval(definicao_info_cobranca.origem_valor_liquido, dados)
        saida.texto_instrucao = eval(definicao_info_cobranca.origem_texto_instrucao, dados)


        participante = eval(definicao_info_cobranca.origem_participante, dados)

        saida.cpf_cnpj_cliente = participante.cpf_cnpj
        saida.nome_cliente = participante.razao_social

        saida.email = participante.contato_cobranca.email

        saida.situacao = definicao_info_cobranca.situacao

        return saida

    def gerar_info_cobranca(self, dados: dict, lista_info_cobranca: List[InfoCobranca], lancamentos: List[Lancamento],
                            definicao_info_cobranca: DefinicaoInfoCobranca, tenant:int):
        if not isinstance(dados, dict):
            dados = dados.__dict__
        info_cobranca = self.criar_info_cobranca(
            dados, definicao_info_cobranca, dados.get("dados_cobranca", None), tenant)
        lista_info_cobranca.append(info_cobranca)
        info_cobranca.id = uuid.uuid4()
        for lancamento in lancamentos:
            if lancamento.numero==definicao_info_cobranca.lancamento_numero:
                lancamento.info_cobranca = info_cobranca.id

