import socket
import random
import time
import json
import enum
import _thread
import argparse
import tkinter as tk

########## SERVER RELATED ELEMENTS ###########
server = "127.0.0.1"
port = 5555

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sck.bind((server, port))
except socket.error as e:
    str(e)

sck.listen(4)

def threaded_client(conn, player):
    global id_count
    conn.send(str(player).encode()) # On envoie l'id du player
    
    player_type = conn.recv(4096).decode() # On reçoit son type en retour
    conn.send(str("True").encode())
    game_obj["players"].insert(player, player_type)

    while True:
        time.sleep(.3)
        try: 
            data = json.loads(conn.recv(4096).decode())
            
            
            if data["action"] == "quit":
                break
            elif data["action"] == "get":
                conn.send(json.dumps(game_obj).encode())
            elif data["action"] == "play":
                make_move(game_obj, game_obj["player_turn"], data["value"]) # TO-DO : check s'il y a une win
                conn.send(json.dumps(game_obj).encode())

                turn_player = game_obj["player_turn"]
                if game_finished(game_obj):
                    game_obj["state"] = GameState.end.value
                
                elif check_win(game_obj, turn_player, game_obj["players"][turn_player]):
                    game_obj["state"] = GameState.end.value
                    game_obj["winner"] = turn_player
                else:
                    # On effectue un changement de tour
                    game_obj["player_turn"] += 1
                    game_obj["player_turn"] %= MAX_PLAYER
        except:
            print("Crash in the threaded client n°"+ str(player))
            break
    conn.close()




####### INIT FENETRE#########

LARG = 700
HAUT = 600

window = tk.Tk()
window.geometry(str(LARG)+"x"+str(HAUT))   # taille de la fenetre
window.title("ESIEE - Puissance 4")

# création de la frame principale stockant toutes les pages

F = tk.Frame(window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

canvas = tk.Canvas(F,width = LARG, height = HAUT)

canvas.place(x=0,y=0)
canvas.configure(background='black')


def init_display():
    global MAX_PLAYER, id_count
    canvas.create_text(
            LARG/2,
            HAUT/2,
            fill="white",
            font="Times 30 italic bold",
            text=f"En attente de connexion - {id_count}/{MAX_PLAYER}"
        )

def animate_window():
    global MAX_PLAYER, id_count
    canvas.delete("all")

    if game_obj["state"] == GameState.connection.value:
        conn, addr = sck.accept()
        _thread.start_new_thread(threaded_client, (conn, id_count))
        id_count += 1
        if id_count == MAX_PLAYER:
            game_obj["state"] = GameState.play.value
        
        
        nb_player = len(game_obj["players"])
        canvas.create_text(
            LARG/2,
            HAUT/2,
            fill="white",
            font="Times 30 italic bold",
            text=f"En attente de connexion - {id_count}/{MAX_PLAYER}"
        )

        

    elif game_obj["state"] == GameState.play.value:
        gui_loop()
    else: # La partie est finie, on affiche le gagnant
        if game_obj["winner"] != None:
            winner = game_obj["winner"]
            canvas.create_text(
                LARG/2,
                HAUT/2,
                fill=game_obj["colors_player"][winner],
                font="Times 30 italic bold",
                text=f"Partie finie - joueur gagnant : n°{winner}"
            )
        else:
            canvas.create_text(
                LARG/2,
                HAUT/2,
                fill="white",
                font="Times 30 italic bold",
                text=f"Partie finie - pas de gagnant"
            )
    window.after(500, animate_window)

######### HELPER ELEMENTS #############
class PlayerType(enum.Enum):
    square = 1
    normal = 0

class GameState(enum.Enum):
    connection = "CONNECTION"
    play = "PLAY"
    end = "END"


####### GAME RELATED VARIABLES #########
parser = argparse.ArgumentParser()
parser.add_argument("nb_player", type=int, help="Set the number of player in the game (value must between 2-4)")
args = parser.parse_args()

ROW_COUNT = 6
COLUMN_COUNT = 7
MAX_PLAYER = max(2, min(args.nb_player, 4))
VACANT = -1

id_count = 0


game_obj = {
    "grid" : [[VACANT, VACANT, VACANT, VACANT, VACANT, VACANT, VACANT] for _ in range(ROW_COUNT)],
    "column_count" : [ROW_COUNT - 1 for _ in range(COLUMN_COUNT)],
    "previous_pos_move": None,
    "winner" : None,
    "players" : [],
    "player_turn": random.randint(0, MAX_PLAYER - 1),
    "colors_player": [ "red", "yellow", "blue", "green"],
    "state" : GameState.connection.value, # On démarre par la phase de connection
}


####### GAME ENGINE FUNCTION ###########
def gui_loop():
    # On affiche la grille de p4
    for i in range(ROW_COUNT):  
        canvas.create_line(0,i*100,LARG,i*100,fill="white", width="4" )
    for i in range(COLUMN_COUNT):
        canvas.create_line(i*100,0,i*100,HAUT,fill="white", width="4" )
    
    for x in range(ROW_COUNT):
            for y in range(COLUMN_COUNT):
                if game_obj["grid"][x][y] != VACANT:
                    xc = x * 100 
                    yc = y * 100 
                    color = game_obj["colors_player"][game_obj["grid"][x][y]]
                    canvas.create_oval(yc+10,xc+10,yc+90,xc+90,outline=color, fill=color, width="4" )
                    canvas.create_text(
                        yc+10,
                        xc+10,
                        fill="white",
                        font="Times 15 italic bold",
                        text=str(game_obj["grid"][x][y])
                    )

def make_move(game_obj, player, column):
    if game_obj["column_count"][column] == -1: return False
    if 0 <= column <= 6:
        game_obj["grid"][game_obj["column_count"][column]][column] = player
        game_obj["previous_pos_move"] =  game_obj["column_count"][column], column
        game_obj["column_count"][column] -= 1
        
        return True
    else:
        return False


def game_finished(game_obj):
    for x in range(ROW_COUNT):
        for y in range(COLUMN_COUNT):
            if game_obj["grid"][x][y] == -1:
                return False
    return True

def check_win(game_obj, player, player_type):

    # Joueur puissance 4 normal
    if int(player_type) == PlayerType.normal.value:
        # Horizontal
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if game_obj["grid"][r][c] == player and game_obj["grid"][r][c+1] == player and game_obj["grid"][r][c+2] == player and game_obj["grid"][r][c+3] == player:
                    game_obj["winner"] = player
                    return True
        #Vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if game_obj["grid"][r][c] == player and game_obj["grid"][r+1][c] == player and game_obj["grid"][r+2][c] == player and game_obj["grid"][r+3][c] == player:
                    game_obj["winner"] = player
                    return True
        # Positive slop diag
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if game_obj["grid"][r][c] == player and game_obj["grid"][r+1][c+1] == player and game_obj["grid"][r+2][c+2] == player and game_obj["grid"][r+3][c+3] == player:
                    game_obj["winner"] = player
                    return True
        # Negative slop diag
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if game_obj["grid"][r][c] == player and game_obj["grid"][r-1][c+1] == player and game_obj["grid"][r-2][c+2] == player and game_obj["grid"][r-3][c+3] == player:
                    game_obj["winner"] = player
                    return True
    else: # Joueur puissance 4 carre
        for c in range(COLUMN_COUNT - 1):
            for r in range(ROW_COUNT - 1):
                if game_obj["grid"][r][c] == player and game_obj["grid"][r][c+1] == player and game_obj["grid"][r+1][c] == player and game_obj["grid"][r+1][c+1] == player:
                    game_obj["winner"] = player
                    return True
    
    return False

window.after(0, init_display)
window.after(2000, animate_window)
canvas.mainloop()

