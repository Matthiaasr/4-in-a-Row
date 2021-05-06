# ------min_max(board, depth, player)------
# Arguments :
#   board : list of list - describes the current state of the game
#   depth : int - describes the current depth in the graph (0 is a leaf)
#   player : int - which player is playing at this depth
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

def min_max(board, depth, player):

    nb_rows = len(board[0])
    depth_max = 4

    winner, advantage = eval_board(board)
    if depth == 0 or winner is not False:
        return advantage

    elif depth == depth_max:  # it's AI turn and it's at this depth it has to choose what move to do
        max_eval = - 1000000
        best_row = 0

        for i in range(nb_rows):
            if row_played_check(board, i):
                update_board(board, player, i)

                value_minmax = min_max(board, depth - 1, 2)
                if max_eval < value_minmax:
                    max_eval = value_minmax
                    best_row = i

                undo_board(board, i)

        print(max_eval)
        update_board(board, player, best_row)

    else:
        if player == 1:  # AI turn, so we have to pick the max children
            max_eval = - 1000000

            for i in range(nb_rows):
                if row_played_check(board, i):
                    update_board(board, player, i)
                    max_eval = max(max_eval, min_max(board, depth - 1, 2))
                    undo_board(board, i)

            return max_eval
        elif player == 2:  # human turn, so we have to pick the min children
            min_eval = 1000000

            for i in range(nb_rows):
                if row_played_check(board, i):
                    update_board(board, player, i)
                    min_eval = min(min_eval, min_max(board, depth - 1, 1))
                    undo_board(board, i)

            return min_eval

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
    draw = True

    max_ai = 0
    max_human = 0

    # we gonna check if there are other pieces of player_piece_checked connected to the piece located in board[i][j]
    for i in range(len(board)):
        for j in range(len(board[i])):

            player_piece_checked = board[i][j]

            if player_piece_checked is not None:

                max_down = 1
                max_right = 1
                max_down_left = 1
                max_down_right = 1

                still_checking_down = True
                still_checking_right = True
                still_checking_down_left = True
                still_checking_down_right = True

                for k in range(1, 4):  # k will be used to increment through the board

                    # --------- check down

                    # can't win if the first piece has less than 4 possible other pieces to connect
                    if i + k < nb_lines and still_checking_down:

                        # if we found a cell not of the same nature than player_piece_checked,
                        # we know this not four in a row
                        if board[i + k][j] != player_piece_checked:
                            still_checking_down = False
                        else:
                            max_down += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return (player_piece_checked, 1000 if player_piece_checked == 1 else -1000)

                    # --------- --------- ---------

                    # --------- check right

                    # can't win if the first piece has less than 4 possible other pieces to connect
                    if j + k < nb_rows and still_checking_right:

                        # if we found a cell not of the same nature than player_piece_checked,
                        # we know this not four in a row
                        if board[i][j + k] != player_piece_checked:
                            still_checking_right = False
                        else:
                            max_right += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return (player_piece_checked, 1000 if player_piece_checked == 1 else -1000)

                    # --------- --------- ---------

                    # --------- check down left

                    # can't win if the first piece has less than 4 possible other pieces to connect
                    if i + k < nb_lines and j - k >= 0 and still_checking_down_left:

                        # if we found a cell not of the same nature than player_piece_checked,
                        # we know this not four in a row
                        if board[i + k][j - k] != player_piece_checked:
                            still_checking_down_left = False
                        else:
                            max_down_left += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return (player_piece_checked, 1000 if player_piece_checked == 1 else -1000)

                    # --------- --------- ---------

                    # --------- check down right

                    # can't win if the first piece has less than 4 possible other pieces to connect

                    if i + k < nb_lines and j + k < nb_rows and still_checking_down_right:

                        # if we found a cell not of the same nature than player_piece_checked,
                        # we know this not four in a row
                        if board[i + k][j + k] != player_piece_checked:
                            still_checking_down_right = False
                        else:
                            max_down_right += 1
                            if k == 3:  # if the test was passed 3 times, it means we have 4 in a row
                                return (player_piece_checked, 1000 if player_piece_checked == 1 else -1000)

                if player_piece_checked == 1:  # AI always plays first
                    max_ai = max([max_ai, max([max_down, max_right, max_down_left, max_down_right])])
                else:
                    max_human = max([max_human, max([max_down, max_right, max_down_left, max_down_right])])
            else:

                draw = False

    if draw:
        return (-1, 0)
    else:
        return (False, max_ai - max_human)