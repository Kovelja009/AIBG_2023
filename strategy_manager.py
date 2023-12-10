from strategy import Strategy

class StrategyManager:
    current_strategy : Strategy
    def __init__(self) -> None:
        self.current_strategy = None

    def transition(self, new_strategy: Strategy):
        self.current_strategy = new_strategy
        self.current_strategy.execute_move()