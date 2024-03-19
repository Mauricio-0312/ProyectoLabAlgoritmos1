import tkinter as tk
from tkinter import messagebox
# from MainData import *
from Helpers import *
from User import *
from typing import List

class Box:
    def __init__(self, canvas: tk.Canvas, mainData, x:int, y:int, l:int, subBoardId: int, row: int, column: int, callBack) -> None:
        self.canvas = canvas
        self.mainData = mainData
        self.id = self.createEmptyBox(x, y, l)
        self.symbol = ""
        self.subBoardId = subBoardId
        self.row = row
        self.column = column
        self.callback = callBack
    
    def createEmptyBox(self, x:int, y:int, l:int):
        rectangle = self.canvas.create_rectangle(x,y,x+l,y+l, outline="black", fill="white")

        self.canvas.tag_bind(rectangle, "<Button-1>", lambda event: self.fillBox(x, y, l, self.mainData))
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
            mainData.currentTurn = mainData.currentTurn + 1 if mainData.currentTurn + 1 < len(mainData.users) else 0

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
        
        if win:
            message = messagebox.showinfo("Fin de la partida actual", f"¡El jugador {userName} suma un punto!. Cierre esta pestaña para empezar la siguiente partida")
            self.mainData.users[self.mainData.currentTurn].points += 1
            self.mainData.board.boards = []
            self.callback(self.mainData)

