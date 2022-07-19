import tkinter as tk
# ----------------------------------------------------------------------------
from tkinter import *
from tkinter import messagebox
from AI_player import Checkers
from AI_player import MiniMax



class firstUI():   
    def __init__(self, root):
        """the beginning's show"""     
    # Create the firstUI
        self.root = root
        self.root.config()
        self.Gframe = tk.Frame(width=600, height=600)
        self.Gframe.pack_propagate(0)
        self.Gframe.pack()
    # the frame has 5 rows
        self.Gframe.rowconfigure(0, pad=0)
        self.Gframe.rowconfigure(1, pad=0)
        self.Gframe.rowconfigure(2, pad=0)
        self.Gframe.rowconfigure(3, pad=0)
        self.Gframe.rowconfigure(4, pad=0)
        self.Gframe.rowconfigure(5, pad=0)

        label = tk.Label(self.Gframe, text='Welcome to the Checkers', font=('Sans', '15', 'bold'))
        label.grid(row=0, ipadx=120, ipady=10, pady=10)

        button = tk.Button(self.Gframe, text='Simple', command=self.change_easy, font=('Sans', '15', 'bold'))
        button.grid(row=1, ipadx=27, ipady=15, pady=15)

        button = tk.Button(self.Gframe, text='Medium', command=self.change_midium, font=('Sans', '15', 'bold'))
        button.grid(row=2, ipadx=27, ipady=15, pady=15)

        button = tk.Button(self.Gframe, text='Game introduction', command=self.introduction, font=('Sans', '15', 'bold'))
        button.grid(row=3, ipadx=10, ipady=15, pady=15)       
    
    def change_easy(self):    #Simple
        global MAX_Height
        MAX_Height = 1
        self.Gframe.destroy()
        self.Gframe = secondUI(self.root)
    def change_midium(self):    #Midium
        global MAX_Height
        MAX_Height = 2
        self.Gframe.destroy()
        self.Gframe = secondUI(self.root)
    def change_difficult(self):    #Difficult
        global MAX_Height
        MAX_Height = 3
        self.Gframe.destroy()
        self.Gframe = secondUI(self.root)
    def introduction(self):
        self.Gframe.destroy()
        self.Gframe = introductUI(self.root)

class introductUI():
    def __init__(self, root):
        self.root = root
        self.text = "Checkers, also known as draughts, is a skill game played on a two-color chessboard with 8x8=64 squares. The victory is to capture or block all the opponent's pieces. Both sides take turns playing chess. The unclaimed king piece can only move diagonally to the upper left or upper right corner of the unoccupied square. When capturing a pawn, the opponent's pawn must be in the upper left or upper right corner of your own pawn, and there must be no pawn in the corresponding upper left or upper right corner of the opponent's pawn. If a pawn can capture a pawn, then it must capture and cannot move other pawns. Pieces can be captured continuously, that is to say, if a piece has captured the opponent's piece, it can still capture another opponent's piece in its new position, and it must continue to capture until it can no longer capture. If there are two pieces that can be captured at the same time, just choose one to capture. When the piece reaches the opponent's bottom line, it can become king and can move backwards. Pieces cannot continue to capture chess immediately after becoming king, and must wait for the next round before they can move. A player loses if there are no more pawns to walk or if all pawns are captured."
        self.root.config()
        self.Gframe = tk.Frame(width=600, height=600)
        self.Gframe.pack_propagate(0)
        self.Gframe.pack()

        self.Gframe.rowconfigure(0, pad=0)
        self.Gframe.rowconfigure(1, pad=0)

        text = tk.Text(self.Gframe, font=('Sans', '15', 'bold'))
        text.pack(fill=BOTH, expand=True, padx=3, pady=2)
        text.insert(END, self.text)
        text.focus_set()
        text.tag_config("a", foreground="blue", justify=CENTER, underline=True)

        button = tk.Button(self.Gframe, text='Enter', command=self.change_GUI, font=('Sans', '15', 'bold'))
        button.pack()
    
    def change_GUI(self):
        self.Gframe.destroy()
        self.Gframe = firstUI(window)

class secondUI():
    def __init__(self, root):
        self.root = root
        self.text = "Note that the blue colored border is the position of the piece that can be clicked to move\nIf you choose an AI level with greater difficulty, the execution speed of the AI will be slower due to the algorithm.\n"
        # self.root.config()
        self.Gframe = tk.Frame(width=600, height=600)
        self.Gframe.pack_propagate(0)
        self.Gframe.pack()

        self.Gframe.rowconfigure(0, pad=0)
        self.Gframe.rowconfigure(1, pad=0)

        text = tk.Text(self.Gframe, font=('Sans', '15', 'bold'))
        text.pack(fill=BOTH, expand=True, padx=3, pady=2)
        text.insert(END, self.text)
        text.focus_set()
        text.tag_config("a", foreground="blue", justify=CENTER, underline=True)

        button = tk.Button(self.Gframe, text='Enter', command=self.changeToGUI, font=('Sans', '15', 'bold'))
        button.pack()
    
    def changeToGUI(self):
        self.Gframe.destroy()
        self.Gframe = GUI()

class GUI:

    def __init__(self) -> None:
        super().__init__()
        global MAX_Height
        self.maxHeight = MAX_Height
        self.player = 0 
        self.load_checkers_images()

        if self.player == AI: 
            MiniMax.AIplay(1-self.player, maxHeight=self.maxHeight, calculate=Checkers.calculate, enablePrint=False)


        self.lastX = None
        self.lastY = None
        self.willCapture = False
        self.cnt = 0

        self.btn = [[None]*Checkers.size for _ in range(Checkers.size)] # size = 8

        # create window-->frame
        frm_board = tk.Frame(master=window)
        frm_board.pack(fill=tk.BOTH, expand=True)

        # create buttons
        for i in range(Checkers.size):
            for j in range(Checkers.size):
                # create frame-->frame
                frame = tk.Frame(master=frm_board)
                frame.grid(row=i, column=j, sticky="nsew")

                self.btn[i][j] = tk.Button(master=frame, width=14, height=4, relief=tk.FLAT)
                self.btn[i][j].bind("<Button-1>", self.click)
                self.btn[i][j].pack(expand=1, fill=tk.BOTH) # , 

        # create window-->frame
        frm_options = tk.Frame(master=window)
        frm_options.pack(expand=True)


        # create window-->frame 
        frm_counter = tk.Frame(master=window)
        frm_counter.pack(expand=True)
        
        # create frame-->lable
        self.lbl_counter = tk.Label(master=frm_counter)
        self.lbl_counter.pack()

        self.update()
        nextPositions = [move[0] for move in Checkers.gotoPositions(self.player)]
        self.Tagging(nextPositions)
        window.mainloop()

    def load_checkers_images(self):  
        global checkers
        i1 = PhotoImage(file="res/2b.gif")
        i2 = PhotoImage(file="res/2bk.gif")
        i3 = PhotoImage(file="res/2h.gif")
        i4 = PhotoImage(file="res/2hk.gif")
        checkers = [0, i1, i2, i3, i4]

    # from state matrx update board
    def update(self):
    # Set up chess pieces GUi
        for i in range(Checkers.size):
            is_PLAYER = (i % 2 == 1)
            for j in range(Checkers.size):
                if is_PLAYER:
                    self.btn[i][j]['bg'] = 'black'
                else:
                    self.btn[i][j]['bg'] = 'HotPink'
                if Checkers.board[i][j] == PLAYER_MAN:
                    self.btn[i][j]['image'] = checkers[1]
                elif Checkers.board[i][j] == PLAYER_KING:
                    self.btn[i][j]['image'] = checkers[2]
                elif Checkers.board[i][j] == AI_MAN:
                    self.btn[i][j]['image'] = checkers[3]
                elif Checkers.board[i][j] == AI_KING:
                    self.btn[i][j]['image'] = checkers[4]
                else:
                    self.btn[i][j]['image'] = ""  
                is_PLAYER = not is_PLAYER
        self.lbl_counter['text'] = f'Current number of steps that not eat: {self.cnt}'
        window.update()

    # highlight the buttons that you shoud select
    def Tagging(self, positions):
    # Some moves displayed on screen
        for x in range(Checkers.size):
            for y in range(Checkers.size):
                defaultbg = self.btn[x][y].cget('bg')
                self.btn[x][y].master.config(highlightbackground=defaultbg, highlightthickness=3)

        for position in positions:
            x, y = position
            self.btn[x][y].master.config(highlightbackground="blue", highlightthickness=3)

    # when we click on the screen, what the program will do
    def click(self, event):
        info = event.widget.master.grid_info()
        x, y = info["row"], info["column"]
        
        if self.lastX == None or self.lastY == None:
            moves = Checkers.gotoPositions(self.player) 
            found = (x, y) in [move[0] for move in moves]          
            if found:
                self.lastX = x
                self.lastY = y
                normal, capture = Checkers.nextPositions(x, y)
                positions = normal if len(capture) == 0 else capture
                self.Tagging(positions)
            else:
                messagebox.showinfo(message="Invalid position!", title="Checkers")
            return

        normalPositions, capturePositions = Checkers.nextPositions(self.lastX, self.lastY)
        positions = normalPositions if (len(capturePositions) == 0) else capturePositions

        if (x, y) not in positions:
            messagebox.showinfo(message="invalid move!", title="Checkers")
            if not self.willCapture:
                self.lastX = None
                self.lastY = None
                nextPositions = [move[0] for move in Checkers.gotoPositions(self.player)]
                self.Tagging(nextPositions)
            return
        
        canCapture, removed, _ = Checkers.Move(self.lastX, self.lastY, x, y)
        self.Tagging([])
        self.update()
        self.cnt += 1
        self.lastX = None
        self.lastY = None
        self.willCapture = False

        if removed != 0:
            self.cnt = 0
        if canCapture:
            _, nextCaptures = Checkers.nextPositions(x, y)
            if len(nextCaptures) != 0:
                self.willCapture = True
                self.lastX = x
                self.lastY = y
                self.Tagging(nextCaptures)
                return
        
        # If don't eat more than 20 steps, it will improve intelligence
        calculate = MiniMax.calculate
        if self.cnt > 20:
            if INCREASE_Height:
                self.maxHeight += 3
        else:
            calculate = MiniMax.calculate
            self.maxHeight = MAX_Height
    
        # Reminders at the end of the game
        cont, reset = MiniMax.AIplay(1-self.player, maxHeight=self.maxHeight, calculate=calculate, enablePrint=False)

        self.cnt += 1
        if not cont:
            messagebox.showinfo(message="You Win!", title="Checkers")
            window.destroy()
            return
        self.update()
        if reset:
            self.cnt = 0
        if self.cnt >= 50:
            messagebox.showinfo(message="Please try again!", title="Checkers")
            window.destroy()
            return
        nextPositions = [move[0] for move in Checkers.gotoPositions(self.player)]
        self.Tagging(nextPositions)
        if len(nextPositions) == 0:
            messagebox.showinfo(message="You lost!", title="Checkers")
            window.destroy()




if __name__=="__main__":

    Checkers = Checkers(8)
    MiniMax = MiniMax(8, Checkers.board)

    MAX_Height = 0
    INCREASE_Height = True

    AI, AI_MAN, AI_KING = 1, 1, 3
    PLAYER, PLAYER_MAN, PLAYER_KING = 0, 2, 4

    window = tk.Tk()
    window.title("Checkers")
    checkers = firstUI(window)
    window.mainloop()
