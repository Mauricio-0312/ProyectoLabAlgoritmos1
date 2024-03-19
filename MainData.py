from typing import List
from User import *
from Board import Board

class MainData:
    def __init__(self, users: List[User], board: Board, currentTurn: int, size: int) -> None:
        self.users = users
        self.board = board
        # Refers to user index
        self.currentTurn = currentTurn
        self.size = size
