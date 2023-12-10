from typing import Tuple
from game_state import TileType, EntityType, GameState, Tile
from exceptions import MoveResultsInConflictException
from movement import move_to, distance


def get_all_tiles_of_type(game_state: GameState, entity_type: EntityType):
    return [tile for tile in game_state.tiles.values() if tile.entity.type == entity_type]


def get_next_move(game_state: GameState, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> Tuple[Tile, int]:
    raise NotImplementedError


def get_closest_tile_of_type(game_state: GameState, entity_type: EntityType, source_tile: Tile) -> Tile:
    '''
    Returns the closest tile of a given type to the source tile
    '''
    tiles = get_all_tiles_of_type(game_state, entity_type)
    closest_tile = None
    closest_dist = float('inf')
    for tile in tiles:
        dist = distance(tile.position, source_tile.position)
        if dist < closest_dist:
            closest_tile = tile
            closest_dist = dist

    return closest_tile


def __check_move_is_safe(game_state: GameState, next_tile: Tile) -> bool:
    """
    Check if moving to this tile results in being next to an enemy player
    """
    enemy_players = [player for player in game_state.players if player.idx != game_state.our_idx]
    for player in enemy_players:
        if distance(player.position, next_tile.position) == 1:
            return False
    return True


def ensure_valid_move(game_state: GameState, next_tile: Tile) -> None:
    """
    Try to execute a move to a tile, if it is safe to do so
    """
    if not __check_move_is_safe(game_state, next_tile):
        raise MoveResultsInConflictException
