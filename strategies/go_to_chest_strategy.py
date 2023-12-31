from strategies.strategy import Strategy
from strategy_manager import StrategyManager
from game_state import EntityType, Tile
from game_utils import get_all_tiles_of_type
from movement import get_next_move
from strategies.go_to_chest_over_leaf_strategy import GoToChestOverLeafStrategy
from typing import Union
import logging
from actions.action import Action
from actions.move_action import MoveAction
from strategies.circle_stone_strategy import CircleStoneStrategy

DISTANCE_THRESHOLD = 3


class GoToChestStrategy(Strategy):
    tried_leaf: bool

    def __init__(self, manager: StrategyManager):
        super().__init__(manager)
        self.tried_leaf = False

    def can_go_over_leaf(self, game_state, chest: Tile) -> Tile:
        """
        Check if we can go over a leaf to get to the chest
        """
        leaf_tiles = get_all_tiles_of_type(game_state, EntityType.LEAVES)
        _, optimal_dist = get_next_move(game_state, game_state.our_player.position, chest.position)

        closest_leaf = None
        min_dist = float('inf')
        # Try going over every leaf node
        for leaf in leaf_tiles:
            _, dist1 = get_next_move(game_state, game_state.our_player.position, leaf.position)
            _, dist2 = get_next_move(game_state, leaf.position, game_state.our_player.position)
            if dist1 + dist2 < optimal_dist + DISTANCE_THRESHOLD:
                if dist1 < min_dist:
                    min_dist = dist1
                    closest_leaf = leaf
        return closest_leaf

    def execute_move(self, game_state) -> Union[Action, None]:
        print("INFO: Executing GoToChestStrategy")
        # Player has sword transition to go to stone
        if game_state.our_player.sword:
            print("INFO: Player has sword transitioning to CircleStoneStrategy")
            self.strategy_manager.transition(game_state, CircleStoneStrategy(self.strategy_manager))

        # Find chest position that corresponds to our player
        chests = get_all_tiles_of_type(game_state, EntityType.CHEST)
        try:
            our_chest = [chest for chest in chests if chest.entity.idx+1 == game_state.our_player.playerIdx][0]
        except IndexError:
            print("ERROR: Could not find our chest")
            return None  # TODO: Handle strategy failure

        if not self.tried_leaf:
            print("INFO: Trying to go over leaf")
            leaf = self.can_go_over_leaf(game_state, our_chest)
            self.tried_leaf = True

            if leaf:
                print("INFO: Going over leaf to the chest")
                self.strategy_manager.transition(game_state, GoToChestOverLeafStrategy(self.strategy_manager, leaf, our_chest))
                return None
        try:
            next_tile, _ = get_next_move(game_state, game_state.our_player.position, our_chest.position)
            return MoveAction(next_tile.position)
        except:
            return None  # TODO: Override strategy and force move
