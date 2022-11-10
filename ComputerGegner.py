from copy import deepcopy
from math import sqrt
from random import randint
import numpy as np
from time import time

############################################### Just Random lvl 0 ###############################################
def ComputerGegnerRandom(Board, Spiel, Game_app, BoardClosed=False):
    BoardX=randint(0,2)
    BoardY=randint(0,2)
    #Alle Felder im Board belegt
    if BoardClosed:
        Board=BoardX+3*BoardY
        while(Spiel.squares[BoardY][BoardX]!=0): ##such neues Board
            BoardX=randint(0,2)
            BoardY=randint(0,2)
            Board=BoardX+3*BoardY
            print("new Board")
            print(Board)
    print("Computer")
    X=randint(0,2) #random zahl
    Y=randint(0,2)
    print(Spiel.MapMap[Board].squares)
    print(Spiel.MapMap[Board].squares[Y][X])
    #checke ob feld frei ist
    i=0
    while Spiel.MapMap[Board].squares[Y][X]!=0:
        print("reroll"+str(X)+str(Y))
        X=randint(0,2) #random zahl
        Y=randint(0,2)
        i=i+1
        print(i)
        if i>100:
            print("pause")
            wait=input("Press Enter")
    print("Set "+str(X)+str(Y))
    print("Ende Computer")
    Game_app.Spieloberflaeche.Gamebtn(Board, X,Y)
############################################### Gewinne das aktuelle Feld lvl 1 ###############################################
def checkWin(squares): #returns winning player 1||2  or 0 if nobody has won, 9 if it is a draw
    #horizontal
    # if self.state!=0:
    #     return 0
    for i in range(0,3):
        if 0 in squares[i]:
            #print("h",i," no win")
            continue
        elif(squares[i][0]==squares[i][1]==squares[i][2]):
            print("h",i," Player ", squares[i][0], " possible win")
            state=squares[i][0]
            return state
    #vertical
    for i in range(1,4):
        if 0 in squares[:3,i-1:i]:
            #print("v",i-1," no win")
            continue
        elif(squares[:3,i-1:i][0][0]==squares[:3,i-1:i][1][0]==squares[:3,i-1:i][2][0]):
            print("v",i-1," Player ",squares[:3,i-1:i][1][0], " possible win")
            state=squares[:3,i-1:i][1][0]
            return state 
    #diagonal
    if (squares[0][0]==squares[1][1]==squares[2][2]!=0):
        print("d1 Player", squares[0][0], " possible win")
        state=squares[0][0]
        return state 
    if (squares[0][2]==squares[1][1]==squares[2][0]!=0):
        print("d2 Player", squares[0][2], " possible win")
        state=squares[0][2]
        return state 
    #unentschieden || not over
    for i in range(0,3):
        for j in range(0,3):
            if(squares[i][j]==0):
                return 0   # not over
    #unentschieden (keine 0er mehr)
    return 9

def winPossible(Spiel, Board): #can i win this borad in this Turn
    Feld=Spiel.MapMap[Board].squares
    for i in range(0,3):
        for j in range(0,3):
            #print(i,j,Feld, Spiel.MapMap[Board].squares)
            if Feld[i][j]==0:
                Feld[i][j]=2
                if checkWin(Feld)==2:
                    Feld[i][j]=0
                    Koordinate=[i, j]
                    return Koordinate
                else:
                    Feld[i][j]=0
    return 0 #no win possible

def blockPossible(Spiel, Board): #can i block the enemy in this Turn
    Feld=Spiel.MapMap[Board].squares
    for i in range(0,3):
        for j in range(0,3):
            if Feld[i][j]==0:
                Feld[i][j]=1
                if checkWin(Feld)==1:
                    Feld[i][j]=0
                    Koordinate=[i, j]
                    return Koordinate
                else:
                    Feld[i][j]=0
    return 0

def ComputerNurLokal(Board, Spiel, Game_app, BoardClosed=False):
    BoardX=randint(0,2)
    BoardY=randint(0,2)
    #Alle Felder im Board belegt
    if BoardClosed:
        # Board=BoardX+3*BoardY
        # while(Spiel.squares[BoardY][BoardX]!=0): ##such neues Board
        #     BoardX=randint(0,2)
        #     BoardY=randint(0,2)
        #     Board=BoardX+3*BoardY
        #     print("new Board")
        #     print(Board)
    #Welches Board
        #print("new Board")
        winAbleBoards=[]
        blockAbleBoards=[]
        #print("ArrayErstellt"+str(winAbleBoards))
        for i in range(0,3):
            for j in range(0,3):
                #print("Board:"+str(i)+str(j))
                if Spiel.squares[i][j]==0:
                    #print("not finished")
                    Board=j+3*i
                    Koordinaten=winPossible(Spiel, Board)
                    #print("W:"+str(Koordinaten)+str(i)+str(j))
                    if Koordinaten!=0:
                        winAbleBoards.append([i,j])
                    Koordinaten=blockPossible(Spiel, Board)
                    #print("B:"+str(Koordinaten)+str(i)+str(j))
                    if Koordinaten!=0:
                        blockAbleBoards.append([i,j])
        print("win"+str(winAbleBoards)+"\nblock"+str(blockAbleBoards))
        if len(winAbleBoards)!=0:
            Board=winAbleBoards[0][1]+3*winAbleBoards[0][0]
            print("new Board")
            print(Board)
        elif len(blockAbleBoards)!=0:
            Board=blockAbleBoards[0][1]+3*blockAbleBoards[0][0]
            print("new Board")
            print(Board)
        else:
            BoardX=randint(0,2)
            BoardY=randint(0,2)
            Board=BoardX+3*BoardY
            while(Spiel.squares[BoardY][BoardX]!=0): ##such neues Board
                BoardX=randint(0,2)
                BoardY=randint(0,2)
                Board=BoardX+3*BoardY
                print("new Board")
                print(Board)
    #Kann ich gewinnen
    Koordinaten=winPossible(Spiel, Board)
    if Koordinaten!=0:
        print("Com will gewinnen"+str(Koordinaten[0])+str(Koordinaten[1]))
        Y=Koordinaten[0]
        X=Koordinaten[1]
        Game_app.Spieloberflaeche.Gamebtn(Board, X,Y)
        return 1
    #kann ich blockieren
    Koordinaten=blockPossible(Spiel, Board)
    if Koordinaten!=0:
        print("Com will blocken"+str(Koordinaten[0])+str(Koordinaten[1]))
        Y=Koordinaten[0]
        X=Koordinaten[1]
        Game_app.Spieloberflaeche.Gamebtn(Board, X,Y)
        return 2
    #kann ich zwei in der Reihe
    Feld=Spiel.MapMap[Board].squares
    PositionenO=np.argwhere(Feld==2)
    PositionenX=np.argwhere(Feld==1)
    if PositionenO.size!=0: #hab ich bereits was in dem Feld
        if PositionenX.size==0: #gegner hat noch nix
            print("Spiele Mitte")
            X=1
            Y=1
            Game_app.Spieloberflaeche.Gamebtn(Board, X,Y)
            return 3
        #suche nach einer reihe mit Siegchance
        Diago1=[[0,0],[1,1],[2,2]]
        Diago2=[[0,2],[1,1],[2,0]]
        ZweierReihe=False
        test=0
        for i in PositionenO:
            print("suche freie Reihe")
            print(i)
            print(Feld)
            if not(1 in Feld[i[0]]): #freie Zeilen
                print("Zeile")
                Y=i[0]
                X=randint(0,2)
                while Feld[Y][X]!=0:
                    test=test+1
                    #print(X,Y,Feld[Y][X])
                    X=randint(0,2)
                    if test>20:
                        quit()
                ZweierReihe=True
                print("Zeile frei"+str(X)+str(Y))
            elif not(1 in Feld[i[0]]): #freie Spalten
                X=i[0]
                Y=randint(0,2)
                while Feld[Y][X]!=0:
                    Y=randint(0,2)
                ZweierReihe=True
                print("Spalte frei"+str(X)+str(Y))
            else:
                for k in Diago1:#Spiel auf der Diagonalen1
                    if np.array_equal(i,k):
                        if Feld[0][0]!=1 and Feld[1][1]!=1 and Feld[2][2]!=1:
                            j=randint(0,2)
                            X=Diago1[j][0]
                            Y=Diago1[j][1]
                            while Feld[Y][X]!=0:
                                j=randint(0,2)
                                X=Diago1[j][0]
                                Y=Diago1[j][1]
                            ZweierReihe=True
                            print("Diago1 frei"+str(X)+str(Y))
                for k in Diago2:
                    if np.array_equal(i,k):#Spiel auf der Diagonalen2
                        if Feld[0][2]!=1 and Feld[1][1]!=1 and Feld[2][0]!=1:
                            j=randint(0,2)
                            X=Diago2[j][0]
                            Y=Diago2[j][1]
                            while Feld[Y][X]!=0:
                                j=randint(0,2)
                                X=Diago2[j][0]
                                Y=Diago2[j][1]
                            ZweierReihe=True
                            print("Diago2 frei"+str(X)+str(Y)) 
            if ZweierReihe:
                Game_app.Spieloberflaeche.Gamebtn(Board, X,Y)
                return 4
        
    #Gewichtung für Anfangen
    print("Poso&PosX"+str(PositionenO)+str(PositionenX))
    if PositionenO.size==0 and PositionenX.size==0:
        Pos=randint(0,3)
        Ecken=[[0,0],[0,2],[2,0],[2,2]]
        X=Ecken[Pos][0]
        Y=Ecken[Pos][1]
        print("Es hat noch niemand gespielt"+str(X)+str(Y))
        Game_app.Spieloberflaeche.Gamebtn(Board, X,Y)
    else:
        print("Com spielt random")
        ComputerGegnerRandom(Board, Spiel, Game_app, BoardClosed)
    return 9
    
############################################### Kurz Vorherschauen lvl 2 ###############################################

def ComputerKurzVorrrausschau():
    #kann ich board gewinnen
        #->wo landet der Gegner
            #Gesamtsieg
            #kann er das gewinnen
                #hilft ihm der Gewinn
    #kann ich Gegner im Board blocken
         #->Wo landet der Gegner
            #kann er das gewinnen
                #hilft ihm der Gewinn
    #kann ich 2 in einer reihe
        #->Wo landet der Gegner
            #kann er das gewinnen
                #hilft ihm der Gewinn
    #wo soll der Gegner nicht hin
        #gewichtung?
    pass

############################################### MCTS lvl 3 ###############################################
#SimPlayer=2

def getAllPosMoves(Spiel, Board=999):
    if Board==999:#geh über alle Boards Rekursive?
        #print("alleBoards")
        possibleBoards={}
        for BoardY in range(0,3):
            for BoardX in range(0,3):
                #print(Spiel.squares)
                if Spiel.squares[BoardY][BoardX]!=0:
                    continue
                Board=BoardX+3*BoardY
                BoardName="Board"+str(Board)
                possibleBoards[BoardName]=getAllPosMoves(Spiel, Board)
        #print(possibleBoards['Board0'])
        return possibleBoards
    else: 
        #geh nur über die Felder im Board
        Feld=Spiel.MapMap[Board].squares
        possibleMoves=[]
        for i in range(0,3): #X
            for j in range(0,3): #Y
                if Feld[j][i]==0:
                    possibleMoves.append([i,j])
        return possibleMoves

# def Updatebewertung(Moves, Bewertung, Fall):
#     Wert=0
#     if Fall==1: #Spieler 1 gewinnt minimap
#         Wert=-0.1#update mit -0.1
#     if Fall==2: #Spieler 2 gewinnt minimap
#         Wert=0.1 #update +0.1
#     if Fall==9: #unentschieden minimap
#         Wert=0 #update mit +0
#     if Fall==3: #verloren Gesamt
#         Wert=-1 #update mit -1
#     if Fall==6: #Gewonnen gesamt
#         Wert=1 #update mit +1
#     if Fall==27: #Gesamtes Spiel Unentschieden
#         Wert=0
#     for Ebene in Moves:
#         for Board in Moves[Ebene]:
#             Bewertung[Ebene]['Sieg'+Board[-1]][Moves[Ebene][Board]]=Bewertung[Ebene]['Sieg'+Board[-1]][Moves[Ebene][Board]]+Wert
#             if Fall==3 or Fall==6 or Fall==27:
#                 Bewertung[Ebene]['Anzahl'+Board[-1]][Moves[Ebene][Board]]=Bewertung[Ebene]['Anzahl'+Board[-1]][Moves[Ebene][Board]]+1
#     #print("updateFunc")
#     # print(Moves[Ebene][Board])
#     # print(Bewertung[Ebene][Board])
#     #print(Bewertung)

def BoardNrToXY(BoardNr):
    if BoardNr<3:
        BoardY=0
    elif BoardNr<6:
        BoardY=1
    else:
        BoardY=2
    BoardX=BoardNr-3*BoardY
    return[BoardX, BoardY]

class TreeNode:
    def __init__(self,Board,X,Y,Anzahl, Punkte):
        self.Board=Board
        self.X=X
        self.Y=Y
        self.Anzahl=Anzahl
        self.Punkte=Punkte
        self.children=[] #Hier liegen die verknüpfungen zu den Kindern
        
    def expand(self, Simspiel, ZielBoard=999):
        #print("Expanding")
        posMoves={}
        Buff=getAllPosMoves(Simspiel, ZielBoard) #call getallmoves
        if ZielBoard!=999:
            posMoves['Board'+str(ZielBoard)]=Buff
        else:
            posMoves=Buff
        for BoardNr in posMoves:
            # print("länge"+str(len(posMoves[BoardNr])))
            # print(posMoves)
            for i in range(0, len(posMoves[BoardNr])):
                NodeBoard=int(BoardNr[-1])
                NodeX=posMoves[BoardNr][i][0]
                NodeY=posMoves[BoardNr][i][1]
                self.children.append(TreeNode(NodeBoard, NodeX,NodeY,0,0))# expand self.children
        # print(self.children)
        # print(len(self.children))
        # print(self.children[3].Board,self.children[3].X,self.children[3].Y)
        
    def select(self, Simspiel, ZielBoard, SimPlayer):
        if len(self.children)==0: #no children  # if neccesary Expand
            if ZielBoard!=999:
                BoardXY=BoardNrToXY(ZielBoard)
                if Simspiel.squares[BoardXY[1]][BoardXY[0]]!=0:
                    ZielBoard=999
            self.expand(Simspiel, ZielBoard) #Expande
        # calculate deciding value
        Bewertung=[]
        Anzahlen=[]
        Pkt=[]
        werte=[]
        wahr=[]
        for child in self.children:
            if child.Anzahl==0:
                Wert=1 #Anpassen
                Warsch=0
            else:
                Wert=sqrt((2*np.log(self.Anzahl))/(child.Anzahl)) #sqrt((2*ln(n_total))/n_i) +odds?
                
                Warsch=child.Punkte/child.Anzahl
            # werte.append(Wert)
            # wahr.append(Warsch)
            # Anzahlen.append(child.Anzahl)
            # Pkt.append(child.Punkte)
            Bewertung.append(Wert+Warsch)
        #find max value and choose
        # print("children")
        # print(self.children)
        if SimPlayer==2:
            Maximum=np.max(Bewertung)
        else:
            Maximum=np.min(Bewertung)
        indizis=np.where(Bewertung==Maximum)[0]
        zufallszahl=randint(0,indizis.size-1)
        Auswahl=self.children[indizis[zufallszahl]]
        #global SimPlayer
        #setzte im SimSpiel
        Status=Simspiel.PlaceSign(Auswahl.Board, Auswahl.X, Auswahl.Y, SimPlayer)
      #  if np.sum(Anzahlen)>0:
        # print("Bewertung")
        # print(Bewertung)
        # print("Wert")
        # print(werte)
        # print("Wahr")
        # print(wahr)
        # print("Anzahl")
        # print(Anzahlen)
        # print("punk")
        # print(Pkt)
        # print("m,i")
        # print(Maximum, indizis)
        # print("board, x,y,player,status")
        # print(Auswahl.Board, Auswahl.X, Auswahl.Y, SimPlayer, Status)
        # print("minimap "+str(Auswahl.Board))
        # print(Simspiel.MapMap[Auswahl.Board].squares)
        # print("megamap")
        # print(Simspiel.squares)
        # print("-------zugende-------")
        if Status!=3 and Status!=6 and Status!=27:
            #print("nach unten, Anzahl: "+str(self.Anzahl)+" Punkte: "+str(self.Punkte))
            #wechsel Spieler
            if SimPlayer==1: SimPlayer=2
            else: SimPlayer=1
            Status=Auswahl.select(Simspiel, Auswahl.X+3*Auswahl.Y, SimPlayer)#rekursive
        else: #aktualisiere das zielkind
            if Status==27: Punteänderung=0#-.1#pass #unentschieden
            elif Status==3: Punteänderung=-1 #Gegner gewinnt
            elif Status==6: Punteänderung=1 #Ich (com) gewinne
            Auswahl.Punkte+=Punteänderung
            Auswahl.Anzahl+=1
        ##aktualisiere alles nach oben
        if Status==27: Punteänderung=-.1#pass #unentschieden
        elif Status==3: Punteänderung=-1 #Gegner gewinnt
        elif Status==6: Punteänderung=1 #Ich (com) gewinne
        else: 
            print("Fehler")
            quit()
        self.Punkte+=Punteänderung
        self.Anzahl+=1
        
        #print("nach oben, Anzahl: "+str(self.Anzahl)+" Punkte: "+str(self.Punkte))
        return Status#return nach oben Sieg Niederlage & Anzahl

def ComputerGegnerMCTS(OrginalSpiel, Board, Game_app, Computerlvl, BoardClosed=False):
    #Expande->Select->Simulate->Update
    # Tree={}
    # Bewertung={}
    # Moves={}
    tree=TreeNode(0,0,0,0,0)
    if Computerlvl==2:
        Bedenkzeit=2
    else:
        Bedenkzeit=4
    start_time=time()
    for i in range(0,1000):
        #print("I="+str(i))
        SimSpiel=deepcopy(OrginalSpiel)
        SimPlayer=2
        if BoardClosed:
            Board=999
        tree.select(SimSpiel, Board, SimPlayer)
        # print("Megamap")
        # print(SimSpiel.squares)
        if time()-start_time>Bedenkzeit: #Time break
            break
    print("duration: "+str(time()-start_time))
    print("TREE infos")
    print(tree.Anzahl)
    Anzahlen=[]
    Bewertung=[]
    for child in tree.children:
        Anzahlen.append(child.Anzahl)
        Bewertung.append(child.Punkte)

    print(Anzahlen)
    print(Bewertung)
    #print("duration: "+str(time()-start_time))
    #Auswählen
    Maximum=np.max(Bewertung)
    indizis=np.where(Bewertung==Maximum)[0]
    zufallszahl=randint(0,indizis.size-1)
    Auswahl=tree.children[indizis[zufallszahl]]
    MaximumAnzahl=np.max(Anzahlen)
    indizisAnzahlen=np.where(Anzahlen==MaximumAnzahl)[0]
    if np.array_equal(indizisAnzahlen,indizis):
        print("Übereinstimmung Anzahl und Bewertung")
    #spiele das
    print("Anzahl:"+str(Auswahl.Anzahl)+" Punkte:"+str(Auswahl.Punkte))
    print("X:"+str(Auswahl.X)+" Y:"+str(Auswahl.Y))
    Game_app.Spieloberflaeche.Gamebtn(Auswahl.Board, Auswahl.X,Auswahl.Y)
    #return 0

    #ToDo:
    # entscheidung ändern wenn gegener zieht (*-1?)