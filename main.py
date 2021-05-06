# ---------------------------------------------------------------------------------------------------------------------
#
#                                                   IMPORTS
#
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
#
#                                                   FUNCTIONS AI
#
# ---------------------------------------------------------------------------------------------------------------------

# ------alpha_beta(board, depth, player, alpha, beta)------
# Arguments :
#   board : list of list - describes the current state of the game
#   depth : int - describes the current depth in the graph (0 is a leaf)
#   alpha : minimum for the max player
#   beta : maximum for the min player
#
# Description :
#   algorithm min max improved with pruning alpha beta
#   recursive algo., simulates all the moves possible for each player, depth first
#   evaluate if the board is to the advantage of the AI or the human on the last move
#   pick the best move
#
# Return value :
#   board advantage if depth is 0 :
#           > 0 : if the board is at the advantage of the AI
#           < 0 : if the board is at the advantage of the human
#           0 : if no one is advantaged
#
#   max or min of all children moves depending at what depth we are

def alpha_beta(board, depth, alpha, beta):
    nb_rows = len(board[0])
    depth_max = 4

    winner, advantage = eval_board(board)
    if depth == 0 or winner is not False:
        return advantage

    else:
        best_row = 0

        for i in range(nb_rows):
            if row_played_check(board, i):

                update_board(board, 1 if depth_max % 2 == depth % 2 else 2, i)
                value_alphabeta = - alpha_beta(board, depth - 1, -beta, -alpha)
                undo_board(board, i)

                if value_alphabeta > alpha:
                    alpha = value_alphabeta
                    best_row = i

                    if alpha >= beta:
                        break

        if depth == depth_max:
            update_board(board, 1, best_row)

        return alpha

# ----------------------------------------------------------------------------------------------------------------------

# ------negmax(board, depth)------
# Arguments :
#   board : list of list - describes the current state of the game
#   depth : int - describes the current depth in the graph (0 is a leaf)
#
# Description :
#   algorithm min max
#   recursive algo., simulates all the moves possible for each player
#   evaluate if the board is to the advantage of the AI or the human on the last move
#   pick the best move
#
# Return value :
#   board advantage if depth is 0 :
#           > 0 : if the board is at the advantage of the AI
#           < 0 : if the board is at the advantage of the human
#           0 : if no one is advantaged
#
#   max or min of all children moves depending at what depth we are


def negmax(board, depth, call_lvl=0):

    nb_rows = len(board[0])

    if depth == 0 or check_winner(board) is not False:
        return eval_board(board)

    else:
        max_eval = - 100000000
        best_row = 0

        for i in range(nb_rows):
            if row_played_check(board, i):
                update_board(board, 1 if call_lvl % 2 == 0 else 2, i)

                value_negmax = - negmax(board, depth - 1, call_lvl=call_lvl + 1)
                if value_negmax > max_eval:
                    max_eval = value_negmax
                    best_row = i

                undo_board(board, i)

        if call_lvl == 0:
            update_board(board, 1, best_row)

        return max_eval

# ----------------------------------------------------------------------------------------------------------------------

# ------check_winner()------
# Arguments :
#   board : list of list - describes the current state of the game
#
# Description :
#   checks for each cell of the board if there is 4 same pieces in a row
#
#   for each cell, checks the 3 next cells to the right, down, diagonally left and diagonally right
#
#   (no need to check the other ways due to the nature of the game [pieces always go to the lowest cell],
#   and how we check it [from the top left corner to the bottom right corner])
#
# Return value :
#   False : if no 4 in a row pieces have been found
#   1 : if 4 in a row pieces have been found for the player 1
#   2 : if 4 in a row pieces have been found for the player 2
#   -1 : if draw


def check_winner(board):
    nb_lines = len(board)
    nb_rows = len(board[0])
    draw = True

    # we gonna check if there are other pieces of player_piece_checked connected to the piece located in board[i][j]
    for i in range(len(board)):
        for j in range(len(board[i])):

            player_piece_checked = board[i][j]

            if player_piece_checked is not None:

                still_checking_down = True
                still_checking_right = True
                still_checking_down_left = True
                still_checking_down_right = True

                for k in range(1, 4):  # k will be used to increment through the board

                    # --------- check down

                    # can't win if the first piece has less than 4 possible other pieces to connect
                    if i <= nb_lines - 4 and still_checking_down:

                        # if we found a cell not of the same nature than player_piece_checked,
                        # we know this not four in a row
                        if board[i + k][j] != player_piece_checked:
                            still_checking_down = False
                        else:
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return player_piece_checked

                    # --------- --------- ---------

                    # --------- check right

                    # can't win if the first piece has less than 4 possible other pieces to connect
                    if j <= nb_rows - 4 and still_checking_right:

                        # if we found a cell not of the same nature than player_piece_checked,
                        # we know this not four in a row
                        if board[i][j + k] != player_piece_checked:
                            still_checking_right = False
                        else:
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return player_piece_checked

                    # --------- --------- ---------

                    # --------- check down left

                    # can't win if the first piece has less than 4 possible other pieces to connect
                    if i <= nb_lines - 4 and j >= 3 and still_checking_down_left:

                        # if we found a cell not of the same nature than player_piece_checked,
                        # we know this not four in a row
                        if board[i + k][j - k] != player_piece_checked:
                            still_checking_down_left = False
                        else:
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                print('down left')
                                return player_piece_checked

                    # --------- --------- ---------

                    # --------- check down right

                    # can't win if the first piece has less than 4 possible other pieces to connect

                    if i <= nb_lines - 4 and j <= nb_rows - 4 and still_checking_down_right:

                        # if we found a cell not of the same nature than player_piece_checked,
                        # we know this not four in a row
                        if board[i + k][j + k] != player_piece_checked:
                            still_checking_down_right = False
                        else:
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                print('down right')
                                return player_piece_checked
            else:

                draw = False

    if draw:
        return -1
    else:
        return False

# ----------------------------------------------------------------------------------------------------------------------

# ------eval_board()------
# Arguments :
#   board : list of list - describes the current state of the game
#
# Description :
#   evaluate the current state of the board
#   check if there is a winner or a draw
#   evaluate if the board is to the advantage of the AI or the human
#
# Return value :
#   tuple (winner, advantage)
#       winner :
#           False : if no 4 in a row pieces have been found
#           1 : if 4 in a row pieces have been found for the player 1
#           2 : if 4 in a row pieces have been found for the player 2
#           -1 : if draw
#
#       advantage :
#           > 0 : if the board is at the advantage of the AI
#           < 0 : if the board is at the advantage of the human
#           0 : if no one is advantaged


def eval_board(board):
    nb_lines = len(board)
    nb_rows = len(board[0])

    max_ai = 0.0
    max_human = 0.0

    i = nb_lines - 1
    while i >= 0:
        for j in range(nb_rows):

            player_piece_checked = board[i][j]

            if player_piece_checked is not None:

                max_up = 1.0
                max_left = 1.0
                max_right = 1.0
                max_down_left = 1.0
                max_down_right = 1.0
                max_up_left = 1.0
                max_up_right = 1.0

                still_checking_up = True
                still_checking_left = True
                still_checking_right = True
                still_checking_down_left = True
                still_checking_down_right = True
                still_checking_up_left = True
                still_checking_up_right = True

                for k in range(1, 4):  # k will be used to increment through the board

                    # --------- check up

                    # no need to evaluate if the first piece has less than 4 possible other pieces to connect
                    if i - 3 >= 0 and still_checking_up:

                        # if we find a cell not of the same nature than player_piece_checked,
                        # we know this not four in a row
                        # if the not-of-the-same-nature cell is a None, there is still a way to
                        # make a 4 in a row on this line
                        # but if it has been countered, there is no more way and it's like we have a solo piece
                        if board[i - k][j] is None:
                            still_checking_up = False
                        elif board[i - k][j] != player_piece_checked:
                            max_up = 1
                            still_checking_up = False
                        else:
                            max_up += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return 4 if player_piece_checked == 1 else -4

                    # --------- --------- ---------

                    # --------- check right

                    # no need to evaluate if the first piece has less than 4 possible other pieces to connect
                    if j + 3 < nb_rows and still_checking_right:

                        # explained before
                        if board[i][j + k] is None:
                            still_checking_right = False

                            # add .2 for each same-nature piece than player_piece_checked
                            # on the same line but not connected yet
                            # make max_right at 1 if there is a not-same-nature piece on the same line
                            if k == 1 or k == 2:
                                for l in range(k + 1, 4):
                                    if board[i][j + l] == (1 if player_piece_checked == 2 else 2):
                                        max_right = 1
                                        break
                                    if board[i][j + l] == player_piece_checked:
                                        max_right += 0.2


                            # remove .1 for each empty cell under the first empty cell
                            # on the right of the connected pieces
                            l = i + 1
                            while l < nb_lines:
                                if board[l][j + k] is None:
                                    max_right -= 0.1
                                else:
                                    break

                                l += 1

                        elif board[i][j + k] != player_piece_checked:
                            max_right = 1
                            still_checking_right = False
                        else:
                            max_right += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return 4 if player_piece_checked == 1 else -4

                    # --------- --------- ---------

                    # --------- check left

                    # no need to evaluate if the first piece has less than 4 possible other pieces to connect
                    if j - 3 >= 0 and still_checking_left:

                        # explained before
                        if board[i][j - k] is None:
                            still_checking_left = False

                            # add .2 for each same-nature piece than player_piece_checked
                            # on the same line but not connected yet
                            # make max_left at 1 if there is a not-same-nature piece on the same line
                            if k == 1 or k == 2:
                                for l in range(k + 1, 4):
                                    if board[i][j - l] == (1 if player_piece_checked == 2 else 2):
                                        max_left = 1
                                        break
                                    if board[i][j - l] == player_piece_checked:
                                        max_left += 0.2

                            # remove .1 for each empty cell under the first empty cell
                            # on the left of the connected pieces
                            l = i + 1
                            while l < nb_lines:
                                if board[l][j - k] is None:
                                    max_left -= 0.1
                                else:
                                    break

                                l += 1

                        elif board[i][j - k] != player_piece_checked:
                            max_left = 1
                            still_checking_left = False
                        else:
                            max_left += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return 4 if player_piece_checked == 1 else -4

                    # --------- --------- ---------

                    # --------- check down left

                    # no need to evaluate if the first piece has less than 4 possible other pieces to connect

                    if i + 3 < nb_lines and j - 3 >= 0 and still_checking_down_left:

                        # explained before
                        if board[i + k][j - k] is None:
                            still_checking_down_left = False

                            # add .2 for each same-nature piece than player_piece_checked
                            # on the same line but not connected yet
                            # make max_down_left at 1 if there is a not-same-nature piece on the same line
                            if k == 1 or k == 2:
                                for l in range(k + 1, 4):
                                    if board[i + l][j - l] == (1 if player_piece_checked == 2 else 2):
                                        max_down_left = 1
                                        break
                                    if board[i + l][j - l] == player_piece_checked:
                                        max_down_left += 0.2

                        elif board[i + k][j - k] != player_piece_checked:
                            max_down_left = 1
                            still_checking_down_left = False
                        else:
                            max_down_left += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return 4 if player_piece_checked == 1 else -4

                    # --------- --------- ---------

                    # --------- check down right

                    # no need to evaluate if the first piece has less than 4 possible other pieces to connect

                    if i + 3 < nb_lines and j + 3 < nb_rows and still_checking_down_right:

                        # explained before
                        if board[i + k][j + k] is None:
                            still_checking_down_right = False

                            # add .2 for each same-nature piece than player_piece_checked
                            # on the same line but not connected yet
                            # make max_down_right at 1 if there is a not-same-nature piece on the same line
                            if k == 1 or k == 2:
                                for l in range(k + 1, 4):
                                    if board[i + l][j + l] == (1 if player_piece_checked == 2 else 2):
                                        max_down_right = 1
                                        break
                                    if board[i + l][j + l] == player_piece_checked:
                                        max_down_right += 0.2

                        elif board[i + k][j + k] != player_piece_checked:
                            max_down_right = 1
                            still_checking_down_right = False
                        else:
                            max_down_right += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return 4 if player_piece_checked == 1 else -4

                    # --------- --------- ---------

                    # --------- check up left

                    # no need to evaluate if the first piece has less than 4 possible other pieces to connect

                    if i - 3 >= 0 and j - 3 >= 0 and still_checking_up_left:

                        # explained before
                        if board[i - k][j - k] is None:
                            still_checking_up_left = False

                            # add .2 for each same-nature piece than player_piece_checked
                            # on the same line but not connected yet
                            # make max_up_left at 1 if there is a not-same-nature piece on the same line
                            if k == 1 or k == 2:
                                for l in range(k + 1, 4):
                                    if board[i - l][j - l] == (1 if player_piece_checked == 2 else 2):
                                        max_up_left = 1
                                        break
                                    if board[i - l][j - l] == player_piece_checked:
                                        max_up_left += 0.2

                        elif board[i - k][j - k] != player_piece_checked:
                            max_up_left = 1
                            still_checking_up_left = False
                        else:
                            max_up_left += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return 4 if player_piece_checked == 1 else -4

                    # --------- --------- ---------

                    # --------- check up right

                    # no need to evaluate if the first piece has less than 4 possible other pieces to connect

                    if i - 3 >= 0 and j + 3 < nb_rows and still_checking_up_right:

                        # explained before
                        if board[i - k][j + k] is None:
                            still_checking_up_right = False

                            # add .2 for each same-nature piece than player_piece_checked
                            # on the same line but not connected yet
                            # make max_up_right at 1 if there is a not-same-nature piece on the same line
                            if k == 1 or k == 2:
                                for l in range(k + 1, 4):
                                    if board[i - l][j + l] == (1 if player_piece_checked == 2 else 2):
                                        max_up_right = 1
                                        break
                                    if board[i - l][j + l] == player_piece_checked:
                                        max_up_right += 0.2

                        elif board[i - k][j + k] != player_piece_checked:
                            max_up_right = 1
                            still_checking_up_right = False
                        else:
                            max_up_right += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return 4 if player_piece_checked == 1 else -4

                if player_piece_checked == 1:  # AI always plays first
                    max_ai = max([max_ai, max([max_up, max_left, max_right, max_down_left, max_down_right,
                                               max_up_left, max_up_right])])
                else:
                    max_human = max([max_human, max([max_up, max_left, max_right, max_down_left, max_down_right,
                                                     max_up_left, max_up_right])])

        i -= 1

    print('max ai : ', max_ai)
    print('max human : ', max_human)
    print()
    print('max_ai - max_human : ', max_ai - max_human)

    return max_ai - max_human


# ---------------------------------------------------------------------------------------------------------------------
#
#                                                   FUNCTIONS GAME
#
# ---------------------------------------------------------------------------------------------------------------------

# ------game()------
# Arguments :
#
# Description :
#   initiate a new game and allows users to play until there is a winner
#
# Return value :
#

def game():
    # ------------------- Game initiation

    nb_rows = 7
    nb_lines = nb_rows - 1

    board = [[None] * nb_rows for __ in range(nb_lines)]  # creates board nb_rows * nb_lines
    # display_game(board)

    winner = False    # 1 if player 1 won, 2 if player 2 won, -1 if draw, False if there is still no winner
    current_player = 1   # 1 or 2

    # -------------------

    # ------------------- Game playing

    while not winner:

        if current_player == 1:
            # negmax(board, 8)
            player_round(board, current_player)
        else:
            player_round(board, current_player)

        current_player = 2 if current_player == 1 else 1

        display_game(board)

        eval_board(board)

        winner = check_winner(board)

    print('Winner : ', winner)

    # -------------------

# ---------------------------------------------------------------------------------------------------------------------

# ------update_board()------
# Arguments :
#   board : list of list - describes the current state of the game
#   current_player : int - number of the current player (1 or 2)
#   row_played : int - row current_player decided to play
#
# Description :
#   update the board
#
# Return value :
#


def update_board(board, current_player, row_played):
    i = len(board) - 1
    while i >= 0:

        if board[i][row_played] is None:
            board[i][row_played] = current_player

            break

        i -= 1

# ----------------------------------------------------------------------------------------------------------------------

# ------undo_board()------
# Arguments :
#   board : list of list - describes the current state of the game
#   row : int - row to undo
#
# Description :
#   undo last move on a specific row the board
#
# Return value :
#


def undo_board(board, row):

    for i in range(len(board)):
        if board[i][row] is not None:
            board[i][row] = None

            break

# ----------------------------------------------------------------------------------------------------------------------

# ------player_round()------
# Arguments :
#   board : list of list - describes the current state of the game
#   current_player : int - number of the current player (1 or 2)
#
# Description :
#   asks the current_player where he wants to play, checks the input through row_played_check(), and update the board
#
# Return value :
#


def player_round(board, current_player):

    # ask the current_player where he wants to play and check the input
    row_played = (int(input('Player ' + str('O' if current_player == 1 else 'X') +
                            ' enter the number of the column you want to play : ')))
    while not row_played_check(board, row_played):
        print()
        print('! Error !')
        row_played = int(input('Player ' + str(current_player) + ' enter the number of the column you want to play : '))

    # update the board
    update_board(board, current_player, row_played)


# ----------------------------------------------------------------------------------------------------------------------

# ------row_played_check()------
# Arguments :
#   board : list of list - describes the current state of the game
#   row_played : int - number of the row the player wants to play
#
# Description :
#   checks if the player can put his piece in this row
#
# Return value :
#   True if the row selected can be played
#   False if not

def row_played_check(board, row_played):

    nb_rows_board = len(board[0])

    if 0 <= row_played < nb_rows_board:
        if board[0][row_played] is None:
            return True  # the row selected can be played

    return False  # the row selected cannot be played

# ----------------------------------------------------------------------------------------------------------------------

# ------display_game()------
# Arguments :
#   board : list of list - describes the current state of the game
#
# Description :
#   displays the board to the players
#
# Return value :
#


def display_game(board):

    for i in range(len(board[0])):
        print(i, end="       ")
    print()

    for __ in board[0]:
        print("", end="")
    print()

    for i in board:
        for j in i:
            if j is None:
                print(" ", end="   |   ")
            elif j == 1:
                print("O", end="   |   ")
            elif j == 2:
                print("X", end="   |   ")

        print()

        for __ in board[0]:
            print("- - - - ", end="")

        print()

    print()
    print()

# ---------------------------------------------------------------------------------------------------------------------
#
#                                                   MAIN
#
# ---------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    game()
