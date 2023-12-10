from typing import Tuple
from game_state import TileType, EntityType, GameState, Tile
from exceptions import MoveResultsInConflictException


def get_all_tiles_of_type(game_state: GameState, entity_type: EntityType):
    return [tile for tile in game_state.tiles.values() if tile.entity.type == entity_type]


def __node_dist(node1: Tuple[int, int], node2: Tuple[int, int]) -> int:
    """
    Returns the distance between two nodes on hexagonal grid by runing a bfs from node1 to node2
    """
    raise NotImplementedError


def run_dijkstra(game_state: GameState, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> Tuple[Tile, int]:
    """
    Returns the next tile to move to on the shortest path from start_tile to end_tile
    """
    raise NotImplementedError


def get_next_move(game_state : GameState, start_pos : Tuple[int, int], end_pos : Tuple[int, int]) -> Tuple[Tile, int]:
    raise NotImplementedError


def __check_move_is_safe(game_state: GameState, next_tile: Tile) -> bool:
    """
    Check if moving to this tile results in being next to an enemy player
    """
    enemy_players = [player for player in game_state.players if player.idx != game_state.our_idx]
    for player in enemy_players:
        if __node_dist(player.position, next_tile.position) == 1:
            return False
    return True


def ensure_valid_move(game_state: GameState, next_tile: Tile) -> None:
    """
    Try to execute a move to a tile, if it is safe to do so
    """
    if not __check_move_is_safe(game_state, next_tile):
        raise MoveResultsInConflictException
