from pydantic import BaseModel, PositiveInt, constr
from uuid import UUID
from typing import Optional

class Contato(BaseModel):
    id:Optional[UUID]
    nome_ou_descricao: constr(min_length=1, max_length=200,strip_whitespace=True)
    telefone:  Optional[constr(min_length=1, max_length=30,strip_whitespace=True)]
    email:  Optional[constr(min_length=1, max_length=200,strip_whitespace=True)]
    pessoa_registro: Optional[UUID]