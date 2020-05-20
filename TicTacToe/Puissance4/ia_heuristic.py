import network
import json
import time
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
if response != True:
    exit()

game_obj = None

print(f"Je suis le player {net.id}")

ROW_COUNT = 6
COLUMN_COUNT = 7


EMPTY = -1
WINDOW_LENGTH = 4

########### IA FUNCTION #############
def make_move(grille, column_count, player, column):
    if column_count[column] == -1: return False
    if 0 <= column <= 6:
        grille[column_count[column]][column] = player
        return True
    else:
        return False

def evaluate_window(window, piece, lst_players):
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
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score +=  evaluate_window(window, piece, lst_players)

    return score


def think(game_obj): # This function returns a move
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




############## MAIN PART #################
while True:
    time.sleep(.3)
    if ia_state == State.waiting.value:
        payload["action"] = "get"
        game_obj = json.loads(net.send(json.dumps(payload)).decode())
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
    