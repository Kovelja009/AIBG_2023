from actions.action import Action
from typing import Tuple
import json


class MoveAction(Action):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)

    def json(self):
        q, r = self.position
        return {
            'action' : f'move,{q},{r}'
        }