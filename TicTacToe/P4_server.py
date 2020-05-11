import socket
import enum
import tkinter as tk



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

def animate_window():
    gui_loop()
    window.after(500, animate_window)

######### HELPER ELEMENTS #############
class PlayerType(enum.Enum):
    square = 1
    normal = 0

####### GAME RELATED VARIABLES #########
ROW_COUNT = 6
COLUMN_COUNT = 7
MAX_PLAYER = 4


game_state = {
    "grid" : [[0,0,0,0,0,0,0] for _ in range(ROW_COUNT)],
    "column_count" : [ROW_COUNT - 1 for _ in range(COLUMN_COUNT)],
    "previous_pos_move": None,
    "winner" : None,
    "player" : [],
    "colors_player": ["black", "red", "yellow", "blue", "green"] # le black est présent pour décaler les indices
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
                xc = x * 100 
                yc = y * 100 
                color = game_state["colors_player"][game_state["grid"][x][y]]
                canvas.create_oval(yc+10,xc+10,yc+90,xc+90,outline=color, fill=color, width="4" )
    # print(game_state["winner"])


def make_move(game_state, player, column):
    if game_state["column_count"][column] == 0: return False
    if 0 <= column <= 6:
        game_state["grid"][game_state["column_count"][column]][column] = player
        game_state["previous_pos_move"] =  game_state["column_count"][column], column
        game_state["column_count"][column] -= 1
        return True
    else:
        return False



def check_win(game_state, player, player_type):

    # Joueur puissance 4 normal
    if player_type == PlayerType.normal.value:
        # Horizontal
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if game_state["grid"][r][c] == player and game_state["grid"][r][c+1] == player and game_state["grid"][r][c+2] == player and game_state["grid"][r][c+3] == player:
                    game_state["winner"] = player
                    return True
        #Vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if game_state["grid"][r][c] == player and game_state["grid"][r+1][c] == player and game_state["grid"][r+2][c] == player and game_state["grid"][r+3][c] == player:
                    game_state["winner"] = player
                    return True
        # Positive slop diag
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if game_state["grid"][r][c] == player and game_state["grid"][r+1][c+1] == player and game_state["grid"][r+2][c+2] == player and game_state["grid"][r+3][c+3] == player:
                    game_state["winner"] = player
                    return True
        # Negative slop diag
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if game_state["grid"][r][c] == player and game_state["grid"][r-1][c+1] == player and game_state["grid"][r-2][c+2] == player and game_state["grid"][r-3][c+3] == player:
                    game_state["winner"] = player
                    return True
    else: # Joueur puissance 4 carre
        for c in range(COLUMN_COUNT - 1):
            for r in range(ROW_COUNT - 1):
                if game_state["grid"][r][c] == player and game_state["grid"][r][c+1] == player and game_state["grid"][r+1][c] == player and game_state["grid"][r+1][c+1] == player:
                    game_state["winner"] = player
                    return True
    
    return False


make_move(game_state, 1, 3)
make_move(game_state, 2, 5)
make_move(game_state, 3, 5)
window.after(100, animate_window)
canvas.mainloop()
