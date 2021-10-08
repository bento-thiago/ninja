from typing import List

from diario_unico.entity.conta_contabil import ContaContabil
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from diario_unico.enum.documentos.item_documento_tipo_imposto import ItemDocumentoTipoImposto
from diario_unico.enum.sinal import Sinal
from diario_unico.repository.abstract_repository import AbstractRepository


class DiarioUnicoRepositoryOld(AbstractRepository):

    def __init__(self):
        super().__init__()

    def get_imposto_acumulado(
            self,
            tipo_imposto: ItemDocumentoTipoImposto,
            tipos_item_documento: List[ItemDocumentoTipo],
            contas_contabeis: List[ContaContabil],
            ano: int,
            mes: int,
            tenant: int
    ):
        """
        Retorna o somatório de todas as colunas do imposto passado no parâmetro "tipo_imposto",
        no período considerado (parâmetros "ano" e "mes"), para o tenant passado, e considerando
        apenas itens do diário unico que se enquadrem nos tipos de item passados ("tipos_item_documento")
        e nas contas contábeis passadas ("contas_contabeis").

        É importando destacar que os impostos são agrupados para estabelecimento e situação (isto é,
        o método retorna o somatório para todos os estabelecimentos de um tenant, separados pela situação).
        """

        # Montando a clausula de campos a retornar:
        campos = ", ".join(["sum({}) as {}".format(campo, campo)
                            for campo in tipo_imposto.value["campos"]])

        # Montando a lista de tipos de item:
        tipos_item = [tipo.value for tipo in tipos_item_documento]

        # Montando a lista de contas contabeis:
        contas = [conta.value.codigo for conta in contas_contabeis]

        # Montando a query em si:
        sql_base = """
            select
                {campos},
                p.codigo as estabelecimento,
                du.situacao
            from
                diario_unico as du join
                pessoas p on (p.pessoa = du.estabelecimento)
            where
                du.sinal = :sinal and
                du.diario_unico_tipo in :du_tipos and
                du.conta_contabil in :du_contas and
                year(du.data) = :ano and
                month(du.data) = :mes and
                du.tenant = :tenant
            group by
                du.estabelecimento,
                du.situacao
        """.format(campos=campos)

        # Executando a query:
        return self.fetchOne(
            sql_base,
            {
                "sinal": Sinal.ENTRADA,
                "du_tipos": tuple(tipos_item),
                "du_contas": tuple(contas),
                "ano": ano,
                "mes": mes,
                "tenant": tenant
            }
        )
