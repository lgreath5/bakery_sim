from typing import Dict, Any
from abc import ABC, abstractmethod
from bakery_sim import BakerySim

class Action:

    def __init__(self, baker, equipment, recipe):
        self.baker = baker
        self.equipment = equipment
        self.recipe = recipe

class Controller(ABC):

    @abstractmethod
    def reset(self, config : Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def step(self, action : Dict[str, Any]) -> Dict[str, Any]:
        pass

class GameController(Controller):

    def __init__(self):
        pass

    def reset(self, config : Dict[str, Any]) -> Dict[str, Any]:
        pass


    def step() -> Dict[str, Any]:
        pass