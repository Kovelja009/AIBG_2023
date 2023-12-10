from typing import Tuple
from game_state import TileType, EntityType, GameState, Tile

def get_all_tiles_of_type(game_state: GameState, entity_type: EntityType):
    return [tile for tile in game_state.tiles.values() if tile.entity.type == entity_type]

def __node_dist(node1: Tuple[int,int], node2: Tuple[int,int]) -> int:
    '''
    Returns the distance between two nodes on hexagonal grid by runing a bfs from node1 to node2
    '''
    return 0

def __check_move_is_safe(game_state: GameState, next_tile: Tile) -> bool:
    '''
    Check if moving to this tile results in being next to an enemy player
    '''
    enemy_players = [player for player in game_state.players if player.idx != game_state.our_idx]
    for player in enemy_players:
        q1,r1 = player.tile.q, player.tile.r
        q2,r2 = next_tile.q, next_tile.r
        if __node_dist((q1,r1), (q2,r2)) == 1:
            return False
    return True

def try_execute_move(game_state: GameState, next_tile: Tile):
    '''
    Try to execute a move to a tile, if it is safe to do so
    '''
    if __check_move_is_safe(game_state, next_tile):
        pass