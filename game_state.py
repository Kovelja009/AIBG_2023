from enum import Enum
from typing import List, Dict

class TileType(Enum):
    EMPTY = 0
    FULL = 1

class EntityType(Enum):
    NONE = 0
    TREES = 1
    CHEST = 2
    STONE = 3
    CLIFF = 4
    ENEMY_PLAYER = 5
    SKULL = 6

class Entity:
    def __init__(self, entity_type, q, r, **kwargs):
        self.type = entity_type
        self.q = q
        self.r = r
        if kwargs:
            self.__dict__.update(kwargs)

class Tile:
    def __init__(self, q, r, tile_type, entity):
        self.q = q
        self.r = r
        self.tileType = tile_type
        self.entity = Entity(**entity)


class Player:
    def __init__(self, type, q, r, playerIdx, name, score, health, attackPower, skull, skullWin, scoreLevel, sword) -> None:
        self.type = type
        self.q = q
        self.r = r
        self.playerIdx = playerIdx
        self.name = name
        self.score = score
        self.health = health
        self.attackPower = attackPower
        self.skull = skull
        self.skullWin = skullWin
        self.scoreLevel = scoreLevel
        self.sword = sword

class GameState:
    turn: int
    size: int
    tiles: Dict[(int,int), Tile]
    players: List[Player]
    skull_win: bool
    our_idx: int
    def __init__(self, turn, map_size, skull_win: bool, tiles: List[Tile] , players: List[Player]):
        self.turn = turn
        self.size = map_size
        self.skull_win = skull_win
        self.tiles = tiles
        self.our_idx = 0
        # go through players and check if q and r is the same as tiles q and r and set tiles entity to player
        for player in players:
            for tile in tiles:
                if player.q == tile.q and player.r == tile.r:
                    tile.entity = player
                    break

        self.tiles = {(tile.q, tile.r): tile for tile in tiles}


# # Creating GameState object from JSON data
# game_state = GameState(
#     json_data['gameState']['turn'],
#     json_data['gameState']['map']['size'],
#     json_data['gameState']['skullWin'],
#     [Tile(**tile) for tile in json_data['gameState']['map']['tiles']],
#     [Player(**player) for player in json_data['gameState']['scoreBoard']['players']
# )
