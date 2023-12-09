from strategy import Strategy

class StrategyManager:
    current_state : Strategy
    def __init__(self) -> None:
        self.current_state = None