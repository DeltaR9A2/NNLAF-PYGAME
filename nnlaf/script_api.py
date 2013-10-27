from world_model import Battle, Target, Terrain


class ScriptAPI:
    """This class encapsulates the functionality available to the game's 'scripts'
    which are python files used to add content and logic to the game without complicating
    the main source files. This is intended to encourage modularity and extensibility
    in the game's content and features.

    The methods defined by this class are the only ways in which such an external script
    should ever interact with the game. Beyond a certain point, the script API will be
    essentially "frozen" to prevent breaking older scripts."""
    def __init__(self, core):
        self._core = core

        self.cache = {}

        self.battles = {}
        self.targets = {}
        self.terrain = {}

    def select_battle(self, battle_id):
        if battle_id not in self.battles:
            self.battles[battle_id] = Battle()

        return self.battles[battle_id]

    def select_target(self, target_id):
        if target_id not in self.targets:
            self.targets[target_id] = Target()

        return self.targets[target_id]

    def select_terrain(self, terrain_id):
        if terrain_id not in self.terrain:
            self.terrain[terrain_id] = Terrain()

        return self.terrain[terrain_id]

    ### Script API Methods

    def add_string(self, name, string):
        key = ("string", name)

        self.cache[key] = string

    def get_string(self, name):
        key = ("string", name)
        return self.cache.get(key, "[DEFAULT STRING]")
