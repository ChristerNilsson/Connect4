import random
import copy

EMPTY = '.'
N = 1000  # number of simulations


#main() is the game loop
def main():
    who_go_first = 'yes'
    grid = game_board()
    output(grid)
    play_game(grid, who_go_first)


#The following sets up 6x7 game grid / display representation
def game_board():
    grid = [[EMPTY for i in range(7)] for j in range(7)]
    for i in range(len(grid)):
        grid[i].insert(0, ' ')
    grid[0] = ' 1234567'
    return grid


def column_full(gb, col):
    return gb[6][col] != EMPTY


#Output() formats our game_board "grid" into an easy-to-read board and display it on python window
def output(game_board):
    for i in range(6, -1, -1):
        print ' '.join(game_board[i])


def play_game(game_board, who_go_first):
    player_symbol = 'X'
    pc_symbol = 'O'
    if who_go_first == '':
        turn = 0
    else:
        turn = -1
    while True:  # if player choose to go first, then turn counts up from 1. If pc goes first, turn counts up from 0
        if turn % 2 == 0:
            turn += 1
            print ''
            print 'Turn #' + str(turn) + '. It is now your turn.'
            user_move(game_board, player_symbol)
            if end_game(game_board, player_symbol):
                print 'Thanks for playing, you have won!'
                break
            elif end_game(game_board, player_symbol) == -1:
                print 'Draw Game. Thanks for playing'
                break
        if turn % 2 != 0:
            turn += 1
            print ''
            print 'Turn #' + str(turn) + '. It is now pc turn.'
            pc_move(game_board, pc_symbol)
            if end_game(game_board, pc_symbol):
                print 'Thanks for playing, the pc had won!'
                break
            elif end_game(game_board, pc_symbol) == -1:
                print 'Draw Game. Thanks for playing'
                break


#usermove attempts to place a chip into the game_board by modifying the variable grid
def user_move(game_board, player_symbol):
    legal_move = False
    while not legal_move:
        column = int(raw_input('Which column would you like to place the chip in?'))
        if column_full(game_board, column):
            print 'YOUR PLACED THE CHIP IN AN INVALID POSITION'
            legal_move = False
        else:
            placement(game_board, column, player_symbol)
            legal_move = True
    output(game_board)


# pc move should run a simulation (option to choose between MonteCarlo() or AI())
# that takes the present state of the game_board "grid" as argument and return column
def pc_move(game_board, pc_symbol):
    legal_move = False
    while not legal_move:
        try:
            column = monte_carlo(game_board)
            placement(game_board, column, pc_symbol)
            legal_move = True
        except IndexError:
            legal_move = False
    output(game_board)
    print 'The computer has placed a chip in column ' + str(column) + '.'


# placement() examines the validity of the move that the pc or the player make,
# if it's valid, modify grid to perform the equivalent of dropping the chip into the column
def placement(game_board, column, symbol):
    empty = EMPTY
    row = 1
    while row < len(game_board):
        if game_board[row][column] == empty:
            game_board[row][column] = symbol
            break
        elif row == len(game_board) - 1:
            raise IndexError('Column already filled')
        row += 1


#simulation MonteCarlo, its expected behavior is to perform the simulation in the way the project description had asked.
def monte_carlo(game_board):
    d = dict()
    print 'Calculating...'
    for col in range(1, 8):
        if column_full(game_board, col):
            d[col] = -1
        else:
            d[col] = column_sim(game_board, col)
    print 'Result:', d
    print 'The best column placement for pc is', best_option(d)
    print ''
    return best_option(d)


# BestOption() to be used by MonteCarlo()
def best_option(d):
    wins = 0
    column = 1
    for key in d:
        if d[key] > wins:
            wins = d[key]
            column = key
    return column


def column_sim(grid, input_column):
    # print 'Calculating winninghood for column#', inputcolumn
    pc1 = 'O'
    pc2 = 'X'
    wins = 0
    temp = copy.deepcopy(grid)  # Makes a deep copy of the array grid
    placement(temp, input_column, pc1)  # pc1 goes first, always placing the chip in the assigned inputcolumn
    i = 0
    # the follow code plays out the remaining of the game in complete randomness
    while i < N:
        copy_board = copy.deepcopy(temp)  # Makes another deep copy of modified gameboard
        while True:
            sim_move(copy_board, pc2)
            if end_game(copy_board, pc2) == True or end_game(copy_board, pc2) == -1: #losing to pc2
                break

            sim_move(copy_board, pc1)
            if end_game(copy_board, pc1) == True or end_game(copy_board, pc1) == -1: #victory by pc1
                wins += 1
                break
        i += 1
    return wins


def sim_move(game_board, symbol):
    while True:
        column = random.randint(1, 7)
        if not column_full(game_board, column):
            placement(game_board, column, symbol)
            break


# end_game basically checks for whether there are 4 symbols in a row in the 4 directions
def end_game(game_board, symbol):

    if horizontal(game_board, symbol):
        return True

    if vertical(game_board, symbol):
        return True

    if left_diagonal(game_board, symbol):
        return True

    if right_diagonal(game_board, symbol):
        return True

    #Checks if the game board is all filled
    for row in [1, 2, 3, 4, 5, 6]:
        if EMPTY in game_board[row]:
            return 0
    return -1


def horizontal(b,s):
    for r in [1, 2, 3, 4, 5, 6]:
        for c in [1, 2, 3, 4]:
            if b[r][c] == s and b[r][c+1] == s and b[r][c+2] == s and b[r][c+3] == s:
                return True
    return False


def vertical(b,s):
    for r in [1, 2, 3]:
        for c in [1, 2, 3, 4, 5, 6, 7]:
            if b[r][c] == s and b[r+1][c] == s and b[r+2][c] == s and b[r+3][c] == s:
                return True
    return False


def left_diagonal(b,s):
    for i in [1, 2, 3]:
        for j in [1, 2, 3, 4]:
            if b[i][j] == s and b[i+1][j+1] == s and b[i+2][j+2] == s and b[i+3][j+3] == s:
                return True
    return False


def right_diagonal(b,s):
    for i in [1, 2, 3]:
        for j in [4, 5, 6, 7]:
            if b[i][j] == s and b[i+1][j-1] == s and b[i+2][j-2] == s and b[i+3][j-3] == s:
                return True
    return False


main()

