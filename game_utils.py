from typing import Tuple
from game_state import EntityType, GameState, Tile
from movement import distance


def get_all_tiles_of_type(game_state: GameState, entity_type: EntityType):
    return [tile for tile in game_state.tiles.values() if tile.entity.type == entity_type]


def get_closest_tile_of_type(game_state: GameState, entity_type: EntityType, source_tile: Tile) -> Tuple[Tile, int]:
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

    return closest_tile, closest_dist
