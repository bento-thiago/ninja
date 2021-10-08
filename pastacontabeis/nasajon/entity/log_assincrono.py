from datetime import datetime
from typing import get_type_hints


class LogAssincrono:
    def __init__(self, token: str = None, recurso: str = None, status: str = None, tenant: str = None):
        self.token = token
        self.recurso: str = recurso
        self.status: str = status
        self.datahora: datetime = None
        self.tenant: str = tenant
