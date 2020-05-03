import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
import sys
import enum
 

#################################################################
##
##  variables du jeu 
 
# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

TBL = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]
        
        
TBL = np.array(TBL,dtype=np.int32)
TBL = TBL.transpose()  ## ainsi, on peut écrire TBL[x][y]


        
ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]

screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM

score = 0
eaten = 0
totalGum = 0
gameStatus = "playing"

class Direction (enum.Enum):
   left = 1
   right = 2
   up = 3
   down = 4
 

###########################################################################################

# création de la fenetre principale  -- NE PAS TOUCHER

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("MaCoSz - ESIEE - PACMAN")

# création de la frame principale stockant plusieurs pages

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
    
    
def WindowAnim():
    MainLoop()
    Window.after(500,WindowAnim) #500

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
################################################################################
#
# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape)
   global totalGum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
            totalGum += 1 
   return GUM
            
GUM = PlacementsGUM()   

PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"  , "left" , "on"]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange", "right", "on"] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  , "up"   , "on"]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"   , "down" , "on"]     )         

 
 
#################################################################
##
##  FNT AFFICHAGE



def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche():
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = "yellow")
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
     
   # texte blabla
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "Score : "+str(score), fill ="yellow", font = PoliceTexte)
 
            
#################################################################
##
##   ADDINGS

def EatingGUMS():
   global score, DistanceMap, eaten
   x,y = PacManPos
   if(GUM[x][y] == 1):
      GUM[x][y]=0
      score += 1
      DistanceMap[x][y] = 100
      eaten += 1

def InitDistanceMap():
   DistanceMap = np.zeros(TBL.shape)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if (TBL[x][y] == 1  or TBL[x][y] == 2):
            DistanceMap[x][y] = sys.maxsize
         elif (GUM[x][y] == 1):
            DistanceMap[x][y] = 0
         else:
            DistanceMap[x][y] = 100
   return DistanceMap

DistanceMap = InitDistanceMap()


def updateDistanceMap():
   global DistanceMap, eaten, totalGum
   while (True):
      change = False
      for x in range(LARGEUR):
         for y in range(HAUTEUR):
            if(DistanceMap[x][y] == sys.maxsize or DistanceMap[x][y] == 0):
               continue
            else:
               left = DistanceMap[max(0, min(x-1, LARGEUR - 1))][y] 
               right = DistanceMap[max(0, min(x+1, LARGEUR - 1))][y] 
               down = DistanceMap[x][max(0, min(y+1, HAUTEUR - 1))] 
               up = DistanceMap[x][max(0, min(y-1, HAUTEUR - 1))]
               minimum = min(left, right, up, down)

               if(minimum+1 != DistanceMap[x][y]):
                  DistanceMap[x][y] = minimum+1
                  change = True
      if(change == False or eaten == totalGum):
         break

updateDistanceMap()

def AfficheGhostsMap(gMap):
   for y in range(HAUTEUR):
      print("(",end='')
      for x in range(LARGEUR):
         if(gMap[x][y] > 1000):
            print("M", end=' ,')
         else:
            print(int(gMap[x][y]), end=' ,')
      print(") \n")

def InitGhostDistanceMap():
   DistanceMap = np.zeros(TBL.shape)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if (TBL[x][y] == 1):
            DistanceMap[x][y] = sys.maxsize
         else:
            DistanceMap[x][y] = 100
   return DistanceMap

PinkGhostMap = InitGhostDistanceMap()
PinkGhostMap[Ghosts[0][0]][Ghosts[0][1]] = 0
OrangeGhostMap = InitGhostDistanceMap()
OrangeGhostMap[Ghosts[1][0]][Ghosts[1][1]] = 0
BlueGhostMap = InitGhostDistanceMap()
BlueGhostMap[Ghosts[2][0]][Ghosts[2][1]] = 0
RedGhostMap = InitGhostDistanceMap()
RedGhostMap[Ghosts[3][0]][Ghosts[3][1]] = 0

def GhostDistanceMap(i, gMap): #update ghost maps one by one
   global eaten, totalGum

   gMap[Ghosts[i][0]][Ghosts[i][1]] = 0 # On maj l'emplacement du fantome
   while (True):
      change = False
      for x in range(LARGEUR):
         for y in range(HAUTEUR):
            if(gMap[x][y] == sys.maxsize or gMap[x][y] == 0):
               continue
            else:
               left = gMap[max(0, min(x-1, LARGEUR - 1))][y]
               right = gMap[max(0, min(x+1, LARGEUR - 1))][y] 
               down = gMap[x][max(0, min(y+1, HAUTEUR - 1))] 
               up = gMap[x][max(0, min(y-1, HAUTEUR - 1))]
               minimum = min(left, right, up, down)
               if(minimum+1 != gMap[x][y]):
                  gMap[x][y] = minimum+1
                  change = True
               
      if(change == False or eaten == totalGum):
         break

GhostDistanceMap(0, PinkGhostMap)
GhostDistanceMap(1, OrangeGhostMap)
GhostDistanceMap(2, BlueGhostMap)
GhostDistanceMap(3, RedGhostMap)

GhostsMap = InitGhostDistanceMap()

def GeneralGhostsMap(): #global map made with the four ghost maps
   global GhostsMap, PinkGhostMap, OrangeGhostMap, BlueGhostMap, RedGhostMap
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(GhostsMap[x][y] == sys.maxsize):
            continue
         else:
            GhostsMap[x][y] = min(PinkGhostMap[x][y], OrangeGhostMap[x][y], BlueGhostMap[x][y], RedGhostMap[x][y])

GeneralGhostsMap()

def CheckMovePac():
   global GhostsMap
   x,y = PacManPos
   L = PacManPossibleMove()
   # print([GhostsMap[elem[0]][elem[1]] for elem in L])
   L = list(filter(lambda pos: GhostsMap[x + pos[0]][y + pos[1]] > 3, L))
   if L:
      n_x, n_y = min(L, key=lambda pos: DistanceMap[x + pos[0]][y + pos[1]])
      return x + n_x, y + n_y
   else:
      n_x, n_y = random.choice(PacManPossibleMove())
      return x + n_x, y + n_y

def CheckWalls(idGhost, direction):
   if(direction=="left"):
      return True if TBL[Ghosts[idGhost][0]-1][Ghosts[idGhost][1]] == 1 else False
   elif(direction=="right"):
      return True if TBL[Ghosts[idGhost][0]+1][Ghosts[idGhost][1]] == 1 else False
   elif(direction=="up"):
      return True if TBL[Ghosts[idGhost][0]][Ghosts[idGhost][1]-1] == 1 else False
   else: #down
      return True if TBL[Ghosts[idGhost][0]][Ghosts[idGhost][1]+1] == 1 else False

def CheckPossibleMoves(idGhost): #possible directions for the ghosts
   count = 0
   PossibleMove = []
   if(TBL[Ghosts[idGhost][0]-1][Ghosts[idGhost][1]]==0):
      count += 1
      PossibleMove.append("left")
   if(TBL[Ghosts[idGhost][0]+1][Ghosts[idGhost][1]]==0):
      count += 1
      PossibleMove.append("right")
   if(TBL[Ghosts[idGhost][0]][Ghosts[idGhost][1]-1]==0):
      count += 1
      PossibleMove.append("up")
   if(TBL[Ghosts[idGhost][0]][Ghosts[idGhost][1]+1]==0):
      count += 1
      PossibleMove.append("down")
   return PossibleMove

def startingMoves(idGhost): #possible directions when the ghosts are in their house
   count = 0
   PossibleMove = []
   if(TBL[Ghosts[idGhost][0]-1][Ghosts[idGhost][1]]!=1):
      count += 1
      PossibleMove.append("left")
   if(TBL[Ghosts[idGhost][0]+1][Ghosts[idGhost][1]]!=1):
      count += 1
      PossibleMove.append("right")
   if(TBL[Ghosts[idGhost][0]][Ghosts[idGhost][1]-1]!=1):
      count += 1
      PossibleMove.append("up")
   if(TBL[Ghosts[idGhost][0]][Ghosts[idGhost][1]+1]!=1):
      count += 1
      PossibleMove.append("down")
   return PossibleMove

#################################################################
##
##  IA RANDOM

def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
def IA():
   global PacManPos, Ghosts, eaten, totalGum, gameStatus
   #deplacement Pacman
   x,y = CheckMovePac()
   PacManPos[0] = x
   PacManPos[1] = y
   EatingGUMS()
   if(eaten == totalGum):
      gameStatus = "won"
   for i in range(0,4):
      if(PacManPos[0] == Ghosts[i][0] and PacManPos[1] == Ghosts[i][1]):
         gameStatus = "GO"

   for i in range(0,4):
      PossibleMove = CheckPossibleMoves(i) if(TBL[Ghosts[i][0]][Ghosts[i][1]] == 0) else startingMoves(i)
      if(i == 0):
         PinkGhostMap[Ghosts[i][0]][Ghosts[i][1]] = 1
      elif(i == 1):
         OrangeGhostMap[Ghosts[i][0]][Ghosts[i][1]] = 1
      elif(i == 2):
         BlueGhostMap[Ghosts[i][0]][Ghosts[i][1]] = 1
      else:
         RedGhostMap[Ghosts[i][0]][Ghosts[i][1]] = 1
         
      if(len(PossibleMove)>=3 or CheckWalls(i,Ghosts[i][3])==True): #croisement ou L
         choix = random.randrange(len(PossibleMove))
         Ghosts[i][3] = PossibleMove[choix]


      if(Ghosts[i][3]=="right"):
         Ghosts[i][0] += 1 #right
      elif(Ghosts[i][3]=="left"):
         Ghosts[i][0] -= 1 #left
      elif(Ghosts[i][3]=="down"):
         Ghosts[i][1] += 1 #down
      else:
         Ghosts[i][1] -= 1 #up
   
      if(PacManPos[0] == Ghosts[i][0] and PacManPos[1] == Ghosts[i][1]):
         gameStatus = "GO"
      
#################################################################
##
##   GAME LOOP

def MainLoop():
   global gameStatus, PinkGhostMap, OrangeGhostMap, BlueGhostMap, RedGhostMap
   if(gameStatus == "playing"):
      IA()
      updateDistanceMap()
      GhostDistanceMap(0, PinkGhostMap)
      GhostDistanceMap(1, OrangeGhostMap)
      GhostDistanceMap(2, BlueGhostMap)
      GhostDistanceMap(3, RedGhostMap)
      GeneralGhostsMap()
      Affiche()
   elif(gameStatus == "won"):
      canvas.delete("all")
      canvas.create_rectangle(0, 0, screeenWidth, screenHeight, fill="blue")
      canvas.create_text(screeenWidth // 2, screenHeight- 300 , text = "Won !", fill ="white", font = PoliceTexte)
   else: #GO
      canvas.delete("all")
      canvas.create_rectangle(0, 0, screeenWidth, screenHeight, fill="black")
      canvas.create_text(screeenWidth // 2, screenHeight- 300 , text = "Game Over", fill ="red", font = PoliceTexte)     


###########################################:
#  demarrage de la fenetre - ne pas toucher

AfficherPage(0)
Window.mainloop()
   
   
    
   
   
