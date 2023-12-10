from strategy import Strategy
from strategy_manager import StrategyManager
from game_state import Tile
from movement import get_next_move
import logging
from typing import Union


class GoToChestOverLeafStrategy(Strategy):
    leafTile: Tile
    chestTile: Tile
    leafReached: bool

    def __init__(self, manager: StrategyManager, leafTile: Tile, chestTile: Tile) -> None:
        super().__init__(manager)
        self.leafTile = leafTile
        self.chestTile = chestTile
        self.leafReached = False

    def execute_move(self, game_state) -> Union[Tile, None]:
        logging.info("Executing GoToChestOverLeafStrategy")
        # Find chest position that corresponds to our player
        our_player = game_state.our_player
        player_pos = our_player.position
        if player_pos == self.leafTile.position:
            self.leafReached = True
        # Get path from player to leaf if leaf not reached
        if not self.leafReached:
            logging.info("Leaf not reached yet, going to leaf")
            try:
                next_tile = get_next_move(game_state, player_pos, self.leafTile.position)
                return next_tile
            except:
                logging.info("Canceled going to leaf, going to chest")
                self.leafReached = True  # Cancel going to leaf
        else:
            logging.info("Leaf reached or aborted, going to chest")
            try:
                next_tile = get_next_move(game_state, player_pos, self.chestTile.position)
                return next_tile
            except:
                logging.error("Conflict while going to chest")
                return None  # TODO: Override strategy and force move
