from enum import Enum 

# DEFAULT_SUGAR = 1
# DEFAULT_BUTTER = 1
# DEFAULT_EGGS = 1
# DEFAULT_FLOUR = 1
# DEFAULT_BAKING_SODA = 1
# DEFAULT_MILK = 1

class RecipeNames(Enum):
    none = 0
    cookies = 1
    cupcakes = 2
    cake = 3

class Recipe:

    def __init__(self, name : str, batch_yield : int, mix_time : int, bake_time : int, decorate_time : int):
        self.name = name
        self.batch_yield = batch_yield
        self.times = {
            'mixer' : mix_time,
            'oven' : bake_time,
            'decorating_station' : decorate_time
        }
    #     self.required_ingredients = {
    #         'sugar' : DEFAULT_SUGAR,
    #         'butter' : DEFAULT_BUTTER,
    #         'eggs' : DEFAULT_EGGS,
    #         'flour' : DEFAULT_FLOUR,
    #         'baking_soda' :DEFAULT_BAKING_SODA ,
    #         'milk' : DEFAULT_MILK
    #     }

    # def set_ingredients(self,recipe, recipe_name :int):
    #     if recipe_name == 1:
    #         recipe.required_ingredients = {
    #         'sugar' : DEFAULT_SUGAR,
    #         'butter' : DEFAULT_BUTTER,
    #         'eggs' : 2,
    #         'flour' : DEFAULT_FLOUR,
    #         'baking_soda' : 0,
    #         'milk' : 0
    #         }

    #     if recipe_name == 2:
    #         recipe.required_ingredients = {
    #         'sugar' : DEFAULT_SUGAR,
    #         'butter' : DEFAULT_BUTTER,
    #         'eggs' : 2,
    #         'flour' : DEFAULT_FLOUR,
    #         'baking_soda' : DEFAULT_BAKING_SODA,
    #         'milk' : DEFAULT_MILK
    #         }

    #     if recipe_name == 3:
    #         recipe.required_ingredients = {
    #         'sugar' : DEFAULT_SUGAR,
    #         'butter' : DEFAULT_BUTTER,
    #         'eggs' : 2,
    #         'flour' : DEFAULT_FLOUR,
    #         'baking_soda' : DEFAULT_BAKING_SODA,
    #         'milk' : DEFAULT_MILK
    #         }
    #     return recipe


