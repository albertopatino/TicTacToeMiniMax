#!/usr/bin/python3
import tkinter as tk
# import tkinter.ttk as ttk
import tkinter.messagebox
#import random

class Node:
    def __init__(self):

        self.pos = 0
        self.value = 0


class TicTacToe(tk.Frame):
    calls = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.board = [' '] * 9
        self.x = self.o = 0 # 000000000 bitmask
        self.space_image = tk.PhotoImage(file='square.gif')
        # self.space_image = tk.PhotoImage(Image.open('square.jpg'))
        self.x_image = tk.PhotoImage(file='x.gif')
        self.o_image = tk.PhotoImage(file='o.gif')
        self.buttons = []
        i = 0
        for x in range(3):
            for y in range(3):
                #self.btn = tk.Button(master, command=lambda loc=i: self.button_pressed(loc))
                self.btn = tk.Button(master, command=lambda i=i: self.button_pressed(i))
                #self.btn.image = self.space_image
                self.btn.configure(image=self.space_image)
                self.btn.grid(row=x, column=y)
                
                self.buttons.append(self.btn)
                i += 1
                # print(i, x, y, len(self.buttons))
        # self.board.filter()

    def button_pressed(self, i):
        # play_human
        print("Human touches: ", i)
        if not self.x_is_available(i):
            return

        print("Board:", self.board)
        if test_winner(self.x):
            self.display_about_message_box("Ganaste Humano!!!!")
            self.reset_game()
            return

        if test_draw(self.board):
            self.display_about_message_box("This is a draw!!! ")
            self.reset_game()
            return

        self.play_computer_ai()

    def play_computer_ai(self):
        
        pos, value = self.minimaxv2(self.board, 'O')

        # print("ai pos =", pos, value)
        self.o_is_available(pos)
        print("Board:", self.board)
        print("Calls: ", self.calls)

        self.calls = 0
        if test_winner(self.o):
            self.display_about_message_box("O Winner! ")
            self.reset_game()

    def set_o(self, i):
        self.board[i] = 'O'
        self.buttons[i].configure(image=self.o_image)
        self.o |= 1 << (8 - i)

    def set_x(self, i):
        self.board[i] = 'X'
        self.buttons[i].configure(image=self.x_image)
        self.x |= 1 << (8 - i)

    def o_is_available(self, i):
        if self.board[i] == ' ':
            self.set_o(i)
            return True
        return False

    def x_is_available(self, i):
        if self.board[i] == ' ':
            self.set_x(i)
            return True
        return False

    def display_about_message_box(self, message):
        tkinter.messagebox.showinfo(
            "About", "{}{}".format("RESULT: ", message, parent=self.master))

    def reset_game(self):
        self.board = [' '] * 9
        self.x = 0
        self.o = 0
        i = 0
        for x in range(3):
            for y in range(3):
                self.buttons[i].configure(image=self.space_image)
                i += 1

    def minimaxv2(self, new_board, player):
        # Check terminal
        # max depth 9
        self.calls += 1
        # print(new_board)

        if test_winner2(new_board, 'X'):
            return -1, -1
        if test_winner2(new_board, 'O'):
            return -1, 1
        if test_draw(new_board):
            return -1, 0

        nodes = []
        i = 0
        for x in range(3):
            for y in range(3):
                if new_board[i] == ' ':
                    node = Node()
                    node.pos = i
                    nodes.append(node)
                i += 1

        if player == 'O':
            best_value = -10
            for node in nodes:
                new_board[node.pos] = player
                t_pos, t_value = self.minimaxv2(new_board, 'X')
                new_board[node.pos] = ' '
                if t_value > best_value:
                    best_value = t_value
                    best_node = node
                    best_node.value = t_value
        else:
            best_value = 10
            for node in nodes:
                new_board[node.pos] = player
                t_pos, t_value = self.minimaxv2(new_board, 'O')
                new_board[node.pos] = ' '
                if t_value < best_value:
                    best_value = t_value
                    best_node = node
                    best_node.value = t_value

        return best_node.pos, best_node.value

# def mmalphabeta(self, board, alpha, beta, player):


def test_winner(v):
    # Test horizontal
    if v & 448 == 448 or v & 56 == 56 or v & 7 == 7:
        return True
    # Test vertical
    if v & 292 == 292 or v & 146 == 146 or v & 73 == 73:
        return True
    # Test diagonal
    if v & 273 == 273 or v & 84 == 84:
        return True
    return False


def test_winner2(board, player):
    value = 0
    i = 0
    for x in range(3):
        for y in range(3):
            if board[i] == player:
                value |= 1 << (8 - i)
            i += 1

    if test_winner(value):
        return True
    return False


def test_draw(board):
    i = 0
    for x in range(3):
        for y in range(3):
            if board[i] == ' ':
                return False
            i += 1
    return True


if __name__ == '__main__':
    p = TicTacToe()
    p.master.mainloop()
