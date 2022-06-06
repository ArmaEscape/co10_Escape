import logging
import os
import shutil
from typing import List, Dict, Any
from os import path

from compile_util.config import Config
from compile_util.mission import Mission
from compile_util.pbopacker import PboPacker


def _replace_placeholders(mission_dir: str, parsed_files: List[str], replace: Dict[str, Any]):
    for root, subFolders, files in os.walk(mission_dir):
        for rfile in parsed_files:
            if rfile in files:
                logging.info('Found {} at {}'.format(rfile, os.path.join(root, rfile)))
                rfile_contents = open(os.path.join(root, rfile)).read()
                for key in replace:
                    if '{* ' + key + ' *}' in rfile_contents:
                        logging.info('Found occurance of {} in file {}. Replacing with {}'
                                     .format(key, rfile, replace[key]))
                        rfile_contents = rfile_contents.replace('{* ' + key + ' *}', replace[key])

                    f = open(os.path.join(root, rfile), 'w')
                    f.write(rfile_contents)
                    f.flush()
                    f.close()


def build_mission(mission: Mission, config: Config, pbo_packer: PboPacker):
    logging.info('Creating a mission with mod {} on island {}'.format(mission.mod, mission.island))

    mission_mod = None
    try:
        mission_mod = config.mods[mission.mod]
    except KeyError:
        logging.error('Mod {} not found.'.format(mission.mod))
        exit(1)

    mission_island = None
    try:
        mission_island = config.islands[mission.island]
    except KeyError:
        logging.error('Island {} not found.'.format(mission.island))
        exit(1)

    mission_dir = path.join(config.data['BuildDir'], 'missionfiles', mission.name + '.' + mission_island.class_name)

    # Copy code, island and mod files to mission path.
    shutil.copytree(config.data['Code'], mission_dir)
    shutil.copytree(mission_island.path, path.join(mission_dir, 'Island'))
    shutil.copytree(mission_mod.path, path.join(mission_dir, 'Units'))

    # Add quotation marks around requirements and concatenate to string.
    require_array = map(lambda x: '"{}"'.format(x), mission_mod.require)
    required = ','.join(require_array)

    # Copy mission file.
    shutil.copy(path.join('./Missions', mission.sqm, 'mission.sqm'), path.join(mission_dir, 'mission.sqm'))

    # Combine all replacements.
    replace = {}
    replace.update(config.replace)
    replace.update(mission_mod.replace)
    replace.update(mission_island.replace)

    replace['REQUIRE'] = required

    # Replace placeholders.
    _replace_placeholders(mission_dir, config.data['ParsedFiles'], replace)

    file_name = mission.name + '.' + mission_island.class_name + '.pbo'

    pbo_packer.pack(mission_dir)

    # Copy build artifact.
    shutil.copyfile(mission_dir + '.pbo', path.join(config.data['PackedDir'], 'Missions', file_name))