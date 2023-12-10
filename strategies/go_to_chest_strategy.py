from strategy import Strategy
from strategy_manager import StrategyManager
from game_state import TileType, EntityType, Tile
from game_utils import get_all_tiles_of_type, run_dijkstra
import logging


class GoToChestStrategy(Strategy):
    def __init__(self, manager: StrategyManager):
        super().__init__(manager)

    def can_go_over_leaf(self, game_state) -> bool:
        """
        Check if we can go over a leaf to get to the chest
        """
        # Try going over every leaf node
        leaf_tiles = get_all_tiles_of_type(game_state, EntityType.LEAVES)
        for leaf in leaf_tiles:
            _, dist = run_dijkstra(game_state, leaf.position, game_state.our_player.position)
            if dist < 3:
                return True



    def execute_move(self, game_state) -> Tile:
        # Find chest position that corresponds to our player
        chests = get_all_tiles_of_type(game_state, EntityType.CHEST)
        try:
            our_chest = [chest for chest in chests if chest.entity.idx == game_state.our_idx][0]
        except IndexError:
            logging.error("Could not find our chest")
            return  # TODO: Handle strategy failure

        our_player = game_state.our_player
        next_tile, _ = run_dijkstra(game_state, our_player.position, our_chest.position)
