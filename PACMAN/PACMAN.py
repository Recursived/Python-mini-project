import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
import sys
 

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
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
   return GUM
            
GUM = PlacementsGUM()   

PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"  ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange"] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"   ]     )         

 
 
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
##  IA RANDOM


      
def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x  ][y-1] == 2 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 2 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 2 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 2 ): L.append((-1,0))
   return L
   
def IA():
   global PacManPos, Ghosts
   #deplacement Pacman
   # L = PacManPossibleMove()
   # choix = random.randrange(len(L))
   x,y = CheckMove()
   PacManPos[0] = x
   PacManPos[1] = y
   # PacManPos[0] += L[choix][0]
   # PacManPos[1] += L[choix][1]
   
   #deplacement Fantome
   for F in Ghosts:
      L = GhostsPossibleMove(F[0],F[1])
      choix = random.randrange(len(L))
      F[0] += L[choix][0]
      F[1] += L[choix][1]

#################################################################
##
##   ADDINGS

def EatingGUMS():
   global score
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if(GUM[x][y] == 1):
            if(PacManPos[0]==x and PacManPos[1]==y):
               GUM[x][y]=0
               score += 1
               updateDistanceMap()

def InitDistanceMap():
   DistanceMap = np.zeros(TBL.shape)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if (TBL[x][y] == 1  or TBL[x][y] == 2): #ok ?
            DistanceMap[x][y] = sys.maxsize
         elif (GUM[x][y] == 1):
            DistanceMap[x][y] = 0
         else: #utile ?
            DistanceMap[x][y] = 100 #utile ?
   return DistanceMap

def updateDistanceMap():
   global DistanceMap
   DistanceMap = InitDistanceMap()
   true = 1
   while (true):
      # print("on reboucle")
      tmpDistanceMap = DistanceMap
      for y in range(HAUTEUR):
         for x in range(LARGEUR):
            if (DistanceMap[x][y] >= 0 and DistanceMap[x][y]<sys.maxsize and GUM[x][y]==0): #attention à ne pas sortir du jeu
               if(x-1 >=0):
                  left = DistanceMap[x-1][y]
               else:
                  left = sys.maxsize
               if(x+1<=LARGEUR):
                  right = DistanceMap[x+1][y]
               else:
                  right = sys.maxsize
               if(y+1<=HAUTEUR):
                  down = DistanceMap[x][y+1]
               else:
                  down = sys.maxsize
               if(y-1 >=0):
                  up = DistanceMap[x][y-1]
               else:
                  up = sys.maxsize
               minimum = min(left, right, up, down)
               if(minimum < DistanceMap[x][y]):
                  # print("avant :", DistanceMapTest[x][y])
                  DistanceMap[x][y] = minimum+1
                  # print("après : ", DistanceMapTest[x][y])
      if(tmpDistanceMap == DistanceMap).all():
         # print("on sort")
         #true = 0
         break

####### TESTS

T = [ [0,0,0,0,0],
        [0,1,1,1,0],
        [0,0,0,1,0],
        [1,1,0,1,0],
        [1,1,0,0,0],
   ]

def PlacementsGUMTest():  # placements des pacgums
   GUMT = np.zeros(TBL.shape)
   GUMT[2][0] = 1
   GUMT[4][4] = 1
   return GUMT
            
GUMT = PlacementsGUMTest()  
        
T = np.array(T,dtype=np.int32)
T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]

def InitDistanceMapTest():
   DistanceMapTest = np.zeros(TBL.shape)
   
   for x in range(5):
      for y in range(5):
         if (T[x][y] == 1  or T[x][y] == 2): #ok ?
            DistanceMapTest[x][y] = sys.maxsize
         elif (GUMT[x][y] == 1):
            DistanceMapTest[x][y] = 0
         else: #utile ?
            DistanceMapTest[x][y] = 100 #utile ?
   return DistanceMapTest

DistanceMapTest = InitDistanceMapTest()

def updateDistanceMapTest():
   global DistanceMapTest
   true = 1
   while (true):
      # print("on reboucle")
      tmpDistanceMap = DistanceMapTest
      for y in range(5):
         for x in range(5):
            if (DistanceMapTest[x][y] > 0 and DistanceMapTest[x][y]<sys.maxsize):
               if(x-1 >=0):
                  left = DistanceMapTest[x-1][y]
               else:
                  left = sys.maxsize
               if(x+1<=4):
                  right = DistanceMapTest[x+1][y]
               else:
                  right = sys.maxsize
               if(y+1<=4):
                  down = DistanceMapTest[x][y+1]
               else:
                  down = sys.maxsize
               if(y-1 >=0):
                  up = DistanceMapTest[x][y-1]
               else:
                  up = sys.maxsize
               minimum = min(left, right, up, down)
               if(minimum < DistanceMapTest[x][y]):
                  print("affichage")
                  AfficheDistanceMapTest()
                  # print("avant :", DistanceMapTest[x][y])
                  DistanceMapTest[x][y] = minimum+1
                  # print("après : ", DistanceMapTest[x][y])
      if(tmpDistanceMap == DistanceMapTest).all():
         # print("on sort")
         true = 0
         break

def AfficheDistanceMapTest():
   global DistanceMapTest
   for x in range(5):
      print("(",end='')
      for y in range(5):
         if(DistanceMapTest[y][x] > 1000):
            print("M", end='')
         else:
            print(DistanceMapTest[y][x], end='')
         print(",", end='')
      print(") \n")

#############

def CheckMove():
   x,y = PacManPos
   MinMove = sys.maxsize
   MinMoveX = sys.maxsize
   MinMoveY = sys.maxsize
   if(TBL[x-1][y] == 0 and DistanceMap[x-1][y]<MinMove and x-1>=0): #left
      # print("left :",MinMove)
      MinMove = DistanceMap[x-1][y]
      MinMoveX = x-1
      MinMoveY = y
   if(TBL[x+1][y] == 0 and DistanceMap[x+1][y]<MinMove and x+1<=LARGEUR): #right
      # print("right :",MinMove)
      MinMove = DistanceMap[x+1][y]
      MinMoveX = x+1
      MinMoveY = y
   if(TBL[x][y+1] == 0 and DistanceMap[x][y+1]<MinMove and y+1<=HAUTEUR): #down
      MinMove = DistanceMap[x][y+1]
      # print("down :",MinMove)
      MinMoveX = x
      MinMoveY = y+1
   if(TBL[x][y-1] == 0 and DistanceMap[x][y-1]<MinMove and y-1>=0): #up
      MinMove = DistanceMap[x][y-1]
      # print("up :",MinMove)
      MinMoveX = x
      MinMoveY = y-1
   # print("move : ",MinMove)
   return MinMoveX, MinMoveY


def AfficheDistanceMap():
   global DistanceMap
   for y in range(HAUTEUR):
      print("(",end='')
      for x in range(LARGEUR):
         if(DistanceMap[x][y] > 1000):
            print("M", end='')
         else:
            print(DistanceMap[x][y], end='')
         print(",", end='')
      print(") \n")
      
#################################################################
##
##   GAME LOOP

def MainLoop():
   updateDistanceMap()
   IA()
   EatingGUMS()
   AfficheDistanceMap()
   Affiche()
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

AfficherPage(0)
Window.mainloop()
   
