from typing import Dict, Any
import simpy
from equipment import EquipmentNames
from recipe import RecipeNames
from baker import BakerNames
from state import State
from task import Task

class BakerySim:

    def __init__(self):
        self.SIM_TIME = 100

        self.env = simpy.Environment()

        # TODO: have state accept config and update state
        self.state = State(self.env, self.SIM_TIME)

        self.equipment_store = simpy.FilterStore(self.env, capacity=7)
        self.equipment_store.items = [
            self.state.mixer_1,
            self.state.mixer_2,
            self.state.oven_1,
            self.state.oven_2,
            self.state.oven_3,
            self.state.decorating_station_1,
            self.state.decorating_station_2
        ]

        self.baker_store = simpy.FilterStore(self.env, capacity=4)
        self.baker_store.items = [
            self.state.baker_1,
            self.state.baker_2,
            self.state.baker_3,
            self.state.baker_4
        ]

        self.task : Task = Task()
        self.action_time : int = None

    def new_manage(self, action : Dict[str, Any]):
        baker = action['baker']
        equipment = action['equipment']
        recipe = action['recipe']
        #raw_ingredients = action['raw_ingredients']
        yield_time = 1

        if self.task.validate_task(self.state, self.equipment_store, equipment, self.baker_store, baker, recipe):

            self.env.process(self.task.ingredient_task(self.state,recipe))

            # If waiting, get the amount of time until the next state change and wait that long
            if baker == 0 and equipment == 0 and recipe == 0:
                yield_time = self.state.get_min_wait_time()

            else:
                self.env.process(self.task.equipment_task(self.env, self.state, self.equipment_store, EquipmentNames(equipment), RecipeNames(recipe)))
                self.env.process(self.task.baker_task(self.env, self.state, self.baker_store, BakerNames(baker), EquipmentNames(equipment), RecipeNames(recipe)))

        # Update state to say that sim has ended/terminating action
        else:
            self.state.sim_halted = True
            return self.state.get_state()

        self.action_time = yield_time

        # Make time pass
        yield self.env.timeout(yield_time)

        # TODO: Maybe find a way to make sure the user/bonsai is only prompted for decision when there is a baker and equipment available
        # After is taken, keep waiting until both a piece of equipment and a baker are free
        # No action can be taken without both
        # This still might result in a scenario where the user MUST wait, but it will decrease

        #while len(self.equipment_store.items) == 0 or len(self.baker_store.items) == 0:
        #    yield self.env.timeout(self.state.get_min_wait_time())

        self.state.print_dessert_case()
        self.state.print_bakers()
        self.state.print_equipment()
        self.state.print_raw_materials()

        #return self.state.get_state()

    def manage(self) -> None:

    #while True:
        print('\n----------------------------------------------------')
        print('\ntime:', self.env.now)
        print('time remaining:', self.SIM_TIME - self.env.now)
        yield_time = 1

        if len(self.equipment_store.items) > 0 and len(self.baker_store.items) > 0:
            self.state.print_dessert_case()
            self.state.print_bakers()
            self.state.print_equipment()
            self.state.print_raw_materials()
            valid_task = False

            while not valid_task:

                action : Dict[str, Any] = self.game_controller_step()
                baker = action['baker']
                equipment = action['equipment']
                recipe = action['recipe']
                # baker = int(input('\ninput baker (1.Chip, 2.Coco, 3.Eclair, 4.Reese, 0.wait): '))
                # equipment = int(input('input action (1.mix, 2.bake, 3.decorate, 0.wait): '))
                # recipe = int(input('input recipe (1.cookies, 2.cupcakes, 3.cake, 0.wait): '))

                if self.task.validate_task(self.state, self.equipment_store, equipment, self.baker_store, baker, recipe):
                    self.env.process(self.task.ingredient_task(self.state,recipe))
                    # If waiting, get the amount of time until the next state change and wait that long
                    if baker == 0 and equipment == 0 and recipe == 0:
                        yield_time = self.state.get_min_wait_time()

                    else:
                        self.env.process(self.task.equipment_task(self.env, self.state, self.equipment_store, EquipmentNames(equipment), RecipeNames(recipe)))
                        self.env.process(self.task.baker_task(self.env, self.state, self.baker_store, BakerNames(baker), EquipmentNames(equipment), RecipeNames(recipe)))

                    valid_task = True

                else:
                    print('\ninput invalid, try again')

        yield self.env.timeout(yield_time)

    def reset(self, config : Dict[str, Any]) -> Dict[str, Any]:

        # TODO: Set state using config
        self.state.set_state(config)

        # TODO: figure out where to call env.run()
        #self.env.process(self.manage())
        self.env.run(until=self.SIM_TIME)

        #print('\nGAME OVER')
        #self.state.print_dessert_case()
        return self.state.get_state()

    # def game_controller_step(self):

    #     baker = int(input('\ninput baker (1.Chip, 2.Coco, 3.Eclair, 4.Reese, 0.wait): '))
    #     equipment = int(input('input action (1.mix, 2.bake, 3.decorate, 0.wait): '))
    #     recipe = int(input('input recipe (1.cookies, 2.cupcakes, 3.cake, 0.wait): '))

    #     return {
    #         'baker' : baker,
    #         'equipment' : equipment,
    #         'recipe' : recipe,
    #         'raw_ingredients' : None
    #     }

    # TODO: Figure out how to return the state (from new_manage) after calling process(new_manage), which doesn't return anything :(
    def step(self, action):

        # new_manage cannot return anything because it will be wrapped by env.process
        # time needs to pass
        # and then we need to return the state
        self.env.process(self.new_manage(action))

        # Time needs to pass here
        #run_until = self.env.now + self.action_time
        #self.env.run(until=run_until)

        self.env.step()

        return self.state.get_state()

bakery_sim = BakerySim()
bakery_sim.reset({'nothing' : None})
bakery_sim.step({'baker' : 1, 'equipment': 1, 'recipe': 1})
bakery_sim.step({'baker' : 2, 'equipment': 1, 'recipe': 2})
        
