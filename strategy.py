from abc import ABC, abstractmethod
from game_state import GameState

class Strategy(ABC):  
    def __init__(self, strategy_manager) -> None:
        self.strategy_manager = strategy_manager

    @abstractmethod
    def execute(self, game_state : GameState) -> None:
        pass