from datetime import date
from diario_unico.enum.situacao import Situacao

class Rpa:
    def __init__(self):
        self.estabelecimento:str = None
        self.token_facilitador : str = None
        self.ultimo_valor : int = None
        self.codigo_barras : str = None
        self.cfop : str = None
        self.codigo_transacao : str = None
        self.fornecedor_nome : str = None
        self.fornecedor_cpf_cnpj : str = None
        self.numero : int = None
        self.data_lancamento : date = None
        self.emissao : date = None
        self.vencimento : date = None
        self.data_cadastro : date = None
        self.data_pagamento : date = None
        self.codigo_consumo : str = None
        self.grupo_tensao : str = None
        self.valor : float = None
        self.Situacao : int = None
        self.foto : str = None
        self.descricao : str = None
        self.tipo_documento : str = None
        self.tipo_item : str = None    
        self.irrf_retido: float  = None
        self.iss_retido: float  = None       
    

