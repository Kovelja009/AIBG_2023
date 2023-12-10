from strategy import Strategy
from strategy_manager import StrategyManager
from game_state import Tile
from movement import get_next_move
import logging
from game_state import GameState
from typing import Union


class HasSwordStrategy(Strategy):

    def __init__(self, manager: StrategyManager):
        super().__init__(manager)

    def execute_move(self, game_state: GameState) -> Union[Tile, None]:
        logging.info("Executing HasSwordStrategy")
        raise NotImplementedError
