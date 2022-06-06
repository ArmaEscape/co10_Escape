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
            return path.join('./Tools', 'JAPM.exe')
        else:
            return path.join('./Tools', 'JAPM')

    def _download_uri(self) -> str:
        if sys.platform == 'win32':
            return self.config.data['JAPM']['windows']
        else:
            return self.config.data['JAPM']['linux']

    def download(self):
        exec_path = self._exec_path()
        if not path.isfile(exec_path):
            logging.info("Downloading JAPM...")
            download_uri = self._download_uri()
            urlretrieve(download_uri, exec_path)
            logging.info("JAPM downloaded.")
        else:
            logging.info("Found JAPM on path {}.".format(exec_path))

    def pack(self, mission_dir: str, output_name: str):
        logging.info('Packing {} into {}.'.format(mission_dir, output_name))
        output_path = path.join(mission_dir, '..', output_name)

        exec_path = self._exec_path()
        subprocess.call([exec_path, '-q', mission_dir, output_path])
