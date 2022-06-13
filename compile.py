import logging
import os
import shutil
from os import path

from compile_util.config import Config
from compile_util.mission_builder import build_mission
from compile_util.pbopacker import PboPacker

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

config = Config.load_config('Configs/config.json')
config.mark_as_dev()
config.set_release('Mission')

# Clean build directory.
logging.info("Cleaning build directory.")
if os.path.exists(config.data['BuildDir']):
    shutil.rmtree(config.data['BuildDir'])

logging.info('Creating build directory in {}.'.format(path.join(config.data['BuildDir'], 'Addons')))
os.makedirs(path.join(config.data['BuildDir'], 'Addons'), exist_ok=True)

logging.info('Creating packed directory in {}.'.format(path.join(config.data['PackedDir'], 'Missions')))
os.makedirs(path.join(config.data['PackedDir'], 'Missions'), exist_ok=True)

logging.info('Creating tools directory in ./Tools if missing.')
os.makedirs('./Tools', exist_ok=True)

pbo_packer = PboPacker(config)
pbo_packer.download()

# Build missions.
for mission in config.missions:
    build_mission(mission, config, pbo_packer)
