from typing import Tuple
from game_state import EntityType, GameState, Tile
from typing import List

def get_all_tiles_of_type(game_state: GameState, entity_type: EntityType):
    return [tile for tile in game_state.tiles.values() if tile.entity.type == entity_type]


def get_closest_tile_of_type(game_state: GameState, entity_type: EntityType, source_pos: Tuple[int, int]) -> Tuple[
    Tile, int]:
    '''
    Returns the closest tile of a given type to the source tile
    '''
    from movement import distance
    tiles = get_all_tiles_of_type(game_state, entity_type)
    closest_tile = None
    closest_dist = float('inf')
    for tile in tiles:
        dist = distance(tile.position, source_pos)
        if dist < closest_dist:
            closest_tile = tile
            closest_dist = dist

    return closest_tile, closest_dist


def get_neighbouring_tiles(game_state: GameState, tile: Tile) -> List[Tile]:
    '''
    Returns a list of neighbouring tiles to the given tile
    '''
    neighbours = []
    offsets = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
    for offset in offsets:
        new_pos = (tile.position[0] + offset[0], tile.position[1] + offset[1])
        if new_pos in game_state.tiles:
            neighbours.append(game_state.tiles[new_pos])
    return neighbours
