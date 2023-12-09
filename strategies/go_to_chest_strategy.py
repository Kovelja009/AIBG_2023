from strategy import Strategy

class GoToChestStrategy(Strategy):
    def __init__(self, world, chest):
        super().__init__(world)
        self.chest = chest

    def execute(self):
        self.world.move_to(self.chest)