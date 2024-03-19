from Box import Box
from typing import List

class Board:
    def __init__(self) -> None:
        self.boards: List[List[Box]] = []
    
    def addBoard(self, newBoard: List[List[Box]]):
        self.boards.append(newBoard)