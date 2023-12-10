from exceptions import MoveResultsInConflictException
from game_state import Tile, GameState
from typing import Tuple
from game_state import EntityType, TileType

class Graph:
    def __init__(self, tiles, sword) -> None:
        self.graph = {}
        for tile in tiles:
            weight = 1

            if tiles.entity_type == EntityType.TREES:
                if sword == True:
                    weight = 2
                else: weight = 3

            if tile.q > -14 and tile.tile_type == TileType.EMPTY:
                self.graph.add(tile.q, tile.r, tile.q - 1, tile.r, weight)
            if tile.q > 14 and tile.tile_type == TileType.EMPTY:
                self.graph.add(tile.q, tile.r, tile.q + 1, tile.r, weight)
            if tile.r > -14 and tile.tile_type == TileType.EMPTY:
                self.graph.add(tile.q, tile.r, tile.q, tile.r - 1, weight)
            if tile.r < 14 and tile.tile_type == TileType.EMPTY:
                self.graph.add(tile.q, tile.r, tile.q, tile.r + 1, weight)
            if tile.r > -14 and tile.q < 14 and tile.tile_type == TileType.EMPTY:
                self.graph.add(tile.q, tile.r, tile.q + 1, tile.r - 1, weight)
            if tile.r < 14 and tile.q > -14 and tile.tile_type == TileType.EMPTY:
                self.graph.add(tile.q, tile.r, tile.q - 1, tile.r + 1, weight)


    def add(self, x, y, q, r, weight) -> None:
        if (x, y) in self.graph:
            self.graph[(x, y)].append((q, r), weight)
        else: self.graph[(x, y)] = [((q, r), weight)]

    def bfs(self, q, r, x, y):
        queue = []
        path = {}
        dist = {}
        tem = 0

        for tem in range(len(queue)):
            for element in self.graph[(queue[tem])]:
                if element in dist:
                    path[element] = queue[tem];
                    dist[element] = dist[queue[tem]] + 1
                    queue.append(element)

        d = dist[(x, y)]

        while path[(x, y)] != (q, r):
            (x, y) = path[(x, y)]

        return (x, y), d
    

def get_next_move(game_state: GameState, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> Tuple[Tile, int]:
    graph = Graph(game_state.tiles, game_state.our_player.sword)
    next_tile, dist = graph.bfs(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
    return next_tile, dist

def __check_move_is_safe(game_state: GameState, next_tile: Tile) -> bool:
    """
    Check if moving to this tile results in being next to an enemy player
    """
    graph = Graph(game_state.tiles, game_state.our_player.sword)
    enemy_players = [player for player in game_state.players if player.idx != game_state.our_idx]
    for player in enemy_players:
        _, dist = graph.bfs(player.position, next_tile.position)
        if dist == 1:
            return False
    return True


def ensure_valid_move(game_state: GameState, next_tile: Tile) -> None:
    """
    Try to execute a move to a tile, if it is safe to do so
    """
    if not __check_move_is_safe(game_state, next_tile):
        raise MoveResultsInConflictException
