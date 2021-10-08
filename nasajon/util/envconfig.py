import os
import pathlib
import socket
import uuid


class EnvConfig:
    DIR_EXECUCAO = "pastas_contabeis"

    _instance = None

    def __init__(self):
        self.dir_execucao = self._trata_diretorio_execucao()
        self.log_path = self.dir_execucao / "logs"
        self.log_level = os.getenv("log_level", "DEBUG")
        self.id_execucao = uuid.uuid4()
        self.log_bd = bool(os.getenv("log_bd", False))

    @staticmethod
    def instance():
        if (EnvConfig._instance == None):
            EnvConfig._instance = EnvConfig()

        return EnvConfig._instance

    def _trata_diretorio_execucao(self):
        # Recupera diretório de usuário:
        user_home = pathlib.Path.home()

        if (user_home == pathlib.Path('/')):
            user_home = pathlib.Path('/var/app_home')

        # Monta path do diretório de configurações:
        dir = user_home / EnvConfig.DIR_EXECUCAO

        # Criando o diretório do JobManager, se necessário:
        if not os.path.exists(dir):
            os.makedirs(dir)

        return dir
