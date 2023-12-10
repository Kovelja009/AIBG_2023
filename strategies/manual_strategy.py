from strategies.strategy import Strategy
from strategy_manager import StrategyManager
from game_state import Tile
import logging
from game_state import GameState
from typing import Union
from actions.action import Action
from game_utils import get_neighbouring_tiles
from game_state import EntityType, TileType, Player
from actions.move_action import MoveAction
from actions.attack_action import AttackAction
import random
from movement import distance


class ManualStrategy(Strategy):

    def __init__(self, manager: StrategyManager):
        super().__init__(manager)
        self.print_commands()

    def print_commands(self):
        print("Enter 1 2 3 4 5 6 to move")

    def print_player_stats(self, player: Player):
        print(f"----------------------------------")
        print(f"Health: {player.health}")
        print(f"Attack power: {player.attackPower}")
        print(f"Score: {player.score}")
        print(f"Skull: {player.skull}")
        print(f"Sword: {player.sword}")
        print(f"----------------------------------")

    def print_state(self, game_state: GameState):
        # Print our stats
        print('########## Our stats ##########')
        self.print_player_stats(game_state.our_player)
        for player in game_state.players:
            if player.playerIdx != game_state.our_player.playerIdx:
                print(f'########## Player {player.playerIdx} stats ##########')
                self.print_player_stats(player)
                dist = distance(game_state, game_state.our_player.position, player.position)
                print(f"Distance: {dist}")

    def execute_move(self, game_state: GameState) -> Union[Action, None]:
        player_tile = game_state.tiles[game_state.our_player.position]
        self.print_state(game_state)

        neighbours = get_neighbouring_tiles(game_state, player_tile)
        possible_actions = []
        possible_neighbours = []
        attackable_types = [EntityType.ENEMY_PLAYER, EntityType.TREES]
        stepable_types = [EntityType.NONE, EntityType.LEAVES, EntityType.CHEST, EntityType.SKULL]
        for neighbour in neighbours:
            if neighbour.entity.type in attackable_types:
                possible_actions.append(AttackAction(neighbour.position))
                possible_neighbours.append(neighbour)
            elif neighbour.entity.type in stepable_types:
                possible_actions.append(MoveAction(neighbour.position))
                possible_neighbours.append(neighbour)

        offsets = [(0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0)]
        print('########## Possible moves ##########')
        # Output which commands are valid
        for i, offset in enumerate(offsets):
            new_pos = (player_tile.position[0] + offset[0], player_tile.position[1] + offset[1])
            if new_pos in game_state.tiles:
                print(new_pos, end=' ')
            else:
                print("X")
            if i == 2:
                print()

        user_input = input("Enter command: ")
        move_idx = int(user_input) - 1
        chosen_offset = offsets[move_idx]
        chosen_pos = (player_tile.position[0] + chosen_offset[0], player_tile.position[1] + chosen_offset[1])
        if not possible_neighbours:
            print('Invalid action, playing random action')
            return random.choice(possible_actions)
        else:
            for i, neighbour in enumerate(possible_neighbours):
                if neighbour.position == chosen_pos:
                    return possible_actions[i]
            return None
