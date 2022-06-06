import logging
import os
from typing import Any, Dict, List


class Mission:
    def __init__(self, island: str, sqm: str, mod: str, replace: Dict[str, Any], name: str):
        self.island = island
        self.sqm = sqm
        self.mod = mod
        self.replace = replace
        self.name = name

    @staticmethod
    def load_missions(mission_dicts: List[Dict[str, Any]]) -> List['Mission']:
        missions = []

        for mission_dict in mission_dicts:

            missions.append(Mission(
                island=mission_dict['island'],
                sqm=mission_dict['sqm'],
                mod=mission_dict['mod'],
                replace=mission_dict['replace'],
                name=mission_dict['name']
            ))

        return missions

