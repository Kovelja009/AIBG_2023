from abc import ABC, abstractmethod
from game_state import GameState, Tile
from strategy_manager import StrategyManager

class Strategy(ABC):
    strategy_manager: StrategyManager
    def __init__(self, strategy_manager) -> None:
        self.strategy_manager = strategy_manager

    @abstractmethod
    def execute_move(self, game_state: GameState) -> Tile:
        pass
