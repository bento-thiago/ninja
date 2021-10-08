from datetime import date
from diario_unico.enum.info_cobranca.situacao_info_cobranca import SituacaoInfoCobranca

class DefinicaoInfoCobranca:
    def __init__(self, lancamento_numero:int = None, origem_data_inicio_multa: str = None,
                origem_data_limite_desconto: str = None, origem_percentual_juros_diario:str = None,
                origem_percentual_multa:str = None, origem_percentual_desconto:str = None, 
                origem_valor_liquido:str = None, origem_valor_bruto:str = None,
                origem_valor_sacado: str = None, origem_vencimento:str = None, 
                origem_texto_instrucao:str = None, origem_participante: str = None, 
                origem_endereco: str = None, origem_contato_cobranca: str = None, 
                situacao:SituacaoInfoCobranca = None):
        self.lancamento_numero: int = lancamento_numero
        self.origem_data_inicio_multa: str = origem_data_inicio_multa
        self.origem_data_limite_desconto: str = origem_data_limite_desconto
        self.origem_percentual_juros_diario:str = origem_percentual_juros_diario
        self.origem_percentual_multa: str = origem_percentual_multa
        self.origem_percentual_desconto: str = origem_percentual_desconto
        self.origem_valor_liquido: str = origem_valor_liquido
        self.origem_valor_bruto: str = origem_valor_bruto
        self.origem_valor_sacado: str = origem_valor_sacado
        self.origem_vencimento: str = origem_vencimento
        self.origem_texto_instrucao: str = origem_texto_instrucao
        self.origem_participante: str = origem_participante
        self.origem_endereco: str = origem_endereco
        self.origem_contato_cobranca: str = origem_contato_cobranca
        self.situacao:SituacaoInfoCobranca = situacao