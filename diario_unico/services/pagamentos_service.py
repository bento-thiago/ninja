from diario_unico.util import service_util
from diario_unico.repository.pagamentos_repository import PagamentosRepository
from diario_unico.entity.info_pagamento import InfoPagamento


class PagamentosService:

    def __init__(self, repository: PagamentosRepository):
        self.repository = repository

    def inserir(self, pagamento: InfoPagamento):
        # Verificando se todos os parâmetros obrigatórios foram passados:
        chaves_obrigatorias = ["id_documento", "vencimento", "situacao"]
        valido, msg = service_util.verificaPropriedadesObjetoEntrada(
            chaves_obrigatorias, pagamento.__dict__)

        if not valido:
            return {'status': 400, 'msg': msg}

        return self.repository.inserir(pagamento)

    def listar(self, tenant: int, situacao: str):
        return self.repository.listar(tenant, situacao)

    def atualizar(self, pagamento: InfoPagamento):
        self.repository.atualizar(pagamento)

        return {"status": "OK"}

    def getPagamentoOperacao(self, tenant: int, id_operacao: str):
        return self.repository.getPagamentoOperacao(tenant, id_operacao)
