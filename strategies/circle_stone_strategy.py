from typing import Union
from game_state import GameState, EntityType, Tile
from strategies.strategy import Strategy
from game_utils import get_closest_tile_of_type
from movement import get_next_move
from actions.action import Action
from actions.move_action import MoveAction


class CircleStoneStrategy(Strategy):

    def __init__(self, strategy_manager):
        super().__init__(strategy_manager)

    def execute_move(self, game_state: GameState) -> Union[Action, int]:
        closest_stone, dist = get_closest_tile_of_type(game_state, EntityType.STONE, game_state.our_player.position)
        next_tile, _ = get_next_move(game_state, game_state.our_player.position, closest_stone.position)
        return MoveAction(next_tile.position)
