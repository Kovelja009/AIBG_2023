from strategies.strategy import Strategy
from game_state import GameState


class StrategyManager:
    current_strategy: Strategy

    def __init__(self) -> None:
        self.current_strategy = None

    def transition(self, new_strategy: Strategy):
        self.current_strategy = new_strategy
        self.current_strategy.execute_move()

    def execute_current_strategy(self, game_state: GameState):
        ret = self.current_strategy.execute_move(game_state)
        while ret is None:
            ret = self.current_strategy.execute_move(game_state)
        return ret
