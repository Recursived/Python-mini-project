import tkinter as tk
from tkinter import messagebox
import random
import numpy as np

###############################################################################
# création de la fenetre principale  - ne pas toucher

LARG = 300
HAUT = 300

Window = tk.Tk()
Window.geometry(str(LARG)+"x"+str(HAUT))   # taille de la fenetre
Window.title("ESIEE - Morpion")


# création de la frame principale stockant toutes les pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
Frame0 = CreerUnePage(0)

canvas = tk.Canvas(Frame0,width = LARG, height = HAUT, bg ="black" )
canvas.place(x=0,y=0)


#################################################################################
#
#  Parametres du jeu
 
Grille = [ [0,0,0], 
           [0,0,0], 
           [0,0,0] ]  # attention les lignes représentent les colonnes de la grille
           
Grille = np.array(Grille)
Grille = Grille.transpose()  # pour avoir x,y
GrilleReset = np.copy(Grille)
Tour = random.randint(1,2) # On choisit le tour au hasard
FinPartie = False
GameState = {
    1 : {
        "victoire" : 0,
        "color" : "red"
    },
    2 : {
        "victoire" : 0,
        "color" : "yellow"
    }
}

  

###############################################################################
#
# gestion du joueur humain et de l'IA
def checkGameFinished(grille):
    return all(grille[i][j] != 0 for i in range(3) for j in range(3))

def resetGame():
    global Grille
    Grille = np.copy(GrilleReset)


def getAvailablePosition(grille):
    return [(i,j) for i in range(3) for j in range(3) if grille[i][j] == 0]

def victoryCheck(grille, x, y, player):
    # On vérifie qu'on ne dépasse pas la taille du tableau

    assert(x <= 2)
    assert(y <= 2)
    # On verifie la ligne horizontale et verticale
    if grille[x][0] == player and grille[x][1] == player and grille[x][2] == player:
        return True
    if grille[0][y] == player and grille[1][y] == player and grille[2][y] == player:
        return True
    
    # On vérifie les deux diagonales
    if grille[0][0] == player and grille[1][1] == player and grille [2][2] == player:
           return True
    if grille[0][2] == player and grille[1][1] == player and grille [2][0] == player:
           return True  

    return False

# La fonction play retourne le gagnat s'il y en a un sinon 0
def Play(x,y, player):             
    Grille[x][y] = player
    return player if victoryCheck(Grille, x, y, player) else 0
          
    
    
################################################################################
#    
# Dessine la grille de jeu

def Dessine(gagnant):
    ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
    canvas.delete("all")
   
    if gagnant == 0 and checkGameFinished(Grille): # Match nul
        canvas.create_rectangle(0,0, LARG, HAUT,fill="white")
        canvas.create_text(
            LARG/2,
            HAUT/2,
            fill="black",
            font="Times 16 italic bold",
            text="Draw - Click to restart"
        )
    elif gagnant == 0: # Partie en cours
        for i in range(4):
            canvas.create_line(i*100,0,i*100,300,fill="blue", width="4" )
            canvas.create_line(0,i*100,300,i*100,fill="blue", width="4" )
            
        for x in range(3):
            for y in range(3):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_line(xc+10,yc+10,xc+90,yc+90,fill="red", width="4" )
                    canvas.create_line(xc+90,yc+10,xc+10,yc+90,fill="red", width="4" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(xc+10,yc+10,xc+90,yc+90,outline="yellow", width="4" )
    else: # Victoire d'un joueur
        
        GameState[gagnant]["victoire"] += 1
        canvas.create_rectangle(0,0, LARG, HAUT,fill=GameState[gagnant]["color"])
        win_red = GameState[1]["victoire"]
        win_yellow = GameState[2]["victoire"]
        canvas.create_text(
            LARG/2,
            HAUT/2,
            fill="black",
            font="Times 16 italic bold",
            text=f"red : {win_red} - yellow : {win_yellow}\nClick to restart"
        )
       
        
  
####################################################################################
#
#  fnt appelée par un clic souris sur la zone de dessin

def MouseClick(event):
    global Tour, FinPartie

    if FinPartie:
        resetGame()
        FinPartie = False
        gagnant = 0
    else:
        if Tour == 1: # Partie joueur
            Window.focus_set()
            x = event.x // 100  # convertit une coordonée pixel écran en coord grille de jeu
            y = event.y // 100

            if ( (x<0) or (x>2) or (y<0) or (y>2) ) : return
            if Grille[x][y] != 0: return
        else: # PARTIE IA 
            x, y = random.choice(getAvailablePosition(Grille))
        
        print(">> clicked at", x,y)
        gagnant = Play(x,y,Tour)  # gestion du joueur humain et de l'IA

    Dessine(gagnant)
    if gagnant or checkGameFinished(Grille):
        FinPartie = True
    Tour = 1 if Tour == 2 else 2
    
canvas.bind('<ButtonPress-1>',    MouseClick)

#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Dessine(0) # Pas de gagnant au départ du programme donc on met un 0
Window.mainloop()


  


    
        

      
 

