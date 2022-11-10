from os.path import isfile
import kivy
import sys
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.resources import resource_add_path, resource_find
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
from ComputerGegner import *
import numpy as np
from ast import literal_eval
import threading

    ######Debug
# OutP= open('./output.txt', 'w')
# OutP.write("Debug Hilfe\n")
# sys.stderr = OutP
# sys.stdout = sys.stderr

# from kivy.logger import LoggerHistory
# print('\n'.join([str(l) for l in LoggerHistory.history]))
    ######Debug Ende

resource_add_path('./Bilder')

Spieler=1
Einspieler=True
SpielEnde=False
Zweimal=False
OpenGame=False
SpielModi=1
PlayerOne=""
PlayerTwo=""
Computerlvl=2
GameStats=[[0,0,0,0],[0,0,0,0],[0,0,0,0]] #[local, Com, Online], lokal=(Game,Win,Lose,Draw)


class Megamap():
    def __init__(self):
        self.MapMap=[]
        for i in range(0,3):                        #0|1|2
            for j in range(0,3):                    #3|4|5
                self.MapMap.append(Map(i,j))        #6|7|8
        #print(self.MapMap[8].Index)
        self.squares=np.array([[0,0,0],[0,0,0],[0,0,0]]) #MegaPlayingfield
        self.state=0
        
    def checkWin(self): #returns winning player 1||2  or 0 if nobody has won, 9 if it is a draw
        #horizontal
        if self.state!=0:
            return 0
        for i in range(0,3):
            if 0 in self.squares[i]:
                #print("h",i," no win")
                continue
            elif(self.squares[i][0]==self.squares[i][1]==self.squares[i][2]):
                #print("h",i," Player ", self.squares[i][0], " wins")
                self.state=self.squares[i][0]
                return self.state
        #vertical
        for i in range(1,4):
            if 0 in self.squares[:3,i-1:i]:
                #print("v",i-1," no win")
                continue
            elif(self.squares[:3,i-1:i][0][0]==self.squares[:3,i-1:i][1][0]==self.squares[:3,i-1:i][2][0]):
                #print("v",i-1," Player ",self.squares[:3,i-1:i][1][0], " wins")
                self.state=self.squares[:3,i-1:i][1][0]
                return self.state 
        #diagonal
        if (self.squares[0][0]==self.squares[1][1]==self.squares[2][2]!=0):
            #print("d1 Player", self.squares[0][0], " wins")
            self.state=self.squares[0][0]
            return self.state 
        if (self.squares[0][2]==self.squares[1][1]==self.squares[2][0]!=0):
            #print("d2 Player", self.squares[0][2], " wins")
            self.state=self.squares[0][2]
            return self.state 
        #unentschieden || not over
        for i in range(0,3):
            for j in range(0,3):
                if(self.squares[i][j]==0):
                    return 0   # not over
        #unentschieden (keine 0er mehr)
        return 9
    def PlaceSign(self, MapNr, x, y, Player):
        MiniMapstate=self.MapMap[MapNr].SetSquare(x, y, Player)
        if MapNr>5:
            I=2
            J=MapNr-6
        elif MapNr>2:
            I=1
            J=MapNr-3
        else:
            I=0
            J=MapNr
        # print(I,J)
        if MiniMapstate>0:
            self.squares[I][J]=MiniMapstate
        self.state=self.checkWin()
        # print("Megamap")
        # print(self.squares)
        # print(self.state)
        if self.state>0:
            MiniMapstate=3*self.state
                # print("winner ges")
                # print(MiniMapstate)
        return MiniMapstate

class Map(Megamap):
    def __init__(self, Ix, Iy):
        self.Index=[Ix,Iy]
        self.squares=np.array([[0,0,0],[0,0,0],[0,0,0]]) #Playingfield
        self.state=0 #wining state player 1||2  or 0 if nobody has won
    def SetSquare(self, x, y, Player): #x=horizontal, y=vertical(down), Player=1||2
        self.squares[y][x]=Player
        #print(self.squares)
        return self.checkWin()

def writetoSettingsFile():
    # print("writing to File")
    f=open("./Settings.txt","w")
    f.write("Modi="+str(SpielModi)+"\nS1="+PlayerOne+"\nS2="+PlayerTwo+"\nComputerlvl="+str(Computerlvl)+"\nGamestats="+str(GameStats))
    f.close()

def writeStat(winner):
    global GameStats
    if Einspieler:
        Spiel=1 #write to ComGame
    else:
        Spiel=0 #write to lokalGame
    GameStats[Spiel][0]=GameStats[Spiel][0]+1#[0,0,0,0] #(Game,Win X,Lose X,Draw)
    if winner=="X":     XOD=1
    if winner=="O":     XOD=2
    if winner=="Draw":  XOD=3
    GameStats[Spiel][XOD]=GameStats[Spiel][XOD]+1
    writetoSettingsFile()

class BitteWartenScreen(FloatLayout):
    pass

class SiegerScreen(FloatLayout):
    def btn(self, Action):
        if Action=="NewGame":
            Game_app.Startseite.CreateNewGame()
        if Action=="Hauptmenu":
            global OpenGame
            OpenGame=False
            Button=Game_app.Startseite.ids["Continue"]
            Button.disabled=True
            Game_app.screen_manager.current="Start Seite"

class SpielerAnzahlScreen(FloatLayout):
    def btn(self, Action):
        global Einspieler, PlayerTwo
        if Action=="Einzelspieler":
            Einspieler=True
            PlayerTwo="Computer"
            Game_app.Startseite.CreateNewGame()
            Game_app.screen_manager.current="Spieloberfläche"
        if Action=="Mehrspieler":
            Einspieler=False
            Game_app.Startseite.CreateNewGame()
            Game_app.screen_manager.current="Spieloberfläche"
        if Action=="Hauptmenu":
            Game_app.screen_manager.current="Start Seite"

class Einstellungen(FloatLayout):
    def btn(self, Action):
        global SpielModi, PlayerOne, PlayerTwo, Computerlvl
        if Action=="SpielmodiNormal":
            SpielModi=1
            Button=self.ids["SpielModiJanni"]
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids["SpielModiNormal"]
            Button.background_color=(0, 1, 0, 5)
            Button.disabled=True
        if Action=="SpielmodiJanni":
            SpielModi=2
            Button=self.ids["SpielModiNormal"]
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids["SpielModiJanni"]
            Button.background_color=(0, 1, 0, 5)
            Button.disabled=True

        if Action=="Submit":
            PlayerOne=str(self.ids.Player1Input.text)
            PlayerTwo=str(self.ids.Player2Input.text)
            Game_app.PlOne=PlayerOne
            Game_app.PlTwo=PlayerTwo
            Game_app.screen_manager.current="Start Seite"
            
        if Action=="Comlvl0":
            Computerlvl=0
            Button=self.ids['ComlvlOne']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids['ComlvlTwo']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids['ComlvlThree']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids["ComlvlZero"]
            Button.background_color=(0, 1, 0, 5)
            Button.disabled=True
        if Action=="Comlvl1":
            Computerlvl=1
            Button=self.ids['ComlvlZero']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids['ComlvlTwo']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids['ComlvlThree']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids["ComlvlOne"]
            Button.background_color=(0, 1, 0, 5)
            Button.disabled=True
        if Action=="Comlvl2":
            Computerlvl=2
            Button=self.ids['ComlvlZero']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids['ComlvlOne']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids['ComlvlThree']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids["ComlvlTwo"]
            Button.background_color=(0, 1, 0, 5)
            Button.disabled=True
        if Action=="Comlvl3":
            Computerlvl=3
            Button=self.ids['ComlvlZero']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids['ComlvlOne']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids['ComlvlTwo']
            Button.background_color=(.9, .9, .9, 1)
            Button.disabled=False
            Button=self.ids["ComlvlThree"]
            Button.background_color=(0, 1, 0, 5)
            Button.disabled=True

        #write changes to File
        writetoSettingsFile()
        if Action=="NewGame":
            Game_app.Startseite.CreateNewGame()
        if Action=="Hauptmenu":
            Game_app.screen_manager.current="Start Seite"

class MainSite(FloatLayout):
    gr0=ObjectProperty(None)
    gr1=ObjectProperty(None)
    gr2=ObjectProperty(None)
    gr3=ObjectProperty(None)
    gr4=ObjectProperty(None)
    gr5=ObjectProperty(None)
    gr6=ObjectProperty(None)
    gr7=ObjectProperty(None)
    gr8=ObjectProperty(None)
    bl0=ObjectProperty(None)
    bl1=ObjectProperty(None)
    bl2=ObjectProperty(None)
    bl3=ObjectProperty(None)
    bl4=ObjectProperty(None)
    bl5=ObjectProperty(None)
    bl6=ObjectProperty(None)
    bl7=ObjectProperty(None)
    bl8=ObjectProperty(None)
    re0=ObjectProperty(None)
    re1=ObjectProperty(None)
    re2=ObjectProperty(None)
    re3=ObjectProperty(None)
    re4=ObjectProperty(None)
    re5=ObjectProperty(None)
    re6=ObjectProperty(None)
    re7=ObjectProperty(None)
    re8=ObjectProperty(None)
    BitteWartenPopUp=Popup(title="Bitte Warten", content=BitteWartenScreen(), size_hint=(0.8,0.3))
    Green=[gr0,gr1,gr2,gr3,gr4,gr5,gr6,gr7,gr8]
    def __init__(self, **kwargs): #Startup
        super().__init__(**kwargs)
        test=self.Green[0]
        print('here test')
        print(test)
        print('nicht test')
        print(self.gr0)
        print(Window.width)
        #self.remove_widget(test)

    def setGreen(self,Board):
        try: self.remove_widget(self.gr0)
        except: print("g0 Fehler")
        try: self.remove_widget(self.gr1)
        except: print("g1 Fehler")
        try: self.remove_widget(self.gr2)
        except: print("g2 Fehler")
        try: self.remove_widget(self.gr3)
        except: print("g3 Fehler")
        try: self.remove_widget(self.gr4)
        except: print("g4 Fehler")
        try: self.remove_widget(self.gr5)
        except: print("g5 Fehler")
        try: self.remove_widget(self.gr6)
        except: print("g6 Fehler")
        try: self.remove_widget(self.gr7)
        except: print("g7 Fehler")
        try: self.remove_widget(self.gr8)
        except: print("g8 Fehler")
        if Board==0: self.add_widget(self.gr0,0,"before")
        elif Board==1: self.add_widget(self.gr1,0,"before")
        elif Board==2: self.add_widget(self.gr2,0,"before")
        elif Board==3: self.add_widget(self.gr3,0,"before")
        elif Board==4: self.add_widget(self.gr4,0,"before")
        elif Board==5: self.add_widget(self.gr5,0,"before")
        elif Board==6: self.add_widget(self.gr6,0,"before")
        elif Board==7: self.add_widget(self.gr7,0,"before")
        elif Board==8: self.add_widget(self.gr8,0,"before")
        if Board=="All":
            self.add_widget(self.gr0,0,"before")
            self.add_widget(self.gr1,0,"before")
            self.add_widget(self.gr2,0,"before")
            self.add_widget(self.gr3,0,"before")
            self.add_widget(self.gr4,0,"before")
            self.add_widget(self.gr5,0,"before")
            self.add_widget(self.gr6,0,"before")
            self.add_widget(self.gr7,0,"before")
            self.add_widget(self.gr8,0,"before")

    def resetButtons(self): #resets all buttons for new game
        for Boards in range(0,9): 
            for Line in range(0,3):
                for Cel in range(0,3):
                    ID=str(Boards)+str(Line)+str(Cel)
                    Button=self.ids[ID]
                    Button.disabled=False
                    Button.text=""
                    Button.background_color=(0.9,0.9,0.9,1)
        self.setGreen("All")
        Label=self.ids['PlayerAmZug']
        Label.text="X ist am Zug"
        Label.color=(0.2,0.2,1,1)
        LabelZwei=self.ids['PlayerAmZugName']
        LabelZwei.text=PlayerOne
        LabelZwei.color=(0.2,0.2,1,1)
        global Spieler
        Spieler=1
        self.remove_widget(self.bl0)
        self.remove_widget(self.bl1)
        self.remove_widget(self.bl2)
        self.remove_widget(self.bl3)
        self.remove_widget(self.bl4)
        self.remove_widget(self.bl5)
        self.remove_widget(self.bl6)
        self.remove_widget(self.bl7)
        self.remove_widget(self.bl8)
        self.remove_widget(self.re0)
        self.remove_widget(self.re1)
        self.remove_widget(self.re2)
        self.remove_widget(self.re3)
        self.remove_widget(self.re4)
        self.remove_widget(self.re5)
        self.remove_widget(self.re6)
        self.remove_widget(self.re7)
        self.remove_widget(self.re8)

    def disableBtns(self,Board):
        for Boards in range(0,9): #disable all buttons
            for Line in range(0,3):
                for Cel in range(0,3):
                    ID=str(Boards)+str(Line)+str(Cel)
                    Button=self.ids[ID]
                    Button.disabled=True
        if Board=="All" and (abs(Spieler)==1 or not Einspieler):
            for Boards in range(0,9):
                for Line in range(0,3): #enable write buttons
                    for Cel in range(0,3):
                        ID=str(Boards)+str(Line)+str(Cel)
                        Button=self.ids[ID]
                        if Button.text!="X" and Button.text!="O":
                            Button.disabled=False
        elif abs(Spieler)==1 or not Einspieler:
            for Line in range(0,3): #enable write buttons
                for Cel in range(0,3):
                    ID=str(Board)+str(Line)+str(Cel)
                    Button=self.ids[ID]
                    if Button.text!="X" and Button.text!="O":
                        Button.disabled=False

    def SetWinnerMiniMap(self, Board, Winner):
        if Winner==1:
            if Board==0: self.add_widget(self.bl0,0,"before")
            elif Board==1: self.add_widget(self.bl1,0,"before")
            elif Board==2: self.add_widget(self.bl2,0,"before")
            elif Board==3: self.add_widget(self.bl3,0,"before")
            elif Board==4: self.add_widget(self.bl4,0,"before")
            elif Board==5: self.add_widget(self.bl5,0,"before")
            elif Board==6: self.add_widget(self.bl6,0,"before")
            elif Board==7: self.add_widget(self.bl7,0,"before")
            elif Board==8: self.add_widget(self.bl8,0,"before")
        elif Winner==2:
            if Board==0: self.add_widget(self.re0,0,"before")
            elif Board==1: self.add_widget(self.re1,0,"before")
            elif Board==2: self.add_widget(self.re2,0,"before")
            elif Board==3: self.add_widget(self.re3,0,"before")
            elif Board==4: self.add_widget(self.re4,0,"before")
            elif Board==5: self.add_widget(self.re5,0,"before")
            elif Board==6: self.add_widget(self.re6,0,"before")
            elif Board==7: self.add_widget(self.re7,0,"before")
            elif Board==8: self.add_widget(self.re8,0,"before")
        
    def Gamebtn(self, Board, X, Y):
        #Verarbeite input
        BoardClosed=False
        ID=str(Board)+str(X)+str(Y)
        Button=self.ids[ID]
        Label=self.ids['PlayerAmZug']
        LabelZwei=self.ids['PlayerAmZugName']
        global Spieler, Zweimal, PlayerOne, PlayerTwo, Einspieler, SpielEnde, Computerlvl
        if Spieler<0:
            Spieler=Spieler*(-1)
            Zweimal=True
            print("darf Zweimal",Zweimal)
        ret=Spiel.PlaceSign(Board,X,Y,Spieler) #call backend
        #print("Hat Jemand gewonnen?"+str(ret))
        if ret>0:
            if ret==1: #Spieler 1 gewinnt minimap
                self.SetWinnerMiniMap(Board, ret)
            if ret==2: #Spieler 2 gewinnt minimap
                self.SetWinnerMiniMap(Board, ret)
            if ret>2 and ret!=9: #Gewinnt Gesamtes Spiel oder Unentschieden
                self.SetWinnerMiniMap(Board, ret/3)
                self.show_Endscreen(ret)
        if Spieler==1:
            Button.text="X"
            Button.background_color=(0,0,1,1)
            if not Zweimal:
                Label.text="O ist am Zug"
                Label.color=(1,0.2,0.2,1)
                LabelZwei.text=PlayerTwo
                LabelZwei.color=(1,0.2,0.2,1)
                print("ändereSpieler")
                Spieler=2
            Zweimal=False
        else:
            Button.text="O"
            Button.background_color=(1,0,0,1)
            if not Zweimal:
                Label.text="X ist am Zug"
                Label.color=(0.2,0.2,1,1)
                LabelZwei.text=PlayerOne
                LabelZwei.color=(0.2,0.2,1,1)
                Spieler=1
            Zweimal=False
        # gehe zu nächsten board
        ##### Wenn zielfeld bereits gespielt #####
        if Spiel.squares[Y][X]!=0: #Feld ist bereits gewonnen
            print("feld bereits geschlossen")
            #Spielmodi "normal"
            if SpielModi==1:
                BoardClosed=True
                self.disableBtns('All')    #schalte alle Buttons frei
                self.setGreen('All')#schalte alle state=0 Felder grün
                for i in range(0,3): #geh über alle boards 
                    for j in range(0,3):
                        if Spiel.squares[i][j]!=0: #wenn state !=0 deaktiviere grün und Button
                            BoardDeakt=j+3*i
                            if   BoardDeakt==0: self.remove_widget(self.gr0)
                            elif BoardDeakt==1: self.remove_widget(self.gr1)
                            elif BoardDeakt==2: self.remove_widget(self.gr2)
                            elif BoardDeakt==3: self.remove_widget(self.gr3)
                            elif BoardDeakt==4: self.remove_widget(self.gr4)
                            elif BoardDeakt==5: self.remove_widget(self.gr5)
                            elif BoardDeakt==6: self.remove_widget(self.gr6)
                            elif BoardDeakt==7: self.remove_widget(self.gr7)
                            elif BoardDeakt==8: self.remove_widget(self.gr8)
                            for Line in range(0,3):
                                for Cel in range(0,3):
                                    ID=str(BoardDeakt)+str(Line)+str(Cel)
                                    Button=self.ids[ID]
                                    Button.disabled=True
                
            #Spielmodi "Jannika Spezial"
            elif SpielModi==2:
                Spieler=Spieler*(-1)# Spieler darf 2 mal
                self.setGreen(X+3*Y)
                self.disableBtns(X+3*Y)
        else:
            self.setGreen(X+3*Y)
            self.disableBtns(X+3*Y)
        def CallBFunc(dt):
            ComputerGegnerMCTS(Spiel, X+3*Y,Game_app, Computerlvl, BoardClosed)            

        #workthread=threading.Thread(target=ComputerGegnerMCTS(Spiel, X+3*Y,Game_app, Computerlvl, BoardClosed))
        if Einspieler and (not SpielEnde) and (Spieler==2 or Spieler==-2): #schucke Computer Gegner an
            #self.BitteWartenPopUp.open()
            print("Computer ist dran, lvl"+str(Computerlvl))
            if Computerlvl==0: ComputerGegnerRandom(X+3*Y, Spiel, Game_app, BoardClosed)
            if Computerlvl==1: ComputerNurLokal(X+3*Y, Spiel, Game_app, BoardClosed)
            if Computerlvl==2 or Computerlvl==3: 
                #Clock.schedule_once(self.disableBtns, 0)
                Clock.schedule_once( CallBFunc,0)
        #Clock.schedule_once(self.BitteWartenPopUp.dismiss,0.001)
        #self.BitteWartenPopUp.dismiss()
        


    def btn(self, Action):
        if Action=="Hauptmenu":
            global OpenGame
            OpenGame=True
            Button=Game_app.Startseite.ids["Continue"]
            Button.disabled=False
            Game_app.screen_manager.current="Start Seite"
        if Action=="NewGame":
            Game_app.Startseite.CreateNewGame()
    def show_Endscreen(self, Sieger):
        global SpielEnde
        Label=Game_app.Endscreen.ids['Sieger']
        if Sieger==3:
            Label.text="X ("+str(Game_app.PlOne)+") hat Gewonnen"
            Label.color=(0.2,0.2,1,1)
            writeStat("X")
        elif Sieger==6:
            Label.text="O ("+str(Game_app.PlTwo)+") hat Gewonnen"
            Label.color=(1,0.2,0.2,1)
            writeStat("O")
        elif Sieger==3*9:
            Label.text="Unentschieden"
            Label.color=(1,1,1,1)
            writeStat("Draw")
        LabelZwei=Game_app.Endscreen.ids['GameNr']
        if Einspieler:
            LabelZwei.text="Einzelspieler\nSpiele: "+str(GameStats[1][0])
            SpielStat=1
        else:
            LabelZwei.text="Mehrspieler\n(lokal)\nSpiele: "+str(GameStats[0][0])
            SpielStat=0
        LabelDrei=Game_app.Endscreen.ids['Stats']
        LabelDrei.text="Von X Gewonnen: "+str(GameStats[SpielStat][1])+" ("+str(round(100*GameStats[SpielStat][1]/GameStats[SpielStat][0],2))+"%)\nVon O Gewonnen: "+str(GameStats[SpielStat][2])+" ("+str(round(100*GameStats[SpielStat][2]/GameStats[SpielStat][0],2))+"%)\n Unentschieden: "+str(GameStats[SpielStat][3])+" ("+str(round(100*GameStats[SpielStat][3]/GameStats[SpielStat][0],2))+"%)"
        SpielEnde=True
        Game_app.screen_manager.current="Endscreen"

class StartSeite(FloatLayout):
    def __init__(self, **kwargs): #Startup
        super().__init__(**kwargs)
    def CreateNewGame(self):
        global Spiel, SpielEnde
        Spiel=Megamap()
        SpielEnde=False
        Game_app.Spieloberflaeche.resetButtons()
        Game_app.screen_manager.current="SpielerAnzahlScreen"
    def btn(self, Action):
        if Action=="NewGame":
            self.CreateNewGame()
        if Action=="Anleitung":
            Game_app.screen_manager.current="Anleitung"
        if Action=="Continue":
            Game_app.screen_manager.current="Spieloberfläche"
        if Action=="Einstellungen":
            Game_app.screen_manager.current="Einstellungen"
    def enableContinue(self):
        pass

class Anleitung(FloatLayout):
    def __init__(self, **kwargs): #Startup
        super().__init__(**kwargs)
    def btn(self, Action):
        if Action=="Zurueck":
            Game_app.screen_manager.current="Start Seite"


class Spieloberfl(App):
    # Window_width=NumericProperty(Window.width) #*app.Test_var 
    # Window_height=NumericProperty(Window.height)
    PlOne=ObjectProperty(PlayerOne)
    PlTwo=ObjectProperty(PlayerTwo)
    #Window.size = (1080/2.5,2273/2.5) #Simulate phone size on PC
    print('Find')
    print(resource_find('Bilder'))
    print(resource_find('Confetti.gif'))
    BilderPath= ObjectProperty(resource_find('Bilder')) #app.TestText# #TestText="paul"
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(Window.width/Window.height)
    print(Window.size)
    Window_ratio=NumericProperty(Window.width/Window.height)
    #TestText= ObjectProperty("Hallllo") #app.TestText# #TestText="paul"
    def build(self):
        self.screen_manager=ScreenManager() 

        self.Startseite=StartSeite()
        screen = Screen(name="Start Seite")
        screen.add_widget(self.Startseite)
        self.screen_manager.add_widget(screen)

        self.Spieloberflaeche=MainSite()
        screen = Screen(name="Spieloberfläche")
        screen.add_widget(self.Spieloberflaeche)
        self.screen_manager.add_widget(screen)

        self.Anleitung=Anleitung()
        screen = Screen(name="Anleitung")
        screen.add_widget(self.Anleitung)
        self.screen_manager.add_widget(screen)

        self.Endscreen=SiegerScreen()
        screen = Screen(name="Endscreen")
        screen.add_widget(self.Endscreen)
        self.screen_manager.add_widget(screen)

        self.Einstellungen=Einstellungen()
        screen = Screen(name="Einstellungen")
        screen.add_widget(self.Einstellungen)
        self.screen_manager.add_widget(screen)

        self.SpielerAnzahlScreen=SpielerAnzahlScreen()
        screen =Screen(name="SpielerAnzahlScreen")
        screen.add_widget(self.SpielerAnzahlScreen)
        self.screen_manager.add_widget(screen)

        if isfile("./Settings.txt"):
            global SpielModi, PlayerOne, PlayerTwo, Computerlvl, GameStats
            f=open("./Settings.txt","r")
            Data=f.read().split("\n")#lese die Daten ein
            SpielModi=int(Data[0].split("=")[1])
            PlayerOne=Data[1].split("=")[1]
            PlayerTwo=Data[2].split("=")[1]
            Computerlvl=int(Data[3].split("=")[1])
            GameStats=literal_eval(Data[4].split("=")[1])
            print("GameStats")
            print(GameStats)
            f.close()
            self.PlOne=PlayerOne
            self.PlTwo=PlayerTwo
            #set right butten as activated in Settings
            if SpielModi==1: self.Einstellungen.btn('SpielmodiNormal')
            elif SpielModi==2: self.Einstellungen.btn('SpielmodiJanni')
            if Computerlvl==0: self.Einstellungen.btn("Comlvl0")
            elif Computerlvl==1: self.Einstellungen.btn("Comlvl1")
            elif Computerlvl==2: self.Einstellungen.btn("Comlvl2")
            elif Computerlvl==3: self.Einstellungen.btn("Comlvl3")
        else:
            self.screen_manager.current="Einstellungen"
        return self.screen_manager
    
if __name__=="__main__":
    Simgame=Megamap()
    Spiel=Megamap()
    Game_app= Spieloberfl()
    Game_app.run()

#ToDo:
# bocken solange computer rechnet
# computer zeitbegrenzt
# set green fehler
# children anschauen ob das passt
# kiterum anschauen bzw mal experimentell gewichten
#schneller
    # im gleichen Baum bleiben?
    # multitask 
    # schneller in C?



#Brenda spezial -> man darf immer überall
#Jannika Spezial -> lande in vollem feld (letzer zug==gleiches feld?)
#regeln/Anleitung Anordung & Bilder
#Bilder machen
#verschiedene Spielstände
#online
#com
    #Monte-carlo tree
    #api
    #random gegner
    #tree vill erst für 3x3



#To Deploy to apk
#buildozer -v android debug deploy run
#adb logcat -s python (~/.buildozer/android/platform/android-sdk/platform-tools/)
#adb shell -> run-as org.test.myapp
#https://pythonprogramming.net/packaging-deployment-kivy-application-python-tutorial/