from datetime import date, datetime
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Field

from diario_unico.entity.item_contrato import ItemContrato
from diario_unico.entity.pessoa import Pessoa
from diario_unico.enum.contratos.contrato_tipo_cobranca import ContratoTipoCobranca
from diario_unico.enum.contratos.contrato_tipo_recorrencia import ContratoTipoRecorrencia
from diario_unico.enum.contratos.item_contrato_situacao import ItemContratoSituacao
from nasajon.util.json_util import JsonUtil


class Contrato(BaseModel):
    """
    Classe que representa os dados de um contrato que devem ser passados para o SDK do Diário Único
    
    Nota:
        Esta classe utiliza recursos da classe pydantic.BaseModel, por isso seus campos devem respeitar aos types
        definidos ou ocorrerá um exception. Um contrutor não deve ser criado explicitamente
    
    Construtores:
        1- Passando os campos nominalmente no construtor: 
            Exemplo: objeto = NomeDaClasse(campo1=valor1, campo2=valor2)
        2- Passando um dicionário para o método de classe parse_obj
            Exemplo: dicionario = {campo1:valor1, campo2:valor2}
                     objeto = NomeDaClasse.parse_obj(dicionario)    
    """
    id_compartilhado: Optional[UUID]
    id_registro: Optional[UUID]
    codigo: constr(min_length=1, max_length=40, strip_whitespace=True)
    descricao: constr(min_length=1, max_length=200)
    data_registro: datetime = Field(default_factory=datetime.now)  # Preenchimento automatico
    participante: Pessoa
    estabelecimento: UUID

    itens: List[ItemContrato]


# Exemplo abaixo:
if __name__ == '__main__':
    from diario_unico.enum.pessoas.pessoa_origem_informacoes import PessoaOrigemInformacoes
    from diario_unico.enum.pessoas.pessoa_qualificacao import PessoaQualificacao
    from diario_unico.enum.pessoas.pessoa_tipo_simples import PessoaTipoSimples
    from diario_unico.entity.endereco import Endereco
    from diario_unico.entity.contato import Contato
    from diario_unico.enum.endereco.uf import UF

    c = Contrato(codigo='01',
                 descricao='teste',
                 estabelecimento=UUID("162b80c1-b589-465c-8418-9ef07fbf7091"),

                 participante=Pessoa(
                     cpf_cnpj='05642157000134',
                     codigo='COPLAN',
                     nome_fantasia='COPLAN CONTABILIDADE PLANEJAMENTO ASSESSORIA LTDA',
                     razao_social='COPLAN CONTABILIDADE PLANEJAMENTO ASSESSORIA LTDA',
                     qualificacao=PessoaQualificacao.PESSOA_JURIDICA_GERAL,
                     origem_informacoes=PessoaOrigemInformacoes.RECEITA_FEDERAL_BRASILEIRA,
                     tipo_simples_nacional=PessoaTipoSimples.OPTANTE,
                     endereco_principal=Endereco(
                         tipo_logradouro='R',
                         cidade_ibge='3304904',
                         logradouro='Dr. Feliciano Sodre',
                         numero='78',
                         cep='24440440',
                         uf=UF.RJ,
                         complemento="casa",
                         bairro="centro"
                     ),
                     endereco_cobranca=None,
                     contato_principal=Contato(
                         nome_ou_descricao='Fulano de tals',
                         telefone='21998364945'
                     ),
                     contato_cobranca=Contato(
                         nome_ou_descricao='Coplan - financeiro',
                         email='financeiro@coplan.com.br'
                     )
                 ),
                 itens=[
                     ItemContrato(
                         id_servico="b1b6f14a-e383-4aa0-952b-5951e943b74f",
                         valor_unitario=100,
                         quantidade=1,
                         valor_total=100,
                         recorrente=True,
                         codigo_item_contrato="CONTABIL",
                         codigo_servico="01.04.02",
                         descricao="Sistema contabil SQL",
                         incidencia_inss=100,
                         aliquota_inss=1,
                         aliquota_ir=2,
                         aliquota_pis=3,
                         aliquota_cofins=4,
                         aliquota_csll=5,
                         competencia_inicio=date(2021, 1, 1),
                         competencia_final=None,
                         dia_processamento=10,
                         dia_vencimento=15,
                         tipo_recorrencia=ContratoTipoRecorrencia.MENSAL,
                         tipo_cobranca=ContratoTipoCobranca.PRE,
                         situacao=ItemContratoSituacao.ATIVO

                     ),
                     ItemContrato(
                         id_servico="10829943-f85a-4c82-ada8-8a2537db26dd",
                         valor_unitario=30,
                         quantidade=4,
                         valor_total=120,
                         recorrente=True,
                         codigo_item_contrato="IMPLANTACAO",
                         codigo_servico="01.04.02",
                         descricao="Implantação dos sistemas",
                         incidencia_inss=120,
                         aliquota_inss=7,
                         aliquota_ir=8,
                         aliquota_pis=9,
                         aliquota_cofins=1,
                         aliquota_csll=2,
                         competencia_inicio=date(2021, 1, 1),
                         competencia_final=None,
                         dia_processamento=10,
                         dia_vencimento=15,
                         tipo_recorrencia=ContratoTipoRecorrencia.MENSAL,
                         tipo_cobranca=ContratoTipoCobranca.PRE,
                         situacao=ItemContratoSituacao.ATIVO
                     )
                 ]
                 )

    from diario_unico.services.contrato_service import ContratoService
    from diario_unico.services.utilitario_service import UtilitarioService
    from diario_unico.repository.contrato_repository import ContratoRepository
    from diario_unico.repository.estabelecimento_repository import EstabelecimentoRepository
    from diario_unico.services.pessoa_service import PessoaService
    from diario_unico.repository.utilitario_repository import UtilitarioRepository
    from diario_unico.repository.pessoas_repository import PessoasRepository
    from diario_unico.services.contato_service import ContatoService
    from diario_unico.repository.contato_repository import ContatoRepository
    from diario_unico.services.endereco_service import EnderecoService
    from diario_unico.repository.endereco_repository import EnderecoRepository

    service = ContratoService(ContratoRepository(), UtilitarioService(UtilitarioRepository()),
                              EstabelecimentoRepository(),
                              PessoaService(PessoasRepository(), UtilitarioService(UtilitarioRepository()),
                                            ContatoService(ContatoRepository()), EnderecoService(EnderecoRepository())))
    d = service.inserir_contrato(c, 47)
    print(JsonUtil().encode(d))
