class TimeFactory:
    @staticmethod
    def getTimeRepository():
        from time_service.repository.time_repository import TimeRepository
        return TimeRepository()

    @staticmethod
    def getTimeService():
        from time_service.service.time_service import TimeService
        return TimeService(TimeFactory.getTimeRepository())
