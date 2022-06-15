#!/usr/bin/env python
# coding: utf-8

# In[7]:


from random import random
import copy
import numpy as np
from time import time
big_number = 10**7
Depth = 3


# In[8]:


class Node:
    def __init__(self):
        self.data = None
        self.parent = None
        self.child = []
        self.move = None
        self.board = None
    
    def set_board(self, board_):
        self.board = board_
    def get_board(self):
        return self.board
    
    def set_move(self, move_):
        self.move = move_
    def get_move(self):
        return self.move
    
    def set_parent(self, parent_):
        self.parent = parent_
    def get_parent(self):
        return self.parent
    
    def set_data(self, value):
        self.data = value
    def get_data(self):
        return self.data
    
    def set_child(self, child_):
        self.child.append(child_)
    def get_child(self):
        return self.child
    
    def set_value(self, value_):
        self.data = value_
    def get_value(self):
        return self.data


# ## Alpha-Beta Pruning Added

# In[20]:


YOU = 1
CPU = -1
EMPTY = 0
class My_Bot:
    __CONNECT_NUMBER = 4
    def __init__(self, board_):
        self.board = board_
        bb = np.array(board_)
        self.rows = bb.shape[0]
        self.columns = bb.shape[1]
        self.tree = None
    
    def drop_piece_in_column(self, board,  move, current_player):
        last_empty_space = 0
        column_index = move - 1
        for i in range(self.rows):
            if (board[i][column_index] == 0):
                last_empty_space = i
        board[last_empty_space][column_index] = current_player
        return board
    
    def calculate_value(self, board_):
        player_id = YOU
        your_value = 0
        your_value += self.calculate_value_diagonally(player_id, board_)
        your_value += self.calculate_value_vertically(player_id, board_)
        your_value += self.calculate_value_horizentally(player_id, board_)
        
        player_id = CPU
        CPU_value = 0
        CPU_value_1 = self.calculate_value_diagonally(player_id, board_)
        CPU_value_2 = self.calculate_value_vertically(player_id, board_)
        CPU_value_3 = self.calculate_value_horizentally(player_id, board_)
        CPU_value = CPU_value_1 + CPU_value_2 + CPU_value_3
#         if your_value + CPU_value >= 2*big_number:
#             if CPU_value_1 == -1*big_number:
                
        return your_value - CPU_value
    
    def change_turn(self, turn):
        if (turn == YOU): 
            return CPU
        else:
            return YOU
    def is_move_valid(self, move, board):
        if (move < 1 or move > self.columns):
            return False
        column_index = move - 1
        return board[0][column_index] == 0
    
    def get_possible_moves(self, board):
        possible_moves = []
        for i in range(self.columns):
            move = i + 1
            if (self.is_move_valid(move, board)):
                possible_moves.append(move)
        return possible_moves
    
    def print_board(self, board):
        print(' ')
        for i in range(self.rows):
            for j in range(self.columns):
                house_char = "O"
                if (board[i][j] == YOU):
                    house_char = "Y"
                elif (board[i][j] == CPU):
                    house_char = "C"
                    
                print(f"{house_char}", end=" ")
            print()
    
    def create_tree(self, root, current_depth, current_player):
        current_depth += 1
        for move in self.get_possible_moves(root.get_board()):
            new_node = Node()
            new_node.set_board(copy.deepcopy(root.get_board()))
            new_node.set_move(move)
            root.set_child(new_node)
            new_node.set_parent(root)
            new_node.set_board(self.drop_piece_in_column(new_node.get_board(),  move, current_player))
            
            if current_depth == Depth:
                new_node.set_data(self.calculate_value(new_node.get_board()))
        
        if current_depth == Depth:
            return root
        
        current_player = self.change_turn(current_player)
        for j in range(len(root.get_child())):
            self.create_tree(root.get_child()[j], current_depth, current_player)

        return root
        
    def calculate_value_horizentally(self, player_id, board):
        value = 0
        for i in range(self.rows):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                possible = None
                num_you = 0
                for x in range(self.__CONNECT_NUMBER):
                    if board[i][j + x] == player_id:
                        num_you += 1
                        possible = True
                    if board[i][j + x] == self.change_turn(player_id):
                        possible = False
                        break
                if possible:
                    value += 1
                if num_you == self.__CONNECT_NUMBER:
                    value = big_number
        return value

    def calculate_value_vertically(self, player_id, board):
        value = 0
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns):
                possible = None
                num_you = 0
                for x in range(self.__CONNECT_NUMBER):
                    if board[i + x][j] == player_id:
                        num_you += 1
                        possible = True
                    if board[i + x][j] == self.change_turn(player_id):
                        possible = False
                        break
                if possible:
                    value += 1
                if num_you == self.__CONNECT_NUMBER:
                    value = big_number
        return value

    def calculate_value_diagonally(self, player_id, board):
        value = 0
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                possible = None
                num_you = 0
                for x in range(self.__CONNECT_NUMBER):
                    if board[i + x][j + x] == player_id:
                        num_you += 1
                        possible = True
                    if board[i + x][j + x] == self.change_turn(player_id):
                        possible = False
                        break
                if possible:
                    value += 1
                if num_you == self.__CONNECT_NUMBER:
                    value = big_number
                possible = None
                num_you = 0
                for x in range(self.__CONNECT_NUMBER):
                    if board[i + self.__CONNECT_NUMBER - 1 - x][j + x] == player_id:
                        num_you += 1
                        possible = True
                    if board[i + self.__CONNECT_NUMBER - 1 - x][j + x] == self.change_turn(player_id):
                        possible = False
                        break
                if possible:
                    value += 1
                if num_you == self.__CONNECT_NUMBER:
                    value = big_number
        return value
    
    
    def max_value(self, state, current_depth, a, b):
        if current_depth == Depth-1:
            value = -1*big_number
            for i in range(len(state.get_child())):
                value = max(value, state.get_child()[i].get_data())
            state.set_data(value)
            return value

        value = -1*big_number
        for i in range(len(state.get_child())):
            value = max(value, self.min_value(state.get_child()[i], current_depth+1, a, b))
            if value>=b:
#                 print('returned max')
                return value
            a = max(a, value)
        state.set_data(value)
        return value
    
    def min_value(self, state, current_depth, a, b):
        if current_depth == Depth-1:
            value = big_number
            for i in range(len(state.get_child())):
                value = min(value, state.get_child()[i].get_data())
            state.set_data(value)
            return value
        
        value = big_number
        for i in range(len(state.get_child())):
            value = min(value, self.max_value(state.get_child()[i], current_depth+1, a, b))
            if value<=a:
#                 print('returned min')
                return value
            b = min(b, value)
        state.set_data(value)
        return value
    
          
    def action(self):
        root = Node()
        root.set_move(2)
        root.set_board(copy.deepcopy(self.board))
        root = self.create_tree(root, 0, YOU)
        max_val = self.max_value(root, 0, -1*big_number, big_number)
        for i in range(len(root.get_child())):
            if max_val == root.get_child()[i].get_data():
                return root.get_child()[i].get_move()


# ## Main Code

# In[10]:


class ConnectSin:
    YOU = 1
    CPU = -1
    EMPTY = 0
    DRAW = 0
    __CONNECT_NUMBER = 4
    board = None

    def __init__(self, board_size=(6, 7), silent=False):
        """
        The main class for the connect4 game
        Inputs
        ----------
        board_size : a tuple representing the board size in format: (rows, columns)
        silent     : whether the game prints outputs or not
        """
        assert len(board_size) == 2, "board size should be a 1*2 tuple"
        assert board_size[0] > 4 and board_size[1] > 4, "board size should be at least 5*5"

        self.columns = board_size[1]
        self.rows = board_size[0]
        self.silent = silent
        self.board_size = self.rows * self.columns

    def run(self, starter=None):
        """
        runs the game!

        Inputs
        ----------
        starter : either -1,1 or None. -1 if cpu starts the game, 1 if you start the game. None if you want the starter
            to be assigned randomly 

        Output
        ----------
        (int) either 1,0,-1. 1 meaning you have won, -1 meaning the player has won and 0 means that the game has drawn
        """
        if (not starter):
            starter = self.__get_random_starter()
        assert starter in [self.YOU, self.CPU], "starter value can only be 1,-1 or None"
        
        self.__init_board()
        turns_played = 0
        current_player = starter
        while(turns_played < self.board_size):
            
            if (current_player == self.YOU):
                self.__print_board()
                player_input = self.get_your_input()
            elif (current_player == self.CPU):
                player_input = self.__get_cpu_input()
            else:
                raise Exception("A problem has happend! contact no one, there is no fix!")
            if (not self.register_input(player_input, current_player)):
                self.__print("this move is invalid!")
                continue
            current_player = self.__change_turn(current_player)
            potential_winner = self.check_for_winners()
            turns_played += 1
            if (potential_winner != 0):
                self.__print_board()
                self.__print_winner_message(potential_winner)
                return potential_winner
        self.__print_board()
        self.__print("The game has ended in a draw!")
        return self.DRAW

    def get_your_input(self):
#         print(555555555555555555555555555555555555555555555555555)
        Board = copy.deepcopy(self.board)
#         Board
#         print(Board)
#         bb = np.array(Board)
#         print(bb.shape)
        my_bot = My_Bot(Board)
        return my_bot.action()
        #TODO: complete here
#         raise NotImplementedError
        
    def check_for_winners(self):
        """
        checks if anyone has won in this position

        Output
        ----------
        (int) either 1,0,-1. 1 meaning you have won, -1 meaning the player has won and 0 means that nothing has happened
        """
        have_you_won = self.check_if_player_has_won(self.YOU)
        if have_you_won:
            return self.YOU
        has_cpu_won = self.check_if_player_has_won(self.CPU)
        if has_cpu_won:
            return self.CPU
        return self.EMPTY

    def check_if_player_has_won(self, player_id):
        """
        checks if player with player_id has won

        Inputs
        ----------
        player_id : the id for the player to check

        Output
        ----------
        (boolean) true if the player has won in this position
        """
        return (
            self.__has_player_won_diagonally(player_id)
            or self.__has_player_won_horizentally(player_id)
            or self.__has_player_won_vertically(player_id)
        )
    
    def is_move_valid(self, move):
        """
        checks if this move can be played

        Inputs
        ----------
        move : the column to place a piece in, in range [1, column count]

        Output
        ----------
        (boolean) true if the move can be played
        """

        if (move < 1 or move > self.columns):
            return False
        column_index = move - 1
        return self.board[0][column_index] == 0
    
    def get_possible_moves(self):
        """
        returns a list of possible moves for the next move

        Output
        ----------
        (list) a list of numbers of columns that a piece can be placed in
        """
        possible_moves = []
        for i in range(self.columns):
            move = i + 1
            if (self.is_move_valid(move)):
                possible_moves.append(move)
        return possible_moves
    
    def register_input(self, player_input, current_player):
        """
        registers move to board, remember that this function changes the board

        Inputs
        ----------
        player_input : the column to place a piece in, in range [1, column count]
        current_player: ID of the current player, either self.YOU or self.CPU

        """
#         print(s)
        if (not self.is_move_valid(player_input)):
            return False
        self.__drop_piece_in_column(player_input, current_player)
        return True

    def __init_board(self):
        self.board = []
        for i in range(self.rows):
            self.board.append([self.EMPTY] * self.columns)

    def __print(self, message: str):
        if not self.silent:
            print(message)

    def __has_player_won_horizentally(self, player_id):
        for i in range(self.rows):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __has_player_won_vertically(self, player_id):
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + x][j] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __has_player_won_diagonally(self, player_id):
        for i in range(self.rows - self.__CONNECT_NUMBER + 1):
            for j in range(self.columns - self.__CONNECT_NUMBER + 1):
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + x][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
                has_won = True
                for x in range(self.__CONNECT_NUMBER):
                    if self.board[i + self.__CONNECT_NUMBER - 1 - x][j + x] != player_id:
                        has_won = False
                        break
                if has_won:
                    return True
        return False

    def __get_random_starter(self):
        players = [self.YOU, self.CPU]
        return players[int(random() * len(players))]
    
    def __get_cpu_input(self):
        """
        This is where clean code goes to die.
        """
        bb = copy.deepcopy(self.board)
        pm = self.get_possible_moves()
        for m in pm:
            self.register_input(m, self.CPU)
            if (self.check_if_player_has_won(self.CPU)):
                self.board = bb
                return m
            self.board = copy.deepcopy(bb)
        if (self.is_move_valid((self.columns // 2) + 1)):
            c = 0
            cl = (self.columns // 2) + 1
            for x in range(self.rows):
                if (self.board[x][cl] == self.CPU):
                    c += 1
            if (random() < 0.65):
                return cl
        return pm[int(random() * len(pm))]
    
    def __drop_piece_in_column(self, move, current_player):
        last_empty_space = 0
        column_index = move - 1
        for i in range(self.rows):
            if (self.board[i][column_index] == 0):
                last_empty_space = i
        self.board[last_empty_space][column_index] = current_player
        return True
        
    def __print_winner_message(self, winner):
        if (winner == self.YOU):
            self.__print("congrats! you have won!")
        else:
            self.__print("gg. CPU has won!")
    
    def __change_turn(self, turn):
        if (turn == self.YOU): 
            return self.CPU
        else:
            return self.YOU

    def __print_board(self):
        if (self.silent): return
        print("Y: you, C: CPU")
        for i in range(self.rows):
            for j in range(self.columns):
                house_char = "O"
                if (self.board[i][j] == self.YOU):
                    house_char = "Y"
                elif (self.board[i][j] == self.CPU):
                    house_char = "C"
                    
                print(f"{house_char}", end=" ")
            print()
            


# In[11]:


board_sizes_to_check = [(6,7), 
                        (7,8), 
                        (7,10)]
# game = ConnectSin(board_size=(6,7), silent=True)

# a = game.run()


# ## 6*7 Map Depth 1 and 3
# 

# In[24]:


Depth_list = [1,3]
for j in range(len(Depth_list)):
    Depth = Depth_list[j]
    you_wone = 0
    cpu_wone = 0
    start = time()
    for r in range(200):
        print('round:', r)
        game = ConnectSin(board_size=board_sizes_to_check[0], silent=True)
        result = game.run()
        if result == 1:
            you_wone += 1
        if result == -1:
            cpu_wone += 1
    end = time()
    print('Depth:', Depth)
    print('time:', end-start, 's')
    print('winning percentage:', you_wone/(you_wone+cpu_wone)*100,"%")
    print(' ')


# ## 7*8 Map

# In[17]:


Depth_list = [1,3]
for j in range(len(Depth_list)):
    Depth = Depth_list[j]
    you_wone = 0
    cpu_wone = 0
    start = time()
    for _ in range(200):
        game = ConnectSin(board_size=board_sizes_to_check[1], silent=True)
        result = game.run()
        if result == 1:
            you_wone += 1
        if result == -1:
            cpu_wone += 1
    end = time()
    print('Depth:', Depth)
    print('time:', end-start, 's')
    print('winning percentage:', you_wone/(you_wone+cpu_wone)*100,"%")
    print(' ')


# ## 7*10 Map

# In[21]:


Depth_list = [1,3]
for j in range(len(Depth_list)):
    Depth = Depth_list[j]
    you_wone = 0
    cpu_wone = 0
    start = time()
    for _ in range(200):
        game = ConnectSin(board_size=board_sizes_to_check[2], silent=True)
        result = game.run()
        if result == 1:
            you_wone += 1
        if result == -1:
            cpu_wone += 1
    end = time()
    print('Depth:', Depth)
    print('time:', end-start, 's')
    print('winning percentage:', you_wone/(you_wone+cpu_wone)*100,"%")
    print(' ')

