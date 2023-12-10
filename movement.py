from exceptions import MoveResultsInConflictException
from game_state import Tile, GameState
from typing import Tuple
from game_state import EntityType, TileType
from actions.action import Action
from actions.attack_action import AttackAction
from actions.move_action import MoveAction
from heapq import heappop, heappush
from game_utils import stone_attacked_tiles

class Graph:
    def __init__(self, game_state: GameState, sword) -> None:
        self.graph = {}
        self.game_state = game_state
        for tile in game_state.tiles.values():
            weight = 1

            if tile.entity_type == EntityType.TREES:
                if sword == True:
                    weight = 2
                else:
                    weight = 3

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
        else:
            self.graph[(x, y)] = [((q, r), weight)]

    def bfs(self, q, r, x, y) -> Tuple[Tuple[int,int], int]:
        queue = []
        path = {}
        dist = {}

        for tem in range(len(queue)):
            for element in self.graph[(queue[tem])]:
                if element in dist:
                    path[element] = queue[tem]
                    dist[element] = dist.get(queue[tem]) + 1
                    queue.append(element)

        d = dist[(x, y)]

        while path[(x, y)] != (q, r):
            (x, y) = path[(x, y)]

        return (x, y), d
    
    def dijkstra(self, src, dest):
        dist: dict[tuple[int, int], int] = {} 
        prev: dict[tuple[int, int], tuple[int, int]] = {}
        for vertex in self.graph:
            dist[vertex] = float('inf')
        dist[src] = 0

        heap = []
        heappush(heap, (dist[src], src))
        while heap:
            d, u = heappop(heap)
            if d != dist[u]:
                continue
            for v, w in self.graph[u]:
                if v in stone_attacked_tiles(self.game_state, (self.game_state.stone_state + d) % 7):
                    alt = dist[u] + w
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
                    heappush(heap, (dist[v], v))
        
        path : list[tuple[int, int]]= []
        u = dest
        while u in prev:
            path.append(u)
            u = prev[u]
        path.reverse()
        if __check_move_is_safe(self.game_state, MoveAction(path[0])):
            return self.game_state.tiles[path[0]], dist[dest]
        else:
            raise MoveResultsInConflictException
        


def distance(game_state : GameState, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> int:
    graph = Graph(game_state.tiles, game_state.our_player.sword)
    next_tile, dist = graph.bfs(start_pos[0], start_pos[1], end_pos[0], end_pos[1])
    return dist


def get_next_move(game_state: GameState, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> Tuple[Tile, int]:
    graph = Graph(game_state.tiles, game_state.our_player.sword)
    return graph.dijkstra(start_pos, end_pos)


def __check_move_is_safe(game_state: GameState, action: Action) -> bool:
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
