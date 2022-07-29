import simpy
from equipment import EquipmentNames
from recipe import RecipeNames
from baker import BakerNames
from state import State
from task import Task

SIM_TIME = 100

env = simpy.Environment()
state = State(env, SIM_TIME)

equipment_store = simpy.FilterStore(env, capacity=7)
equipment_store.items = [
    state.mixer_1,
    state.mixer_2,
    state.oven_1,
    state.oven_2,
    state.oven_3,
    state.decorating_station_1,
    state.decorating_station_2
]

baker_store = simpy.FilterStore(env, capacity=4)
baker_store.items = [
    state.baker_1,
    state.baker_2,
    state.baker_3,
    state.baker_4
]

# ingredient_store = simpy.FilterStore(env, capacity=6)
# ingredient_store.items = [
#     state.sugar_container,
#     state.butter_container,
#     state.eggs_container,
#     state.flour_container,
#     state.baking_soda_container,
#     state.milk_container
# ]



task : Task = Task()

def manage() -> None:

    while True:
        print('\n----------------------------------------------------')
        print('\ntime:', env.now)
        print('time remaining:', SIM_TIME - env.now)
        yield_time = 1

        if len(equipment_store.items) > 0 and len(baker_store.items) > 0:
            state.print_dessert_case()
            state.print_bakers()
            state.print_equipment()
            state.print_raw_materials()
            valid_task = False

            while not valid_task:
                baker = int(input('\ninput baker (1.Chip, 2.Coco, 3.Eclair, 4.Reese, 0.wait): '))
                equipment = int(input('input action (1.mix, 2.bake, 3.decorate, 0.wait): '))
                recipe = int(input('input recipe (1.cookies, 2.cupcakes, 3.cake, 0.wait): '))
                refill = int(input('input raw material to refill (1.sugar, 2.butter, 3.eggs, 4.flour, 5.baking soda, 6.milk, 0.wait): '))

                if task.validate_task(state, equipment_store, equipment, baker_store, baker, recipe):
                    env.process(task.ingredient_task(state,recipe, refill))
                    # If waiting, get the amount of time until the next state change and wait that long
                    if baker == 0 and equipment == 0 and recipe == 0:
                        yield_time = state.get_min_wait_time()

                    else:
                        env.process(task.equipment_task(env, state, equipment_store, EquipmentNames(equipment), RecipeNames(recipe)))
                        env.process(task.baker_task(env, state, baker_store, BakerNames(baker), EquipmentNames(equipment), RecipeNames(recipe)))

                    valid_task = True

                else:
                    print('\ninput invalid, try again')

        yield env.timeout(yield_time)

env.process(manage())
env.run(until=SIM_TIME)

print('\nGAME OVER')
state.print_dessert_case()
