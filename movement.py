from exceptions import MoveResultsInConflictException
from game_state import Tile, GameState
from typing import Tuple

def move_to(source: tuple, dest: tuple) -> tuple:
    raise NotImplementedError

def distance(source: tuple, dest: tuple) -> int:
    raise NotImplementedError

def get_next_move(game_state: GameState, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> Tuple[Tile, int]:
    raise NotImplementedError

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
