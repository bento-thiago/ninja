from pydantic import BaseModel, PositiveInt, constr
from typing import Optional
from diario_unico.enum.endereco.uf import UF
from uuid import UUID

class Endereco(BaseModel):
    id: Optional[UUID]
    pessoa_registro: Optional[UUID]
    tipo_logradouro:constr(min_length=1, max_length=10,strip_whitespace=True)
    cidade_ibge:constr(min_length=7, max_length=7,strip_whitespace=True)
    logradouro:constr(min_length=1, max_length=100,strip_whitespace=True)
    numero:constr(min_length=1, max_length=10,strip_whitespace=True)
    complemento:constr(min_length=1, max_length=100,strip_whitespace=True)
    bairro:constr(min_length=1, max_length=100,strip_whitespace=True)
    cep:constr(min_length=8, max_length=8,strip_whitespace=True)
    uf:UF
    pais_codigo:constr(min_length=1, max_length=4,strip_whitespace=True) ='1058'#Brasil='1058'
    referencia:Optional[constr(min_length=1, max_length=100,strip_whitespace=True)]