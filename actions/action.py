from typing import Tuple
from abc import ABC


class Action(ABC):
    position: Tuple[int, int]

    def __init__(self, postion: Tuple[int, int]):
        self.position = postion

    def json(self):
        pass
