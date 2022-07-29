import math
import simpy
from typing import Dict, Any
from baker import Baker, BakerNames
from recipe import Recipe, RecipeNames
from equipment import Equipment, EquipmentNames


class State:

    def __init__(self, environment : simpy.Environment, sim_time : int):

        self.recipes = {
            RecipeNames.cookies : Recipe(RecipeNames.cookies.name, 12, 8, 10, 5),
            RecipeNames.cupcakes : Recipe(RecipeNames.cupcakes.name, 6, 10, 15, 10),
            RecipeNames.cake : Recipe(RecipeNames.cake.name, 1, 10, 20, 15),
        }

        self.baker_1 = Baker(environment, sim_time, BakerNames.Chip, True, True, True, 0, sim_time)
        self.baker_2 = Baker(environment, sim_time, BakerNames.Coco, True, True, False, 0, sim_time)
        self.baker_3 = Baker(environment, sim_time, BakerNames.Eclair, True, True, True, 0, math.floor(sim_time / 2))
        self.baker_4 = Baker(environment, sim_time, BakerNames.Reese, False, False, True, math.floor(sim_time / 2), sim_time)

        self.mixer_1 = Equipment(EquipmentNames.mixer.name, environment)
        self.mixer_2 = Equipment(EquipmentNames.mixer.name, environment)
        self.oven_1 = Equipment(EquipmentNames.oven.name, environment)
        self.oven_2 = Equipment(EquipmentNames.oven.name, environment)
        self.oven_3 = Equipment(EquipmentNames.oven.name, environment)
        self.decorating_station_1 = Equipment(EquipmentNames.decorating_station.name, environment)
        self.decorating_station_2 = Equipment(EquipmentNames.decorating_station.name, environment)

        self.sugar_container = simpy.Container(environment, init = 10, capacity=10)
        self.butter_container = simpy.Container(environment, init = 5, capacity=5)
        self.eggs_container = simpy.Container(environment, init = 20, capacity=20)
        self.flour_container = simpy.Container(environment, init = 10, capacity=10)
        self.baking_soda_container = simpy.Container(environment, init = 5, capacity=5)
        self.milk_container = simpy.Container(environment, init = 5, capacity=5)

        # Holds completed items
        self.dessert_case = {
            RecipeNames.cookies : 0,
            RecipeNames.cupcakes : 0,
            RecipeNames.cake : 0,
        }

        self._env = environment
        self._sim_time = sim_time

    def print_equipment(self) -> None:
        print('\nBAKERY EQUIPMENT')
        self.mixer_1.print_equipment()
        self.mixer_2.print_equipment()
        self.oven_1.print_equipment()
        self.oven_2.print_equipment()
        self.oven_3.print_equipment()
        self.decorating_station_1.print_equipment()
        self.decorating_station_2.print_equipment()

    def print_raw_materials(self) -> None:
        print('\nRAW MATERIALS')
        print("Amount of sugar: ",self.sugar_container.level)
        print("Amount of butter: ",self.butter_container.level)
        print("Amount of eggs: ",self.eggs_container.level)
        print("Amount of flour: ",self.flour_container.level)
        print("Amount of baking soda: ",self.baking_soda_container.level)
        print("Amount of milk: ",self.milk_container.level)


    def print_bakers(self) -> None:
        print('\nBAKERS')
        self.baker_1.print_baker()
        self.baker_2.print_baker()
        self.baker_3.print_baker()
        self.baker_4.print_baker()

    def print_dessert_case(self) -> None:
        print('\nDESSERT CASE')
        print(RecipeNames.cookies.name, self.dessert_case[RecipeNames.cookies])
        print(RecipeNames.cupcakes.name, self.dessert_case[RecipeNames.cupcakes])
        print(RecipeNames.cake.name, self.dessert_case[RecipeNames.cake])

    # Returns the amount of time until the next state change (equipment or baker becomes available)
    def get_min_wait_time(self) -> int:
        wait_times = [
            self.mixer_1.remaining_time(),
            self.mixer_2.remaining_time(),
            self.oven_1.remaining_time(),
            self.oven_2.remaining_time(),
            self.oven_3.remaining_time(),
            self.decorating_station_1.remaining_time(),
            self.decorating_station_2.remaining_time(),
            self.baker_1.busy_until - self._env.now if self.baker_1.busy_until != None else 0,
            self.baker_2.busy_until - self._env.now if self.baker_2.busy_until != None else 0,
            self.baker_3.busy_until - self._env.now if self.baker_3.busy_until != None else 0,
            self.baker_4.busy_until - self._env.now if self.baker_4.busy_until != None else 0,
        ]
        wait_times = [x for x in wait_times if x > 0]

        # Needed when everything is available, but the user decides to wait
        # This is needed at the end of the game when bakers won't start a task they can't complete by end of their shift
        # This will end the game
        if len(wait_times) == 0:
            return self._sim_time

        return min(wait_times)

    def get_state(self) -> Dict[str, Any]:
        return {

            # EQUIPMENT
            'mixer_1_recipe' : RecipeNames(self.mixer_1.current_recipe.name).value if self.mixer_1.current_recipe != None else 0,
            'mixer_1_time_remaining' : self.mixer_1.remaining_time(),
            'mixer_2_recipe' : RecipeNames(self.mixer_2.current_recipe.name).value if self.mixer_2.current_recipe != None else 0,
            'mixer_2_time_remaining' : self.mixer_2.remaining_time(),

            'oven_1_recipe' : RecipeNames(self.oven_1.current_recipe.name).value if self.oven_1.current_recipe != None else 0,
            'oven_1_time_remaining' : self.oven_1.remaining_time(),
            'oven_2_recipe' : RecipeNames(self.oven_2.current_recipe.name).value if self.oven_2.current_recipe != None else 0,
            'oven_2_time_remaining' : self.oven_2.remaining_time(),
            'oven_3_recipe' : RecipeNames(self.oven_3.current_recipe.name).value if self.oven_3.current_recipe != None else 0,
            'oven_3_time_remaining' : self.oven_3.remaining_time(),

            'decorating_station_1_recipe' : RecipeNames(self.decorating_station_1.current_recipe.name).value if self.decorating_station_1.current_recipe != None else 0,
            'decorating_station_1_time_remaining' : self.decorating_station_1.remaining_time(),
            'decorating_station_2_recipe' : RecipeNames(self.decorating_station_2.current_recipe.name).value if self.decorating_station_2.current_recipe != None else 0,
            'decorating_station_2_time_remaining' : self.decorating_station_2.remaining_time(),

            # BAKERS
            

            # RECIPES

            # DESSERT CASE
        }