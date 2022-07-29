from pickle import FALSE
import simpy
from equipment import Equipment, EquipmentNames
from recipe import Recipe, RecipeNames
from baker import Baker, BakerNames
from state import State

DEFAULT_SUGAR = 1
DEFAULT_BUTTER = 1
DEFAULT_EGGS = 1
DEFAULT_FLOUR = 1
DEFAULT_BAKING_SODA = 1
DEFAULT_MILK = 1

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

    def ingredient_task(self,  state : State, recipe : int, refill : int) -> bool:

        # Get the recipe and required ingredients
        if recipe == 1:
            required_ingredients = {
            'sugar' : DEFAULT_SUGAR,
            'butter' : DEFAULT_BUTTER,
            'eggs' : DEFAULT_EGGS,
            'flour' : DEFAULT_FLOUR,
            'baking_soda' : 0 ,
            'milk' : 0
        }

        if recipe == 2:
            required_ingredients = {
            'sugar' : DEFAULT_SUGAR,
            'butter' : DEFAULT_BUTTER,
            'eggs' : 2,
            'flour' : DEFAULT_FLOUR,
            'baking_soda' :DEFAULT_BAKING_SODA ,
            'milk' : DEFAULT_MILK
        }

        if recipe == 3:
            required_ingredients = {
            'sugar' : DEFAULT_SUGAR,
            'butter' : DEFAULT_BUTTER,
            'eggs' : 2,
            'flour' : DEFAULT_FLOUR,
            'baking_soda' :DEFAULT_BAKING_SODA ,
            'milk' : 2
        }

        #Check level
        sugar = state.sugar_container.level
        butter = state.butter_container.level
        eggs = state.eggs_container.level
        flour = state.flour_container.level
        baking_soda = state.baking_soda_container.level
        milk = state.milk_container.level

        #If validate take it 
        if required_ingredients['sugar'] < sugar:
            yield state.sugar_container.get(required_ingredients['sugar'])
        else:
            print("Need to buy more sugar")
            return FALSE
        
        if required_ingredients['butter'] < butter:
            yield state.butter_container.get(required_ingredients['butter'])
        else:
            print("Need to buy more butter")
            return FALSE


        if required_ingredients['eggs'] < eggs:
            yield state.eggs_container.get(required_ingredients['eggs'])
        else:
            print("Need to buy more eggs")
            return FALSE

        if required_ingredients['flour'] < flour:
            yield state.flour_container.get(required_ingredients['flour'])
        else:
            print("Need to buy more flour")
            return FALSE

        if required_ingredients['baking_soda'] < baking_soda & required_ingredients['baking_soda'] != 0:
            yield state.baking_soda_container.get(required_ingredients['baking_soda'])
        else:
            print("Need to buy more baking soda")
            return FALSE

        if required_ingredients['milk'] < milk & required_ingredients['milk'] != 0:
            yield state.milk_container.get(required_ingredients['milk'])
        else:
            print("Need to buy more milk")
            return FALSE

        if refill != 0:
            if refill == 1:
                yield state.sugar_container.put(10)
            if refill == 2:
                yield state.butter_container.put(5)
            if refill == 3:
                yield state.eggs_container.put(20)
            if refill == 4:
                yield state.flour_container.put(10)
            if refill == 5:
                yield state.baking_soda_container.put(5)
            if refill == 6:
                yield state.milk_container.put(5)
        return True

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