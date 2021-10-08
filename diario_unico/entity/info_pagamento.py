from datetime import date
from diario_unico.enum.info_pagamento.situacao_info_pagamento import SituacaoInfoPagamento
from typing import List, Optional
from pydantic import BaseModel, constr

class InfoPagamento(BaseModel):
    """
    Classe que representa os dados de um A Pagar
    """

    vencimento:  Optional [ date ]
    situacao:  Optional [ SituacaoInfoPagamento ]
    id_operacao:  Optional [ str ]
    id_documento:  Optional [ str ]
    mensagem_erro:  Optional [ str ]
    id_pagamento:  Optional [ str ]
    tenant:  Optional [ int ]



