import network
import json
import time
import math
import enum
import random
from pprint import pprint
from copy import deepcopy

########### HELPER ELEMENTS ###########
class State(enum.Enum):
    waiting = 0
    playing = 1
    quitting = 2


############ IA ELEMENTS #############

type_ia = 0 # ia normale de P4
ia_state = State.waiting.value
payload = {}
net = network.Network()
net.connect()
response = bool(net.send(str(type_ia)).decode())
two_player = False
if response != True:
    exit()

game_obj = None

print(f"Je suis le player {net.id}")

ROW_COUNT = 6
COLUMN_COUNT = 7


EMPTY = -1
WINDOW_LENGTH = 4
SELF_AI = net.id
OTHER_AI = 0 if SELF_AI == 1 else 1

########### IA FUNCTION #############
def make_move(grille, column_count, player, column):
    if column_count[column] == -1: return False
    if 0 <= column <= 6:
        grille[column_count[column]][column] = player
        return True
    else:
        return False

def evaluate_window(window, piece, lst_players):
    if not two_player:
        score = 0
        if window.count(piece) == 4:
            score = 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score = 30
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score = 10

        for i in range(len(lst_players)):
            if i != piece and  window.count(i) == 3 and window.count(EMPTY) == 1:
                score = 50
            if i != piece and window.count(i) == 2 and window.count(EMPTY) == 2:
                score = 15
            
        return score
    else:
        score = 0
        opp_piece = OTHER_AI if piece == SELF_AI else SELF_AI
        if window.count(piece) == 4:
            score = 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score = 30
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score = 10
        elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
                score = 50
        elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
                score = 15
            

        return score

def score_position(board, piece, lst_players):
    score = 0

    ## Score center column
    center_array = [val[COLUMN_COUNT//2] for val in board]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [val for val in board[r][:]]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score +=  evaluate_window(window, piece, lst_players)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [val[c] for val in board]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score +=  evaluate_window(window, piece, lst_players)

    ## Score positive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score +=  evaluate_window(window, piece, lst_players)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r
            +3-i][c+i] for i in range(WINDOW_LENGTH)]
            score +=  evaluate_window(window, piece, lst_players)

    return score

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def get_valid_locations(lst_columns):
    possible_moves = []
    for i, value in enumerate(lst_columns):
        if value >= 0:
            possible_moves.append(i)
    return possible_moves
    

def is_terminal_node(board, lst_columns):
    return winning_move(board, SELF_AI) or winning_move(board, OTHER_AI) or len(get_valid_locations(lst_columns)) == 0

def minimax(board, lst_columns, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(lst_columns)
    is_terminal = is_terminal_node(board, lst_columns)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, SELF_AI):
                return (None, 100000000000000)
            elif winning_move(board, OTHER_AI):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, SELF_AI, lst_columns))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = deepcopy(board)
            lst_columns_copy = deepcopy(lst_columns)
            make_move(b_copy, lst_columns, SELF_AI, col)
            lst_columns_copy[col]-=1
            new_score = minimax(b_copy, lst_columns_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = deepcopy(board)
            lst_columns_copy = deepcopy(lst_columns)
            make_move(b_copy, lst_columns, OTHER_AI, col)
            lst_columns_copy[col]-=1
            new_score = minimax(b_copy, lst_columns_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def think(game_obj): # This function returns a move
    if not two_player:
        possible_moves = []
        for i, value in enumerate(game_obj["column_count"]):
            if value >= 0:
                possible_moves.append(i)
        grille = game_obj["grid"]

        score = -9999999999
        best_move = random.choice(possible_moves)
        for move in possible_moves:
            c_grille = deepcopy(grille)
            make_move(c_grille, game_obj["column_count"], net.id, move)
            pos_score = score_position(c_grille, net.id, game_obj["players"])
            if pos_score > score:
                best_move = move
                score = pos_score

        return best_move
    else:
        col, minimax_score = minimax(game_obj["grid"], game_obj["column_count"], 7, -math.inf, math.inf, True)
        return col





############## MAIN PART #################
while True:
    time.sleep(.3)
    if ia_state == State.waiting.value:
        payload["action"] = "get"
        game_obj = json.loads(net.send(json.dumps(payload)).decode())
        two_player = True if len(game_obj["players"]) == 2 else False
        if game_obj["state"] == "PLAY" and int(game_obj["player_turn"]) == int(net.id): # Si c'est au tour de l'ia
            ia_state = State.playing.value
        elif game_obj["state"] == "END":
            ia_state = State.quitting.value
    elif ia_state == State.playing.value:
        payload["action"] = "play"
        payload["value"] = think(game_obj)
        print("Player made move --> " + str(payload["value"]))

        game_obj = json.loads(net.send(json.dumps(payload)).decode())
        ia_state = State.waiting.value
    else:
        payload["action"] = "quit"
        net.send(json.dumps(payload))
        print("quitting the game")
        break
    