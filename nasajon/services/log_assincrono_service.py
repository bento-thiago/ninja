from nasajon.repository.log_assincrono_repository import LogAssincronoRepository, LogAssincrono


class LogAssincronoService:

    def __init__(self, repository: LogAssincronoRepository):
        self.repository = repository

    def inserir(self, log_assincrono: LogAssincrono):
        self.repository.inserir(log_assincrono)

    def atualizar(self, log_assincrono: LogAssincrono):
        self.repository.atualizar(log_assincrono)

    def getStatusLogAssincrono(self, token: str, tenant: int, recurso: str = None):
        return self.repository.getStatusLogAssincrono(token, tenant, recurso)
