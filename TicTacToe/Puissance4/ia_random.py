import network
import json
import time
import enum
import random

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


########### IA FUNCTION #############

def think(game_obj): # This function returns a move
    possible_moves = []
    for i, value in enumerate(game_obj["column_count"]):
        if value >= 0:
            possible_moves.append(i)
    return random.choice(possible_moves)

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
    print(game_obj)
    