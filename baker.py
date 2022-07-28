
import simpy
from equipment import EquipmentNames
from recipe import Recipe
from enum import Enum

class BakerNames(Enum):
    Chip = 1
    Coco = 2 
    Eclair = 3
    Reese = 4
    
class Baker:

    def __init__(self, env : simpy.Environment, sim_time : int, name : BakerNames, trained_on_mixer : bool, trained_on_oven : bool, trained_on_decorating : bool, shift_from : int, shift_to : int):

        self.name = name

        self.trained_on = {
            EquipmentNames.mixer : trained_on_mixer,
            EquipmentNames.oven : trained_on_oven,
            EquipmentNames.decorating_station : trained_on_decorating
        }

        self._environment = env
        self._sim_time = sim_time
        self.shift_from = shift_from
        self.shift_to = shift_to
        self.busy_until = None

    def set_as_busy(self, task_time : int) -> None:
        self.busy_until = self._environment.now + task_time

    def set_as_not_busy(self) -> None:
        self.busy_until = None

    def can_complete_task(self, equipment : EquipmentNames, recipe : Recipe) -> bool:
        task_time = None

        # It only takes 5 minutes to load mixer or oven
        if equipment == EquipmentNames.mixer or equipment == EquipmentNames.oven:
            task_time = 5
        # If decorating, get recipe's decorating time
        else:
            task_time = recipe.times[equipment.name]

        # Bakers won't start a task they can't complete before the end of their shift
        if self._environment.now >= self.shift_from and self._environment.now + task_time <= self.shift_to and self.busy_until == None and self.trained_on[equipment]:
            return True
        else:
            return False

    def print_baker(self) -> None:
        print(self.name.name, 'is trained on:', 
            EquipmentNames.mixer.name if self.trained_on[EquipmentNames.mixer] else '-',
            EquipmentNames.oven.name if self.trained_on[EquipmentNames.oven] else '-',
            EquipmentNames.decorating_station.name if self.trained_on[EquipmentNames.decorating_station] else '-',
        )
        if self._environment.now < self.shift_from:
            print(' - arriving in', self.shift_from - self._environment.now, 'mins')
        elif self._environment.now > self.shift_to:
            print(' - gone for the day')
        elif self.busy_until != None:
            print(' - busy for', self.busy_until - self._environment.now, 'mins')
        else:
            print(' - ready!')

        if self.shift_to < self._sim_time and self.shift_to > self._environment.now:
            print(' - leaving in', self.shift_to - self._environment.now, 'mins')

        