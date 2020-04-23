import tkinter as tk
import random
import numpy as np
import copy
import sys
import time

#################################################################################
#
#   Données de partie

Data = [   [1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,0,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,0,0,0,0,0,0,0,0,0,0,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1] ]

GInit  = np.array(Data,dtype=np.int8)
GInit  = np.flip(GInit,0).transpose()

LARGEUR = 13
HAUTEUR = 17


# container pour passer efficacement toutes les données de la partie

class Game:
    def __init__(self, Grille, PlayerX, PlayerY, Score=0):
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.Score   = Score
        self.Grille  = Grille
    
    def copy(self): 
        return copy.deepcopy(self)

GameInit = Game(GInit,6,4)

##############################################################
#
#   création de la fenetre principale  - NE PAS TOUCHER

L = 20  # largeur d'une case du jeu en pixel    
largeurPix = LARGEUR * L
hauteurPix = HAUTEUR * L
nb = 10000


Window = tk.Tk()
Window.geometry(str(largeurPix)+"x"+str(hauteurPix))   # taille de la fenetre
Window.title("TRON")


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

canvas = tk.Canvas(Frame0,width = largeurPix, height = hauteurPix, bg ="black" )
canvas.place(x=0,y=0)

#   Dessine la grille de jeu - ne pas toucher


def Affiche(Game):
    canvas.delete("all")
    H = canvas.winfo_height()
    
    def DrawCase(x,y,coul):
        x *= L
        y *= L
        canvas.create_rectangle(x,H-y,x+L,H-y-L,fill=coul)
    
    # dessin des murs 
   
    for x in range (LARGEUR):
       for y in range (HAUTEUR):
           if Game.Grille[x,y] == 1  : DrawCase(x,y,"gray" )
           if Game.Grille[x,y] == 2  : DrawCase(x,y,"cyan" )
   
    
    # dessin de la moto
    DrawCase(Game.PlayerX,Game.PlayerY,"red" )

def AfficheScore(Game):
   info = "SCORE : " + str(Game.Score)
   canvas.create_text(80, 13,   font='Helvetica 12 bold', fill="yellow", text=info)


###########################################################
#
# gestion du joueur IA

# VOTRE CODE ICI

def GetPlayablePosition(game, x, y):
    pos = []
    if game.Grille[x,y+1] == 0:
        pos.append([0,1])
    if game.Grille[x,y-1] == 0:
        pos.append([0,-1])
    if game.Grille[x+1,y] == 0:
        pos.append([1,0])
    if game.Grille[x-1,y] == 0:
        pos.append([-1,0])

    return pos

def SimulationPartie(Game):
    while True:
        lst = GetPlayablePosition(Game, Game.PlayerX, Game.PlayerY)
        try:
            Game.Grille[Game.PlayerX,Game.PlayerY] = 2
            n_x, n_y = random.choice(lst)
            Game.PlayerX += n_x
            Game.PlayerY += n_y
            Game.Score += 1
            
            #print(f"score partie : {Game.score}")
        except Exception as e:
            #print("je suis partie de la fonction")
            return Game.Score


def MonteCarlo(Game, nbParties, n_x, n_y):
    total = 0
    for i in range(nbParties):
        copy_game = Game.copy()
        copy_game.PlayerX += n_x
        copy_game.PlayerY += n_y
        copy_game.Score += 1
        total += SimulationPartie(copy_game)
    
    #print(f"total = {total} for ({n_x}, {n_y})")
    return total


def Play(Game):   
    
    x,y = Game.PlayerX, Game.PlayerY

    Game.Grille[x,y] = 2  # laisse la trace de la moto
   
    score_lst = []
    for playable_pos in GetPlayablePosition(Game,x,y):
        total = MonteCarlo(Game, nb, *playable_pos)
        score_lst.append((playable_pos, total/nb ))
        
    if not score_lst:
        return True
    else:
        # print(score_lst)
        n_x, n_y = max(score_lst, key=lambda lst: lst[1])[0] 
        Game.PlayerX += n_x
        Game.PlayerY += n_y
        Game.Score += 1

###########################################################
#                   Partie Vectorielle                    #
###########################################################



# Liste des directions :
# 0 : sur place   1: à gauche  2 : en haut   3: à droite    4: en bas

dx = np.array([0, -1, 0,  1,  0],dtype=np.int8)
dy = np.array([0,  0, 1,  0, -1],dtype=np.int8)

# scores associés à chaque déplacement
ds = np.array([0,  1,  1,  1,  1],dtype=np.int8)

Debug = False


def Simulate(Game):

    # on copie les datas de départ pour créer plusieurs parties en //
    G      = np.tile(Game.Grille,(nb,1,1))
    X      = np.tile(Game.PlayerX,nb)
    Y      = np.tile(Game.PlayerY,nb)
    S      = np.tile(Game.Score,nb)
    I      = np.arange(nb)  # 0,1,2,3,4,5...
    decalage_gauche_bas = np.full(nb, -1, dtype=np.int8)
    decalage_droite_haut = np.full(nb, 1, dtype=np.int8)

    boucle = True
    if Debug : AffGrilles(G,X,Y)

    last_sum = np.sum(S)

    while(boucle) :

        if Debug :print("X : ",X)
        if Debug :print("Y : ",Y)
        if Debug :print("S : ",S)

        # marque le passage de la moto
        G[I, X, Y] = 2
        
        LPossibles = np.zeros((nb,4),dtype=np.int8)
        Indices = np.zeros(nb, dtype=np.int8)

        VGauche =  (G[I, X + decalage_gauche_bas, Y] == 0) * 1
        LPossibles[I,Indices] = VGauche
        Indices = Indices + (G[I, X + decalage_gauche_bas, Y] == 0) * 1
       
        VHaut = (G[I, X, Y + decalage_droite_haut] == 0) * 2
        LPossibles[I,Indices] = VHaut
        Indices = Indices + (G[I, X, Y + decalage_droite_haut] == 0) * 1
        
        VDroite =  (G[I, X + decalage_droite_haut, Y] == 0) * 3
        LPossibles[I,Indices] = VDroite
        Indices = Indices + (G[I, X + decalage_droite_haut, Y] == 0) * 1
       
        VBas = (G[I, X, Y + decalage_gauche_bas] == 0) * 4
        LPossibles[I,Indices] = VBas
        Indices = Indices + (G[I, X, Y + decalage_gauche_bas] == 0) * 1
        

        Indices[Indices == 0] = 1
        # print("Indices", Indices)
        # print("LPossibles", LPossibles)

        R = np.random.randint(12,size=nb)
        R = R % Indices
        # print("avant R", R)



        #DEPLACEMENT
        DX = dx[LPossibles[I,R]]
        DY = dy[LPossibles[I,R]]
        if Debug : print("DX : ", DX)
        if Debug : print("DY : ", DY)
        X += DX
        Y += DY
        S += ds[LPossibles[I,R]]
        
        sum_val = np.sum(S)
        if sum_val == last_sum:
            break
        else:
            last_sum = sum_val

        #debug
        if Debug : AffGrilles(G,X,Y)
        if Debug : time.sleep(2)

    return np.mean(S)

def PlayParallel(Game):   
    
    x,y = Game.PlayerX, Game.PlayerY

    Game.Grille[x,y] = 2  # laisse la trace de la moto
   
    score_lst = []
    for playable_pos in GetPlayablePosition(Game,x,y):
        copy_game = Game.copy()
        n_x, n_y = playable_pos
        copy_game.PlayerX += n_x
        copy_game.PlayerY += n_y
        copy_game.Score += 1
        score = Simulate(copy_game)
        if score != 0: # Si c'est la fin
            score_lst.append((playable_pos, score))


    if not score_lst:
        return True
    else:
        # print(score_lst)
        n_x, n_y = max(score_lst, key=lambda lst: lst[1])[0] 
        Game.PlayerX += n_x
        Game.PlayerY += n_y
        Game.Score += 1
 

     
CurrentGame = GameInit.copy()
 

def Partie():

    PartieTermine = PlayParallel(CurrentGame) # Version parallèle
    # PartieTermine = Play(CurrentGame) # Version simple
    
    if not PartieTermine :
        Affiche(CurrentGame)
        # rappelle la fonction Partie() dans 30ms
        # entre temps laisse l'OS réafficher l'interface
        tsart = time.time()
        Window.after(1,Partie) 
        tfin = time.time()
        print(f"temps : {tfin - tsart}")
    else :
        AfficheScore(CurrentGame)


#####################################################################################
#
#  Mise en place de l'interface - ne pas toucher

AfficherPage(0)
Window.after(100,Partie)
Window.mainloop()
      

    
        

      
 

