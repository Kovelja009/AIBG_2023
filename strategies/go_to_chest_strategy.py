from strategy import Strategy
from strategy_manager import StrategyManager
from game_state import TileType, EntityType
from game_utils import get_all_tiles_of_type
import logging

class GoToChestStrategy(Strategy):
    def __init__(self, manager: StrategyManager):
        super().__init__(manager)
    
    def execute(self, game_state):
        # Find chest position that corresponds to our player
        chests = get_all_tiles_of_type(game_state, EntityType.CHEST)
        our_chest = None
        try:
            our_chest = [chest for chest in chests if chest.entity.idx == game_state.our_idx][0]
        except IndexError:
            logging.error("Could not find our chest")
            return # TODO: Handle strategy failure

        our_player = game_state.players[game_state.our_idx]

