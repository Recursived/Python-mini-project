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

ROW_COUNT = 6
COLUMN_COUNT = 7


EMPTY = -1
WINDOW_LENGTH = 4


########## HELPER FUNCTION ##########

def clamp(n, smallest, largest): return max(smallest, min(n, largest))


########### IA FUNCTION #############
def make_move(grille, column_count, player, column):
    if column_count[column] == -1: return False
    if 0 <= column <= 6:
        grille[column_count[column]][column] = player
        return True
    else:
        return False

def get_score(window, piece, lst_players):
    if window.count(piece) == 3 and window.count(EMPTY) == 1:
        return 100
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        return 30
    elif window.count(piece) == 1  and window.count(EMPTY) == 3:
        return 10
    else:
        for id_player in range(len(lst_players)):
            if id_player != lst_players:
                if window.count(id_player) == 3 and window.count(EMPTY) == 1:
                    return 50
                elif window.count(piece) == 2 and window.count(EMPTY) == 2:
                    return 15
    return 0


def score_position(board, position, piece, lst_players):
    score = 0
    x, y = position

    if x == COLUMN_COUNT // 2:
        score += 5
    
    left = clamp(x-WINDOW_LENGTH+1,0, COLUMN_COUNT) # On rajoute un pour le slicing 
    right = clamp(x+WINDOW_LENGTH, 0, COLUMN_COUNT)
    up = clamp(y-WINDOW_LENGTH+1, 0, ROW_COUNT) # On rajoute un pour le slicing 
    down = clamp(y+WINDOW_LENGTH, 0, ROW_COUNT)

    horizontal = board[y][left:right]
    vertical = [board[i][x] for i in range(up, down)]
    positive_diag = [board[y-i][x-i] for i in range(3, -1,  -1) if y - i >= 0 and x-i >= 0] + [board[y+i][x+i] for i in range(1, 4) if y + i < ROW_COUNT and x + i < COLUMN_COUNT]
    negative_diag = [board[y+i][x-i] for i in range(3, -1,  -1) if y + i < ROW_COUNT  and x-i >= 0] + [board[y-i][x+i] for i in range(1, 4) if y - i >= 0 and x + i < COLUMN_COUNT]

    for i in range(len(horizontal) - WINDOW_LENGTH):
        window = horizontal[i:WINDOW_LENGTH+i]
        score = max(score, get_score(window, piece, lst_players))
    
    for i in range(len(vertical) - WINDOW_LENGTH):
        window = vertical[i:WINDOW_LENGTH+i]
        score = max(score, get_score(window, piece, lst_players))

    if len(positive_diag) >= 4:
        for i in range(len(positive_diag) - WINDOW_LENGTH):
            window = positive_diag[i:WINDOW_LENGTH+i]
            score = max(score, get_score(window, piece, lst_players))

    if len(negative_diag) >= 4:
        for i in range(len(negative_diag) - WINDOW_LENGTH):
            window = negative_diag[i:WINDOW_LENGTH+i]
            score = max(score, get_score(window, piece, lst_players))
        
    return score+5 if  x == COLUMN_COUNT // 2 else score
    


def think(game_obj): # This function returns a move
    possible_moves = []
    for i, value in enumerate(game_obj["column_count"]):
        if value >= 0:
            possible_moves.append(i)
    grille = game_obj["grid"]

    score = 0
    best_move = random.choice(possible_moves)
    print("*********************")
    pprint(grille)
    for move in possible_moves:
        if game_obj["column_count"][move] == -1:
            continue

        pos =  move, game_obj["column_count"][move]
        pos_score = score_position(grille, pos, net.id, game_obj["players"])
        print(f"move pos : {move} --> score : {pos_score}")
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
    