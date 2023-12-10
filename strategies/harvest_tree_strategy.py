from strategy import Strategy
from strategy_manager import StrategyManager
from game_state import Tile, EntityType
from game_utils import get_closest_tile_of_type
from movement import get_next_move
import logging
from game_state import GameState
from typing import Union


class HarvestTreeStrategy(Strategy):
    arrived_at_tree: bool
    def __init__(self, manager: StrategyManager):
        super().__init__(manager)
        self.arrived_at_tree = False

    def execute_move(self, game_state: GameState) -> Union[Tile, None]:
        logging.info("Executing HarvestTreeStrategy")

        # Find the closest tree
        our_player = game_state.our_player
        tree, dist = get_closest_tile_of_type(game_state, EntityType.TREES, our_player.position)
        self.arrived_at_tree =
        if not self.arrived_at_tree:
            logging.info("Going to closest tree")
            # Move to the tree
            try:
                next_tile = get_next_move(game_state, our_player.position, tree.position)
                return next_tile
            except:
                logging.error("Conflict while moving to tree")
                return None # TODO: Handle this
        else:

