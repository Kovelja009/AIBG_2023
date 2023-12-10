from strategy import Strategy
from strategy_manager import StrategyManager
from game_state import Tile
from game_utils import get_next_move, ensure_valid_move


class GoToChestOverLeafStrategy(Strategy):
    leafTile: Tile
    chestTile: Tile
    leafReached: bool

    def __init__(self, manager: StrategyManager, leafTile: Tile, chestTile: Tile) -> None:
        super().__init__(manager)
        self.leafTile = leafTile
        self.chestTile = chestTile
        self.leafReached = False

    def execute_move(self, game_state) -> Tile:
        # Find chest position that corresponds to our player
        our_player = game_state.our_player
        player_pos = our_player.position
        if player_pos == self.leafTile.position:
            self.leafReached = True
        # Get path from player to leaf if leaf not reached
        if not self.leafReached:
            try:
                next_tile = get_next_move(game_state, player_pos, self.leafTile.position)
                return next_tile
            except:
                self.leafReached = True  # Cancel going to leaf
        else:
            try:
                next_tile = get_next_move(game_state, player_pos, self.chestTile.position)
                return next_tile
            except:
                return None  # TODO: Override strategy and force move
