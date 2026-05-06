import math
from Game import Game, Type
from Token import Token
import numpy as np


class GameAgent:
    def __init__(self, token: Token):
        self._token = token

    def token(self):
        return self._token

    def make_move(self, game: Game):
        """
        Returns the next move for the given game state.
        Tic-Tac-Toe: returns (row, col). Connect Four: returns column index.
        Returning (-1,-1) or -1 triggers a random fallback move.
        """
        # dispatch by game type
        if game.get_type() == Type.TIC_TAC_TOE:
            return self.ttt_move(game)

        return self.connect4_move(game)



    def ttt_move(self, game: Game):
        board = game.get_board()
        my_val = self._token.value()
        if game.player1_token().value() == my_val:
            opp_val = game.player2_token().value()
        else:
            opp_val = game.player1_token().value()
        best_score = -math.inf
        best_move = None
        for r, c in self.cells(board):
            board[r][c] = my_val
            score = self.minimax(board, False, my_val, opp_val)
            board[r][c] = ''
            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move if best_move is not None else (-1, -1)

    def minimax(self, board, maximizing, my_val, opp_val):
        if self.winner(board, my_val):
            return 1
        if self.winner(board, opp_val):
            return -1
        empty = self.cells(board)
        if not empty:
            return 0
        if maximizing:
            best_score = -math.inf
            for r, c in empty:
                board[r][c] = my_val
                score = self.minimax(board, False, my_val, opp_val)
                board[r][c] = ''
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for r, c in empty:
                board[r][c] = opp_val
                score = self.minimax(board, True, my_val, opp_val)
                board[r][c] = ''
                best_score = min(score, best_score)
            return best_score

    def cells(self, board):
        empty = []
        for r in range(3):
            for c in range(3):
                if board[r][c] == '':
                    empty.append((r, c))
        return empty
    def winner(self, board, val):
        boardlen=3
        for r in range(boardlen):
            if board[r][0]==val and board[r][1]==val and board[r][2] == val:
                return True
        for c in range(boardlen):
            if board[0][c]==val and board[1][c] ==val and board[2][c] == val:
                return True
        if board[0][0] ==val and board[1][1]==val and board[2][2] == val:
            return True
        if board[2][0]==val and board[1][1] == val and board[0][2] == val:
            return True
        return False


    def connect4_move(self, game: Game):
        if game.number_of_players() == 3:
            return self.connect4_multiplayer_move(game)

        board = game.get_board()
        my_val = self._token.value()
        seq = game.number_of_seq_tokens_needed()
        if game.player1_token().value()==my_val:
            opp_val = game.player2_token().value()
        else:
            opp_val = game.player1_token().value()
        valid_moves = self.valid_columns(board)
        if not valid_moves:
            return -1

        for col in valid_moves:
            temp = board.copy()
            row = self.try_move(temp, col, my_val)
            if self.is_win_at(temp, row, col, my_val, seq):
                return col

        for col in valid_moves:
            temp = board.copy()
            row = self.try_move(temp, col, opp_val)
            if self.is_win_at(temp, row, col, opp_val, seq):
                return col

        cols = board.shape[1]
        if cols <= 7:
            depth = 5
        elif cols <= 10:
            depth = 4
        else:
            depth = 3

        ordered = self._ordered_moves(valid_moves, cols)
        top_score = -math.inf
        best_col = ordered[0]
        for col in ordered:
            temp = board.copy()
            row = self.try_move(temp, col, my_val)
            if self.is_win_at(temp, row, col, my_val, seq):
                return col
            currscore = self.minimax_c4(temp, depth, False, my_val, opp_val, -math.inf, math.inf, seq)
            if currscore > top_score:
                top_score = currscore
                best_col = col

        return best_col

    def minimax_c4(self, board, depth, maximizing, my_val, opp_val, alpha, beta, seq):
        valid_moves = self.valid_columns(board)
        if depth == 0 or not valid_moves:
            return self.evaluate(board, my_val, opp_val, seq)

        cols = board.shape[1]
        ordered = self._ordered_moves(valid_moves, cols)

        if maximizing:
            best = -math.inf
            for col in ordered:
                temp = board.copy()
                row = self.try_move(temp, col, my_val)
                if self.is_win_at(temp, row, col, my_val, seq):
                    return 100000
                score = self.minimax_c4(temp, depth-1, False, my_val, opp_val, alpha, beta, seq)
                if score > best:
                    best = score
                if best > alpha:
                    alpha = best
                if alpha >= beta:
                    break
            return best
        else:
            best = math.inf
            for col in ordered:
                temp = board.copy()
                row = self.try_move(temp, col, opp_val)
                if self.is_win_at(temp, row, col, opp_val, seq):
                    return -100000
                score = self.minimax_c4(temp, depth-1, True, my_val, opp_val, alpha, beta, seq)
                if score < best:
                    best = score
                if best < beta:
                    beta = best
                if alpha >= beta:
                    break
            return best

    def valid_columns(self, board):
        cols=[]
        num_cols=board.shape[1]
        num_rows=board.shape[0]
        for col in range(num_cols):
            for row in range(num_rows):
                if board[row][col]=='':
                    cols.append(col)
                    break
        return cols
    def try_move(self, board, col, token):
        for row in range(board.shape[0]-1, -1, -1):
            if board[row][col] == '':
                board[row][col] = token
                return row
        return -1

    def is_win_at(self, board, row, col, token, seq):

        if row < 0:
            return False
        rows, cols = board.shape
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            count = 1
            r, c = row + dr, col + dc
            while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
                count += 1
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < rows and 0 <= c < cols and board[r][c] == token:
                count += 1
                r -= dr
                c -= dc
            if count >= seq:
                return True
        return False

    def _ordered_moves(self, valid_moves, num_cols):
        center = num_cols // 2
        return sorted(valid_moves, key=lambda c: abs(c - center))

    def is_win(self, board, token, seq=4):
        rows=board.shape[0]
        cols=board.shape[1]
        for r in range(rows):
            for c in range(cols):
                count=0
                for i in range(seq):
                    if c+i<cols and board[r][c+i]==token:
                        count+=1
                if count==seq:
                    return True
        for c in range(cols):
            for r in range(rows):
                count = 0
                for i in range(seq):
                    if r+i < rows and board[r+i][c]==token:
                        count+=1
                if count==seq:
                    return True
        for r in range(rows):
            for c in range(cols):
                count=0
                for i in range(seq):
                    if r+i<rows and c+i<cols and board[r+i][c+i]==token:
                        count+=1
                if count==seq:
                    return True
        for r in range(rows):
            for c in range(cols):
                count = 0
                for i in range(seq):
                    if r-i>=0 and c+i<cols and board[r-i][c+i]==token:
                        count += 1
                if count==seq:
                    return True
        return False

    def connect4_multiplayer_move(self, game: Game):
        b = game.get_board()
        myVal = self._token.value()
        seq = game.number_of_seq_tokens_needed()
        #treat H as  enemy
        oppList = []
        if game.get_type()==Type.CONNECT_4_HIDDEN_MULTIPLAYER:
            oppList = ['H']
        else:
            for t in [game.player1_token(), game.player2_token(), game.player3_token()]:
                if t is not None and t.value() != myVal:
                    oppList.append(t.value())

        moves = self.valid_columns(b)
        if not moves:
            return -1
        for col in moves:
            tmp = b.copy()
            r = self.try_move(tmp, col, myVal)
            if self.is_win_at(tmp, r, col, myVal, seq):
                return col
        for opp in oppList:
            for col in moves:
                tmp = b.copy()
                r = self.try_move(tmp, col, opp)
                if self.is_win_at(tmp, r, col, opp, seq):
                    return col

        num_cols = b.shape[1]
        ordered = self._ordered_moves(moves, num_cols)
        bestCol = ordered[0]
        topScore = -math.inf
        for col in ordered:
            tmp = b.copy()
            self.try_move(tmp, col, myVal)
            s = self.mp_eval(tmp, myVal, oppList, seq)
            if s > topScore:
                topScore = s
                bestCol = col
        return bestCol

    def mp_eval(self, board, myVal, oppList, seq=4):
        rows=board.shape[0]
        cols=board.shape[1]
        currscore=0
        mid=cols//2
        midcol=list(board[:, mid])
        currscore += midcol.count(myVal)*6
        w = seq-1
        for r in range(rows):
            for c in range(cols):
                mc=0
                oc=0
                for i in range(w):
                    if c+i < cols:
                        cell = board[r][c+i]
                        if cell == myVal:
                            mc+=1
                        elif cell in oppList:
                            oc+=1
                if oc==0 and mc==w:
                    currscore+=10
                if mc==0 and oc==w:
                    currscore-=10
        return currscore

    def evaluate(self, board, my_val, opp_val, seq=4):
        rows=board.shape[0]
        cols = board.shape[1]
        currscore=0
        center=cols//2
        center_col=list(board[:, center])
        center_count=center_col.count(my_val)
        currscore += center_count*6
        window=seq-1
        for r in range(rows):
            for c in range(cols):
                my_count=0
                opp_count=0
                for i in range(window):
                    if c + i < cols:
                        if board[r][c+i]==my_val:
                            my_count+=1
                        elif board[r][c+i]==opp_val:
                            opp_count+=1
                if opp_count== 0 and my_count==window:
                    currscore+= 10
                if my_count==0 and opp_count==window:
                    currscore-=10
        return currscore