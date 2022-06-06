import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any

from compile_util.addon import Addon
from compile_util.island import Island
from compile_util.mission import Mission
from compile_util.mod import Mod


class Config:
    def __init__(self, mods: Dict[str, Mod], islands: Dict[str, Island], missions: List[Mission], addons: List[Addon],
                 replace: Optional[Dict[str, Any]], data: Dict[str, Any]):
        self.mods = mods
        self.islands = islands
        self.missions = missions
        self.addons = addons
        self.replace = replace

        self.data = data

    @classmethod
    def load_config(cls, config_file: str) -> 'Config':
        logging.info('Loading config {}.'.format(config_file))

        with open(config_file, 'r') as json_data_file:
            data = json.load(json_data_file)

        replace_data = data['replace'] if 'replace' in data else None

        config = Config(
            mods=Mod.load_mods(data['Mods']),
            islands=Island.load_islands(data['Islands']),
            missions=Mission.load_missions(data['Missions']),
            addons=Addon.load_addons(data['Addons']),
            replace=replace_data,
            data=data
        )

        # Load subconfigs and merge into this config.
        if 'Subconfigs' in data:
            for sub_config_file in data['Subconfigs']:
                sub_config = cls.load_config(sub_config_file)
                config.merge(sub_config)

        return config

    def merge(self, other: 'Config'):
        for mod_name, mod in other.mods.items():
            self.mods[mod_name] = mod

        for island_name, island in other.islands.items():
            self.islands[island_name] = island

        self.missions.extend(other.missions)

        self.addons.extend(other.addons)

    def mark_as_dev(self):
        self.replace['VERSION'] = '{} dev {}'.format(self.replace['VERSION'], datetime.today().strftime("%y%m%d %H%M"))

    def set_release(self, release: str):
        self.replace['RELEASE'] = release
