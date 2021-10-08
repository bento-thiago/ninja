from datetime import date
from pydantic import BaseModel, constr
from typing import List, Optional

class Dados_Cobranca(BaseModel):
    
    vencimento: date
    data_inicio_multa: Optional[date]
    data_limite_desconto: Optional[date]
    percentual_juros_diario: Optional[float] = 0
    percentual_multa: Optional[float] = 0
    percentual_desconto: Optional[float] = 0
    texto_instrucao: Optional[str]
    