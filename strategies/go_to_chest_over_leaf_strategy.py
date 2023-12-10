from strategies.strategy import Strategy
from strategy_manager import StrategyManager
from game_state import Tile
from movement import get_next_move
import logging
from typing import Union
from actions.action import Action
from actions.move_action import MoveAction
from strategies.circle_stone_strategy import CircleStoneStrategy

class GoToChestOverLeafStrategy(Strategy):
    leafTile: Tile
    chestTile: Tile
    leafReached: bool

    def __init__(self, manager: StrategyManager, leafTile: Tile, chestTile: Tile) -> None:
        super().__init__(manager)
        self.leafTile = leafTile
        self.chestTile = chestTile
        self.leafReached = False

    def execute_move(self, game_state) -> Union[Action, None]:
        print("INFO: Executing GoToChestOverLeafStrategy")
        # Player has sword transition to go to stone
        if game_state.our_player.sword:
            print("INFO: Player has sword transitioning to CircleStoneStrategy")
            self.strategy_manager.transition(game_state, CircleStoneStrategy(self.strategy_manager))
            return None
        # Find chest position that corresponds to our player
        our_player = game_state.our_player
        player_pos = our_player.position
        if player_pos == self.leafTile.position:
            self.leafReached = True
        # Get path from player to leaf if leaf not reached
        if not self.leafReached:
            print("INFO: Leaf not reached yet, going to leaf")
            try:
                next_tile, _ = get_next_move(game_state, player_pos, self.leafTile.position)
                return MoveAction(next_tile.position)
            except:
                print("INFO: Canceled going to leaf, going to chest")
                self.leafReached = True  # Cancel going to leaf
        else:
            print("INFO: Leaf reached or aborted, going to chest")
            try:
                next_tile, _ = get_next_move(game_state, player_pos, self.chestTile.position)
                return MoveAction(next_tile.position)
            except:
                print("ERROR: Conflict while going to chest")
                return None  # TODO: Override strategy and force move
