from random import randint
import numpy as np

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
            print("h",i," Player ", squares[i][0], " wins")
            state=squares[i][0]
            return state
    #vertical
    for i in range(1,4):
        if 0 in squares[:3,i-1:i]:
            #print("v",i-1," no win")
            continue
        elif(squares[:3,i-1:i][0][0]==squares[:3,i-1:i][1][0]==squares[:3,i-1:i][2][0]):
            print("v",i-1," Player ",squares[:3,i-1:i][1][0], " wins")
            state=squares[:3,i-1:i][1][0]
            return state 
    #diagonal
    if (squares[0][0]==squares[1][1]==squares[2][2]!=0):
        print("d1 Player", squares[0][0], " wins")
        state=squares[0][0]
        return state 
    if (squares[0][2]==squares[1][1]==squares[2][0]!=0):
        print("d2 Player", squares[0][2], " wins")
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
        print("new Board")
        winAbleBoards=[]
        blockAbleBoards=[]
        print("ArrayErstellt"+str(winAbleBoards))
        for i in range(0,3):
            for j in range(0,3):
                print("Board:"+str(i)+str(j))
                if Spiel.squares[i][j]==0:
                    print("not finished")
                    Board=j+3*i
                    Koordinaten=winPossible(Spiel, Board)
                    print("W:"+str(Koordinaten)+str(i)+str(j))
                    if Koordinaten!=0:
                        winAbleBoards.append([i,j])
                    Koordinaten=blockPossible(Spiel, Board)
                    print("B:"+str(Koordinaten)+str(i)+str(j))
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

def ComputerGegnerMCTS():
    #Expande->Select->Simulate->Update
        #get all posible moves
        #select move
            #choose Kirterium sqrt((2*ln(n_total))/n_i) +odds?
            #random (start)
        #simulate einmal ganz runter
        #update
    pass