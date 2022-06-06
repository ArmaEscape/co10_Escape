from typing import List, Dict, Any


class Mod:
    def __init__(self, name: str, path: str, require: List[str], replace: Dict[str, Any]):
        self.name = name
        self.path = path
        self.require = require
        self.replace = replace

    @staticmethod
    def load_mods(mod_dicts: List[Dict[str, Any]]) -> Dict[str, 'Mod']:
        mods = {}

        for mod_dict in mod_dicts:
            name = mod_dict['name']

            mods[name] = Mod(
                name=name,
                path=mod_dict['path'],
                require=mod_dict['require'],
                replace=mod_dict['replace']
            )

        return mods
