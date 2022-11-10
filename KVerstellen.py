import os
f=open("/home/felix/Documents/Coding/python/HelloWorld/TicTacToe/newTTT/AutoKv.txt","w")

f.write("""#:kivy 2.0
<FeldButton@Button>:
    size_hint: 3/49, app.Window_ratio*3/49
    text: ""
    background_color: .9, .9, .9, 1
<BitteWartenScreen>:
Label:
    id:ComputerSpielt
    text: "Computer spielt gerade\\n Bitte warten"
    size_hint: 0.6, 0.2
    pos_hint: {"x":0.2, "y":0.5}
<SiegerScreen>:
    # Image:
    #     id:Background_winner
    #     source: app.BilderPath+'Confetti.gif'#'./Bilder/Confetti.gif'
    #     size_hint: 0.8, 0.8
    #     pos_hint:{"x":0.1, "y":0.25}
    #     anim_loop: 1
    Label:
        id: Sieger
        text: "X ("+app.PlOne+") hat Gewonnen"
        pos_hint:{"x":0.35, "y":0.65}
        size_hint: 0.3,0.1
        font_size:self.width*0.2
        bold: True
    Label:
        id:GameNr
        text:"Einzelspieler\\nSpiele: 1"
        pos_hint:{"x":0.1, "y":0.35}
        size_hint: 0.3,0.1
        halign: "left"
    Label:
        id:Stats
        text:"Von X Gewonnen: 1 (50%)\\nVon O Gewonnen: 1 (100%)\\n Unentschieden: 0 (0%)"
        pos_hint:{"x":0.5, "y":0.35}
        #text_size: self.size/2
        size_hint: 0.3,0.1
        halign: "left"
    Button:
        id:PlayAggain
        text: "Nochmal Spielen"
        on_press:root.btn("NewGame")
        pos_hint:{"x":0.1, "y":0.225}
        size_hint: 0.8,0.1
    Button:
        id:Hauptmenu
        text: "Hauptmenü"
        on_press:root.btn("Hauptmenu")
        pos_hint:{"x":0.1, "y":0.1}
        size_hint: 0.8,0.1
<Einstellungen>:
    Label:
        id:EinstellTitel
        text: "Einstellungen"
        pos_hint:{"x":0.35, "y":0.9}
        size_hint: 0.3,0.1
        bold: True
    Label:
        id:Spielm
        text: "Spielmodus:"
        pos_hint:{"x":0.1, "y":0.8}
        size_hint: 0.3,0.1
    Button:
        id:SpielModiNormal
        text: "normal"
        on_press:root.btn("SpielmodiNormal")
        pos_hint:{"x":0.4, "y":0.81}
        size_hint: 0.2,0.08
        background_color: 0, 1, 0, 5
        disabled: True
    Button:
        id:SpielModiJanni
        text: "Jannika Spezial"
        on_press:root.btn("SpielmodiJanni")
        pos_hint:{"x":0.6, "y":0.81} 
        size_hint: 0.3,0.08
        background_color: .9, .9, .9, 1
    Label:
        id:SpielModiErklärung
        text: "Erklärung der Spielmodi findest du in der Anleitung"
        pos_hint:{"x":0.1, "y":0.73}
        size_hint: 0.8,0.1
    Label:
        id:ComputerLvl
        text: "Schwierigkeit\\ndes Gegners:"
        pos_hint:{"x":0.1, "y":0.65}
        size_hint: 0.3,0.1
    Button:
        id:ComlvlZero
        text: "0"
        on_press:root.btn("Comlvl0")
        pos_hint:{"x":0.4, "y":0.67}
        size_hint: 0.125,0.05
        background_color: .9, .9, .9, 1
    Button:
        id:ComlvlOne
        text: "1"
        on_press:root.btn("Comlvl1")
        pos_hint:{"x":0.525, "y":0.67}
        size_hint: 0.125,0.05
        background_color: 0, 1, 0, 5
        disabled: True
    Button:
        id:ComlvlTwo
        text: "2"
        on_press:root.btn("Comlvl2")
        pos_hint:{"x":0.65, "y":0.67}
        size_hint: 0.125,0.05
        background_color: .9, .9, .9, 1
    Button:
        id:ComlvlThree
        text: "3"
        on_press:root.btn("Comlvl3")
        pos_hint:{"x":0.775, "y":0.67}
        size_hint: 0.125,0.05
        background_color: .9, .9, .9, 1
    Label:
        id:ComputerLvlErklaerung
        text: "Bei Level 2 hat der PC bis zu 2 Sec bedenkzeit,\\n bei Level 3 bis zu 4 Sec"
        pos_hint:{"x":0.1, "y":0.58}
        size_hint: 0.8,0.1
    Label:
        id:Player1Text
        text: "Spieler 1:"
        pos_hint:{"x":0.1, "y":0.5}
        size_hint: 0.3,0.1
    TextInput:
        id:Player1Input
        hint_text: "Spieler 1"
        text: app.PlOne
        pos_hint:{"x":0.4, "y":0.51}
        size_hint: 0.5,0.08
    Label:
        id:Player2Text
        text: "Spieler 2:"
        pos_hint:{"x":0.1, "y":0.4}
        size_hint: 0.3,0.1
    TextInput:
        id:Player2Input
        hint_text: "Spieler 2"
        text: app.PlTwo
        pos_hint:{"x":0.4, "y":0.41}
        size_hint: 0.5,0.08
    Button:
        id:Submit
        text: "Submit"
        on_press:root.btn("Submit")
        pos_hint:{"x":0.1, "y":0.25}
        size_hint: 0.8,0.1
    Button:
        id:Hauptmenu
        text: "Hauptmenü"
        on_press:root.btn("Hauptmenu")
        pos_hint:{"x":0.1, "y":0.1}
        size_hint: 0.8,0.1
<MainSite>:""")
############################# Canvas #############################5*self.height/27-
for i in range(0,9):
    f.write("""
    gr"""+str(i)+""": Green_Rect"""+str(i)+""".__self__
    bl"""+str(i)+""": Blue_Rect"""+str(i)+""".__self__
    re"""+str(i)+""": Red_Rect"""+str(i)+""".__self__""")
f.write("""\n
    canvas.before:
        Color:
            rgba: .5, .5, .5, 1
""")
for Lines in range(0,3):
    for Cols in range(0,3):
        f.write("""
        Rectangle:
            pos: 2*self.width/49+"""+str(Cols)+"""*16*self.width/49,self.height*0.8-9*self.width/49-"""+str(Lines)+"""*16*self.width/49 
            size: 13*self.width/49, 13*self.width/49
"""     )
for i in range(0,9):
    f.write("""
    GreenRect"""+str(i)+""":
        id: Green_Rect"""+str(i)+"""
    BlueRect"""+str(i)+""":
        id: Blue_Rect"""+str(i)+"""
    RedRect"""+str(i)+""":
        id: Red_Rect"""+str(i)+"""
""" )
############################# Titel #############################
f.write("""
    #Title
    Label:
        id:Title
        text: "Mega Tic Tac Toe"
        pos_hint:{"x":0.35, "y":0.9}
        size_hint: 0.3,0.1
    Label:
        id:PlayerAmZug
        text: "X ist am Zug"
        color: 0.2,0.2,1,1
        size_hint: 0.3, 0.1
        pos_hint:{"x":.6, "y":0.85}
    Label:
        id:PlayerAmZugName
        text: app.PlOne
        color: 0.2,0.2,1,1
        size_hint: 0.3, 0.1
        pos_hint:{"x":.6, "y":0.825}
    #Buttons
""")
############################# Buttons #############################
for BoardsY in range(0,3):
    f.write("#Line nr."+str(BoardsY)+"\n")
    for BoardsX in range(0,3):
        f.write("#Board nr."+str(BoardsX+3*BoardsY))
        for YinBoard in range (0,3):
            for XinBoard in range(0,3):
                f.write("""
    FeldButton:
        id: """+str(BoardsX+3*BoardsY)+str(XinBoard)+str(YinBoard)+"""
        on_press:root.Gamebtn("""+str(BoardsX+3*BoardsY)+""","""+str(XinBoard)+""","""+str(YinBoard)+""") #Board, x, y
        pos_hint:{"x":"""+str(3+4*XinBoard+16*BoardsX)+"""/49, "y":.8-"""+str(4*YinBoard+16*BoardsY)+"""/(49/app.Window_ratio)}
""")
f.write("""
    Label:
        id:MadeBy
        text: "Made by Felix"
        size_hint: 0.1, 0.1
        pos_hint:{"x":0.8, "y":0.05}
    Button:
        id: Hauptmenu
        text: "Hauptmenü"
        on_press:root.btn("Hauptmenu") #Board, x, y
        pos_hint:{"x":0.1, "y":0.075}
        size_hint: 0.3, 0.05
""")
############################# Dynamic Canvas #############################            
for Lines in range(0,3):
    for Cols in range(0,3):
        f.write("""
<GreenRect"""+str(Cols+3*Lines)+"""@Widget>:
    canvas:
        Color:
            rgba: 0, 1, 0, 0.5
        Rectangle:
            pos: 2*self.width/49+"""+str(Cols)+"""*16*self.width/49,self.height*0.8-9*self.width/49-"""+str(Lines)+"""*16*self.width/49 
            size: 13*self.width/49, 13*self.width/49
<BlueRect"""+str(Cols+3*Lines)+"""@Widget>:
    canvas:
        Color:
            rgba: 0, 0, 1, 1
        Rectangle:
            pos: 1*self.width/49+"""+str(Cols)+"""*16*self.width/49,self.height*0.8-10*self.width/49-"""+str(Lines)+"""*16*self.width/49 
            size: 1*self.width/49, 15*self.width/49
        Rectangle:
            pos: 2*self.width/49+"""+str(Cols)+"""*16*self.width/49,self.height*0.8-10*self.width/49-"""+str(Lines)+"""*16*self.width/49 
            size: 13*self.width/49, 1*self.width/49
        Rectangle:
            pos: 15*self.width/49+"""+str(Cols)+"""*16*self.width/49,self.height*0.8-10*self.width/49-"""+str(Lines)+"""*16*self.width/49 
            size: 1*self.width/49, 15*self.width/49
        Rectangle:
            pos: 2*self.width/49+"""+str(Cols)+"""*16*self.width/49,self.height*0.8+4*self.width/49-"""+str(Lines)+"""*16*self.width/49 
            size: 13*self.width/49, 1*self.width/49
<RedRect"""+str(Cols+3*Lines)+"""@Widget>:
    canvas:
        Color:
            rgba: 1, 0, 0, 1
        Rectangle:
            pos: 1*self.width/49+"""+str(Cols)+"""*16*self.width/49,self.height*0.8-10*self.width/49-"""+str(Lines)+"""*16*self.width/49 
            size: 1*self.width/49, 15*self.width/49
        Rectangle:
            pos: 2*self.width/49+"""+str(Cols)+"""*16*self.width/49,self.height*0.8-10*self.width/49-"""+str(Lines)+"""*16*self.width/49 
            size: 13*self.width/49, 1*self.width/49
        Rectangle:
            pos: 15*self.width/49+"""+str(Cols)+"""*16*self.width/49,self.height*0.8-10*self.width/49-"""+str(Lines)+"""*16*self.width/49 
            size: 1*self.width/49, 15*self.width/49
        Rectangle:
            pos: 2*self.width/49+"""+str(Cols)+"""*16*self.width/49,self.height*0.8+4*self.width/49-"""+str(Lines)+"""*16*self.width/49 
            size: 13*self.width/49, 1*self.width/49
"""         )
############################# Start Seite ############################# 
f.write("""
<StartSeite>:
    Label:
        id:TitleStartScreen
        text: "Mega Tic Tac Toe"
        pos_hint:{"x":0.35, "y":0.9}
        size_hint: 0.3,0.1
    Button:
        id: Continue
        text: "Continue"
        on_press:root.btn("Continue") #Board, x, y
        pos_hint:{"x":0.1, "y":0.8}
        size_hint: 0.8, 0.1
        disabled: True
    Button:
        id: StartNewGame
        text: "New Game"
        on_press:root.btn("NewGame") #Board, x, y
        pos_hint:{"x":0.1, "y":0.65}
        size_hint: 0.8, 0.1
    Button:
        id: Anleitung
        text: "Anleitung/ Regeln"
        on_press:root.btn("Anleitung") #Board, x, y
        pos_hint:{"x":0.1, "y":0.5}
        size_hint: 0.8, 0.1
    Button:
        id: Online
        text: "Online Game"
        on_press:root.btn("Online") #Board, x, y
        pos_hint:{"x":0.1, "y":0.35}
        size_hint: 0.8, 0.1
        disabled: True
    Button:
        id: Einstellungen
        text: "Einstellungen"
        on_press:root.btn("Einstellungen") #Board, x, y
        pos_hint:{"x":0.1, "y":0.2}
        size_hint: 0.8, 0.1
    Label:
        id:MadeBy
        text: "Made by Felix"
        size_hint: 0.1, 0.1
        pos_hint:{"x":0.8, "y":0.05}
""")
############################# SpielerAnzahlScreen ############################# 
f.write("""
<SpielerAnzahlScreen>:
    Label:
        id:TitleSpielerAnzahl
        text: "Wähle:"
        pos_hint:{"x":0.35, "y":0.9}
        size_hint: 0.3,0.1
        bold: True
    Button:
        id: Einzelspieler
        text: "Einzelspieler Game"
        on_press:root.btn("Einzelspieler") #Board, x, y
        pos_hint:{"x":0.1, "y":0.8}
        size_hint: 0.8, 0.1
    Button:
        id: Mehrspieler
        text: "Mehrspieler Game (lokal)"
        on_press:root.btn("Mehrspieler") #Board, x, y
        pos_hint:{"x":0.1, "y":0.65}
        size_hint: 0.8, 0.1
    Button:
        id: Hauptmenu
        text: "Hauptmenü"
        on_press:root.btn("Hauptmenu") #Board, x, y
        pos_hint:{"x":0.1, "y":0.5}
        size_hint: 0.8, 0.1
""")
############################# Anleitung ############################# 
f.write("""
<Anleitung>:
    Label:
        id:Anleitung
        text: "Anleitung"
        pos_hint:{"x":0.35, "y":0.9}
        size_hint: 0.3,0.1
        bold:True
    Label:
        id:Spielfeld
        text: '''Das Feld besteht aus einem großen Tic-Tac-Toe Feld. \\nIn jedem Feld befindet sich ein kleines Spielfeld.\\nEs gelten die Normalen Tic-Tac-Toe Regeln. Schafft man es \\nin einem kleinen Feld 3 in einer Reihe zu haben gewinnt man \\ndas Feld. Dieser Sieg gilt als Zeichen im großen Feld. \\nDurch 3 in einer Reihe im großen Feld gewinnt man das ganze \\nSpiel.\\n\\nDer erste Spieler darf frei wählen wo er spielt. \\nJeder weitere Spielzug ist abhängig vom Vorherigen. \\nBsp. X spielt im gewählten kleinen Feld rechts oben. So muss \\nder nächste Spieler im rechts oberen Board weiterspielen. \\nSpielt O dann in dem Bord in der Mitte, muss X im mittleren \\nBoard weiter spielen.\\n\\nEs gibt zwei verschiedene Spielmodi zur Auswahl\\nNormal: Wird man in ein Feld geschickt welches bereits ge-\\nwonnen ist, so darf man frei wählen wo man weiter spielen \\nmöchte.\\n\\nJannika Spezial: Wird man in ein Feld geschickt welches \\nbereits gewonnen ist, so muss in eines der \\nfreien Felder spiele aber darf danach im nächsten Board \\ndirekt nochmal (beachte die Anzeige wer am Zug ist).'''
        font_size:self.width*0.035
        line_wrap: True
        pos_hint:{"x":0.05, "y":0.6}
        size_hint: 0.9,0.05
        halign: "left"
    # Label:
    #     id:Springen
    #     text: '''Der erste Spieler darf frei wählen wo er spielt. \\nJeder weitere Spielzug ist abhängig vom Vorherigen. \\nBsp. X spielt im gewählten kleinen Feld rechts oben. So muss \\nder nächste Spieler im rechts oberen Board weiterspielen. \\nSpielt O dann in dem Bord in der Mitte, muss X im mittleren \\nBoard weiter spielen. '''
    #     font_size:self.width*0.035
    #     # pos_hint:{"x":0.05, "y":0.6}
    #     # size_hint: 0.9,0.05
    #     halign: "left"
    # Label:
    #     id:Spielmodus
    #     text: '''Es gibt zwei verschiedene Spielmodi zur Auswahl'''
    #     font_size:self.width*0.035
    #     # pos_hint:{"x":0.05, "y":0.5}
    #     # size_hint: 0.9,0.05
    #     #halign: "left"
    # Label:
    #     id:Spielmodusnomal
    #     text: '''Normal: Wird man in ein Feld geschickt welches bereits ge-\\nwonnen ist, so darf man frei wählen wo man weiter spielen \\nmöchte.'''
    #     font_size:self.width*0.035
    #     # pos_hint:{"x":0.05, "y":0.45}
    #     # size_hint: 0.9,0.05
    #     halign: "left"
    # Label:
    #     id:Spielmodusjanni
    #     text: '''Jannika Spezial: Wird man in ein Feld geschickt welches \\nbereits gewonnen ist, so muss in eines der \\nfreien Felder spiele aber darf danach im nächsten Board \\ndirekt nochmal (beachte die Anzeige wer am Zug ist).'''
    #     font_size:self.width*0.035
    #     # pos_hint:{"x":0.05, "y":0.38}
    #     # size_hint: 0.9,0.05
    #     halign: "left"
    Button:
        id: Zurueck
        text: "Zurück"
        on_press:root.btn("Zurueck") #Board, x, y
        pos_hint:{"x":0.1, "y":0.1}
        size_hint: 0.8, 0.1
""")
f.close()
os.rename("/home/felix/Documents/Coding/python/HelloWorld/TicTacToe/newTTT/AutoKv.txt","/home/felix/Documents/Coding/python/HelloWorld/TicTacToe/newTTT/spieloberfl.kv")
#        0 1 2 X
#     0  0|1|2
#     1  3|4|5
#     2  6|7|8
#     Y