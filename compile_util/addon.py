from typing import List, Any, Dict


class Addon:
    def __init__(self, name: str, mods: List[str]):
        self.name = name
        self.mods = mods

    @staticmethod
    def load_addons(addon_dicts: List[Dict[str, Any]]) -> List['Addon']:
        addons = []

        for addon_dict in addon_dicts:
            addons.append(Addon(
                name=addon_dict['name'],
                mods=addon_dict['mods']
            ))

        return addons
