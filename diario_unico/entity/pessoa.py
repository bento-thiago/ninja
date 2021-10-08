from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, constr

from diario_unico.entity.contato import Contato
from diario_unico.entity.endereco import Endereco
from diario_unico.enum.pessoas.pessoa_origem_informacoes import PessoaOrigemInformacoes
from diario_unico.enum.pessoas.pessoa_papel import PessoaPapel
from diario_unico.enum.pessoas.pessoa_qualificacao import PessoaQualificacao
from diario_unico.enum.pessoas.pessoa_tipo_simples import PessoaTipoSimples


class Pessoa(BaseModel):
    id_compartilhado: Optional[UUID]
    id_registro: Optional[UUID]
    cpf_cnpj: constr(min_length=11, max_length=14, strip_whitespace=True)
    codigo: constr(min_length=1, max_length=40, strip_whitespace=True)
    nome_fantasia: constr(min_length=1, max_length=200, strip_whitespace=True)
    razao_social: constr(min_length=1, max_length=200, strip_whitespace=True)
    qualificacao: PessoaQualificacao
    inscricao_municipal: Optional[constr(min_length=1, max_length=40, strip_whitespace=True)]
    inscricao_estadual: Optional[constr(min_length=1, max_length=40, strip_whitespace=True)]
    origem_informacoes: PessoaOrigemInformacoes
    tipo_simples_nacional: PessoaTipoSimples = PessoaTipoSimples.NAO_INFORMADO
    registro_papel: PessoaPapel = PessoaPapel.NAO_DEFINIDO

    endereco_principal: Optional[Endereco]
    endereco_cobranca: Optional[Endereco]
    enderecos_outros: List[Endereco] = []

    contato_principal: Optional[Contato]
    contato_cobranca: Optional[Contato]
    contatos_outros: List[Contato] = []

    # IDs de tabelas extrangeiras que poderão estar associadas aos registros. No futuro, terá docfis, contratos, bens, etc
    contrato_id: Optional[UUID]
