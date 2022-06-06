from typing import Dict, Any, List


class Island:
    def __init__(self, name: str, class_name: str, path: str, replace: Dict[str, Any]):
        self.name = name
        self.class_name = class_name
        self.path = path
        self.replace = replace

    @staticmethod
    def load_islands(island_dicts: List[Dict[str, Any]]) -> Dict[str, 'Island']:
        islands = {}

        for island_dict in island_dicts:
            name = island_dict['name']

            islands[name] = Island(
                name=name,
                class_name=island_dict['class'],
                path=island_dict['path'],
                replace=island_dict['replace']
            )

        return islands
