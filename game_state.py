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
        self.posiiton = (q, r)
        if kwargs:
            self.__dict__.update(kwargs)


class Tile:
    def __init__(self, q, r, tile_type, entity):
        self.position = (q, r)
        self.tileType = tile_type
        self.entity = Entity(**entity)
        self.is_attacked = False


class Player:
    def __init__(self, type, q, r, playerIdx, name, score, health, attackPower, skull, skullWin, scoreLevel,
                 sword) -> None:
        self.type = type
        self.position = (q, r)
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
    tiles: Dict[(int, int), Tile]
    players: List[Player]
    skull_win: bool
    our_idx: int
    stone_state: int
    our_player: Player

    def __init__(self, turn, map_size, our_idx, skull_win: bool, tiles: List[Tile], players: List[Player],
                 stone_attacks: List[(int, int)]):
        self.turn = turn
        self.size = map_size
        self.skull_win = skull_win
        self.our_idx = our_idx
        self.players = players

        # go through players and check if q and r is the same as tiles q and r and set tiles entity to player
        for player in players:
            for tile in tiles:
                if player.position == tile.position:
                    tile.entity = player
                    break

        # traverse through players and find our player
        for player in players:
            if player.playerIdx == our_idx:
                self.our_player = player
                break

        self.tiles = {tile.position: tile for tile in tiles}

        for stone_attack in stone_attacks:
            self.tiles[stone_attack].is_attacked = True
        self.stone_state = 0

    # if in state 0-5 it has one type of attacks
    # if in state 6 it has another type of attacks
    def change_stone_state(self):
        self.stone_state += 1
        self.stone_state %= 7

# # Creating GameState object from JSON data
# game_state = GameState(
#     json_data['gameState']['turn'],
#     json_data['gameState']['map']['size'],
#     json_data['gameState']['skullWin'],
#     [Tile(**tile) for tile in json_data['gameState']['map']['tiles']],
#     [Player(**player) for player in json_data['gameState']['scoreBoard']['players']
# )
