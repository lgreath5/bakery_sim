import simpy
from enum import Enum
from recipe import Recipe

class EquipmentNames(Enum):
    none = 0
    mixer = 1
    oven = 2
    decorating_station = 3

class Equipment:

    def __init__(self, name : str, environment : simpy.Environment):
        self.name = name
        self.current_recipe : Recipe = None
        self._start_time : int = None
        self._environment = environment

    def remaining_time(self) -> int: 

        if self._start_time != None:
            remaining_time = self._finish_time() - self._environment.now
            return remaining_time if remaining_time > 0 else 0

        return 0

    def _finish_time(self) -> int:
        return self._start_time + self.current_recipe.times[self.name]

    def set_in_use(self, recipe : Recipe, start_time : int) -> None:
        self.current_recipe = recipe
        self._start_time = start_time

    def set_not_in_use(self) -> None:
        self.current_recipe = None
        self._start_time = None

    def print_equipment(self) -> None:

        if self.current_recipe == None:
            print(self.name + ':', '-')

        elif self.remaining_time() == 0:
            print(self.name + ':', self.current_recipe.name, 'ready!')

        else:
            print(self.name + ':', self.current_recipe.name, 'in', self.remaining_time(), 'mins')
