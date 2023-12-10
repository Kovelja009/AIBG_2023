from strategies.strategy import Strategy
from strategy_manager import StrategyManager
from game_state import Tile
import logging
from game_state import GameState
from typing import Union
from actions.action import Action
from harvest_tree_strategy import HarvestTreeStrategy

class HasSwordStrategy(Strategy):

    def __init__(self, manager: StrategyManager):
        super().__init__(manager)

    def execute_move(self, game_state: GameState) -> Union[Action, None]:
        logging.info("Executing HasSwordStrategy")
        self.strategy_manager.transition(game_state, HarvestTreeStrategy(self.strategy_manager))
        return None
