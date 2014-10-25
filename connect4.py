import random
import copy
import time

EMPTY = '.'
X = 'X'
O = 'O'

N = 1000  # number of simulations

# b = board
# col = column


# main() is the game loop
def main():
    print
    b = create_board()
    display_board(b)
    play_game(b)


# The following sets up 6x7 game board. Indices zero are not used for chips.
def create_board():
    b = [[EMPTY for _ in range(7)] for _ in range(7)]
    for i in range(len(b)):
        b[i].insert(0, ' ')
    b[0] = ' 1234567'
    return b


def is_board_full(b):
    return not EMPTY in b[6]


def is_column_full(b, col):
    return b[6][col] != EMPTY


# Output() formats our game_board "grid" into an easy-to-read board and display it on python window
def display_board(b):
    for i in range(6, -1, -1):
        print ' '.join(b[i])


def play_game(b):
    turn = 0
    res = ''
    while True:
        turn += 1
        print ''
        if turn % 2 == 0:
            chip = X
            user_move(b, chip)
        else:
            chip = O
            pc_move(b, chip)
        display_board(b)
        if is_winner(b, chip):
            res = chip + ' win!'
            break
        if is_board_full(b):
            res = 'Draw Game.'
            break
    print res


# asks user for his move and drops the chip
def user_move(b, chip):
    col = int(raw_input('Your move: '))
    drop_chip(b, col, chip)


# finds out best move using monte carlo simulation
def pc_move(b, chip):
    start = time.clock()
    col, result = monte_carlo(b)
    print 'Computer move: ' + str(col) + ' ' + str(result) + ' ' + str(int(1000*(time.clock()-start))) + ' ms'
    drop_chip(b, col, chip)


# drops a chip in a column
def drop_chip(b, col, chip):
    row = 1
    while row < len(b):
        if b[row][col] == EMPTY:
            b[row][col] = chip
            break
        row += 1


# returns best column and statistics
def monte_carlo(b):
    d = {}
    for col in range(1, 8):
        if not is_column_full(b, col):
            d[col] = simulate_column(b, col) - N
    return find_best_column(d), d


# returns column with best score
def find_best_column(d):
    wins = -N-N
    col = 1
    for key in d:
        if d[key] > wins:
            wins = d[key]
            col = key
    return col


# returns wins - losses for col
def simulate_column(board, col):
    chip1, chip2 = O, X
    wins = N
    w = -1
    temp = copy.deepcopy(board)  # Makes a deep copy of the array grid
    drop_chip(temp, col, chip1)  # pc1 goes first, always placing the chip in the assigned input_column
    for i in range(N):
        b = copy.deepcopy(temp)  # Makes another deep copy of modified board
        while True:
            simulate_move(b, chip2)
            if is_winner(b, chip2):
                wins += w
                break
            if is_board_full(b):
                break
            chip1, chip2 = chip2, chip1
            w = -w
    return wins


def simulate_move(b, chip):
    while True:
        col = random.randint(1, 7)
        if not is_column_full(b, col):
            drop_chip(b, col, chip)
            break


# are there 4 symbols in a row in the 4 directions anywhere ?
def is_winner(b, chip):
    return is_4(1,6,1,4,b,chip,0,1) or is_4(1,3,1,7,b,chip,1,0) or is_4(1,3,1,4,b,chip,1,1) or is_4(4,6,1,4,b,chip,-1,1)


def is_4(r1, r2, c1, c2, b, chip, dr, dc):
    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            if b[r][c] == chip and b[r+dr][c+dc] == chip and b[r+2*dr][c+2*dc] == chip and b[r+3*dr][c+3*dc] == chip:
                return True
    return False

main()
