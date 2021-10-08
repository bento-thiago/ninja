import datetime
import enum
from typing import List

from diario_unico.entity.lancamento import SituacaoDiario
from diario_unico.entity.servicos.fatura_prestacao_servicos import FaturaPrestacaoServicos
from diario_unico.enum.codigo_contabil_financeiro import CodigoContabilFinanceiro
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from diario_unico.enum.documentos.item_documento_tipo_imposto import ItemDocumentoTipoImposto
from diario_unico.enum.info_cobranca.situacao_info_cobranca import SituacaoInfoCobranca
from diario_unico.enum.info_pagamento.situacao_info_pagamento import SituacaoInfoPagamento
from diario_unico.enum.lancamento.lancamento_natureza import LancamentoNatureza
from diario_unico.enum.pasta_contabil import PastaContabil
from diario_unico.enum.situacao import Situacao
from nasajon.entity.dados_cobranca import Dados_Cobranca
from nasajon.entity.dados_faturamento import DadosFaturamento
from nasajon.entity.definicao_info_cobranca import DefinicaoInfoCobranca
from nasajon.entity.definicao_info_pagamento import DefinicaoInfoPagamento
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from nasajon.pastas_contabeis.abstract_pasta_contabil import AbstractPastaContabil
from nasajon.pastas_contabeis.pasta_quitacao_padrao import PastaQuitacaoPadrao
from nasajon.pastas_contabeis.pastas_router import MomentoContabil
from nasajon.util.diario_util import DiarioUtil
from nasajon.util.json_util import JsonUtil
from nasajon.util.lancamento_util import LancamentosUtil
from nasajon.util.objeto_util import ObjetosUtils


class PastaPrestacaoServicos(AbstractPastaContabil, PastaQuitacaoPadrao):
    """
        Pasta Contábil referente a operações relacionadas com a prestação de serviços


    """

    def __init__(self, diario_util: DiarioUtil):
        super().__init__(diario_util, PastaContabil.PRESTACAO_DE_SERVICOS)

        self.documento_tipo: enum.Enum = DocumentoTipo.FATURA_PRESTACAO_SERVICOS
        self.item_tipo = ItemDocumentoTipo.SERVICO
        self.item_descricao = 'Serviço'

    def simular(self, dados: dict):
        # TODO: O módulo de orçamentos será feito no futuro
        pass

    def escriturar_futuro(self, dados):
        """
        TODO: Ainda não há escrituração futura para fatura_prestacao_servicos
        """
        pass

    def faturar(self, dados: DadosFaturamento):
        """
        Nao Aplicável
        """
        pass

    def get_dados_escrituracao_futura(self, dados: dict):
        """
        TODO: Ainda não há escrituração futura para fatura_prestacao_servicos
        """
        pass

    def apropriar(self, dados: dict):
        """
        dados:
            dict com os campos da entity fatura_prestacao_servicos + o campo tenant
        """
        # Primeiro, convertemos o dicionario de dados de entrada para uma fatura_prestacao_servicos
        fatura_prestacao_servicos = dados["fatura_prestacao_servicos"]

        dados_cobranca = dados["dados_cobranca"]

        """ dados_cobranca = dados["dados_cobranca"] """

        # Obtemos as regras para a criação dos lançamentos envolvidos
        definicoes_lancamentos = self.get_definicoes_lancamentos_apropriacao()

        # Depois, buscamos as definicoes de lancamentos e de cobranças referentes a apropriacao
        # Para notas de prestação de serviço, pode ser importante verificar se será cobrado 
        # "pela nota" ou "pelo contrato". Se for "pelo contrato" não faz sentido preencher aqui
        deve_gerar_titulo_para_esta_nota_especifica = True
        if deve_gerar_titulo_para_esta_nota_especifica:
            definicao_info_cobranca = self.get_definicao_info_cobranca_apropriacao()
        else:
            definicao_info_cobranca = None

        # Prepara dicionario de dados que será usado para a criação dos lançamentos
        for item in fatura_prestacao_servicos.itens:
            dados_lanc = {"fatura_prestacao_servicos": fatura_prestacao_servicos, "item": item,
                          "dados_cobranca": dados_cobranca}

            item.lancamentos = LancamentosUtil().criar_lancamentos(
                dados_lanc, definicoes_lancamentos, None, definicao_info_cobranca)

        LancamentosUtil().gerar_info_cobranca(dados_lanc,
                                              fatura_prestacao_servicos.infos_cobranca,
                                              sum([item.lancamentos for item in fatura_prestacao_servicos.itens], []),
                                              definicao_info_cobranca,
                                              dados["tenant"])

        # Invoco o diário para persistir os dados
        self._diario_util.apropriar_fatura_prestacao_servicos(dados["tenant"], fatura_prestacao_servicos)

        # Retorna o documento tratado
        return fatura_prestacao_servicos

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
        # Não há faturamento para fatura_prestacao_servicos
        return dados

    def get_dados_apropriacao(self, dados: dict):
        return dados

    def get_dados_cancelamento(self, dados: dict):
        # TODO
        pass

    def get_dados_quitacao(self, dados: dict):
        # TODO
        return self.get_dados_quitacao_padrao(dados)

    def get_definicoes_lancamentos_apropriacao(self) -> List[DefinicaoLancamento]:
        saida = list()
        # valor do item com retenções
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza=LancamentoNatureza.D,
            conta='placeholder',
            historico='Valor ref. a prestação de serviços - {fatura_prestacao_servicos.numero} - {fatura_prestacao_servicos.participante.nome_fantasia}',
            formula='item.valor - item.iss_retido - item.pis_retido - item.cofins_retido - item.csll_retido - item.irrf_retido - item.inss_retido',
            formula_data='fatura_prestacao_servicos.emissao',
            situacao=SituacaoDiario.REALIZADO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.CLIENTES_A_RECEBER
        ))
        # ISS Retido
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza=LancamentoNatureza.D,
            conta='placeholder',
            historico='Valor ref. a retenção do imposto ' + ItemDocumentoTipoImposto.ISS.name + ' em prestação de serviços - {fatura_prestacao_servicos.numero} - {fatura_prestacao_servicos.participante.nome_fantasia}',
            formula='item.iss_retido',
            formula_data='fatura_prestacao_servicos.emissao',
            situacao=SituacaoDiario.REALIZADO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.ISS_RECUPERAR
        ))
        # PIS Retido
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=3,
            natureza=LancamentoNatureza.D,
            conta='placeholder',
            historico='Valor ref. a retenção do imposto ' + ItemDocumentoTipoImposto.PIS.name + ' em prestação de serviços - {fatura_prestacao_servicos.numero} - {fatura_prestacao_servicos.participante.nome_fantasia}',
            formula='item.pis_retido',
            formula_data='fatura_prestacao_servicos.emissao',
            situacao=SituacaoDiario.REALIZADO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.PIS_RECUPERAR
        ))
        # COFINS Retido
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=4,
            natureza=LancamentoNatureza.D,
            conta='placeholder',
            historico='Valor ref. a retenção do imposto ' + ItemDocumentoTipoImposto.COFINS.name + ' em prestação de serviços - {fatura_prestacao_servicos.numero} - {fatura_prestacao_servicos.participante.nome_fantasia}',
            formula='item.cofins_retido',
            formula_data='fatura_prestacao_servicos.emissao',
            situacao=SituacaoDiario.REALIZADO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.COFINS_RECUPERAR
        ))
        # CSLL Retido
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=5,
            natureza=LancamentoNatureza.D,
            conta='placeholder',
            historico='Valor ref. a retenção do imposto ' + ItemDocumentoTipoImposto.CSLL.name + ' em prestação de serviços - {fatura_prestacao_servicos.numero} - {fatura_prestacao_servicos.participante.nome_fantasia}',
            formula='item.csll_retido',
            formula_data='fatura_prestacao_servicos.emissao',
            situacao=SituacaoDiario.REALIZADO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.CSLL_RECUPERAR
        ))
        # IRRF Retido
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=6,
            natureza=LancamentoNatureza.D,
            conta='placeholder',
            historico='Valor ref. a retenção do imposto ' + ItemDocumentoTipoImposto.IRRF.name + ' em prestação de serviços - {fatura_prestacao_servicos.numero} - {fatura_prestacao_servicos.participante.nome_fantasia}',
            formula='item.irrf_retido',
            formula_data='fatura_prestacao_servicos.emissao',
            situacao=SituacaoDiario.REALIZADO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.IRRF_RECUPERAR
        ))
        # INSS Retido
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=7,
            natureza=LancamentoNatureza.D,
            conta='placeholder',
            historico='Valor ref. a retenção do imposto INSS em prestação de serviços - {fatura_prestacao_servicos.numero} - {fatura_prestacao_servicos.participante.nome_fantasia}',
            formula='item.inss_retido',
            formula_data='fatura_prestacao_servicos.emissao',
            situacao=SituacaoDiario.REALIZADO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.INSS_RECUPERAR
        ))
        # Receita de venda (valor bruto do item)
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=8,
            natureza=LancamentoNatureza.C,
            conta='placeholder',
            historico='Valor de receita de prestação de serviços - {fatura_prestacao_servicos.numero} - {fatura_prestacao_servicos.participante.nome_fantasia}',
            formula='item.valor',
            formula_data='fatura_prestacao_servicos.emissao',
            situacao=SituacaoDiario.REALIZADO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.RECEITA_PRESTACAO_SERVICO
        ))

        ###Lançamentos de quitação

        # valor do item com retenções
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.QUITACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=1,
            natureza=LancamentoNatureza.D,
            conta='placeholder',
            historico='Valor ref. a prestação de serviços - {fatura_prestacao_servicos.numero} - {fatura_prestacao_servicos.participante.nome_fantasia}',
            formula='item.valor_liquido',
            formula_data='dados_cobranca.vencimento',
            situacao=SituacaoDiario.PREVISTO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.CAIXA
        ))
        # ISS Retido
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.QUITACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=2,
            natureza=LancamentoNatureza.C,
            conta='placeholder',
            historico='Valor ref. a prestação de serviços - {fatura_prestacao_servicos.numero} - {fatura_prestacao_servicos.participante.nome_fantasia}',
            formula='item.valor_liquido',
            formula_data='dados_cobranca.vencimento',
            situacao=SituacaoDiario.PREVISTO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.CLIENTES_A_RECEBER
        ))
        return saida

    def get_definicoes_lancamentos_escrituracao_futura(self) -> List[DefinicaoLancamento]:
        saida = list()
        return saida

    def get_definicoes_lancamentos_quitacao(self) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=1,
            natureza=LancamentoNatureza.D,
            conta='placeholder',
            historico='Recebimento em caixa da prestação de serviços',
            formula='item.valor',
            formula_data='dados_cobranca.vencimento',
            situacao=SituacaoDiario.REALIZADO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.CAIXA
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=2,
            natureza=LancamentoNatureza.C,
            conta='placeholder',
            historico='Prestação de serviços recebida de cliente',
            formula='item.valor',
            formula_data='dados_cobranca.vencimento',
            situacao=SituacaoDiario.REALIZADO,
            pasta_contabil=self.pasta_contabil,
            codigo_contabil_financeiro=CodigoContabilFinanceiro.CLIENTES_A_RECEBER
        ))
        return saida

    def get_definicao_info_cobranca_apropriacao(self):
        return DefinicaoInfoCobranca(
            lancamento_numero=2,
            origem_data_inicio_multa='dados_cobranca.data_inicio_multa',
            origem_data_limite_desconto='dados_cobranca.data_limite_desconto',
            origem_percentual_juros_diario='dados_cobranca.percentual_juros_diario',
            origem_percentual_multa='dados_cobranca.percentual_multa',
            origem_percentual_desconto='dados_cobranca.percentual_desconto',
            origem_valor_liquido='fatura_prestacao_servicos.valor_liquido',
            origem_valor_bruto='fatura_prestacao_servicos.valor_servicos',
            origem_valor_sacado='fatura_prestacao_servicos.valor_liquido',
            origem_vencimento='dados_cobranca.vencimento',
            origem_texto_instrucao='dados_cobranca.texto_instrucao',
            origem_participante='fatura_prestacao_servicos.participante',
            origem_endereco='fatura_prestacao_servicos.participante.endereco_cobranca',
            origem_contato_cobranca='fatura_prestacao_servicos.participante.contato_cobranca',
            situacao=SituacaoInfoCobranca.PREVISTO
        )

    def get_definicao_info_pagamento_quitacao(self):
        return DefinicaoInfoPagamento(
            numero_lancamento=1,
            formula_vencimento="data_pagamento",
            situacao=SituacaoInfoPagamento.QUITADO
        )

    def validar_percentagem_imposto(self, nota: FaturaPrestacaoServicos):
        ObjetosUtils().validar_range_percentagem(nota, "pis_retido", "valor", 5, 0)
        ObjetosUtils().validar_range_percentagem(nota, "cofins_retido", "valor", 5, 0)
        ObjetosUtils().validar_range_percentagem(nota, "csll_retido", "valor", 2, 0)
        ObjetosUtils().validar_range_percentagem(nota, "irrf_retido", "valor", 28, 0)
        ObjetosUtils().validar_range_percentagem(nota, "iss_retido", "valor", 15, 0)


if __name__ == '__main__':
    from diario_unico.entity.servicos.fatura_prestacao_servicos import FaturaPrestacaoServicos
    from diario_unico.entity.servicos.item_fatura_prestacao_servicos import ItemFaturaPrestacaoServicos
    from diario_unico.entity.pessoa import Pessoa
    from diario_unico.enum.pessoas.pessoa_origem_informacoes import PessoaOrigemInformacoes
    from diario_unico.enum.pessoas.pessoa_qualificacao import PessoaQualificacao
    from diario_unico.enum.pessoas.pessoa_tipo_simples import PessoaTipoSimples
    from diario_unico.enum.documentos.item_documento_tipo_tributacao_iss import ItemDocumentoTipoTributacaoIss
    from diario_unico.entity.endereco import Endereco
    from diario_unico.entity.contato import Contato
    from diario_unico.enum.endereco.uf import UF

    # Exemplo 1
    entrada = dict()
    fatura_prestacao_servicos_entrada = FaturaPrestacaoServicos(estabelecimento="36ccf228-d7fb-4b90-ae10-84a810eab744",
                                                                token_facilitador=None,
                                                                cnae="1234567",
                                                                numero=1,
                                                                serie=None,
                                                                emissao=datetime.date(2021, 9, 1),
                                                                municipio_prestacao='2253364',
                                                                base_iss=1000,
                                                                iss_retido=0,
                                                                base_irrf=1000,
                                                                irrf_retido=0,
                                                                base_inss=1000,
                                                                inss_retido=0,
                                                                base_pis=1000,
                                                                pis_retido=0,
                                                                base_cofins=1000,
                                                                cofins_retido=0,
                                                                base_csll=1000,
                                                                csll_retido=0,
                                                                participante=Pessoa(cpf_cnpj='05642157000134',
                                                                                    codigo='COPLAN',
                                                                                    nome_fantasia='COPLAN CONTABILIDADE PLANEJAMENTO ASSESSORIA LTDA',
                                                                                    razao_social='COPLAN CONTABILIDADE PLANEJAMENTO ASSESSORIA LTDA',
                                                                                    qualificacao=PessoaQualificacao.PESSOA_JURIDICA_GERAL,
                                                                                    origem_informacoes=PessoaOrigemInformacoes.RECEITA_FEDERAL_BRASILEIRA,
                                                                                    tipo_simples_nacional=PessoaTipoSimples.OPTANTE,
                                                                                    endereco_cobranca=Endereco(
                                                                                        tipo_logradouro='R',
                                                                                        cidade_ibge='3304904',
                                                                                        logradouro='Dr. Feliciano Sodre',
                                                                                        numero='78',
                                                                                        cep='24440440',
                                                                                        uf=UF.RJ,
                                                                                        complemento="casa",
                                                                                        bairro="centro"
                                                                                    ),
                                                                                    contato_cobranca=Contato(
                                                                                        nome_ou_descricao='Coplan - financeiro',
                                                                                        email='financeiro@coplan.com.br'
                                                                                    )
                                                                                    ),
                                                                itens=[
                                                                    ItemFaturaPrestacaoServicos(codigo='IT01',
                                                                                                descricao='Item 01',
                                                                                                tipo_tributacao_iss=ItemDocumentoTipoTributacaoIss.ISENTO,
                                                                                                valor=200,
                                                                                                base_iss=200,
                                                                                                aliquota_iss=0,
                                                                                                iss_retido=0,
                                                                                                base_irrf=200,
                                                                                                aliquota_irrf=0,
                                                                                                irrf_retido=0,
                                                                                                base_inss=200,
                                                                                                incidencia_inss=0,
                                                                                                inss_retido=0,
                                                                                                base_csll=200,
                                                                                                aliquota_csll=0,
                                                                                                csll_retido=0,
                                                                                                base_pis=200,
                                                                                                aliquota_pis=0,
                                                                                                pis_retido=0,
                                                                                                base_cofins=200,
                                                                                                aliquota_cofins=0,
                                                                                                cofins_retido=0,
                                                                                                recorrente=True,
                                                                                                ordem=1
                                                                                                ),
                                                                    ItemFaturaPrestacaoServicos(codigo='IT02',
                                                                                                descricao='Item 02',
                                                                                                tipo_tributacao_iss=ItemDocumentoTipoTributacaoIss.ISENTO,
                                                                                                valor=800,
                                                                                                base_iss=800,
                                                                                                aliquota_iss=0,
                                                                                                iss_retido=0,
                                                                                                base_irrf=800,
                                                                                                aliquota_irrf=0,
                                                                                                irrf_retido=0,
                                                                                                base_inss=800,
                                                                                                incidencia_inss=0,
                                                                                                inss_retido=0,
                                                                                                base_csll=800,
                                                                                                aliquota_csll=0,
                                                                                                csll_retido=0,
                                                                                                base_pis=800,
                                                                                                aliquota_pis=0,
                                                                                                pis_retido=0,
                                                                                                base_cofins=800,
                                                                                                aliquota_cofins=0,
                                                                                                cofins_retido=0,
                                                                                                recorrente=True,
                                                                                                ordem=2
                                                                                                )
                                                                ]
                                                                )

    dados_cobranca = Dados_Cobranca(vencimento=datetime.date(2021, 9, 20),
                                    data_inicio_multa=None,
                                    data_limite_desconto=None,
                                    percentual_juros_diario=0,
                                    percentual_multa=0,
                                    percentual_desconto=0,
                                    texto_instrucao='fatura_prestacao_servicos nr. 236456')

    entrada["fatura_prestacao_servicos"] = fatura_prestacao_servicos_entrada
    entrada["dados_cobranca"] = dados_cobranca
    entrada["tenant"] = 47
    # Exemplo 2
    entrada_2 = dict()
    # total de impostos retidos: 10 + 20 + 30 + 40 + 50 + 60 = 210
    # valor líquido: 790
    fatura_prestacao_servicos_entrada_2 = FaturaPrestacaoServicos(
        estabelecimento="36ccf228-d7fb-4b90-ae10-84a810eab744",
        token_facilitador=None,
        cnae="1234568",
        numero=1,
        serie=None,
        emissao=datetime.date(2021, 9, 5),
        municipio_prestacao='2254364',
        base_iss=1000,
        iss_retido=10,
        base_irrf=1000,
        irrf_retido=20,
        base_inss=1000,
        inss_retido=30,
        base_pis=1000,
        pis_retido=40,
        base_cofins=1000,
        cofins_retido=50,
        base_csll=1000,
        csll_retido=60,
        situacao=Situacao.REALIZADO,
        participante=Pessoa(cpf_cnpj='05642157000134',
                            codigo='COPLAN',
                            nome_fantasia='COPLAN CONTABILIDADE PLANEJAMENTO ASSESSORIA LTDA',
                            razao_social='COPLAN CONTABILIDADE PLANEJAMENTO ASSESSORIA LTDA',
                            qualificacao=PessoaQualificacao.PESSOA_JURIDICA_GERAL,
                            origem_informacoes=PessoaOrigemInformacoes.RECEITA_FEDERAL_BRASILEIRA,
                            tipo_simples_nacional=PessoaTipoSimples.OPTANTE,
                            endereco_cobranca=Endereco(
                                tipo_logradouro='R',
                                cidade_ibge='3304904',
                                logradouro='Dr. Feliciano Sodre',
                                numero='78',
                                cep='24440440',
                                uf=UF.RJ,
                                complemento="casa",
                                bairro="centro"
                            ),
                            contato_cobranca=Contato(
                                nome_ou_descricao='Coplan - financeiro',
                                email='financeiro@coplan.com.br'
                            )
                            ),
        itens=[
            ItemFaturaPrestacaoServicos(codigo='IT01',
                                        descricao='Item 01',
                                        tipo_tributacao_iss=ItemDocumentoTipoTributacaoIss.TRIBUTADO,
                                        valor=200,
                                        base_iss=200,
                                        aliquota_iss=0,
                                        iss_retido=5,
                                        base_irrf=200,
                                        aliquota_irrf=0,
                                        irrf_retido=15,
                                        base_inss=200,
                                        incidencia_inss=0,
                                        inss_retido=10,
                                        base_csll=200,
                                        aliquota_csll=0,
                                        csll_retido=20,
                                        base_pis=200,
                                        aliquota_pis=0,
                                        pis_retido=25,
                                        base_cofins=200,
                                        aliquota_cofins=0,
                                        cofins_retido=20,
                                        recorrente=True,
                                        ordem=1
                                        ),
            ItemFaturaPrestacaoServicos(codigo='IT02',
                                        descricao='Item 02',
                                        tipo_tributacao_iss=ItemDocumentoTipoTributacaoIss.TRIBUTADO,
                                        valor=800,
                                        base_iss=800,
                                        aliquota_iss=0,
                                        iss_retido=5,
                                        base_irrf=800,
                                        aliquota_irrf=0,
                                        irrf_retido=5,
                                        base_inss=800,
                                        incidencia_inss=0,
                                        inss_retido=20,
                                        base_csll=800,
                                        aliquota_csll=0,
                                        csll_retido=40,
                                        base_pis=800,
                                        aliquota_pis=0,
                                        pis_retido=15,
                                        base_cofins=800,
                                        aliquota_cofins=0,
                                        cofins_retido=30,
                                        recorrente=True,
                                        ordem=2
                                        )
        ]
    )

    dados_cobranca_2 = Dados_Cobranca(vencimento=datetime.date(2021, 9, 15),
                                      data_inicio_multa=datetime.date(2021, 9, 16),
                                      data_limite_desconto=None,
                                      percentual_juros_diario=0,
                                      percentual_multa=10,
                                      percentual_desconto=0,
                                      texto_instrucao='fatura_prestacao_servicos nr. 236458')

    entrada_2["fatura_prestacao_servicos"] = fatura_prestacao_servicos_entrada_2
    entrada_2["dados_cobranca"] = dados_cobranca_2
    entrada_2["tenant"] = 47
    pasta = PastaPrestacaoServicos(DiarioUtil())

    """ #Teste Exemplo 1
    fatura_prestacao_servicos = pasta.apropriar(entrada)

    #Print Exemplo 1
    print(JsonUtil().encode(fatura_prestacao_servicos)) """

    # Teste Exemplo 2
    fatura_prestacao_servicos_2 = pasta.apropriar(entrada_2)

    # Print Exemplo 2
    print(JsonUtil().encode(fatura_prestacao_servicos_2))

    lista_faturas = pasta._diario_util.listar_fatura_prestacao_servicos(47)
    print(JsonUtil().encode(lista_faturas[0]))
