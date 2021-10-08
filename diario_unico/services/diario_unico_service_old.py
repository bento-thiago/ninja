from diario_unico.entity.conta_contabil import ContaContabil
from diario_unico.enum.documentos.item_documento_tipo_imposto import ItemDocumentoTipoImposto
from diario_unico.enum.documentos.item_documento_tipo import ItemDocumentoTipo
from diario_unico.entity.plano_conta_condominio import PlanoContasCondominio

from diario_unico.repository.diario_unico_repository_old import DiarioUnicoRepository

from typing import List


class DiarioUnicoServiceOld:

    def __init__(self, repository: DiarioUnicoRepository):
        self.repository = repository

    def get_imposto_acumulado_aquisicao_servico(
        self,
        tipo_imposto: ItemDocumentoTipoImposto,
        ano: int,
        mes: int,
        tenant: int
    ):
        return self.get_imposto_acumulado(
            tipo_imposto,
            [ItemDocumentoTipo.SERVICO],
            [PlanoContasCondominio.CC_1_1_1_01],
            ano,
            mes,
            tenant
        )

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

        resultset = self.repository.get_imposto_acumulado(
            tipo_imposto,
            tipos_item_documento,
            contas_contabeis,
            ano,
            mes,
            tenant
        )

        # Instanciando a classe referente ao imposto (tipo da classe mapeada no atributo "type_acumulado"
        # do enum de tipos de imposto):
        imposto_acumulado = tipo_imposto.value["type_acumulado"]()

        # Resolvendo os nomes dos campos no result_set:
        campo_valor_retido_original = tipo_imposto.value["campos"][0]
        campo_valor_retido = tipo_imposto.value["campos"][1]
        campo_base_retido_original = tipo_imposto.value["campos"][2]
        campo_base_retido = tipo_imposto.value["campos"][3]
        campo_aliquota = tipo_imposto.value["campos"][4]

        # Preenchendo a entidade pelo result_set:
        imposto_acumulado.estabelecimento = resultset["estabelecimento"]
        imposto_acumulado.situacao = resultset["situacao"]
        imposto_acumulado.valor_retido_original = resultset[campo_valor_retido_original]
        imposto_acumulado.valor_retido = resultset[campo_valor_retido]
        imposto_acumulado.base_original = resultset[campo_base_retido_original]
        imposto_acumulado.base = resultset[campo_base_retido]
        imposto_acumulado.aliquota = resultset[campo_aliquota]

        # Retornando o objeto do imposto:
        return imposto_acumulado
