from typing import Tuple
from actions.action import Action
import json

class AttackAction(Action):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)

    def json(self):
        q, r = self.position
        return {
            'action' : f'attack,{q},{r}'
        }