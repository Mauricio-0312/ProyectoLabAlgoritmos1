import tkinter as tk
from tkinter import messagebox
# from MainData import *
from Helpers import *
from User import *
from typing import List

class Box:
    def __init__(self, canvas: tk.Canvas, mainData, x:int, y:int, l:int, subBoardId: int, row: int, column: int, boardSize: int,
                  callBack, changingInterfaceElements: List[tk.Label]) -> None:
        self.canvas = canvas
        self.mainData = mainData
        self.subBoardId = subBoardId
        self.symbol = ""
        self.row = row
        self.column = column
        self.boardSize = boardSize
        self.callback = callBack
        self.changingInterfaceElements = changingInterfaceElements
        self.id = self.createEmptyBox(x, y, l)
    
    def createEmptyBox(self, x:int, y:int, l:int):
        boardSize = self.boardSize*l
        startYCoord = self.subBoardId*boardSize
        boardMarginTop = (self.subBoardId + 1)*20
        
        rectangle = self.canvas.create_rectangle(x, boardMarginTop + startYCoord + y,x+l, boardMarginTop + startYCoord + y+l, outline="black", fill="white")

        self.canvas.tag_bind(rectangle, "<Button-1>", lambda event: self.fillBox(x, boardMarginTop + startYCoord + y, l, self.mainData))
        return rectangle

    def fillBox(self, x, y, l, mainData):
        # print("hello")
        if self.symbol == "":
            # print("hey")
            # print(mainData.users, mainData.currentTurn, x, y, l)
            if mainData.users[mainData.currentTurn].symbol == "o":
                staticCircle(self.canvas, x+l/2, y+l/2, l/3, "red")
                self.symbol = "o"

            if mainData.users[mainData.currentTurn].symbol == "x":

                cross(self.canvas, x+l/2, y+l/2, l/3, "blue")
                self.symbol = "x"
            
            self.verifyLine()

    def verifyLine(self):
        subBoardId = self.subBoardId
        row = self.row
        column = self.column
        symbol = self.mainData.board.boards[subBoardId][row][column].symbol
        winColor = "red" if symbol == "o" else "blue"
        userName = self.mainData.users[self.mainData.currentTurn].name
        win = False
        # Verify row
        if all(box.symbol == symbol for box in self.mainData.board.boards[subBoardId][row]):
            for j in range(self.mainData.size):
                self.canvas.itemconfig(self.mainData.board.boards[subBoardId][row][j].id, fill=winColor)

            win = True
        
        # Verify column
        elif all(self.mainData.board.boards[subBoardId][i][column].symbol == symbol for i in range(self.mainData.size)):
            for i in range(self.mainData.size):
                self.canvas.itemconfig(self.mainData.board.boards[subBoardId][i][column].id, fill=winColor)

            win = True
        
        # Verify diagonal
        elif row == column and all(self.mainData.board.boards[subBoardId][i][i].symbol == symbol for i in range(self.mainData.size)):
            for i in range(self.mainData.size):
                self.canvas.itemconfig(self.mainData.board.boards[subBoardId][i][i].id, fill=winColor)

            win = True
        
        # Comprobar inversa
        elif row + column == self.mainData.size - 1 and all(self.mainData.board.boards[subBoardId][i][self.mainData.size - 1 - i].symbol == symbol for i in range(self.mainData.size)):
            for i in range(self.mainData.size):
                self.canvas.itemconfig(self.mainData.board.boards[subBoardId][i][self.mainData.size - 1 - i].id, fill=winColor) 
            
            win = True

        elif all(all(all(element.symbol != "" for element in row) for row in subBoard) for subBoard in self.mainData.board.boards):
            messagebox.showinfo("Fin de la partida actual", f"¡Hubo un empate!. Cierre esta pestaña para empezar la siguiente partida")
            
            # Switch symbols
            temp = self.mainData.users[0].symbol
            self.mainData.users[0].symbol = self.mainData.users[1].symbol
            self.mainData.users[1].symbol = temp

            # Set current turn to the first user 
            self.mainData.currentTurn = 0

            # Get rid off old boards
            self.mainData.board.boards = []

            self.callback(self.mainData)

            return None
        
        if win:
            messagebox.showinfo("Fin de la partida actual", f"¡El jugador {userName} suma un punto!. Cierre esta pestaña para empezar la siguiente partida")
            # Increase points of winning user
            self.mainData.users[self.mainData.currentTurn].points += 1
           
            # Switch symbols
            temp = self.mainData.users[0].symbol
            self.mainData.users[0].symbol = self.mainData.users[1].symbol
            self.mainData.users[1].symbol = temp

            # Set current turn to the first user 
            self.mainData.currentTurn = 0
            
            # Get rid off old boards
            self.mainData.board.boards = []
            
            self.callback(self.mainData)

            return None
        
        # Update current turn
        self.mainData.currentTurn = self.mainData.currentTurn + 1 if self.mainData.currentTurn + 1 < len(self.mainData.users) else 0

        # Update "current turn" Label
        self.changingInterfaceElements[0].config(text=f"Turno actual: {self.mainData.users[self.mainData.currentTurn].symbol}")

