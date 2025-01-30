#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""The Royal Game of Ur, by Faarah"""


import random
import sys

X_PLAYER = 'X'
O_PLAYER = 'O'
EMPTY = ' '

X_HOME = 'x_home'
O_HOME = 'o_home'
X_GOAL = 'x_goal'
O_GOAL = 'o_goal'

ALL_SPACES = 'hgfetsijklmnopdcbarq'
X_TRACK = 'HefghijklmnopstG'  # H stands for Home, G stands for Goal
O_TRACK = 'HabcdijklmnopqrG'

FLOWER_SPACES = ('h', 't', 'l', 'd', 'r')

# Board template for display
BOARD_TEMPLATE = """
                    {}                 {}
                    Home              Goal 
                     v                 ^
                      
+-----+-----+-----+--v--+           +--^--+-----+  
|*****|     |     |     |           |*****|     |
|*{}  *<  {}   < {}  <  {}  |           |* {} *<  {} |
|****h|    g|    f|    e|           |****t|    s|
+--v--+-----+-----+-----+-----+-----+-----+--^--+ 
|     |     |     |*****|     |     |     |     |
| {}   >  {}  >  {}  >* {} *>  {}  >  {}  >  {}  > {} |
|    i|    j|    k|****l|    m|    n|    o|    p|
+-----+-----+-----+-----+-----+-----+-----+-----+
|*****|     |     |     |           |*****|     |
|*{}  *<  {}   < {}  <  {}  |           |* {} *<  {} |
|****d|    c|    b|    a|           |****r|    q|
+-----+-----+-----+--^--+-----+-----+--v--+--^--+                    
                     ^                 v
                   Home              Goal
                    {}                 {}
"""

# Main game logic
def main():
    print("The Royal Game of Ur, by Faarah")
    input('Press Enter to begin...')

    gameBoard = getNewBoard()
    turn = O_PLAYER

    while True:
        # Determine the current player's setup
        if turn == X_PLAYER:
            opponent = O_PLAYER
            home, track, goal, opponentHome = X_HOME, X_TRACK, X_GOAL, O_HOME
        else:
            opponent = X_PLAYER
            home, track, goal, opponentHome = O_HOME, O_TRACK, O_GOAL, X_HOME

        displayBoard(gameBoard)

        input(f"It is {turn}'s turn. Press Enter to flip...")

        # Flip dice and calculate flips
        flipTally = 0
        print('Flips: ', end='')
        for i in range(4):
            result = random.randint(0, 1)
            print('H' if result == 1 else 'T', end='-' if i != 3 else '')
            flipTally += result
        print()

        if flipTally == 0:
            input('You lose a turn. Press Enter to continue...')
            turn = opponent
            continue

        validMoves = getValidMoves(gameBoard, turn, flipTally)

        if not validMoves:
            input('No possible moves. Press Enter to continue...')
            turn = opponent
            continue

        # Ask the player to choose a move
        while True:
            print(f'Select move {flipTally} spaces: ', end='')
            print(' '.join(validMoves) + ' quit')
            move = input('> ').lower()

            if move == 'quit':
                print('Thanks for playing!')
                sys.exit()
            if move in validMoves:
                break

            print('That is not a valid move.')

        # Process the move
        if move == 'home':
            gameBoard[home] -= 1
            nextTrackSpaceIndex = flipTally
        else:
            gameBoard[move] = EMPTY
            nextTrackSpaceIndex = track.index(move) + flipTally

        movingOntoGoal = nextTrackSpaceIndex == len(track) - 1
        if movingOntoGoal:
            gameBoard[goal] += 1
            if gameBoard[goal] == 7:
                displayBoard(gameBoard)
                print(f'{turn} has won the game!')
                print('Thanks for playing!')
                sys.exit()
        else:
            nextBoardSpace = track[nextTrackSpaceIndex]

            if gameBoard[nextBoardSpace] == opponent:
                gameBoard[opponentHome] += 1

            gameBoard[nextBoardSpace] = turn

            if nextBoardSpace in FLOWER_SPACES:
                print(f'{turn} landed on a flower space and goes again.')
                input('Press Enter to continue...')
            else:
                turn = opponent


# Create a new game board
def getNewBoard():
    board = {X_HOME: 7, X_GOAL: 0, O_HOME: 7, O_GOAL: 0}
    for spaceLabel in ALL_SPACES:
        board[spaceLabel] = EMPTY
    return board


# Display the current board state
def displayBoard(board):
    print('\n' * 60)
    xHomeTokens = ('X' * board[X_HOME]).ljust(7, '.')
    xGoalTokens = ('X' * board[X_GOAL]).ljust(7, '.')
    oHomeTokens = ('O' * board[O_HOME]).ljust(7, '.')
    oGoalTokens = ('O' * board[O_GOAL]).ljust(7, '.')

    spaces = []
    spaces.append(xHomeTokens)
    spaces.append(xGoalTokens)
    for spaceLabel in ALL_SPACES:
        spaces.append(board[spaceLabel])
    spaces.append(oHomeTokens)
    spaces.append(oGoalTokens)

    print(BOARD_TEMPLATE.format(*spaces))


# Determine valid moves for a player
def getValidMoves(board, player, flipTally):
    validMoves = []

    if player == X_PLAYER:
        opponent, track, home = O_PLAYER, X_TRACK, X_HOME
    else:
        opponent, track, home = X_PLAYER, O_TRACK, O_HOME

    if board[home] > 0 and board[track[flipTally]] == EMPTY:
        validMoves.append('home')

    for trackSpaceIndex, space in enumerate(track):
        if space in ('H', 'G') or board[space] != player:
            continue
        nextTrackSpaceIndex = trackSpaceIndex + flipTally
        if nextTrackSpaceIndex >= len(track):
            continue
        nextBoardSpaceKey = track[nextTrackSpaceIndex]
        if nextBoardSpaceKey == 'G' or board[nextBoardSpaceKey] in (EMPTY, opponent):
            validMoves.append(space)

    return validMoves


# Start the game
if __name__ == '__main__':
    main()




