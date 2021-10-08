from nasajon.entity.dados_escrituracao_futura import ValoresAnteriores
from diario_unico.entity.documento import Documento

from typing import List

import datetime
from dateutil.relativedelta import relativedelta
from diario_unico.util.date_util import ultimoDiaMes

class DiarioUtilMock:
    tenant_recebidos: List[int] = list()
    documento_recebidos: List[Documento] = list()

    def recuperar_ultimo_trimestre(self, tenant: int, dados: dict, data: datetime.date, entidade_negocio: str, tipo_documento: int) -> List[ValoresAnteriores]:

        valor = ValoresAnteriores()
        valor.valor = 134.0

        result = list()
        result.append(valor)

        return result

    def escriturar_antecipadamente_documento(self, tenant: int, conteudo: object):
        self.tenant_recebidos.append(tenant)
        self.documento_recebidos.append(conteudo)

    def recuperar_documentos_por_estabelecimento_tipo_data(self, tenant: int, estabelecimento: str, data_inicial: datetime.date, data_final: datetime.date, tipo_documento: int):
        doc1 = Documento()
        doc1.numero="01"
        doc1.estabelecimento=estabelecimento
        doc1.data_lancamento=data_inicial
        doc1.tipo = tipo_documento

        doc2 = Documento()
        doc2.numero="02"
        doc2.estabelecimento=estabelecimento
        doc2.data_lancamento=ultimoDiaMes(data_final - relativedelta(months=1))
        doc2.tipo = tipo_documento

        doc3 = Documento()
        doc3.numero="03"
        doc3.estabelecimento=estabelecimento
        doc3.data_lancamento=data_final
        doc3.tipo = tipo_documento

        return [doc3, doc1, doc2]
    
    def cadastrarPessoa(self, cpf, nome, tenant):
        pass
