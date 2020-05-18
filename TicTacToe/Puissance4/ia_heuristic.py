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


def score_position(board, position, piece):
    score = 0
    x, y = position

    if x == COLUMN_COUNT // 2:
        score += 5
    
    left = clamp(x-3,0, COLUMN_COUNT-1)
    right = clamp(x+3, 0, COLUMN_COUNT-1)
    up = clamp(y-3, 0, ROW_COUNT-1)
    down = clamp(y+3, 0, ROW_COUNT-1)

    count_enemy = 0
    count_self = 0
    for i in range(left, x+1):
        if board[y][i] == piece:
            count_self += 1
        elif board[y][i] != EMPTY and board[y][i] != piece:
            count_enemy += 1

        if count_enemy > 0 and count_self > 0:
            count_enemy = 0
            count_self = 0
            break
    
    score += count_self * 25
    score += count_enemy * 25

    count_enemy = 0
    count_self = 0
    for i in range(x, right):
        if board[y][i] == piece:
            count_self += 1
        elif board[y][i] != EMPTY and board[y][i] != piece:
            count_enemy += 1

        if count_enemy > 0 and count_self > 0:
            count_enemy = 0
            count_self = 0
            break
    
    score += count_self * 25
    score += count_enemy * 25

    count_enemy = 0
    count_self = 0
    for i in range(up, y+1):
        if board[i][x] == piece:
            count_self += 1
        elif board[i][x] != EMPTY and board[i][x] != piece:
            count_enemy += 1

        if count_enemy > 0 and count_self > 0:
            count_enemy = 0
            count_self = 0
            break
    
    score += count_self * 25
    score += count_enemy * 25

    count_enemy = 0
    count_self = 0
    for i in range(y, down):
        if board[i][x] == piece:
            count_self += 1
        elif board[i][x] != EMPTY and board[i][x] != piece:
            count_enemy += 1

        if count_enemy > 0 and count_self > 0:
            count_enemy = 0
            count_self = 0
            break
    
    score += count_self * 25
    score += count_enemy * 25

    # Upper left 
    index = 0
    count_enemy = 0
    count_self = 0
    while x + index >= 0 and y + index >= 0:
        if board[y + index][x + index] == piece:
            count_self += 1
        elif board[y + index][x + index] != EMPTY and board[y + index][x + index] != piece:
            count_enemy += 1

        if count_enemy > 0 and count_self > 0:
            count_enemy = 0
            count_self = 0
            break
        
        index -= 1

    score += count_self * 25
    score += count_enemy * 25

    # Bottom right
    index = 0
    count_enemy = 0
    count_self = 0
    while x + index  < COLUMN_COUNT and y + index < ROW_COUNT:
        if board[y + index][x + index] == piece:
            count_self += 1
        elif board[y + index][x + index] != EMPTY and board[y + index][x + index] != piece:
            count_enemy += 1

        if count_enemy > 0 and count_self > 0:
            count_enemy = 0
            count_self = 0
            break
        
        index += 1
    
    score += count_self * 25
    score += count_enemy * 25

    # Bottom left
    index = 0
    count_enemy = 0
    count_self = 0
    while x - index  >= 0 and y + index < ROW_COUNT:
        if board[y + index][x - index] == piece:
            count_self += 1
        elif board[y + index][x - index] != EMPTY and board[y + index][x - index] != piece:
            count_enemy += 1

        if count_enemy > 0 and count_self > 0:
            count_enemy = 0
            count_self = 0
            break
        
        index += 1
    
    score += count_self * 25
    score += count_enemy * 25

    index = 0
    count_enemy = 0
    count_self = 0
    while x + index  < COLUMN_COUNT and y - index >= 0:
        if board[y - index][x + index] == piece:
            count_self += 1
        elif board[y - index][x + index] != EMPTY and board[y - index][x + index] != piece:
            count_enemy += 1

        if count_enemy > 0 and count_self > 0:
            count_enemy = 0
            count_self = 0
            break
        
        index += 1
    
    score += count_self * 25
    score += count_enemy * 25

    return score
    


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
        pos_score = score_position(grille, pos, net.id)
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
    