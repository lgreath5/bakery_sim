from enum import Enum 

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

