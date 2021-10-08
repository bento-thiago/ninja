class CrawlerFactory:
    @staticmethod
    def getFinanceiroRepository():
        from crawlers.repository.financeiro_repository import FinanceiroRepository
        return FinanceiroRepository()

    @staticmethod
    def getFinanceiroService():
        from crawlers.services.financeiro_service import FinanceiroService
        return FinanceiroService(CrawlerFactory.getFinanceiroRepository())
