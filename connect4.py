import random
import copy

n = 1000 #number of simulations

#main() is the game loop
def main():
    print 'Welcome to Connect Four'
    AI_OPTION, n = initialize()
    whogofirst = raw_input('Would you like to go first? ["Enter" = yes, Anykey = no]:')
    grid = gameboard()
    output(grid)
    playgame(grid, whogofirst, AI_OPTION, n)

def initialize():
    AI_OPTION = raw_input('Please choose a simulation ["Enter" = Monte Carlo, AnyKey = AI]:')
    if AI_OPTION == '':
        while True:
            setting = raw_input('Number of simulations per column? ["Enter" = default(100) or enter an integer]:')
            if setting == '':
                n = 100
                break
            else:
                try:
                    n = int(setting)
                    break
                except:
                    print 'Invalid input'
    else:
        n = 100
    return AI_OPTION, n
            
#The following sets up 6x7 game grid / display representation
def gameboard():
    grid = [ [ ' ' for i in range(7) ] for j in range(7) ]
    for i in range(len(grid)):
        grid[i].insert(0, str(i))
    grid[0] = '01234567'
    return grid    

#Output() formats our gameboard "grid" into an easy-to-read board and display it on python window
def output(gameboard):
    i=6
    while i > -1:
        print ' '.join(gameboard[i])
        i = i-1

def playgame(gameboard, whogofirst, AI_OPTION, n):
    playersymbol = 'X'
    pcsymbol = 'O'
    turn = 0
    if whogofirst == '':
        turn = 0
    else:
        turn = -1
    while True: #Note if player choose to go first, then the turn counts up from 1. If pc goes first, turn counts up from 0
        if turn % 2 == 0:
            turn = turn + 1
            print ''
            print 'Turn #'+str(turn)+'. It is now your turn.'
            usermove(gameboard, playersymbol)
            if endgame(gameboard, playersymbol) == True:
                print 'Thanks for playing, you have won!'
                break
            elif endgame(gameboard, playersymbol) == -1:
                print 'Draw Game. Thanks for playing'
                break
        if turn % 2 != 0:
            turn=turn+1
            print ''
            print 'Turn #'+str(turn)+'. It is now pc turn.'
            pcmove(gameboard, pcsymbol, AI_OPTION,n)
            if endgame(gameboard, pcsymbol) == True:
                print 'Thanks for playing, the pc had won!'
                break
            elif endgame(gameboard, pcsymbol) == -1:
                print 'Draw Game. Thanks for playing'
                break
        
    


#usermove attempts to place a chip into the gameboard by modifying the variable grid
def usermove(gameboard, playersymbol):
    legalmove = False
    while legalmove == False:
        try:
            column = int(raw_input('Which column would you like to place the chip in?'))
            placement(gameboard, column, playersymbol)
            legalmove = True
        except IndexError:
            print 'YOUR PLACED THE CHIP IN AN INVALID POSITION (either column out of range or the chosen column is already filled), TRY AGAIN!'
        except ValueError:
            print 'YOU DID NOT ENTER AN INTEGER TO INDICATE THE COLUMN, TRY AGAIN!'
    output(gameboard)

#pc move should run a simulation (option to choose between MonteCarlo() or AI()) that takes the present state of the gameboard "grid" as argument and return column    
def pcmove(gameboard, pcsymbol, AI_OPTION, n):
    legalmove = False
    while legalmove == False:
        try:
            if AI_OPTION == '':
                column = MonteCarlo(gameboard, n)
            else:
                column = random.randint(1,7) #CHECK FOR ARGUMENT OF AI()
            placement(gameboard, column, pcsymbol)
            legalmove = True
        except IndexError:
            legalmove = False
    output(gameboard)
    print 'The computer has placed a chip in column '+str(column)+'.'
        

#placement() examines the validity of the move that the pc or the player make, if it's valid, modify grid to perform the equivalent of dropping the chip into the column
def placement(gameboard, column, symbol):
    empty = ' '
    row = 1
    while row < len(gameboard):
        if gameboard[row][column] == empty:
            gameboard[row][column] = symbol
            break
        elif row == len(gameboard)-1:
            raise IndexError('Column already filled')
        row=row+1

#simulation MonteCarlo, its expected behavior is to perform the simulaton in the way the project description had asked.
def MonteCarlo(gameboard, n):
    d = dict()
    print 'Calculating...'
    for col in range(1,8):
        d[col] = ColumnSim(gameboard, col, n)
        print '.'
    print 'Result:',d
    print 'The best column placement for pc is', BestOption(d)
    print ''
    return BestOption(d)

# BestOption() to be used by MonteCarlo()
def BestOption(d):
    wins = 0
    column = 1
    for key in d:
        if d[key] > wins:
            wins = d[key]
            column = key
    return column

def ColumnSim(grid, inputcolumn, n):
    #print 'Calculating winninghood for column#', inputcolumn
    pc1 = 'O'
    pc2 = 'X'
    wins = 0
    temp = copy.deepcopy(grid) #Makes a deep copy of the array grid
    placement(temp, inputcolumn, pc1) #pc1 goes first, always placing the chip in the assigned inputcolumn
    i = 0
    #the follow code plays out the remaining of the game in complete randomness
    while i < n:
        copyboard = copy.deepcopy(temp) #Makes another deep copy of modified gameboard (with the placed in the assigned inputcolumn)
        while True:
            SimMove(copyboard, pc2)
            if endgame(copyboard, pc2) == True or endgame(copyboard, pc2) == -1: #losing to pc2
                #output(copyboard)
                #print 'PC1 LOST'
                break
            
            SimMove(copyboard, pc1)
            if endgame(copyboard, pc1) == True or endgame(copyboard, pc1) == -1: #victory by pc1
                #output(copyboard)
                wins = wins + 1
                #print 'Number of wins:', wins
                break
        i = i + 1
#    print 'Wins:', wins
#    print ''
    return wins        

def SimMove(gameboard, symbol):
    while True:
        try:
            column = random.randint(1,7)
            placement(gameboard, column, symbol)
            break
        except:
            pass
#    output(gameboard)

### ColumnSim() to be used by MonteCarlo(); it performs n simulations with each sims begin by placing the chip at column "column", plays out the fullgame at random, and return the number of wins
##def ColumnSim(grid, inputcolumn, n):
##    playersymbol = 'X'
##    pcsymbol = 'O'
##    wins = 0
##    i = 0
##    while i < n:
##        copyboard = copy.deepcopy(grid)
##        option = 0
##        while True:
##            SimMove(copyboard, pcsymbol, inputcolumn, option)
##            if endgame(copyboard, pcsymbol) == True: #sim pc wins
##                wins = wins + 1
##                break
##            elif endgame(copyboard, pcsymbol) == -1: #draw game
##                wins = wins + 0
##                break
##            option = 1
##            SimMove(copyboard, playersymbol, inputcolumn, option)
##            if endgame(copyboard, playersymbol) == True: #sim player wins
##                wins = wins + 0
##                break
##            elif endgame(copyboard, playersymbol) == -1: #draw game
##                wins = wins + 0
##                break
##        i = i + 1
##        output(copyboard)
##    return wins

##def MonteCarlo(gameboard, N):
##    pc1 = 'O'
##    pc2 = 'X'
##    d={1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
##    copyboard = gameboard
##    n=0
##    for i in range(1,8): #fixing the ith column
##        option = 0
##        j = 1
##        while j <= N: #for each column, perform simulation N times.
##            while True: #plays the simulation until one wins
##                play = 0
##                count = 0
##                if option == 0 and play%2==0 : #if this is the first move and it's pc1 turn to move
##                    try:
##                        placement(copyboard, i, pc1)
##                        option = 1
##                    except IndexError:
##                        d[i] = d[i] + 0 #in case the column is given already filled so the first placement is out of bound
##                elif option != 0 and play%2==0: #if not the first move but is pc1's turn
##                    try:
##                        placement(copyboard, random.randint(1,7), pc1)
##                        if endgame(copyboard, pc1) == True:
##                            d[i] = d[i] + 1
##                            #n+=1 #counter of number of total simulations
##                            j=j+1 #pc1 won, move on to j+1 simulation
##                            option = 0
##                            break
##                        elif endgame(copyboard, pc1) == -1:
##                            d[i] = d[i] + 0
##                            j=j+1 #drawgame, move on to next simulation
##                            break
##                    except IndexError:
##                        play = play + 0
##                play = play + 1
##
##                if play % 2 != 0:
##                    try:
##                        placement(copyboard, random.randint(1,7), pc2)
##                        if endgame(copyboard, pc2) == True: #pc2 won
##                            #n+=1
##                            j = j+1
##                            break
##                    except:
##                        play = play + 0
##                play = play + 1
##            output(copyboard)
##    print d
                        

        

#endgame basically checks for whether there are 4 symbols in a row in the 4 directions (horizontal, vertical, left diagonal and right diagonal)
def endgame(gameboard, symbol):
    empty = ' '
    #Checks the horizontal conditions
    H = horizontal_string(gameboard)
    for i in range(len(H)):
        if symbol*4 in H[i]:
            return True

    #Checks the vertical conditions
    V = vertical_string(gameboard)
    for i in range(len(V)):
        if symbol*4 in V[i]:
            return True

    #Checks the right diagonal conditions
    RD = right_diagonal(gameboard)
    for i in range(len(RD)):
        if symbol*4 in RD[i]:
            return True

##    #Checks the left diagonal conditions
##    LD = left_diagonal(gameboard)
##    for i in range(len(LD)):
##        if symbol*4 in LD[i]:
##            return True
##        
    #Checks if the game board is all filled
    row = 1
    while row < len(gameboard):
        if empty in gameboard[row]:
            break
        else:
            row = row + 1
    if row == len(gameboard):
        return -1
    return 0


def horizontal_string(gameboard):
   list_of_rows=[]
   for i in range(1,7):
       list_of_rows.append(''.join(gameboard[i]))       
   return list_of_rows 


def vertical_string(gameboard):
   list_of_columns=[]
   for j in range(1,8):
       pre_list_of_columns=[]
       for i in range(1,7):
           pre_list_of_columns.append(gameboard[i][j])
       x=''.join(pre_list_of_columns)
       list_of_columns.append(x)
   return list_of_columns

def right_diagonal(gameboard):
    list_of_diagonals1=[]
    list_of_diagonals2=[]
    for j in range(7):
        pre_list_diagonals=[]
        for i in range(j+1):
            pre_list_diagonals.append(gameboard[i][j-i])
        x=''.join(pre_list_diagonals)
        list_of_diagonals1.append(x)
    for j in range(1,7):
        pre_list_diagonal=[]
        rightindex=0
        i=j
        while i<7:
            pre_list_diagonal.append(gameboard[i][6-rightindex])
            i=i+1
            rightindex+=1
        x=''.join(pre_list_diagonal)
        list_of_diagonals2.append(x)
    return list_of_diagonals1+list_of_diagonals2
main()


#Things to work on:
#1. implement endgame() check in pcmove(), usermove(), and maybe placement()
#2. complete the coding for ColumnSim
#3. write an AI() simulation
#4. Make a option allowing the choosing of MonteCarlo() or AI()
#5. Return turn = -1 when all rows columns are filled, i.e. '' not in any row column
#6. replace grid variable with gameboard, see to removing gloabl variable in preparation for simulation
