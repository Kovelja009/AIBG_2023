from strategies.strategy import Strategy
from strategy_manager import StrategyManager
from game_state import Tile, EntityType
from game_utils import get_closest_tile_of_type
from movement import get_next_move
import logging
from game_state import GameState
from typing import Union
from actions.action import Action
from actions.move_action import MoveAction
from game_utils import get_neighbouring_tiles
from math import ceil
from actions.attack_action import AttackAction
from movement import ensure_valid_move
from exceptions import MoveResultsInConflictException



class HarvestTreeStrategy(Strategy):
    arrived_at_tree: bool
    score_at_start: int

    def __init__(self, manager: StrategyManager):
        super().__init__(manager)
        self.arrived_at_tree = False
        self.score_at_start = 0

    def tree_has_enemy_as_neighbor(self, game_state: GameState, tree: Tile) -> bool:
        neighbors = get_neighbouring_tiles(game_state, tree)
        for neighbor in neighbors:
            if neighbor.entity.type == EntityType.ENEMY_PLAYER:
                return True
        return False

    def switch_tree(self, game_state: GameState, tree: Tile) -> Tile:
        raise NotImplementedError

    def execute_move(self, game_state: GameState) -> Union[Action, None]:
        logging.info("Executing HarvestTreeStrategy")

        # Find the closest tree
        our_player = game_state.our_player
        tree, dist = get_closest_tile_of_type(game_state, EntityType.TREES, our_player.position)
        if not self.arrived_at_tree and dist == 1:
            self.arrived_at_tree = True
            self.score_at_start = our_player.score

        if not self.arrived_at_tree:
            logging.info("Going to closest tree")
            # Move to the tree
            try:
                next_tile, _ = get_next_move(game_state, our_player.position, tree.position)
                return MoveAction(next_tile.position)
            except:
                logging.error("Conflict while moving to tree")
                return None  # TODO: Handle this
        else:
            logging.info("Harvesting tree")
            time_to_harvest = ceil(tree.entity.health / our_player.attackPower)
            if time_to_harvest == 2 and self.tree_has_enemy_as_neighbor(game_state, tree):
                logging.info("Tree has enemy as neighbor, should probably switch") # TODO: Implement this
            attack_action = AttackAction(tree.position)
            try:
                ensure_valid_move(game_state, attack_action)
                return attack_action
            except MoveResultsInConflictException:
                logging.error("Conflict while harvesting tree")
                # TODO: Switch tree for now just move in a valid direction
                player_tile = game_state.tiles[our_player.position]
                for neighbor in get_neighbouring_tiles(game_state, player_tile):
                    alt_action = MoveAction(neighbor.position)
                    try:
                        ensure_valid_move(game_state, alt_action)
                        return alt_action
                    except:
                        pass
                return None

