"""
CIS 163
Final Project - Chess - piece_model.py
By: Elijah Morgan, Austin Jackson, Stephen Robinson
3/27/2023
"""
import random
import copy

import pygame as pg
from enum import Enum

class Color(Enum):
    """
    Determines whose turn it currently is.
    """
    BLACK = 0
    WHITE = 1

    def opposite(self):
        if self.value == 0:
            return self.WHITE
        return self.BLACK

class Game:
    def __init__(self):
        self.color = Color.WHITE
        self.board = [[None]*8 for i in range(8)]
        self.moves = []  # Previous board states are stored here in this "stack"

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, col):
        if not isinstance(col, Color):
            raise ValueError('Color must be black or white')
        self._color = col

    def reset(self):
        self.board = [[None] * 8 for i in range(8)]
        self.color = Color.WHITE
        self._setup_pieces()
        self.moves = [self.board]


    def _setup_pieces(self):
        """
        Places the pieces on the board in the start positions, assumes Black (Computer) will be at the top.
        """
        i = 0
        copy_pawn_b = Pawn(Color.BLACK)
        not_pawn_b = [Rook(Color.BLACK), Knight(Color.BLACK), Bishop(Color.BLACK), Queen(Color.BLACK),
                      King(Color.BLACK), Bishop(Color.BLACK), Knight(Color.BLACK), Rook(Color.BLACK)]

        not_pawn_w = [Rook(Color.WHITE), Knight(Color.WHITE), Bishop(Color.WHITE), Queen(Color.WHITE), King(Color.WHITE),
                    Bishop(Color.WHITE), Knight(Color.WHITE), Rook(Color.WHITE)]
        copy_pawn_w = Pawn(Color.WHITE)

        while i < len(self.board):
            #white
            self.board[7][i] = not_pawn_w[i].copy()
            self.board[6][i] = copy_pawn_w.copy()
            #black
            self.board[0][i] = not_pawn_b[i].copy()
            self.board[1][i] = copy_pawn_b.copy()

            i += 1



    def print_board(self, board: list):
        # print('###################')
        # for y in range(len(board)):
        #     for x in range(len(board[y])):
        #         print(f'{y}{x}', end=' ')
        #     print()
        # print('###################')
        print('###################')
        for col in board:
            for tile in col:
                if tile is None:
                    print('O', end =' ')
                elif tile.color == Color.WHITE:
                    print(f'W', end=' ')
                else:
                    print(f'B', end=' ')
            print()
        print('###################')
    def get(self, y:int, x: int):
        if y > 7:
            y = 7
        if x > 7:
            x = 7
        return self.board[y][x]

    def switch_player(self) -> None:
        if self.color == Color.WHITE:
            count = 0
        else:
            count = 1
        self.color = Color(count)

    def undo(self) -> bool:
        if len(self.moves) >= 1: # Might have to be set to "<= 1". Try that if you run into an IndexError
            self.board = self.moves[-1]
            self.moves.pop(-1)
            return True
        else:
            return False

    def copy_board(self):

        board_copy = [[None]*8 for i in range(8)]
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] != None:
                    board_copy[y][x] = self.board[y][x].copy()
        return board_copy

    def move(self, piece, y: int, x: int, y2: int, x2: int) -> bool:
        # for index, m in enumerate(self.moves):
        #         print('index', index)
        #         self.print_board(m)
        self.moves.append(self.copy_board())
        # for index, m in enumerate(self.moves):
        #         print('index', index)
        #         self.print_board(m)

        # "Moving" Piece Object
        self.board[y2][x2] = piece
        self.board[y][x] = None

        #if piece was a pawn set first_move to false
        if isinstance(self.board[y2][x2], Pawn):
            self.board[y2][x2].first_move = False


        # Check if move puts current player in check, if so, reverse the move (undo() method).
        if self.check(self.color):

            self.undo()

            print('You cant put yourself in check')
            return False

        # Check if piece is pawn, if so, check if pawn has made it to the opposite side of the board (finish lines depend on Color)
        if isinstance(self.board[y2][x2], Pawn):
            if (self.color == Color.WHITE) and (y2 == 0):
                self.board[y2][x2] = Queen(Color.WHITE)
                #self.board[y2][x2].color = Color.WHITE
            if (self.color == Color.BLACK) and (y2 == 7):
                self.board[y2][x2] = Queen(Color.BLACK)
                #self.board[y2][x2].color = Color.BLACK

        ##check win conditions
        if self.check(self.color.opposite()):#check if opposite player is in check
            #check if other player is in checkmate, if so game ends
            self.mate(self.color.opposite())
            return True
        elif self.check_Win(piece.color):
            print(f'{piece.color} wins!!')
            exit()

        #self.print_board()
        return True
    def check_Win(self, color: Color) -> bool:
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):##scans the entire board for the opposite color king
                tile = self.get(y,x)
                if tile != None: #if it is a piece
                    if tile.color == color.opposite() and isinstance(tile, King):
                        return False
        return True

    def check(self, input_color: Color)-> bool:
        #return False
        """
        Checks if input color is in check
        :param input_color: Color = 0 or 1
        :return: bool
        """
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):##scans the entire board
                if self.board[y][x] != None: #if it is a piece
                    if self.board[y][x].color == input_color.opposite(): #if it is piece is opposite color
                        for move in self.board[y][x].valid_moves(y, x): #scan through all valid move of that piece
                                if isinstance(self.get(move[0], move[1]), King): #if space contains current color king
                                    return True
        return False

    def mate(self, input_color: Color) -> bool:
        #return False
        """
        Checks if input_color has been checkmated
        only called if already in check
        :param input_color: Color
        :return: bool
        """
        def rest(lst):
            # lov -> lov
            # returns the tail of a list
            return lst[1:]

        def cons(v, lst):
            # v lov -> lov
            # appends a value onto the head of a list
            return [v]+lst

        def make_set(lov):
            # make_set: lov -> lov
            # accepts a list-of-values;
            # returns a list of the same values in no particular order
            # with all duplicates eliminated
            if lov == [] or len(lov) == 1:
                return lov
            else:
                if lov[0] in rest(lov):
                    return make_set(rest(lov))
                else:
                    return cons(lov[0], make_set(rest(lov)))

        """
        Checks if input_color has been checkmated
        only called if already in check
        :param input_color: Color
        :return: bool
        """
        ##Checks if king can move anywhere first
        all_opponent_moves = []
        king_moves = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):##scans the entire board
                if self.board[y][x] != None: #if it is a piece
                    if self.board[y][x].color == input_color.opposite(): ##if it is peice is opposite color
                        #adding all possible moves for opposite color to a list
                        all_opponent_moves = make_set(all_opponent_moves + self.board[y][x].valid_moves(y, x))
                    elif isinstance(self.board[y][x], King): #if its an (index_color) King
                        king_moves = self.board[y][x].valid_moves(y, x)
        for move in king_moves:
            if move not in all_opponent_moves:
                return False

        #check if any possible moves from input_color result in them no longer in check
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):##scans the entire board
                if self.board[y][x] != None: #if it is a piece
                    if self.board[y][x].color == input_color: ##if it is input color
                        for move in self.board[y][x].valid_moves(y, x):
                            if not self.mate2(input_color, y, x, move[0], move[1]):
                                return False
        return True

    def mate2(self,input_color, y: int, x: int, y2: int, x2: int) -> bool:
        self.moves.append(self.copy_board())

        # "Moving" Piece Object
        self.board[y2][x2] = self.board[y][x]
        self.board[y][x] = None

        # if move put takes them out of check return false
        if not self.check(input_color):
            self.undo()
            return False
        else:
            self.undo()
            return True

    def _computer_move(self):
        """
        Makes the computer opponent do a completely random move, even if the last move was undone.
        """
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                tile = self.get(y,x)
                if tile is not None:
                    if tile.color == Color.BLACK:
                        possible_moves = tile.valid_moves(y, x)
                        print(tile, (y,x), possible_moves)

                        if len(possible_moves) == 0:
                            continue
                        #checkmate
                        #
                        # for y2, x2 in possible_moves:
                        #     # print(y,x, y2, x2)
                        #     # self.print_board()
                        #     if self.move(tile, y, x, y2, x2):
                        #         if self.check(Color.WHITE):
                        #             if self.mate(Color.WHITE):
                        #                 break
                        #             else:
                        #                 self.undo()

                        #check

                        for y2, x2 in possible_moves:
                            if self.move(tile, y, x, y2, x2):
                                if self.check(Color.WHITE):
                                    return
                                else:
                                    self.undo()
        if self.target(King):
            return
        if self.target(Queen):
            return
        if self.target(Bishop):
            return
        if self.target(Knight):
            return
        if self.target(Rook):
            return
        if self.target(Pawn):
            return
        self.random_comp_move()


    def target(self, piece_type):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                tile = self.get(y,x)
                if tile is not None:
                    if tile.color == Color.BLACK:
                        possible_moves = tile.valid_moves(y, x)
                        print(tile, (y,x), possible_moves)

                        for y2, x2 in possible_moves:
                            if isinstance(self.get(y2, x2), piece_type):
                                if self.move(tile, y, x, y2, x2):
                                    return True
        return False


    def random_comp_move(self):
        piece_coords = [] #make a list of all the coords of black pieces
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                piece = self.get(y, x)
                if piece is not None:
                    if piece.color == Color.BLACK:
                        piece_coords.append((y,x))
        y, x = piece_coords[random.randint(0, len(piece_coords)-1)] #random piece

        moves = self.get(y,x).valid_moves(y,x)
        if moves != []:
            y2, x2 = moves[random.randint(0, len(moves)-1)] #random move from list of valid moves
            if not self.move(self.get(y,x), y,x,y2,x2):#if it puts itself in check, it goes again
                self.random_comp_move()
        else:
            self.random_comp_move()









class Piece:
    SPRITESHEET = pg.image.load("./images/pieces.png")
    _game = None

    PXL = 105
    def set_game(game):
        """
        Checks if an instance of game is currently active.
        """
        if not isinstance(game, Game):
            raise ValueError("You must provide a valid Game instance.")
        Piece._game = game

    def __init__(self, color: Color):
        self._color = color
        self._image = pg.Surface((105, 105), pg.SRCALPHA)



    @property
    def color(self):
        return self._color

    def set_image(self, x: int, y: int) -> None:
        """
        Gets each piece's sprite from the chess spritesheet.
        """
        self._image = pg.Surface((105, 105), pg.SRCALPHA)
        self._image.blit(Piece.SPRITESHEET, (0, 0), pg.rect.Rect(x, y, 105, 105))
    def _diagonal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int):
        """
        Finds all legal diagonal moves within a given distance.
        However, this function doesn't account for check or checkmate.
        """
        moves = []
        for current_dist in range(1, distance + 1):
            move_pos = (y + (current_dist * y_d), x + (current_dist * x_d))
            if move_pos[0] < 0 or move_pos[0] > 7 or move_pos[1] < 0 or move_pos[1] > 7:
                continue
            pos_piece = self._game.board[move_pos[0]][move_pos[1]]
            if pos_piece is None:
                moves.append(move_pos)
            elif pos_piece.color != self.color: #Checks if the position we're attacking is of the opponent's color.
                moves.append(move_pos)
                return moves
            else:
                return moves
        return moves

    def _horizontal_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int):
        """
        Finds all legal horizontal moves within a given distance.
        However, this function doesn't account for check or checkmate.
        """
        moves = []
        for current_dist in range(1, distance + 1):
            move_pos = (y, x + (current_dist * x_d))
            if move_pos[0] < 0 or move_pos[0] > 7 or move_pos[1] < 0 or move_pos[1] > 7:
                continue
            pos_piece = self._game.get(move_pos[0], move_pos[1])
            #print('hor', pos_piece)
            if pos_piece == None:
                moves.append(move_pos)
            elif pos_piece.color != self.color:  # Checks if the position we're attacking is of the opponent's color.
                moves.append(move_pos)
                return moves
            else:
                return moves
        return moves

    def _vertical_moves(self, y: int, x: int, y_d: int, x_d: int, distance: int):
        """
        Finds all legal vertical moves within a given distance.
        However, this function doesn't account for check or checkmate.
        """
        moves = []
        for current_dist in range(1, distance + 1):
            move_pos = (y + (current_dist * y_d), x)
            if move_pos[0] < 0 or move_pos[0] > 7 or move_pos[1] < 0 or move_pos[1] > 7:
                continue
            pos_piece = self._game.board[move_pos[0]][move_pos[1]]
            #print(pos_piece)

            if pos_piece is None:
                moves.append(move_pos)
            elif pos_piece.color != self.color:  # Checks if the position we're attacking is of the opponent's color.
                moves.append(move_pos)
                return moves
            else:
                return moves
        return moves

    def get_diagonal_moves(self, y: int, x: int, distance: int): # Originally had a "moves" argument. Deleted, because it did nothing.
        moves = []
        moves.extend(self._diagonal_moves(y, x, -1, -1, distance))
        moves.extend(self._diagonal_moves(y, x, 1, -1, distance))
        moves.extend(self._diagonal_moves(y, x, -1, 1, distance))
        moves.extend(self._diagonal_moves(y, x, 1, 1, distance))
        moves = list(filter(((0, 0)).__ne__, moves))  # takes a list, and returns False if value is equal to (0, 0). Removes unnecessary (0, 0) tuples
        return moves

    def get_horizontal_moves(self, y: int, x: int, distance: int):
        moves = []
        moves.extend(self._horizontal_moves(y, x, 0, -1, distance))
        moves.extend(self._horizontal_moves(y, x, 0, 1, distance))
        #moves = list(filter(((0, 0)).__ne__, moves))  # takes a list, and returns False if value is equal to (0, 0). Removes unnecessary (0, 0) tuples
        #moves = list(filter(((0, 7)).__ne__, moves))  # Due to the way I avoided index errors, we want to filter out excess instances of (0, 7) tuples
        #moves.append((0, 7))
        return moves

    def get_vertical_moves(self, y: int, x: int, distance: int):
        moves = []
        moves.extend(self._vertical_moves(y, x, -1, 0, distance))
        moves.extend(self._vertical_moves(y, x, 1, 0, distance))
        #moves = list(filter(((0, 0)).__ne__, moves))  # takes a list, and returns False if value is equal to (0, 0). Removes unnecessary (0, 0) tuples
        return moves

    def valid_moves(self, y: int, x: int):
        raise Warning("The valid_moves() method should be used by child classes only.")

    def copy(self):
        raise Warning("The copy() method should be used by child classes only.")

class King(Piece):
    def __init__(self, color: Color):
        self._image = None
        super().__init__(color)
        if self.color is Color.WHITE:
            self.set_image(x=0, y=0)
        else:
            self.set_image(x=0,y=Piece.PXL)

    def valid_moves(self, y: int, x: int):
        moves = []
        moves.extend(super().get_diagonal_moves(y, x, distance=1))
        moves.extend(super().get_horizontal_moves(y, x, distance=1))
        moves.extend(super().get_vertical_moves(y, x, distance=1))
        return moves

    def copy(self):
        king_copy = King(self.color)
        king_copy._color = self._color
        king_copy._image = self._image

        return king_copy
        #return copy.deepcopy(self)

class Queen(Piece):
    def __init__(self, color: Color):
        self._image = None
        super().__init__(color)
        if self.color is Color.WHITE:
            self.set_image(x=Piece.PXL * 1, y=0)
        else:
            self.set_image(x=Piece.PXL * 1, y=Piece.PXL)

    def valid_moves(self, y: int, x: int):
        moves = []
        moves.extend(super().get_diagonal_moves(y, x, distance=8))
        moves.extend(super().get_horizontal_moves(y, x, distance=8))
        moves.extend(super().get_vertical_moves(y, x, distance=8))
        return moves

    def copy(self):
        queen_copy = Queen(self.color)
        queen_copy._color = self._color
        queen_copy._image = self._image

        return queen_copy
        #return copy.deepcopy(self)

class Bishop(Piece):
    def __init__(self, color: Color):
        self._image = None
        super().__init__(color)
        if self.color is Color.WHITE:
            self.set_image(x=Piece.PXL * 2, y=0)
        else:
            self.set_image(x=Piece.PXL * 2, y=Piece.PXL)

    def valid_moves(self, y: int, x: int):
        moves = []
        moves.extend(super().get_diagonal_moves(y, x, distance=8))
        return moves

    def copy(self):
        bishop_copy = Bishop(self.color)
        if self.color:
            bishop_copy._color = Color.WHITE
        else:
            bishop_copy._color = Color.BLACK
        bishop_copy._color = self._color
        bishop_copy._image = self._image

        return bishop_copy
        #return copy.deepcopy(self)

class Knight(Piece):
    def __init__(self, color: Color):
        self._image = None
        super().__init__(color)
        if self.color is Color.WHITE:
            self.set_image(x=Piece.PXL * 3, y=0)
        else:
            self.set_image(x=Piece.PXL * 3, y=Piece.PXL)

    def valid_moves(self, y: int, x: int):
        #FIXME cannot move onto spot with same color piece <- Isn't that normal for all pieces? -Eli

        moves = [(y-2,x-1), (y-2,x+1), (y-1,x-2), (y-1,x+2), (y+1,x-2), (y+1,x+2), (y+2,x-1), (y+2,x+1)]
        new = []
        for my, mx in moves:
            if my in range(0, 8) and mx in range(0, 8):
                if self._game.get(my, mx) == None:
                    new.append((my, mx))
                elif self._game.get(my,mx).color != self.color:
                    new.append((my,mx))
        return new

    def copy(self):
        knight_copy = Knight(self.color)
        knight_copy._color = self._color
        knight_copy._image = self._image

        return knight_copy
        #return copy.deepcopy(self)

class Rook(Piece):
    def __init__(self, color: Color):
        self._image = None
        super().__init__(color)
        if self.color is Color.WHITE:
            self.set_image(x=Piece.PXL * 4, y=0)
        else:
            self.set_image(x=Piece.PXL * 4, y=Piece.PXL)

    def valid_moves(self, y: int, x: int):
        moves = []
        moves.extend(super().get_horizontal_moves(y, x, distance=8))
        moves.extend(super().get_vertical_moves(y, x, distance=8))
        return moves

    def copy(self):
        rook_copy = Rook(self.color)
        if self.color:
            rook_copy._color = Color.WHITE
        else:
            rook_copy._color = Color.BLACK
        rook_copy._color = self._color
        rook_copy._image = self._image

        return rook_copy

        #return copy.deepcopy(self)

class Pawn(Piece):
    def __init__(self, color: Color):
        self._image = None
        super().__init__(color)

        if self.color is Color.WHITE:
            self.set_image(x=Piece.PXL * 5, y=0)
        else:
            self.set_image(x=Piece.PXL * 5, y=Piece.PXL)

        self.first_move = True

    def valid_moves(self, y: int, x: int):
        moves = []
        distance = 1
        if self.color == Color.WHITE:
            pos_piece = self._game.get(y-1, x)
            if pos_piece is None:
                moves.append((y-1, x))
            #first move
            if self.first_move:
                pos_piece = self._game.get(y-2, x)
                if pos_piece is None:
                    moves.append((y-2, x))
            #diagonal attack
            pos_piece = self._game.get(y-1, x-1)
            if pos_piece is not None:
                if pos_piece.color == Color.BLACK:
                    moves.append((y-1, x-1))
            pos_piece = self._game.get(y-1, x+1)
            if pos_piece is not None:
                if pos_piece.color == Color.BLACK:
                    moves.append((y-1, x+1))

        else:
            pos_piece = self._game.get(y+1, x)
            if pos_piece is None:
                moves.append((y+1, x))
            #first move
            if self.first_move:
                pos_piece = self._game.get(y+2, x)
                if pos_piece is None:
                    moves.append((y+2, x))
            #diagonal attack
            pos_piece = self._game.get(y+1, x-1)
            if pos_piece is not None:
                if pos_piece.color == Color.WHITE:
                    moves.append((y+1, x-1))
            pos_piece = self._game.get(y+1, x+1)
            if pos_piece is not None:
                if pos_piece.color == Color.WHITE:
                    moves.append((y+1, x+1))

        removed = []
        for y2, x2 in moves:
            if  y != y2 and x != x2:
                removed.append((y2,x2))
            if y2 in range(0,8) and x2 in range(0,8):
                removed.append((y2,x2))
        return removed

    def copy(self):
        pawn_copy = Pawn(self.color)
        if self.color == Color.WHITE:
            pawn_copy._color = Color.WHITE
        else:
            pawn_copy._color = Color.BLACK
        pawn_copy._color = self._color
        pawn_copy._image = self._image
        pawn_copy.first_move = self.first_move

        return pawn_copy
        #return copy.deepcopy(self)

"""
#FIXME r/anarchychess
class Knook(Piece):
    print("Holy hell")

delete this before turning in lol.

def main():
    b = Color.BLACK
    w = Color.WHITE
    print(b.opposite(), w.opposite())
    assert b.opposite() == w
if __name__ == '__main__':
    main()
"""
