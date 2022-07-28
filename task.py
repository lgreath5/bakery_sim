import simpy
from equipment import Equipment, EquipmentNames
from recipe import Recipe, RecipeNames
from baker import Baker, BakerNames
from state import State

class Task:

    def __init__(self):
        pass

    def equipment_task(self, env : simpy.Environment, state : State, equipment_store : simpy.FilterStore, equipment : EquipmentNames, recipeName : RecipeNames) -> None :

        # Get the full recipe from the state
        recipe : Recipe = state.recipes[recipeName]

        # If baking or decorating, empty the previous piece of equipment that recipe is currently in
        if equipment != EquipmentNames.mixer:
            from_equipment : Equipment = yield equipment_store.get(lambda x: x.name == EquipmentNames(equipment.value -1).name and x.current_recipe == recipe and x.remaining_time() == 0)
            from_equipment.set_not_in_use()
            yield equipment_store.put(from_equipment)

        # Move recipe to next piece of equipment
        to_equipment : Equipment = yield equipment_store.get(lambda x: x.name == equipment.name and x.current_recipe == None)
        to_equipment.set_in_use(recipe, env.now)
        yield env.timeout(recipe.times[equipment.name])

        # If recipe was just decorated, it is complete
        # Empty the decorating station and add score
        if equipment == EquipmentNames.decorating_station:
            to_equipment.set_not_in_use()
            state.dessert_case[recipeName] += recipe.batch_yield

        yield equipment_store.put(to_equipment)

    def baker_task(self, env : simpy.Environment, state : State, baker_store : simpy.FilterStore, baker : BakerNames, equipment : EquipmentNames, recipe_name : RecipeNames) -> None:

        baker : Baker = yield baker_store.get(lambda x: x.name == baker)
        task_time = None
        
        # The baker only needs 5 minutes to load the mixer or over and then their free again
        if equipment == EquipmentNames.mixer or equipment == EquipmentNames.oven:
            task_time = 5
        # If decorating, get recipe's decorating time
        else:
            task_time = state.recipes[recipe_name].times[equipment.name]

        baker.set_as_busy(task_time)
        yield env.timeout(task_time)
        baker.set_as_not_busy()
        yield baker_store.put(baker)

    def validate_task(self, state : State, equipment_store : simpy.FilterStore, equipment : int, baker_store : simpy.FilterStore, baker : int, recipe : int) -> bool:
        
        # Waiting is always a valid option
        if baker == 0 and equipment == 0 and recipe == 0:
            return True

        # Make sure baker, equipment, and recipe options exist
        if equipment not in [x.value for x in EquipmentNames] or recipe not in [x.value for x in RecipeNames] or baker not in [x.value for x in BakerNames]:
            return False

        actual_recipe = state.recipes[RecipeNames(recipe)]

        # Make sure the baker is available and qualified
        baker_validated = False
        available_bakers = [x for x in baker_store.items if x.name == BakerNames(baker) and x.can_complete_task(EquipmentNames(equipment), actual_recipe)]
        #available_bakers = [x for x in baker_store.items if x.name == BakerNames(baker).name]
        #can_task = available_bakers.pop().can_complete_task(EquipmentNames(equipment), actual_recipe)

        # Make sure there is an empty piece of matching equipment
        available_equipment = [x for x in equipment_store.items if x.name == EquipmentNames(equipment).name and x.current_recipe == None]
        available_recipes = []

        # If mixing a new batch, recipe is always available (ingredients are in infinite supply)
        if EquipmentNames(equipment) == EquipmentNames.mixer:
            available_recipes = [x.name for x in RecipeNames]

        # If baking or decorating, make sure there is batter or pastry ready for this step
        else:
            available_recipes = [x.current_recipe.name for x in equipment_store.items if x.name == EquipmentNames(equipment - 1).name and x.current_recipe != None]

        return len(available_bakers) > 0 and len(available_equipment) > 0 and RecipeNames(recipe).name in available_recipes