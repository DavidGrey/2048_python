"""
The MIT License (MIT)
Copyright (c) 2015 David Greydanus
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Created on Oct 25, 2014

@author: DavidGrey

>>>Text based implementation of 2048 made for the Python 2.7 CLI<<<
"""
import sys
from random import choice
from msvcrt import getwch

class Move(object):
    """Class for shifting 2048 states in any given direction.
      Format for use: Move(state).direction()
      Methods(up, down, left, right"""
    def __init__(self, state):
        self.state = state

    def shift_right(self):
        """Shift state right
        -Other move methods are based on the move right method"""
        start = self.state
        new = []
        for row in self.state:
            new_row = []
            new_row.append([tile for tile in row if tile != 0])
            new.append([0]*(4-len(new_row[0]))+new_row[0])
        self.state = []
        for row in new:
            for i in range(2, -1, -1):
                if row[i] == row[i+1]:
                    row[i+1] = row[i]*2
                    row[i] = 0
            self.state.append(row)
        new = []
        for row in self.state:
            new_row = []
            new_row.append([tile for tile in row if tile != 0])
            new.append([0]*(4-len(new_row[0]))+new_row[0])
        if start == new:
            return False
        else:
            return new


    def shift_left(self):
        """Shifts state to the left
        -Runs move right in reverse"""
        new_state = Move([row[::-1] for row in self.state]).shift_right()
        if new_state:
            return [row[::-1] for row in new_state]
        else:
            return False


    def shift_up(self):
        """Shifts state to up
        -Runs move right with state turned 90 degrees clockwise"""
        new_state = []
        for i in range(4):
            new_row = []
            for row in self.state:
                new_row.append(row[i])
            new_state.append(new_row[::-1])

        new_state = Move(new_state).shift_right()
        if not new_state:
            return False
        self.state = []
        for i in range(3, -1, -1):
            new_row = []
            for row in new_state:
                new_row.append(row[i])
            self.state.append(new_row)
        return self.state


    def shift_down(self):
        """Shifts state to down
        -Runs move right with state turned 90 degrees counter-clockwise"""
        new_state = []
        for i in range(4):
            new_state.append([row[i] for row in self.state][::-1])

        new_state = Move(new_state).shift_left()

        if not new_state:
            return False
        self.state = []
        for i in range(3, -1, -1):
            self.state.append([row[i] for row in new_state])
        return self.state


def rand_tile(state):
    """Takes a 2048 state as input, randomly places a tile on,
    and returns the updated state
    -The spawned tile has a 90% chance of spawning as a 2,
    and a 10% chance of spawning as a 4"""
    zeros = []
    for row in range(4):
        for tile in range(4):
            if state[row][tile] == 0:
                zeros.append((row, tile))
    spawn = choice(zeros)
    state[spawn[0]][spawn[1]] = choice([2]*9+[4])
    return state


def make_board():
    """Generates a 2048 board
    -Runs rand_tile twice on an empty board"""
    return rand_tile(rand_tile([[0, 0, 0, 0], [0, 0, 0, 0],
                                [0, 0, 0, 0], [0, 0, 0, 0]]))


def board_print(board):
    """Prints the board on 4 separate lines
    -makes it look readable"""
    print '\n'*20
    for row in board:
        nrow = '|'
        for i in row:
            if i != 0:
                nrow += str(i) + ' |'
            else:
                nrow += '__|'
        print nrow


def main():
    """Runs game until player cannot make a legal move"""
    board = make_board()
    options = {'d':Move(board).shift_right(),
               'a':Move(board).shift_left(),
               'w':Move(board).shift_up(),
               's':Move(board).shift_down()}
    board_print(board)
    print '\n' + 'WASD'
    while any(options.values()):
        moved = False
        while not moved:
            pressed_key = getwch()
            if pressed_key == 'x':
                sys.exit(0)
            elif pressed_key in options:
                if options[pressed_key]:
                    board = rand_tile(options[pressed_key])
                    board_print(board)
                    moved = True
        options = {'d':Move(board).shift_right(),
                   'a':Move(board).shift_left(),
                   'w':Move(board).shift_up(),
                   's':Move(board).shift_down()}
    raw_input("Game Over")


if __name__ == '__main__':
    main()
