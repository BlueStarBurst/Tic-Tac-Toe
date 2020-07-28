import math

def minimax(input, maximizing, player):
    w = checkW(input)

    if w == player:
        #print(input)
        return 1
    elif w == 'tie':
        #print(input)
        return 0
    elif w != player and w != ' ':
        #print(input)
        return -1

    if maximizing:
        turn = player
    else:
        if player == "x":
            turn = "o"
        else:
            turn = "x"

    scores = []

    for i in range(0,3):
        for j in range(0,3):
            if input[i][j] == " ":
                input[i][j] = turn
                scores.append(minimax(input, not maximizing, player))
                input[i][j] = " "

    return max(scores) if maximizing else min(scores)









def checkW(input):
    for r in input:
        if r[0] == r[1] == r[2] and r[0] != ' ':
            return r[0]

    for i in range(0, len(input)):
        if input[0][i] == input[1][i] == input[2][i] and input[0][i] != ' ':
            return input[0][i]

    if input[0][0] == input[1][1] == input[2][2] and input[1][1] != ' ':
        return input[1][1]

    if input[2][0] == input[1][1] == input[0][2] and input[1][1] != ' ':
        return input[1][1]

    for r in input:
        for c in r:
            if c == ' ':
                return ' '

    return 'tie'


def bestMove(input, player):
    bestScore = -math.inf
    move = []
    for i in range(3):
        for j in range(3):
            if input[i][j] == ' ':
                input[i][j] = player
                score = minimax(input, False, player)
                input[i][j] = ' '
                if score > bestScore:
                    bestScore = score
                    move = [i, j]
                #print(f"{i}, {j} - {score}")
    return move

"""
def minimax(input, maximizing, player):

    w = checkW(input)

    if w == player:
        return 1
    if w != player and w != ' ':
        return -1
    if w == 'tie':
        return 0

    thisTurn = ''

    if maximizing:
        thisTurn = player
    else:
        if player == 'x':
            thisTurn = 'o'
        else:
            thisTurn = 'x'

    stuff = []

    for i in range(0,3):
        for j in range(0,3):
            if input[i][j] == ' ':
                input[i][j] = thisTurn
                stuff.append(minimax(input, not maximizing, player))
                input[i][j] = ' '

    if maximizing:
        bestScore = max(stuff)
    else:
        bestScore = min(stuff)

    return bestScore
    
"""


turn = 'x'
board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
x = bestMove(board, turn)
board[x[0]][x[1]] = turn
print(board)

turn = 'o'
x = bestMove(board, turn)
board[x[0]][x[1]] = turn
print(board)
turn = 'x'
x = bestMove(board, turn)
board[x[0]][x[1]] = turn
print(board)
turn = 'o'
x = bestMove(board, turn)
board[x[0]][x[1]] = turn
print(board)



