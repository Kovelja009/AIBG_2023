from exceptions import MoveResultsInConflictException
from game_state import Tile, GameState
from typing import Tuple
from game_state import EntityType, TileType
from actions.action import Action
from actions.attack_action import AttackAction
from actions.move_action import MoveAction
from graph import Graph, enemy_is_neighbor_of_tile, check_move_is_safe


def distance(game_state: GameState, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> int:
    graph = Graph(game_state.tiles, game_state.our_player.sword)
    next_tile, dist = graph.dijkstra(start_pos, end_pos)
    return dist


def get_next_move(game_state: GameState, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> Tuple[Tile, int]:
    graph = Graph(game_state, game_state.our_player.sword)
    return graph.dijkstra(start_pos, end_pos)


def ensure_valid_move(game_state: GameState, action: Action) -> None:
    """
    Try to execute a move to a tile, if it is safe to do so
    """
    if isinstance(action, MoveAction):
        if not check_move_is_safe(game_state, action):
            raise MoveResultsInConflictException
    else:
        if not check_move_is_safe(game_state, action):
            raise MoveResultsInConflictException
