from crawlers.repository.financeiro_repository import FinanceiroRepository


class FinanceiroService:
    def __init__(self, financeiro_repository: FinanceiroRepository):
        self.financerio_repository = financeiro_repository

    def getConta(self, iban, tenant):
        return self.financerio_repository.getConta(iban, tenant)
