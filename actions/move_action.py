from action import Action
from typing import Tuple


class MoveAction(Action):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)
