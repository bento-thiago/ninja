from datetime import date
from typing import get_type_hints
from diario_unico.enum.situacao import Situacao


class ContaConsumo:
    def __init__(self, token_facilitador: str = None, estabelecimento: str = None):
        self.token_facilitador = token_facilitador
        self.estabelecimento: str = estabelecimento
        self.ultimo_valor: int = None
        self.codigo_barras: str = None
        self.codigo_transacao: str = None
        self.fornecedor_nome: str = None
        self.fornecedor_cnpj: str = None
        self.numero: int = None
        self.data_lancamento: date = None
        self.emissao: date = None
        self.vencimento: date = None
        self.data_cadastro: date = None
        self.data_pagamento: date = None
        self.codigo_consumo: str = None
        self.grupo_tensao: str = None
        self.valor: float = None
        self.situacao: Situacao = None
        self.foto: str = None
        self.descricao: str = None
        self.tipo: int = None
        self.tipo_item: int = None
        self.url_documento: str = None
        self.identificador_contrato: str = None
