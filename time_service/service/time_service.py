from time_service.repository.time_repository import TimeRepository
from time_service.entity.redis import Redis

import datetime
import os


class TimeService:

    def __init__(self, repository: TimeRepository):
        self.repository = repository

    def inserir(self, time: datetime.datetime):
        self.repository.inserir(time)

    @staticmethod
    def now()->datetime:

        usar_time_service = os.getenv("usar_time_service", False) == "True"

        if (not usar_time_service) or \
                Redis.getClientInstance().get("hora_real") == None or \
                Redis.getClientInstance().get("hora_arbitrada") == None:
            return datetime.datetime.now()

        hora_real = datetime.datetime.strptime(
            Redis.getClientInstance().get("hora_real").decode("utf-8"), "%Y-%m-%d %H:%M:%S")

        hora_arbitrada = datetime.datetime.strptime(
            Redis.getClientInstance().get("hora_arbitrada").decode("utf-8"), "%Y-%m-%d %H:%M:%S")

        hora_atual = datetime.datetime.now()

        intervalo_set = hora_atual - hora_real
        hora_retorno = hora_arbitrada + intervalo_set
        return hora_retorno
