from game_state import GameState, EntityType, TileType, Tile
from heapq import heappop, heappush
from typing import Tuple, List

from game_utils import get_neighbouring_tiles, get_all_tiles_of_type
from actions.move_action import MoveAction
from exceptions import MoveResultsInConflictException
from actions.action import Action
import time


def enemy_is_neighbor_of_tile(game_state: GameState, tile: Tile):
    neighbors = get_neighbouring_tiles(game_state, tile)
    for neighbour in neighbors:
        if neighbour.entity.type == EntityType.ENEMY_PLAYER:
            return True
    return False


def check_move_is_safe(game_state: GameState, action: Action) -> bool:
    """
    Check if moving to this tile results in being next to an enemy player
    """
    if isinstance(action, MoveAction):
        next_tile = game_state.tiles[action.position]
        if enemy_is_neighbor_of_tile(game_state, next_tile):
            return False
        return True
    else:
        current_tile = game_state.tiles[game_state.our_player.position]
        if enemy_is_neighbor_of_tile(game_state, current_tile):
            return False
        return True


class Graph:
    def __init__(self, game_state: GameState, sword) -> None:
        self.graph = {}
        self.game_state = game_state
        for tile in game_state.tiles.values():
            weight = 1

            if tile.entity.type == EntityType.TREES:
                if sword == True:
                    weight = 2
                else:
                    weight = 3

            neighbours = get_neighbouring_tiles(game_state, tile)
            for neighbour in neighbours:
                q1,r1 = tile.position
                q2,r2 = neighbour.position
                self.add(q1,r1,q2,r2, weight)

    def add(self, x, y, q, r, weight) -> None:
        if (x, y) in self.graph:
            self.graph[(x, y)].append(((q, r), weight))
        else:
            self.graph[(x, y)] = [((q, r), weight)]

    def bfs(self, q, r, x, y) -> Tuple[Tuple[int, int], int]:
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

    def stone_attacked_tiles(self, game_state: GameState, stones: List[Tile], stone_state):
        attacked_tiles = []
        for stone in stones:
            q, r = stone.position
            if stone_state == 0:
                attacked_tiles.append((q + 1, r - 1))
                attacked_tiles.append((q + 2, r - 2))
            elif stone_state == 1:
                attacked_tiles.append((q + 1, r))
                attacked_tiles.append((q + 2, r))
            elif stone_state == 2:
                attacked_tiles.append((q, r + 1))
                attacked_tiles.append((q, r + 2))
            elif stone_state == 3:
                attacked_tiles.append((q - 1, r + 1))
                attacked_tiles.append((q - 2, r + 2))
            elif stone_state == 4:
                attacked_tiles.append((q - 1, r))
                attacked_tiles.append((q - 2, r))
            elif stone_state == 5:
                attacked_tiles.append((q, r - 1))
                attacked_tiles.append((q, r - 2))
            elif stone_state == 6:
                attacked_tiles.append((q + 2, r - 2))
                attacked_tiles.append((q + 2, r - 1))
                attacked_tiles.append((q + 1, r + 1))
                attacked_tiles.append((q, r + 2))
                attacked_tiles.append((q - 2, r + 2))
                attacked_tiles.append((q - 2, r + 1))
                attacked_tiles.append((q - 1, r - 1))
                attacked_tiles.append((q, r - 2))
            else:
                raise Exception("Invalid stone state")
        return attacked_tiles

    def dijkstra(self, src, dest):
        stones = get_all_tiles_of_type(self.game_state, EntityType.STONE)
        dist: dict[tuple[int, int], int] = {}
        prev: dict[tuple[int, int], tuple[int, int]] = {}
        for vertex in self.graph:
            dist[vertex] = float('inf')
        dist[src] = 0

        heap = []
        popped_nodes = set()
        heappush(heap, (dist[src], src))
        while heap:
            d, u = heappop(heap)
            if u == dest:
                break
            if u in popped_nodes:
                continue
            popped_nodes.add(u)
            for v, w in self.graph[u]:
                if v in self.stone_attacked_tiles(self.game_state, stones, (self.game_state.stone_state + d) % 7):
                    continue
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heappush(heap, (dist[v], v))

        path: list[tuple[int, int]] = []
        u = dest
        while u in prev:
            path.append(u)
            u = prev[u]
        path.reverse()
        if check_move_is_safe(self.game_state, MoveAction(path[0])):
            return self.game_state.tiles[path[0]], dist[dest]
        else:
            raise MoveResultsInConflictException
