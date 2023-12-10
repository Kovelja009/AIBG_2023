from strategies.strategy import Strategy
from strategy_manager import StrategyManager
from game_state import Tile
import logging
from game_state import GameState
from typing import Union
from actions.action import Action
from harvest_tree_strategy import HarvestTreeStrategy
from game_utils import get_neighbouring_tiles
from game_state import EntityType, TileType
from actions.move_action import MoveAction
from actions.attack_action import AttackAction
import random


class RandomStrategy(Strategy):

    def __init__(self, manager: StrategyManager):
        super().__init__(manager)

    def execute_move(self, game_state: GameState) -> Union[Action, None]:
        player_tile = game_state.tiles[game_state.our_player.position]
        neighbours = get_neighbouring_tiles(game_state, player_tile)
        possible_actions = []
        attackable_types = [EntityType.ENEMY_PLAYER, EntityType.TREES]
        stepable_types = [EntityType.NONE,EntityType.LEAVES,EntityType.CHEST, EntityType.SKULL]
        for neighbour in neighbours:
            if neighbour.entity.type in attackable_types:
                possible_actions.append(AttackAction(neighbour.position))
            elif neighbour.entity.type in stepable_types:
                possible_actions.append(MoveAction(neighbour.position))

        if len(possible_actions) == 0:
            raise Exception("No possible actions")
        return random.choice(possible_actions)
