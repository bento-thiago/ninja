from time_service.repository.abstract_repository import AbstractRepository
import uuid
from django.db import connections, transaction
from nasajon.util.cursor_util import CursorUtil
import datetime


class TimeRepository(AbstractRepository):
    # Insere a hora falsa no banco de dados
    def inserir(self, time: datetime.datetime):
        existe = self.fetchOne("SELECT 1 from time_service", {})
        if existe is None:
            sql = """INSERT INTO time_service
                (data_hora_gravada, ultima_alteracao)
                VALUES(:data_hora_gravada, now())"""

            # Executa a query
            self.execute(sql, {"data_hora_gravada": time})
        else:
            sql = """UPDATE time_service
                            set data_hora_gravada = :data_hora_gravada,
                            ultima_alteracao = now()"""

            self.execute(sql, {"data_hora_gravada": time})
