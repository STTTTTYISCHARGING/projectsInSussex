import random
import time
# ----------------------------------------------------------------------------
from collections import Counter
from tkinter import *


# start values which are used to represent AI or players
AI, AI_MAN, AI_KING = 1, 1, 3
PLAYER, PLAYER_MAN, PLAYER_KING = 0, 2, 4

# The direction of chess pieces movement
DirectionX = [1, 1, -1, -1]
DirectionY = [1, -1, 1, -1]


# Various operations on the chessboard
class Checkers():

    # Creating chessboard
    def __init__(self, size):
        self.size = size
        self.board = []

        piece = AI_MAN
        # The state matrix, which changes the value of the chessboard through the transformation of the matrix
        for i in range(size):
            chess_board = []
            is_PLAYER = (i % 2 == 1)
            # The top(0-3 lines) is AI and the bottom(5-7 lines) is PLAYER, there are spaces between each piece
            if i == (size / 2 - 1):
                piece = 0
            elif i == (size / 2 + 1):
                piece = PLAYER_MAN         
            # One Empty one Road, alternate
            for _ in range(size):
                if is_PLAYER:
                    chess_board.append(piece)
                else:
                    chess_board.append(0)
                # The next line is contrary
                is_PLAYER = (not is_PLAYER)
            self.board.append(chess_board)
            '''
            0:[0, 1, 0, 1, 0, 1, 0, 1]
            1:[1, 0, 1, 0, 1, 0, 1, 0]
            2:[0, 1, 0, 1, 0, 1, 0, 1]
            3:[0, 0, 0, 0, 0, 0, 0, 0]
            4:[0, 0, 0, 0, 0, 0, 0, 0]
            5:[2, 0, 2, 0, 2, 0, 2, 0]
            6:[0, 2, 0, 2, 0, 2, 0, 2]
            7:[2, 0, 2, 0, 2, 0, 2, 0]
            '''
        

    # Record the situation 
    def RecordBoard(self):
        value = 0
        for i in range(self.size):
            for j in range(self.size):
            # The minimum value is 9
            # As long as it does not repeat the assignment above, it is arbitrary
                num = i * self.size + j + 9
                value += num * self.board[i][j]
        return value

    # Check if the position is inside the board
    def isValid(self, x, y):
        return (x >= 0) and (x < self.size) and (y >= 0) and (y < self.size)
    
    # Get the possible next positions
    def nextPositions(self, x, y):
        # Nothing happened when you choose the empty position
        if self.board[x][y] == 0:
            return []
        # Judge whether it is PLAYER or AI, 0 is PLAYER, 1 is AI
        player = self.board[x][y] % 2
        StepsMove = []
        OneStepMove = []
        if player == AI:
            color_sign = 1
        else:
            color_sign = -1
      # Judge whether it is Man or King, use >2 to judge whether it is king or not
        if self.board[x][y] <= 2:
            is_king = 2
        else:
            is_king = 4
        # Man only have 0 or 1(Two directions at most), King has 0,1,2,3(Four directions at most)
        for i in range(is_king):
            nx = x + color_sign * DirectionX[i]
            ny = y + color_sign * DirectionY[i]
            # If the next move point is empty, then move normally
            if self.isValid(nx, ny):
                if self.board[nx][ny] == 0:
                    OneStepMove.append((nx, ny))
                # If the next one is the opponent's chess and the diagonal is empty, then make a special move
                elif self.board[nx][ny] % 2 == 1 - player:
                    nx += color_sign * DirectionX[i]
                    ny += color_sign * DirectionY[i]
                    if self.isValid(nx, ny) and self.board[nx][ny] == 0:
                        StepsMove.append((nx, ny))
        return OneStepMove, StepsMove

    # Determine whether the position at x, y is the pawn that is executing the round
    def isCurrentPiece(self, x, y, player):
        return (self.board[x][y] != 0) and (self.board[x][y] % 2 == player)


    # Use a tuple to store where each position can be moved
    def gotoPositions(self, player):
        # Initialize possible moves
        StepsMove = []
        OneStepMove = []
        for x in range(self.size):
            for y in range(self.size):
                # Determine the movable pieces and mobile mode
                if self.isCurrentPiece(x, y, player):
                    normal, capture = self.nextPositions(x, y) 
                    if len(normal) != 0:
                        OneStepMove.append(((x, y), normal))
                    if len(capture) != 0:
                        StepsMove.append(((x, y), capture))       
        # Forced capture, you must make a special move
        if len(StepsMove) != 0:
            return StepsMove
        return OneStepMove

    # From (x, y) to (nx, ny)
    def Move(self, x, y, nx, ny):
        # Change the state matrix of the pawn
        self.board[nx][ny] = self.board[x][y]
        self.board[x][y] = 0
        removed = 0

        # Jump move, remove the captured piece 
        if abs(nx - x) == 2:
            DirectionX = nx - x
            DirectionY = ny - y
            removed = self.board[x + DirectionX // 2][y + DirectionY // 2]
            time.sleep(0.3) 
            self.board[x + DirectionX // 2][y + DirectionY // 2] = 0

        # When the piece arrived the end, it will promote to king 
        if self.board[nx][ny] == AI_MAN and nx == self.size - 1:
            self.board[nx][ny] = AI_KING
            return False, removed, True
        elif self.board[nx][ny] == PLAYER_MAN and nx == 0:
            self.board[nx][ny] = PLAYER_KING
            return False, removed, True
        
        # Normally move
        if abs(nx - x) != 2:
            return False, removed, False

        # Regicide -if Man manages to capture King, he is instantly crowned King
        if self.board[nx][ny] == AI_MAN and removed == PLAYER_KING:
            self.board[nx][ny] = AI_KING
            return True, removed, True
        elif self.board[nx][ny] == PLAYER_MAN and removed == AI_KING:
            self.board[nx][ny] = PLAYER_KING
            return True, removed, True
        else:
            return True, removed, False

    # Backtracking During Algorithm Execution
    def backtracking(self, x, y, nx, ny, removed=0, promoted=False):
        # If Man captured King before, he should be back to Man
        if self.board[nx][ny] == AI_MAN and removed == PLAYER_KING:
            self.board[x][y] = AI_MAN
        elif self.board[nx][ny] == PLAYER_MAN and removed == AI_KING:
            self.board[x][y] = PLAYER_MAN
        # If Man arrived the end before, he should be back to Man
        if promoted:
            if self.board[nx][ny] == AI_KING:
                self.board[nx][ny] = AI_MAN
            elif self.board[nx][ny] == PLAYER_KING:
                self.board[nx][ny] = PLAYER_MAN
        #Restore to original
        self.board[x][y] = self.board[nx][ny]
        self.board[nx][ny] = 0
        if abs(nx - x) == 2:
            DirectionX = nx - x
            DirectionY = ny - y
            self.board[x + DirectionX // 2][y + DirectionY // 2] = removed

# Algorithm
class MiniMax(Checkers):

    MAX = 0x32769
    K = 100

    def __init__(self, size, board):
        super(MiniMax, self).__init__(size)
        self.board = board

    # calculate the current state of the board
    def calculate(self, maxormin): 
        # Initialize all kinds of scores
        men, kings = 0, 0
        back_row, middle_box, middle_row = 0, 0, 0
        vulnerable, protected = 0, 0

        #Calculate all kinds of scores
        for i in range(8):
            for j in range(8):
                # Judge whether it is empty or not
                if self.board[i][j] != 0:
                    if self.board[i][j] % 2 == maxormin:
                        sign = 1
                    else:
                        sign = -1
                    # Judge whether it is King or not
                    if self.board[i][j] <= 2:
                        men += sign*1
                    else:
                        kings += sign*1
                    # Judge whether it is back row or not
                    if (sign == 1) and ((i == 0 and maxormin == AI) or (i == self.size-1 and maxormin == PLAYER)):
                        back_row += 1
                    # Judge whether it is middle row or not
                    if (i == self.size/2-1) or (i == self.size/2):
                        if (j >= self.size/2-2) and (j < self.size/2+2):
                            middle_box += sign*1
                        else:
                            middle_row += sign*1
                    # Judge whether it is protected or not
                    if maxormin == AI:
                        myDir = 1
                    else:
                        myDir = -1
                    vul = False
                    for k in range(4):
                        x = i + DirectionX[k]
                        y = j + DirectionY[k]
                        n = i - DirectionX[k]
                        m = j - DirectionY[k]
                        opDir = abs(x-n)/(x-n)
                        if self.isValid(x, y) and (self.board[x][y] != 0) and (self.board[x][y] % 2 != maxormin) and self.isValid(n, m) and (self.board[n][m] == 0) and (self.board[x][y] > 2 or myDir != opDir):
                            vul = True
                            break
                    if vul:
                        vulnerable += sign*1
                    else:
                        protected += sign*1
        return men*self.K + kings*2*self.K + back_row*0.2*self.K + middle_box*0.2*self.K + middle_row*0.2*self.K - self.K*vulnerable + self.K*protected

    # Return the score by using Minimax evaluation and Alpha-Beta pruning.
    def minimax(self, player, maxormin, Height=0, alpha=-MAX, beta=MAX, maxHeight=5, calculate=calculate, multiStepsMoves=None):
        # Termination condition
        if multiStepsMoves == None:
            multiStepsMoves = super().gotoPositions(player)
        if len(multiStepsMoves) == 0 or Height == maxHeight:
            score = self.calculate(maxormin)
            # If there is no escape from losing, maximize number of moves to lose
            if score < 0:
                score += Height
            return score

        # init the algorithm parameters
        greatValue = -self.MAX
        if player != maxormin:
            greatValue = self.MAX
        
        # sort that reduce the compulation
        multiStepsMoves.sort(key=lambda move: len(move[1]))

        # recursive execution
        for node in multiStepsMoves:
            x, y = node[0]
            for nx, ny in node[1]:
                canCapture, removed, promoted = super().Move(x, y, nx, ny)
                played = False
                if canCapture:
                    _, nextCaptures = super().nextPositions(nx, ny)
                    if len(nextCaptures) != 0:
                        played = True
                        nMoves = [((nx, ny), nextCaptures)]
                        if player == maxormin:
                            greatValue = max(greatValue, self.minimax(player, maxormin, Height + 1, alpha, beta, maxHeight, calculate, nMoves))
                            alpha = max(alpha, greatValue)
                        else:
                            greatValue = min(greatValue, self.minimax(player, maxormin, Height + 1, alpha, beta, maxHeight, calculate, nMoves))
                            beta = min(beta, greatValue)
                if not played:
                    if player == maxormin:
                        greatValue = max(greatValue, self.minimax(1 - player, maxormin, Height + 1, alpha, beta, maxHeight, calculate))
                        alpha = max(alpha, greatValue)
                    else:
                        greatValue = min(greatValue, self.minimax(1 - player, maxormin, Height + 1, alpha, beta, maxHeight, calculate))
                        beta = min(beta, greatValue)
                super().backtracking(x, y, nx, ny, removed, promoted)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return greatValue

    # AI executes chess process
    def AIplay(self, player: int, multiStepsMoves=None, maxHeight=5, calculate=calculate, enablePrint=True): 
        self.stateCounter = Counter() 

        # init
        if multiStepsMoves == None:
            multiStepsMoves = super().gotoPositions(player)

        # Boundary conditions
        if len(multiStepsMoves) == 0:
            return False, False

        # Parameters required to initialize the algorithm
        self.stateCounter[super().RecordBoard()] += 1
        random.shuffle(multiStepsMoves)
        greatValue = -self.MAX
        bestMove = None

        for node in multiStepsMoves: 
            x, y = node[0]
            for nx, ny in node[1]:
                _, removed, promoted = super().Move(x, y, nx, ny)
                value = self.minimax(1 - player, player, maxHeight=maxHeight, calculate=calculate) 
                super().backtracking(x, y, nx, ny, removed, promoted)
                if value > greatValue:
                    greatValue = value
                    bestMove = (x, y, nx, ny)

        x, y, nx, ny = bestMove
        
        # AI move
        canCapture, removed, _ = super().Move(x, y, nx, ny)
        if canCapture:
            _, captures = super().nextPositions(nx, ny)
            if len(captures) != 0:
                self.AIplay(player, [((nx, ny), captures)], maxHeight, calculate, enablePrint)
                
        self.stateCounter[super().RecordBoard()] += 1
        result = removed != 0
        return True, result

