import random
import copy

EMPTY = '.'
N = 1000  # number of simulations

# main() is the game loop
def main():
    b = game_board()
    output(b)
    play_game(b)

# The following sets up 6x7 game grid / display representation
def game_board():
    b = [[EMPTY for i in range(7)] for j in range(7)]
    for i in range(len(b)):
        b[i].insert(0, ' ')
    b[0] = ' 1234567'
    return b

def full(b):
    return not EMPTY in b[6]

def column_full(b, col):
    return b[6][col] != EMPTY

# Output() formats our game_board "grid" into an easy-to-read board and display it on python window
def output(b):
    for i in range(6, -1, -1):
        print ' '.join(b[i])

def play_game(b):
    turn = 0
    res = ''
    while True:
        turn += 1
        print ''
        if turn % 2 == 0:
            symbol = 'X'
            user_move(b, symbol)
        else:
            symbol = 'O'
            pc_move(b, symbol)
        if winner(b, symbol):
            res = symbol + ' win!'
            break
        if full(b):
            res = 'Draw Game.'
            break
    print res

# user_move attempts to place a chip into the game_board by modifying the variable grid
def user_move(b, s):
    col = int(raw_input('Your move: '))
    placement(b, col, s)
    output(b)

# pc move should run a simulation (option to choose between MonteCarlo() or AI())
# that takes the present state of the game_board "grid" as argument and return column
def pc_move(b, s):
    col,result = monte_carlo(b)
    placement(b, col, s)
    print 'Computer move: ' + str(col) + ' ' + str(result)
    output(b)

# placement() examines the validity of the move that the pc or the player make,
# if it's valid, modify grid to perform the equivalent of dropping the chip into the column
def placement(b, col, s):
    row = 1
    while row < len(b):
        if b[row][col] == EMPTY:
            b[row][col] = s
            break
        row += 1

# returns best column
def monte_carlo(b):
    d = {}
    for col in range(1, 8):
        if not column_full(b, col):
            d[col] = column_sim(b, col) - N
    return best_option(d),d

# returns column with best score
def best_option(d):
    wins = 0
    col = 1
    for key in d:
        if d[key] > wins:
            wins = d[key]
            col = key
    return col

# returns wins - losses for col
def column_sim(grid, col):
    pc1, pc2 = 'O', 'X'
    wins = N
    w = -1
    temp = copy.deepcopy(grid)  # Makes a deep copy of the array grid
    placement(temp, col, pc1)  # pc1 goes first, always placing the chip in the assigned input_column
    for i in range(N):
        b = copy.deepcopy(temp)  # Makes another deep copy of modified board
        while True:
            sim_move(b, pc2)
            if winner(b, pc2):
                wins += w
                break
            if full(b):
                break
            pc1,pc2 = pc2,pc1
            w = -w
    return wins

def sim_move(b, s):
    while True:
        column = random.randint(1, 7)
        if not column_full(b, column):
            placement(b, column, s)
            break

# checks if there are 4 symbols in a row in the 4 directions
def winner(b, s):
    return check(1,6,1,4,b,s,0,1) or check(1,3,1,7,b,s,1,0) or check(1,3,1,4,b,s,1,1) or check(1,3,4,7,b,s,1,-1)

def check(r1,r2,c1,c2,b,s,dr,dc):
    for r in range(r1,r2):
        for c in range(c1,c2):
            if b[r][c] == s and b[r+dr][c+dc] == s and b[r+2*dr][c+2*dc] == s and b[r+3*dr][c+3*dc] == s:
                return True
    return False

main()
