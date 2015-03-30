"""Logic funtions for 2048 Tkinter program"""
from random import choice

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


def new_game():
    """Generates a 2048 board
    -Runs rand_tile twice on an empty board"""
    return rand_tile(rand_tile([[0, 0, 0, 0], [0, 0, 0, 0],
                                [0, 0, 0, 0], [0, 0, 0, 0]]))

def game_state(mat):
    """Analyze current game state"""
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return 'win'
    for i in range(len(mat)-1):
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return 'not over'
    for i in range(len(mat)): #check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    for k in range(len(mat)-1): #to check the left/right entries on the last row
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1): #check up/down entries on last column
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'


def right(state):
    """Shift state right
    -Other move methods are based on the move right method"""
    start = state
    new = []
    changed = True
    for row in state:
        new_row = []
        new_row.append([tile for tile in row if tile != 0])
        new.append([0]*(4-len(new_row[0]))+new_row[0])
    state = []
    for row in new:
        for i in range(2, -1, -1):
            if row[i] == row[i+1]:
                row[i+1] = row[i]*2
                row[i] = 0
        state.append(row)
    new = []
    for row in state:
        new_row = []
        new_row.append([tile for tile in row if tile != 0])
        new.append([0]*(4-len(new_row[0]))+new_row[0])
    if start == new:
        changed = False
    return (new, changed)


def left(state):
    """Shifts state to the left
    -Runs move right in reverse"""
    new_state = right([row[::-1] for row in state])
    return ([row[::-1] for row in new_state[0]], new_state[1])


def up(state):
    """Shifts state to up
    -Runs move right with state turned 90 degrees clockwise"""
    new_state = []
    for i in range(4):
        new_row = []
        for row in state:
            new_row.append(row[i])
        new_state.append(new_row[::-1])

    new_state = right(new_state)
    new_state, changed = new_state[0], new_state[1]

    if not new_state:
        return False
    state = []
    for i in range(3, -1, -1):
        new_row = []
        for row in new_state:
            new_row.append(row[i])
        state.append(new_row)
    return (state, changed)


def down(state):
    """Shifts state to down
    -Runs move right with state turned 90 degrees counter-clockwise"""
    new_state = []
    for i in range(4):
        new_row = []
        for row in state:
            new_row.append(row[i])
        new_state.append(new_row[::-1])

    new_state = left(new_state)
    new_state, changed = new_state[0], new_state[1]

    if not new_state:
        return False
    state = []
    for i in range(3, -1, -1):
        new_row = []
        for row in new_state:
            new_row.append(row[i])
        state.append(new_row)
    return (state, changed)
