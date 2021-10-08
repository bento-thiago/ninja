from diario_unico.util import service_util
from diario_unico.repository.cobrancas_repository import CobrancasRepository
from diario_unico.entity.info_cobranca import InfoCobranca


class CobrancasService:

    def __init__(self, repository: CobrancasRepository):
        self.repository = repository

    def inserir(self, cobranca: InfoCobranca):
        # Verificando se todos os parâmetros obrigatórios foram passados:
        chaves_obrigatorias = ["id_documento", "juros_mensal", "multa_atraso",
                               "desconto", "texto_instrucao", "vencimento", "situacao", "numero"]
        valido, msg = service_util.verificaPropriedadesObjetoEntrada(
            chaves_obrigatorias, cobranca.__dict__)

        if not valido:
            return {'status': 400, 'msg': msg}

        return self.repository.inserir(cobranca)

    def listar(self, tenant: int, situacao: str, vencimento_apos: str):
        return self.repository.listar(tenant, situacao, vencimento_apos)

    def atualizar(self, cobranca: InfoCobranca):
        self.repository.atualizar(cobranca)

        return {"status": "OK"}

    def getByIdDocumento(self, tenant, id_documento):
        return self.repository.getByIdDocumento(tenant, id_documento)

    def getDadosCobranca(self, tenant, cpf_cnpj_pessoa):
        retorno = self.repository.getDadosCobranca(tenant, cpf_cnpj_pessoa)

        if retorno == None:
            raise Exception('CPF ou CNPJ nao encontrado: ' + cpf_cnpj_pessoa)

        return retorno
