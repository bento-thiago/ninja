class NasajonFactory:
    @staticmethod
    def getLogAssincronoRepository():
        from nasajon.repository.log_assincrono_repository import LogAssincronoRepository
        return LogAssincronoRepository()

    @staticmethod
    def getLogAssincronoService():
        from nasajon.services.log_assincrono_service import LogAssincronoService
        return LogAssincronoService(NasajonFactory.getLogAssincronoRepository())
