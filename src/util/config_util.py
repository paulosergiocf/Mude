from time import sleep
import platform as pt
from src.config.constants import Plataform
from pathlib import Path
import os

class ConfigUtil:

    @staticmethod
    def wait_timeout():
        TIME_OUT = 0
        sleep(TIME_OUT)
        return

    @staticmethod
    def get_user_location():
        if pt.system() in [Plataform.LINUX.value, Plataform.WINDOWS.value]:
            return Path(os.path.expanduser('~'), ".mude/")

        return os.getcwd()