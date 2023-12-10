from typing import Tuple
from abc import ABC, abstractmethod


class Action(ABC):
    position: Tuple[int, int]

    def __init__(self, postion: Tuple[int, int]):
        self.position = postion

    @abstractmethod
    def json(self):
        pass
