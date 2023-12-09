from strategy import Strategy
from strategy_manager import StrategyManager

class GoToChestStrategy(Strategy):
    def __init__(self, manager: StrategyManager):
        super().__init__(manager)
    
    def execute(self, game_state):
        # Find chest position that corresponds to our player
        chest = None
        for tile in game_state.tiles.values():
            if tile.entity.type == 6:
                chest = tile
                break