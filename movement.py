from exceptions import MoveResultsInConflictException
from game_state import Tile, GameState
from typing import Tuple
from game_state import EntityType, TileType
from actions.action import Action
from actions.attack_action import AttackAction
from actions.move_action import MoveAction
from graph import Graph
from game_utils import stone_attacked_tiles


def distance(game_state: GameState, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> int:
    graph = Graph(game_state.tiles, game_state.our_player.sword)
    next_tile, dist = graph.dijkstra(start_pos, end_pos)
    return dist


def check_move_is_safe(game_state: GameState, action: Action) -> bool:
    """
    Check if moving to this tile results in being next to an enemy player
    """
    graph = Graph(game_state.tiles, game_state.our_player.sword)
    enemy_players = [player for player in game_state.players if player.idx != game_state.our_idx]
    for player in enemy_players:
        _, dist = graph.bfs(player.position, action.position)
        if dist == 1:
            return False
    return True


def get_next_move(game_state: GameState, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> Tuple[Tile, int]:
    graph = Graph(game_state, game_state.our_player.sword)
    return graph.dijkstra(start_pos, end_pos)


def ensure_valid_move(game_state: GameState, action: Action) -> None:
    """
    Try to execute a move to a tile, if it is safe to do so
    """
    if action is MoveAction:
        if not __check_move_is_safe(game_state, action):
            raise MoveResultsInConflictException
    else:
        if not __check_move_is_safe(game_state, action):
            raise MoveResultsInConflictException
