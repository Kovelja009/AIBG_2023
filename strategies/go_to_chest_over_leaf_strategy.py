from strategy import Strategy
from strategy_manager import StrategyManager
from game_state import Tile
from game_utils import run_dijkstra
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
        # Get path from player to leaf if leaf not reached
        if not self.leafReached:
            next_tile, _ = run_dijkstra(game_state, player_pos, self.leafTile.position)
            if next_tile == self.leafTile:
                self.leafReached = True

