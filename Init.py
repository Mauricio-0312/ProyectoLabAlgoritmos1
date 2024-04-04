import tkinter as tk
from tkinter import messagebox
from Box import *
from Board import *
from User import *
from MainData import *

def centerWindow(window):
    window.update_idletasks()
    windowWidth = window.winfo_width()
    windowHeight = window.winfo_height()
    x_location = (window.winfo_screenwidth() // 2) - (windowWidth // 2)
    y_location = (window.winfo_screenheight() // 2) - (windowHeight // 2)
    window.geometry('{}x{}+{}+{}'.format(windowWidth, windowHeight, x_location, y_location))

class TicTacToe:
    def __init__(self):
        
        self.size = 0
        # self.showMainMenu()

    def showMainMenu(self):
        self.root = tk.Tk()
        self.root.title("N en raya 3D")
        tk.Label(self.root, text="¿Desea jugar a N en raya 3D?").pack(pady=10)
        yesButton = tk.Button(self.root, text="Sí", command=self.showPreGameMenu)
        yesButton.pack(pady=5)
        noButton = tk.Button(self.root, text="No", command=self.root.destroy)
        noButton.pack(pady=5)
        centerWindow(self.root)
        self.root.mainloop()
        # self.root.geometry('+350+200')  # Ajustar la posición de la ventana principal

    def showPreGameMenu(self):
        self.root.destroy()
        self.preGameRoot = tk.Tk()
        self.preGameRoot.title("Configuración del Juego")
        tk.Label(self.preGameRoot, text="Ingrese los nombres de los jugadores:").pack(pady=10)
        self.player1Name = tk.Entry(self.preGameRoot)
        self.player1Name.pack(pady=5)
        self.player2Name = tk.Entry(self.preGameRoot)
        self.player2Name.pack(pady=5)
        tk.Label(self.preGameRoot, text="Ingrese la dimensión N del tablero:").pack(pady=5)
        self.sizeInput = tk.Entry(self.preGameRoot)
        self.sizeInput.pack(pady=5)
        tk.Button(self.preGameRoot, text="Iniciar juego", command=self.initializeGame).pack(pady=5)
        tk.Button(self.preGameRoot, text="Regresar", command=self.goBackFromPreGame).pack(pady=5)
        
        centerWindow(self.preGameRoot)  # Centrar la ventana pre-juego
        self.preGameRoot.mainloop()

    def goBackFromPreGame(self):
        self.preGameRoot.destroy()
        self.showMainMenu()

    def initializeGame(self):
        self.player1 = self.player1Name.get()
        self.player2 = self.player2Name.get()
        size = self.sizeInput.get()
        if not self.player1 or not self.player2 or not size:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        if self.player1 == self.player2:
            messagebox.showerror("Error", "Los nombres de los jugadores no pueden ser iguales.")
            return
        try:
            size = int(size)
            if size <= 2:
                messagebox.showerror("Error", "La dimensión del tablero debe ser mayor que 2.")
                return
            self.size = size
        except ValueError:
            messagebox.showerror("Error", "La dimensión del tablero debe ser un número entero.")
            return
        
        user1 = User(self.player1, 0, "x")
        user2 = User(self.player2, 0, "o")
        self.board: Board = Board()
        self.mainData: MainData = MainData([user1, user2], self.board, 0, self.size)
        self.preGameRoot.destroy()
        self.showGame(size, self.mainData)

    def showGame(self, size, mainData):
        # self.gameRoot = tk.Toplevel(self.root)
        # self.gameRoot.title("N en raya 3D - Juego")
        # Código para mostrar el juego...
        # centerWindow(self.gameRoot)  # Centrar la ventana del juego
        try:
            if size > 0:
                self.gameRoot = tk.Tk()
                
                frame = tk.Frame(self.gameRoot)
                interfaceElements = []
                currentTurn = tk.Label(frame, text=f"Turno actual: {mainData.users[mainData.currentTurn].symbol}")
                currentTurn.pack(pady=5)
                interfaceElements.append(currentTurn)
                
                tk.Label(frame, text=f"Jugador 1: {mainData.users[0].name}").pack(pady=5)
                tk.Label(frame, text=f"Puntos: {mainData.users[0].points}").pack()
                tk.Label(frame, text=f"Ficha: {mainData.users[0].symbol}").pack()

                tk.Label(frame, text=f"Jugador 2: {mainData.users[1].name}").pack(pady=5)
                tk.Label(frame, text=f"Puntos: {mainData.users[1].points}").pack()
                tk.Label(frame, text=f"Ficha: {mainData.users[1].symbol}").pack()

                tk.Button(frame, text="Finalizar juego", command=self.gameRoot.destroy).pack(pady=5)

                frame.grid(row=0, column=0, padx=10)

                side = 30
                marginTop = 20
                width = side*size
                height = side*size*size + marginTop*(size+1)

                canvasFrame = tk.Frame(self.gameRoot)

                canvas = tk.Canvas(
                canvasFrame, 
                scrollregion=(0,0, width, height)
                )

                canvas.pack()

                canvasFrame.grid(row=0, column=1, columnspan=4)
                self.gameRoot.title("N en raya 3D")


                # create a scrollbar widget and set its command to the text widget
                scrollbar = tk.Scrollbar(self.gameRoot, orient='vertical', command=canvas.yview)
                scrollbar.grid(row=0, column=5, sticky=tk.NS)

                # #  communicate back to the scrollbar
                canvas['yscrollcommand'] = scrollbar.set

                for m in range(size):
                    newBoard = []

                    for i in range(size):
                        row = []
                        for j in range(size):
                            newBox = Box(canvas, mainData, j*side, i*side, side, m, i, j, size, self.callBack, interfaceElements)
                            row.append(newBox)
                        newBoard.append(row)
                    self.board.addBoard(newBoard)
                
                centerWindow(self.gameRoot)
                self.gameRoot.mainloop()
                return 
                
            else:
                messagebox.showerror("Error", "El tamaño del tablero debe ser mayor que 0.")
        except ValueError:
            messagebox.showerror("Error", "Introduzca un número válido para el tamaño del tablero.")
    
    def callBack(self, mainData):
        self.gameRoot.destroy()
        self.showGame(self.size, mainData)
        

if __name__ == "__main__":
    ticTacToe: TicTacToe = TicTacToe()
    ticTacToe.showMainMenu()
    # root = tk.Tk()
    # # root.geometry("300x400")
    # # root.config(width=300, height=100)
    # # root.resizable(False, False)
    # root.title("Scrollbar Widget Example")

    # frame = tk.Frame(root)
    # interfaceElements = []
    # currentTurn = tk.Label(frame, text=f"Turno actual:")
    # currentTurn.pack(pady=5)
    
    # tk.Label(frame, text=f"Jugador 1:").pack(pady=5)
    # tk.Label(frame, text=f"Puntos:").pack()
    # tk.Label(frame, text=f"Ficha:").pack()

    # tk.Label(frame, text=f"Jugador 2:").pack(pady=5)
    # tk.Label(frame, text=f"Puntos:").pack()
    # tk.Label(frame, text=f"Ficha:").pack()

    # tk.Button(frame, text="Finalizar juego", command=root.destroy).pack(pady=5)

    # frame.grid(row=0, column=0, padx=10)
    
    # canvasFrame = tk.Frame(root)

    # canvas = tk.Canvas(
    # canvasFrame, 
    # scrollregion=(0,0, 200, 600)
    # )

    # canvas.pack()

    # canvasFrame.grid(row=0, column=1, columnspan=4)
    # root.title("N en raya 3D")

    

    # # create a scrollbar widget and set its command to the text widget
    # scrollbar = tk.Scrollbar(root, orient='vertical', command=canvas.yview)
    # scrollbar.grid(row=0, column=5, sticky=tk.NS)

    # # #  communicate back to the scrollbar
    # canvas['yscrollcommand'] = scrollbar.set

    # root.mainloop()




'''
    def verificar_linea_fila(self, tablero, casilla):
        pass

    def verificar_linea_columna(self, tablero, casilla):
        pass

    def verificar_linea_diagonal(self, tablero, casilla):
        pass

    def verificar_linea_diagonal_inversa(self, tablero, casilla):
        pass

    def verificar_linea_intertablero(self, tablero, casilla):
        pass

    def verificar_linea_fila_intertablero(self, tablero, casilla):
        pass

    def verificar_linea_columna_intertablero(self, tablero, casilla):
        pass

    def verificar_linea_diagonal_intertablero(self, tablero, casilla):
        pass

    def verificar_linea_diagonal_inversa_intertablero(self, tablero, casilla):
        pass

    def aumentar_puntaje(self, jugador, juego):
        pass

    def reiniciar_tablero(self, juego):
        pass

    def intercambiar_turnos(self, juego):
        pass'''