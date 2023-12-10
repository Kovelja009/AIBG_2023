from typing import Tuple
from action import Action


class AttackAction(Action):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)
