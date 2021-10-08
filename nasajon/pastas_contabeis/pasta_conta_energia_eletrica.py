from datetime import date

from nasajon.entity.conta_consumo import ContaConsumo
from nasajon.entity.definicao_lancamento import DefinicaoLancamento
from diario_unico.enum.documentos.documento_tipo import DocumentoTipo
from diario_unico.entity.lancamento import SituacaoDiario

from nasajon.pastas_contabeis.pasta_conta_consumo import PastaContaConsumo
from nasajon.pastas_contabeis.pastas_router import MomentoContabil

from nasajon.util.diario_util import DiarioUtil

from typing import List, ClassVar
import enum


class PastaContaEnergiaEletrica(PastaContaConsumo):

    def __init__(self, diario_util: DiarioUtil):
        super().__init__(diario_util)

        self.documento_tipo = DocumentoTipo.CONTA_ENERGIA
        self.item_descricao = 'Energia Elétrica'

    def get_definicoes_lancamentos_escrituracao_futura(self) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='4.1.1.08.0002',
            historico='Despesa com conta de energia elétrica',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_energia.esc_futura.despesa'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='2.1.2.04',
            historico='Conta de energia elétrica a pagar',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_energia.esc_futura.provisao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=2,
            ordem=1,
            natureza='D',
            conta='2.1.2.04',
            historico='Pagamento de conta de energia elétrica',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_energia.esc_futura.conclusao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.ESCRITURACAO_FUTURA,
            tipo=self.documento_tipo,
            numero=2,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de conta de energia elétrica',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_energia.esc_futura.pagamento'
        ))
        return saida

    def get_definicoes_lancamentos_apropriacao(self) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='4.1.1.08.0002',
            historico='Despesa com conta de energia elétrica',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='conta_energia.apropriacao.despesa'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='2.1.2.04',
            historico='Conta de energia elétrica a pagar',
            formula='valor',
            formula_data='data_lancamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='conta_energia.apropriacao.provisao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=1,
            natureza='D',
            conta='2.1.2.04',
            historico='Pagamento de conta de energia elétrica',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_energia.apropriacao.conclusao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.APROPRIACAO,
            tipo=self.documento_tipo,
            numero=2,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de conta de energia elétrica',
            formula='valor',
            formula_data='vencimento',
            situacao=SituacaoDiario.PREVISTO,
            definicao='conta_energia.apropriacao.caixa'
        ))
        return saida

    def get_definicoes_lancamentos_quitacao(self) -> List[DefinicaoLancamento]:
        saida = list()
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.QUITACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=1,
            natureza='D',
            conta='2.1.2.04',
            historico='Pagamento de conta de energia elétrica',
            formula='valor',
            formula_data='data_pagamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='conta_energia.pagamento.conclusao'
        ))
        saida.append(DefinicaoLancamento(
            momento=MomentoContabil.QUITACAO,
            tipo=self.documento_tipo,
            numero=1,
            ordem=2,
            natureza='C',
            conta='1.1.1.01',
            historico='Pagamento de conta de energia elétrica',
            formula='valor',
            formula_data='data_pagamento',
            situacao=SituacaoDiario.REALIZADO,
            definicao='conta_energia.pagamento.caixa'
        ))
        return saida

    # def get_tipo_documento(self) -> DocumentoTipo:
    #     pass


# Teste sobre apropriacao de conta de energia eletrica
if __name__ == "__main__":
    from diario_unico.entity.documento import DocumentoTipo
    from diario_unico.enum.situacao import Situacao
    from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
    import manage
    manage.main()
    pasta = PastaContaEnergiaEletrica(DiarioUtil())
    conta = ContaConsumo()
    conta.codigo_barras = "codigo_barras"
    conta.data_lancamento = date(2019, 10, 1)
    conta.descricao = "Conta de energia elétrica"
    conta.emissao = date(2019, 10, 1)
    conta.estabelecimento = "743"
    conta.fornecedor_cnpj = "16524275634712"
    conta.fornecedor_nome = "LIGHT"
    conta.foto = "blablabla.jpg"
    conta.identificador_contrato = "123"
    conta.numero = 1
    conta.situacao = Situacao.REALIZADO
    conta.tipo = DocumentoTipo.CONTA_ENERGIA
    conta.tipo_item = ItemDocumentoTipo.ITEM_CONTA_CONSUMO
    conta.url_documento = "url_documento"
    conta.valor = 8000
    conta.vencimento = date(2019, 10, 15)
    conta.tenant = 47
    pasta.apropriar(conta.__dict__)
