import logging
import subprocess
import sys
from os import path
from urllib.request import urlretrieve

from compile_util.config import Config


class PboPacker:
    def __init__(self, config: Config):
        self.config = config

    def _exec_path(self) -> str:
        if sys.platform == 'win32':
            return path.join('./Tools', 'cpbo.exe')
        else:
            return path.join('./Tools', 'cpbo')

    def _download_uri(self) -> str:
        if sys.platform == 'win32':
            return self.config.data['CpboPath']['windows']
        else:
            return self.config.data['CpboPath']['linux']

    def download(self):
        exec_path = self._exec_path()
        if not path.isfile(exec_path):
            logging.info("Downloading CPBO...")
            download_uri = self._download_uri()
            urlretrieve(download_uri, exec_path)
            logging.info("CPBO downloaded.")
        else:
            logging.info("Found CPBO on path {}.".format(exec_path))

    def pack(self, mission_dir: str):
        logging.info('Packing {}.'.format(mission_dir))

        exec_path = self._exec_path()
        subprocess.call([exec_path, "-y", "-p", mission_dir])
