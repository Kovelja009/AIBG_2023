from game_state import GameState


class StrategyManager:

    def __init__(self, startStrategy) -> None:
        self.current_strategy = startStrategy

    def transition(self, game_state: GameState, new_strategy):
        self.current_strategy = new_strategy
        self.current_strategy.execute_move(game_state)

    def execute_current_strategy(self, game_state: GameState):
        ret = self.current_strategy.execute_move(game_state)
        while ret is None:
            ret = self.current_strategy.execute_move(game_state)
        return ret
