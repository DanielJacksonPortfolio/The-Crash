#                                   TO FIX
#   ____________________________________________________________________________
#   TOO FAST UNFADING ON POP UP MENU QUIT
#   THE POP UP MENU BREAKS IF YOU PRESS BUTTON TOO EARLY
#   _____________________________________________________________________________

#                                   TO DO
#   ____________________________________________________________________________
#   LOAD GAME



import sys, pygame, time
from pygame.locals import *

##import cProfile
##import re
##cProfile.run('re.compile("foo|bar")')

#FUNCTIONS

def buttonify(Picture,width,height, coords, surface): #The generic code for making a button. Takes in the image, size and the coords
    image = pygame.transform.scale(pygame.image.load(Picture).convert_alpha(),(int(width*sscale),int(height*sscale)))
    imagerect = image.get_rect()
    imagerect.topright = coords
    surface.blit(image,imagerect)
    return (image,imagerect)

def colorPulse(colorMult,fade): #Pulses the color of the the text on the start screen
    if colorMult == 100:
        fade = True
    elif colorMult == 250:
        fade = False
    if fade == False:
        colorMult -= 1
    elif fade:
        colorMult += 1
    return (colorMult,fade)

def textify(font,text,antiA,color,coords,surface): # Used to blit any giv text to the screen.Takes in the font, text, anit aliasing bool, color, coordinates
    image = font.render(text,antiA,color)
    surface.blit(image,coords)
    return image

def lightSwitch(lightImage,lft,speed): # Blinks the light object between green and red
    if lft >= speed:
        lft = 0
        if lightImage == "Images/TUTORIAL/REDLIGHT.png":
            lightImage = "Images/TUTORIAL/GREENLIGHT.png"
        else:
            lightImage = "Images/TUTORIAL/REDLIGHT.png"
    return [lightImage,lft]

def menuGlide():# Glides the menu box in and out when a button is clicked
    global flags,sscale,menuBoxX,menuButtonX,menuGlideMult,menuTextX
    
    if flags["MenuGlideIn"]:
        if menuBoxX*sscale < 0:
            menuBoxX += menuGlideMult//10
            menuButtonX += menuGlideMult//10
            menuTextX += menuGlideMult//10
        else:
            flags["MenuGlideIn"] = False
        menuGlideMult -= 1

    if flags["MenuGlideOut"]:
        if menuBoxX*sscale > -460*sscale:
            menuBoxX -= menuGlideMult//10
            menuButtonX -= menuGlideMult//10
            menuTextX -= menuGlideMult//10
        else:
            flags["MenuGlideOut"] = False
        menuGlideMult -= 1

def fadeInitialize(fadeWaitV,ftv,fadeSpeedV,fadeAlphaV): # Used to initialize the fadeing out of the screen
    global fadeWait, ft, fadeSpeed, fadeAlpha
    
    fadeWait = fadeWaitV
    ft = ftv
    fadeSpeed = fadeSpeedV
    fadeAlpha = fadeAlphaV

def menuGlideInitialize(): # Initalizes the menu glide
    global menuGlideMult, menuBoxX, menuButtonX, menuTextX
    
    menuGlideMult = 100
    menuBoxX = -460
    menuButtonX = -300
    menuTextX = -345

def get_music(area): # Changes the music currently playing
    playlist = []
    if area == 1:
        playlist = ["Sounds/OGG/START.ogg"]
    elif area == 2:
        playlist = ["Sounds/OGG/WE BUILT THIS CITY.ogg"]
    return playlist

def deactivateButtons(): # gets rid of the highlights on every inventory command
    global flags
    flags["OpenButtonActive"] = False
    flags["CloseButtonActive"] = False
    flags["PushButtonActive"] = False
    flags["PullButtonActive"] = False
    flags["LookAtButtonActive"] = False
    flags["GiveButtonActive"] = False
    flags["TalkToButtonActive"] = False
    flags["PickUpButtonActive"] = False
    flags["UseButtonActive"] = False
        
#PYGAME STUFF

pygame.init()#Initializes pygame

infoObject = pygame.display.Info()

#This calculates the screen size and then maximises the windo placing black bars in the gaps
sscale = infoObject.current_h/700
if 1000*sscale < infoObject.current_w:
    barTop = False
    barSizeX = (infoObject.current_w - (1000*sscale))/2
    barSizeY = 0
    screenWidth = 1000*sscale+2*barSizeX
    screenHeight = 700*sscale
else:
    barTop = True
    sscale = infoObject.current_w/1000
    barSizeY = (infoObject.current_h-64 - (700*sscale))/2
    barSizeX = 0
    screenWidth = 1000*sscale
    screenHeight = 700*sscale+2*barSizeY

#Initializes the surfaces

screen = pygame.display.set_mode((int(screenWidth),int(screenHeight)))
fadeSurface = pygame.Surface((int(screenWidth),int(screenHeight)))
popUpScreen = pygame.display.set_mode((int(screenWidth),int(screenHeight)))

clock = pygame.time.Clock()
fps = 60
textFPS = 100

#Counters

bpt = 0 #Button Pressed Timer
it = 0 # Intro Timer
fpst = 0 # FPS Timer
lft = 0 # Light Flicker Timer

#FADING

fadeInitialize(100,0,20,0)

#FLAGS

Inventory = [
              ]

# These are the flags. These make up most of the game as they dictate the current game state. n the future these will be used for saving
flags = {"ShowStart":True,
         "ShowMenu":False,
         "ShowLoadMenu":False,
         "ShowSettingsMenu":False,
         "ShowIntroCutscene":False,
         "ShowTutorialBridge":False,
         "ShowTutorialEngine":False,
         "StartButtonPressed":False,
         "NewGameButtonPressed":False,
         "LoadGameButtonPressed":False,
         "SettingsButtonPressed":False,
         "BackButtonPressed":False,
         "LoadGameButton1Pressed":False,
         "LoadGameButton2Pressed":False,
         "LoadGameButton3Pressed":False,
         "LoadBackButtonPressed":False,
         "ResolutionMenuButtonPressed":False,
         "SettingsBackButtonPressed":False,
         "PlayMusic":True,
         "StopMusic":False,
         "IntroStage1":False,
         "IntroStage2":False,
         "FadeIn":False,
         "FadeOut":False,
         "Blackout":False,
         "MenuGlideIn":False,
         "MenuGlideOut":False,
         "NextSong":False,
         "CursorOverride":False,
         "ShowTape":True,
         "TapeActive":False,
         "ShowPopUpMenu":False,
         "ResumeGameButtonPressed":False,
         "QuitButtonPressed":False,
         "InitializeMenu":False,
         "PopUpIn":False,
         "PopUpOut":False,
         "QuitAnimation":False,
         "OpenButtonActive":False,
         "CloseButtonActive":False,
         "PushButtonActive":False,
         "PullButtonActive":False,
         "LookAtButtonActive":False,
         "GiveButtonActive":False,
         "TalkToButtonActive":False,
         "PickUpButtonActive":False,
         "UseButtonActive":False,
         "ShowUserInterface":False,
         "ResolutionButton1Pressed":False,
         "ResolutionButton2Pressed":False,
         "ResolutionButton3Pressed":False,
         "ResolutionBackButtonPressed":False,
         "ShowResolutionMenu":False}

#COLORS

colorMult = 250
fade = True

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
grayBlue = (10,85,175)
darkGrayBlue = (5,35,70)

newGameColor = white
loadGameColor = white
settingsColor = white
backColor = white

loadGame1Color = white
loadGame2Color = white
loadGame3Color = white
loadBackColor = white

resolution1Color = white
resolution2Color = white
resolution3Color = white
resolutionBackColor = white

resolutionMenuButtonColor = white
settingsBackColor = white

resumeGameColor = white
quitColor = white

backgroundColor = (255,0,0)
textColor = (250,0,0),

#TEXT

playText = "Click anywhere to continue..."
fpsText = "0"

#IMAGE VARIABLES - These are the file paths of all the images in the game

menuBackgroundImage = "Images/MENU/MENU.png"
newGameButtonImage = "Images/MENU/MENUBUTTON.png"
loadGameButtonImage = "Images/MENU/MENUBUTTON.png"
settingsButtonImage = "Images/MENU/MENUBUTTON.png"
backButtonImage = "Images/MENU/MENUBUTTON.png"

loadGameButton1Image = "Images/MENU/MENUBUTTON.png"
loadGameButton2Image = "Images/MENU/MENUBUTTON.png"
loadGameButton3Image = "Images/MENU/MENUBUTTON.png"
loadBackButtonImage = "Images/MENU/MENUBUTTON.png"

resolutionMenuButtonImage = "Images/MENU/MENUBUTTON.png"
settingsBackButtonImage = "Images/MENU/MENUBUTTON.png"

resolutionButton1Image = "Images/MENU/MENUBUTTON.png"
resolutionButton2Image = "Images/MENU/MENUBUTTON.png"
resolutionButton3Image = "Images/MENU/MENUBUTTON.png"
resolutionBackButtonImage = "Images/MENU/MENUBUTTON.png"

openButtonImage = "Images/UI/Open1.png"
closeButtonImage = "Images/UI/Close1.png"
pushButtonImage = "Images/UI/Push1.png"
pullButtonImage = "Images/UI/Pull1.png"
lookAtButtonImage = "Images/UI/Look At1.png"
giveButtonImage = "Images/UI/Give1.png"
talkToButtonImage = "Images/UI/Talk To1.png"
pickUpButtonImage = "Images/UI/Pick Up1.png"
useButtonImage = "Images/UI/Use1.png"

resumeGameButtonImage = "Images/MENU/MENUBUTTON.png"
quitButtonImage = "Images/MENU/MENUBUTTON.png"

tutorialBridgeBackgroundImage = "Images/MENU/MENU.png"
lightImage = "Images/TUTORIAL/REDLIGHT.png"

TapeImage = "Images/TUTORIAL/Tape1.png"

#IMAGES - Loads a few static images

menuBackground = pygame.image.load(menuBackgroundImage).convert()
tutorialBridgeBackground = pygame.image.load(tutorialBridgeBackgroundImage).convert()
menuBox = pygame.image.load("Images/MENU/MENUBOX.png").convert_alpha()

nextRoom = ""

loopTime = 0

menuGlideInitialize()


#MUSIC INITIALIZATION

TRACK_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(TRACK_END)

track = 0
area = 1
TRACKS = get_music(area)

while 1:
    
    #INITIALIZE
    screen.fill(green)
    mouse = pygame.mouse.get_pos()
    loopTime = clock.get_time()
    #Increments Timers
    bpt += loopTime # Button Pressed Time
    fpst += loopTime # Frames Per Second Time
    ft += loopTime # Fade Time
    lft += loopTime # Light Flicker Time

    #FLAG CHECKS
    
    if flags["CursorOverride"]: # Changes the cursor when hovering over a button
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        
    
    if flags["PlayMusic"]: # Plays music based on the current area
        track = 0
        TRACKS = get_music(area)
        pygame.mixer.music.load(TRACKS[track])
        pygame.mixer.music.play()
        flags["PlayMusic"] = False
        
    if flags["StopMusic"]: # Stops playing music
        pygame.mixer.music.pause()
        flags["StopMusic"] = False
    
    if flags["ShowStart"]: # Displays the start screen and pulses the color of the text
        pygame.display.set_caption("Start")
        screen.blit(pygame.transform.scale(menuBackground,(int(1000*sscale),int(700*sscale))),(0+barSizeX,0+barSizeY))
        playTextImage = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),playText,True,(colorMult,colorMult,colorMult),(round(25*sscale)+barSizeX,round(250*sscale)+barSizeY),screen)
        colorPulseData = colorPulse(colorMult,fade)
        colorMult = colorPulseData[0]
        fade = colorPulseData[1]
        
        if flags["StartButtonPressed"]:
            if bpt >= 200:
                flags["StartButtonPressed"] = False
                nextRoom = "MainMenu"

    if flags["ShowMenu"]: # Displays the menu
        pygame.display.set_caption("Menu")
        screen.blit(pygame.transform.scale(menuBackground,(int(1000*sscale),int(700*sscale))),(round(0+barSizeX),round(0+barSizeY)))
        screen.blit(pygame.transform.scale(menuBox,(int(350*sscale),int(484*sscale))),(round(menuBoxX*sscale+barSizeX),round(108*sscale+barSizeY)))
        
        menuGlide()   # Glides the menu in

        #The buttons that make up the main menu
        newGameButton = buttonify(newGameButtonImage,200,100,((menuButtonX+140)*sscale+barSizeX,132*sscale+barSizeY),screen)
        loadGameButton = buttonify(loadGameButtonImage,200,100,((menuButtonX+140)*sscale+barSizeX,246*sscale+barSizeY),screen)
        settingsButton = buttonify(settingsButtonImage,200,100,((menuButtonX+140)*sscale+barSizeX,360*sscale+barSizeY),screen)
        backButton = buttonify(backButtonImage,200,100,((menuButtonX+140)*sscale+barSizeX,474*sscale+barSizeY),screen)
        
        newGameText = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"New Game",True,newGameColor,((menuTextX)*sscale+barSizeX,168*sscale+barSizeY),screen)
        loadGameText = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Load Game",True,loadGameColor,((menuTextX)*sscale+barSizeX,282*sscale+barSizeY),screen)
        settingsText = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Settings",True,settingsColor,((menuTextX+20)*sscale+barSizeX,396*sscale+barSizeY),screen)
        backText = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Back",True,backColor,((menuTextX+45)*sscale+barSizeX,510*sscale+barSizeY),screen)

        #HOVER CHECKS - if the cursor is over a button it changes the color of the text if the mouse is clicked it changes the image to a darker one.
        if flags["NewGameButtonPressed"] == False:
            newGameButtonImage = "Images/MENU/MENUBUTTON.png"
            if newGameButton[1].collidepoint(mouse):
                newGameColor = grayBlue
            else:
                newGameColor = white
        else:
            newGameButtonImage = "Images/MENU/MENUBUTTON2.png"
            newGameColor = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["NewGameButtonPressed"] = False
                nextRoom = "Intro"
                
        if flags["LoadGameButtonPressed"] == False:
            loadGameButtonImage = "Images/MENU/MENUBUTTON.png"
            if loadGameButton[1].collidepoint(mouse):
                loadGameColor = grayBlue
            else:
                loadGameColor = white
        else:
            loadGameButtonImage = "Images/MENU/MENUBUTTON2.png"
            loadGameColor = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["LoadGameButtonPressed"] = False
                nextRoom = "LoadMenu"
                
        if flags["SettingsButtonPressed"] == False:
            settingsButtonImage = "Images/MENU/MENUBUTTON.png"
            if settingsButton[1].collidepoint(mouse):
                settingsColor = grayBlue
            else:
                settingsColor = white
        else:
            settingsButtonImage = "Images/MENU/MENUBUTTON2.png"
            settingsColor = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["SettingsButtonPressed"] = False
                nextRoom = "SettingsMenu"
                
        if flags["BackButtonPressed"] == False:
            backButtonImage = "Images/MENU/MENUBUTTON.png"
            if backButton[1].collidepoint(mouse):
                backColor = grayBlue
            else:
                backColor = white
        else:
            backButtonImage = "Images/MENU/MENUBUTTON2.png"
            backColor = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["BackButtonPressed"] = False
                nextRoom = "Start"

        if newGameButton[1].collidepoint(mouse) or loadGameButton[1].collidepoint(mouse) or backButton[1].collidepoint(mouse) or settingsButton[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False

    if flags["ShowLoadMenu"]: # Sames as the main menu but for the load menu
        pygame.display.set_caption("Load Game")
        bpt += loopTime
        screen.blit(pygame.transform.scale(menuBackground,(int(1000*sscale),int(700*sscale))),(round(0+barSizeX),round(0+barSizeY)))
        screen.blit(pygame.transform.scale(menuBox,(int(350*sscale),int(484*sscale))),(round(menuBoxX*sscale+barSizeX),round(108*sscale+barSizeY)))

        menuGlide()

        loadGameButton1 = buttonify(loadGameButton1Image,200,100,((menuButtonX+140)*sscale+barSizeX,132*sscale+barSizeY),screen)
        loadGameButton2 = buttonify(loadGameButton2Image,200,100,((menuButtonX+140)*sscale+barSizeX,246*sscale+barSizeY),screen)
        loadGameButton3 = buttonify(loadGameButton3Image,200,100,((menuButtonX+140)*sscale+barSizeX,360*sscale+barSizeY),screen)
        loadBackButton = buttonify(loadBackButtonImage,200,100,((menuButtonX+140)*sscale+barSizeX,474*sscale+barSizeY),screen)
        
        loadGameButton1Text = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Save 1",True,loadGame1Color,((menuTextX+35)*sscale+barSizeX,168*sscale+barSizeY),screen)
        loadGameButton2Text = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Save 2",True,loadGame2Color,((menuTextX+35)*sscale+barSizeX,282*sscale+barSizeY),screen)
        loadGameButton3Text = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Save 3",True,loadGame3Color,((menuTextX+35)*sscale+barSizeX,396*sscale+barSizeY),screen)
        loadBackText = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Back",True,loadBackColor,((menuTextX+45)*sscale+barSizeX,510*sscale+barSizeY),screen)

        #HOVER CHECKS
        if flags["LoadGameButton1Pressed"] == False:
            loadGameButton1Image = "Images/MENU/MENUBUTTON.png"
            if loadGameButton1[1].collidepoint(mouse):
                loadGame1Color = grayBlue
            else:
                loadGame1Color = white
        else:
            loadGameButton1Image = "Images/MENU/MENUBUTTON2.png"
            loadGame1Color = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["LoadGameButton1Pressed"] = False
                
        if flags["LoadGameButton2Pressed"] == False:
            loadGameButton2Image = "Images/MENU/MENUBUTTON.png"
            if loadGameButton2[1].collidepoint(mouse):
                loadGame2Color = grayBlue
            else:
                loadGame2Color = white
        else:
            loadGameButton2Image = "Images/MENU/MENUBUTTON2.png"
            loadGame2Color = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["LoadGameButton2Pressed"] = False

        if flags["LoadGameButton3Pressed"] == False:
            loadGameButton3Image = "Images/MENU/MENUBUTTON.png"
            if loadGameButton3[1].collidepoint(mouse):
                loadGame3Color = grayBlue
            else:
                loadGame3Color = white
        else:
            loadGameButton3Image = "Images/MENU/MENUBUTTON2.png"
            loadGame3Color = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["LoadGameButton3Pressed"] = False
                
        if flags["LoadBackButtonPressed"] == False:
            loadBackButtonImage = "Images/MENU/MENUBUTTON.png"
            if loadBackButton[1].collidepoint(mouse):
                loadBackColor = grayBlue
            else:
                loadBackColor = white
        else:
            loadBackButtonImage = "Images/MENU/MENUBUTTON2.png"
            loadBackColor = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["LoadBackButtonPressed"] = False
                nextRoom = "MainMenu"
                
        if loadGameButton1[1].collidepoint(mouse) or loadGameButton2[1].collidepoint(mouse) or loadBackButton[1].collidepoint(mouse) or loadGameButton3[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False

    if flags["ShowSettingsMenu"]: #Same as the other menus
        pygame.display.set_caption("Settings")
        bpt += loopTime
        screen.blit(pygame.transform.scale(menuBackground,(int(1000*sscale),int(700*sscale))),(round(0+barSizeX),round(0+barSizeY)))
        screen.blit(pygame.transform.scale(menuBox,(int(350*sscale),int(484*sscale))),(round(menuBoxX*sscale+barSizeX),round(108*sscale+barSizeY)))

        menuGlide()

        resolutionMenuButton = buttonify(resolutionMenuButtonImage,200,100,((menuButtonX+140)*sscale+barSizeX,132*sscale+barSizeY),screen)
        settingsBackButton = buttonify(settingsBackButtonImage,200,100,((menuButtonX+140)*sscale+barSizeX,474*sscale+barSizeY),screen)
        
        resolutionMenuButtonText1 = textify(pygame.font.Font("Fonts/ROTG.otf",int(25*sscale)),"Change",True,resolutionMenuButtonColor,((menuTextX+35)*sscale+barSizeX,148*sscale+barSizeY),screen)
        resolutionMenuButtonText2 = textify(pygame.font.Font("Fonts/ROTG.otf",int(25*sscale)),"Resolution",True,resolutionMenuButtonColor,((menuTextX+20)*sscale+barSizeX,188*sscale+barSizeY),screen)
        settingsBackText = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Back",True,settingsBackColor,((menuTextX+45)*sscale+barSizeX,510*sscale+barSizeY),screen)

        #HOVER CHECKS
        if flags["ResolutionMenuButtonPressed"] == False:
            resolutionMenuButtonImage = "Images/MENU/MENUBUTTON.png"
            if resolutionMenuButton[1].collidepoint(mouse):
                resolutionMenuButtonColor = grayBlue
            else:
                resolutionMenuButtonColor = white
        else:
            resolutionMenuButtonImage = "Images/MENU/MENUBUTTON2.png"
            resolutionMenuButtonColor = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["ResolutionMenuButtonPressed"] = False
                nextRoom = "ResolutionMenu"
                
        if flags["SettingsBackButtonPressed"] == False:
            settingsBackButtonImage = "Images/MENU/MENUBUTTON.png"
            if settingsBackButton[1].collidepoint(mouse):
                settingsBackColor = grayBlue
            else:
                settingsBackColor = white
        else:
            settingsBackButtonImage = "Images/MENU/MENUBUTTON2.png"
            settingsBackColor = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["SettingsBackButtonPressed"] = False
                nextRoom = "MainMenu"
                
        if resolutionMenuButton[1].collidepoint(mouse) or settingsBackButton[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False

    if flags["ShowResolutionMenu"]: # Same as the other menus
        pygame.display.set_caption("Resolution Menu")
        bpt += loopTime
        screen.blit(pygame.transform.scale(menuBackground,(int(1000*sscale),int(700*sscale))),(round(0+barSizeX),round(0+barSizeY)))
        screen.blit(pygame.transform.scale(menuBox,(int(350*sscale),int(484*sscale))),(round(menuBoxX*sscale+barSizeX),round(108*sscale+barSizeY)))

        menuGlide()

        resolutionButton1 = buttonify(resolutionButton1Image,200,100,((menuButtonX+140)*sscale+barSizeX,132*sscale+barSizeY),screen)
        resolutionButton2 = buttonify(resolutionButton2Image,200,100,((menuButtonX+140)*sscale+barSizeX,246*sscale+barSizeY),screen)
        resolutionButton3 = buttonify(resolutionButton3Image,200,100,((menuButtonX+140)*sscale+barSizeX,360*sscale+barSizeY),screen)
        resolutionBackButton = buttonify(resolutionBackButtonImage,200,100,((menuButtonX+140)*sscale+barSizeX,474*sscale+barSizeY),screen)
        
        resolutionButton1Text = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"900x630",True,resolution1Color,((menuTextX+10)*sscale+barSizeX,168*sscale+barSizeY),screen)
        resolutionButton2Text = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"1000x700",True,resolution2Color,((menuTextX+5)*sscale+barSizeX,282*sscale+barSizeY),screen)
        resolutionButton3Text = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"1200x840",True,resolution3Color,((menuTextX+5)*sscale+barSizeX,396*sscale+barSizeY),screen)
        resolutionBackText = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Back",True,resolutionBackColor,((menuTextX+45)*sscale+barSizeX,510*sscale+barSizeY),screen)

        #HOVER CHECKS
        if flags["ResolutionButton1Pressed"] == False:
            resolutionButton1Image = "Images/MENU/MENUBUTTON.png"
            if resolutionButton1[1].collidepoint(mouse):
                resolution1Color = grayBlue
            else:
                resolution1Color = white
        else:
            resolutionButton1Image = "Images/MENU/MENUBUTTON2.png"
            resolution1Color = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["ResolutionButton1Pressed"] = False
                sscale = 1.28
                
        if flags["ResolutionButton2Pressed"] == False:
            resolutionButton2Image = "Images/MENU/MENUBUTTON.png"
            if resolutionButton2[1].collidepoint(mouse):
                resolution2Color = grayBlue
            else:
                resolution2Color = white
        else:
            resolutionButton2Image = "Images/MENU/MENUBUTTON2.png"
            resolution2Color = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["ResolutionButton2Pressed"] = False

        if flags["ResolutionButton3Pressed"] == False:
            resolutionButton3Image = "Images/MENU/MENUBUTTON.png"
            if resolutionButton3[1].collidepoint(mouse):
                resolution3Color = grayBlue
            else:
                resolution3Color = white
        else:
            resolutionButton3Image = "Images/MENU/MENUBUTTON2.png"
            resolution3Color = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["ResolutionButton3Pressed"] = False
                
        if flags["ResolutionBackButtonPressed"] == False:
            resolutionBackButtonImage = "Images/MENU/MENUBUTTON.png"
            if resolutionBackButton[1].collidepoint(mouse):
                resolutionBackColor = grayBlue
            else:
                resolutionBackColor = white
        else:
            resolutionBackButtonImage = "Images/MENU/MENUBUTTON2.png"
            resolutionBackColor = darkGrayBlue
            fadeInitialize(100,0,20,0)
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["ResolutionBackButtonPressed"] = False
                nextRoom = "SettingsMenu"
                
        if resolutionButton1[1].collidepoint(mouse) or resolutionButton2[1].collidepoint(mouse) or resolutionBackButton[1].collidepoint(mouse) or resolutionButton3[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False
            
    if flags["ShowIntroCutscene"]: # Displays the introduction - Timer begins incrementing, when it reaches thresholds the text displayed changes
        pygame.display.set_caption("Intro")
        screen.fill(black)
        it += loopTime
        if it < 3000:
            gameText = "THIS IS A"
            placeholder = 0
            textWait = 100
            gameTextImage = pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)).render("",True,white)
            
        if it >= 3000 and it < 4000:
            gameTextImage = textify(pygame.font.Font("Fonts/ROTG.otf",int(50*sscale)),gameText[:placeholder],True,green,(250*sscale+barSizeX,325*sscale+barSizeY),screen)
            if textWait < it and placeholder != len(gameText):
                textWait = it+100
                placeholder+=1
                
        if it >= 4000 and it < 4500:
            gameTextImage = textify(pygame.font.Font("Fonts/ROTG.otf",int(50*sscale)),"THIS IS A",True,green,(250*sscale+barSizeX,325*sscale+barSizeY),screen)
            gameText = "TEMPORARY INTRO!"
            placeholder = 0
            textWait = 100
        if it >= 4500 and it < 6000:
            gameTextImage = textify(pygame.font.Font("Fonts/ROTG.otf",int(50*sscale)),gameText[:placeholder],True,green,(250*sscale+barSizeX,325*sscale+barSizeY),screen)
            if textWait < it and placeholder != len(gameText):
                textWait = it+100
                placeholder+=1
        if it >= 6000 and it < 7000:
            gameTextImage = textify(pygame.font.Font("Fonts/ROTG.otf",int(50*sscale)),"TEMPORARY INTRO!",True,green,(250*sscale+barSizeX,325*sscale+barSizeY),screen)
        if flags["IntroStage1"] and it >= 0:
            pygame.mixer.music.load("Sounds/OGG/LOADING.ogg")
            pygame.mixer.music.play()
            flags["IntroStage1"] = False
        if flags["IntroStage2"] and it >= 6200:
            flags["FadeOut"] = True
            lft = 0
            it = 0
            flags["IntroStage2"] = False

        elif it >= 6500:
            nextRoom = "TutorialBridge"
            flags["IntroStage2"] = True

    if flags["ShowTutorialBridge"]: # SHows the initial room of the game
        screen.fill(black)
        flags["ShowUserInterface"] = True
        if flags["ShowPopUpMenu"] == False:
            pygame.display.set_caption("Bridge")
        #Displays light
        light = pygame.image.load(lightImage).convert_alpha()
        light = pygame.transform.rotate(light,-16)
        screen.blit(pygame.transform.scale(light,(int(12*sscale),int(6*sscale))),(100*sscale+barSizeX,230*sscale+barSizeY))
        #Flickers Light
        if lft>= 1000:
            lightSwitchData = lightSwitch(lightImage,lft,100)
            lightImage = lightSwitchData[0]
            lft = lightSwitchData[1]
        #Displays ape and its highlighting
        if flags["ShowTape"]:
            Tape = buttonify(TapeImage,150,38,(500*sscale+barSizeX,350*sscale+barSizeY),screen)
            if flags["TapeActive"]:
                TapeImage = "Images/TUTORIAL/Tape2.png"
            else:
                TapeImage = "Images/TUTORIAL/Tape1.png"
            if flags["ShowPopUpMenu"] == False:
                if Tape[1].collidepoint(mouse):
                    flags["TapeActive"] = True
                else:
                    flags["TapeActive"] = False

    if flags["ShowUserInterface"]:#Displays the UI, commands on the left         
        openButton = buttonify(openButtonImage,110,50,(133*sscale+barSizeX,520*sscale+barSizeY),screen)
        closeButton = buttonify(closeButtonImage,135,50,(145*sscale+barSizeX,570*sscale+barSizeY),screen)
        giveButton = buttonify(giveButtonImage,100,50,(123*sscale+barSizeX,620*sscale+barSizeY),screen)
        lookAtButton = buttonify(lookAtButtonImage,174,50,(327*sscale+barSizeX,520*sscale+barSizeY),screen)
        talkToButton = buttonify(talkToButtonImage,174,50,(327*sscale+barSizeX,570*sscale+barSizeY),screen)
        pickUpButton = buttonify(pickUpButtonImage,164,50,(317*sscale+barSizeX,620*sscale+barSizeY),screen)
        pushButton = buttonify(pushButtonImage,110,50,(447*sscale+barSizeX,520*sscale+barSizeY),screen)
        pullButton = buttonify(pullButtonImage,110,50,(447*sscale+barSizeX,570*sscale+barSizeY),screen)
        useButton = buttonify(useButtonImage,85,50,(430*sscale+barSizeX,620*sscale+barSizeY),screen)
        
        if flags["OpenButtonActive"] == False:
            if openButton[1].collidepoint(mouse):
                openButtonImage = "Images/UI/Open2.png"
            else:
                openButtonImage = "Images/UI/Open1.png"
        else:
            openButtonImage = "Images/UI/Open2.png"
            
        if flags["CloseButtonActive"] == False:
            if closeButton[1].collidepoint(mouse):
                closeButtonImage = "Images/UI/Close2.png"
            else:
                closeButtonImage = "Images/UI/Close1.png"
        else:
            closeButtonImage = "Images/UI/Close2.png"
            
        if flags["PushButtonActive"] == False:
            if pushButton[1].collidepoint(mouse):
                pushButtonImage = "Images/UI/Push2.png"
            else:
                pushButtonImage = "Images/UI/Push1.png"
        else:
            pushButtonImage = "Images/UI/Push2.png"
            
        if flags["PullButtonActive"] == False:
            if pullButton[1].collidepoint(mouse):
                pullButtonImage = "Images/UI/Pull2.png"
            else:
                pullButtonImage = "Images/UI/Pull1.png"
        else:
            pullButtonImage = "Images/UI/Pull2.png"
            
        if flags["LookAtButtonActive"] == False:
            if lookAtButton[1].collidepoint(mouse):
                lookAtButtonImage = "Images/UI/Look At2.png"
            else:
                lookAtButtonImage = "Images/UI/Look At1.png"
        else:
            lookAtButtonImage = "Images/UI/Look At2.png"
            
        if flags["GiveButtonActive"] == False:
            if giveButton[1].collidepoint(mouse):
                giveButtonImage = "Images/UI/Give2.png"
            else:
                giveButtonImage = "Images/UI/Give1.png"
        else:
            giveButtonImage = "Images/UI/Give2.png"

        if flags["TalkToButtonActive"] == False:
            if talkToButton[1].collidepoint(mouse):
                talkToButtonImage = "Images/UI/Talk To2.png"
            else:
                talkToButtonImage = "Images/UI/Talk To1.png"
        else:
            talkToButtonImage = "Images/UI/Talk To2.png"

        if flags["PickUpButtonActive"] == False:
            if pickUpButton[1].collidepoint(mouse):
                pickUpButtonImage = "Images/UI/Pick Up2.png"
            else:
                pickUpButtonImage = "Images/UI/Pick Up1.png"
        else:
            pickUpButtonImage = "Images/UI/Pick Up2.png"

        if flags["UseButtonActive"] == False:
            if useButton[1].collidepoint(mouse):
                useButtonImage = "Images/UI/Use2.png"
            else:
                useButtonImage = "Images/UI/Use1.png"
        else:
            useButtonImage = "Images/UI/Use2.png"
        
        
    if flags["ShowPopUpMenu"]: # The menu that appears when paused, the only difference to the other menus is that it fades the rest of screen slightly (or should)
        pygame.display.set_caption("Pop Up Menu")
        
        if fadeWait < ft:
            fadeWait += fadeSpeed
            if flags["PopUpIn"]:
                if fadeAlpha < 100:
                    fadeAlpha += 10
                if fadeAlpha == 100:
                    flags["PopUpIn"] = False
            if flags["PopUpOut"]:
                if menuBoxX <= -300:
                    if fadeAlpha > 0:
                        fadeAlpha -= 10
                    if fadeAlpha == 0:
                        flags["PopUpOut"] = False
                    
        fadeSurface.set_alpha(fadeAlpha)
        popUpScreen.set_alpha(0)
        fadeSurface.fill(black)
        screen.blit(pygame.transform.scale(fadeSurface,(int(1000*sscale+barSizeX),int(700*sscale+barSizeY))),(0,0))
        screen.blit(pygame.transform.scale(popUpScreen,(int(1000*sscale+barSizeX),int(700*sscale+barSizeY))),(0,0))
        popUpScreen.blit(pygame.transform.scale(menuBox,(int(350*sscale+barSizeX),int(484*sscale+barSizeY))),(round(menuBoxX*sscale),round(108*sscale)))

        menuGlide()

        resumeGameButton = buttonify(resumeGameButtonImage,200,100,((menuButtonX+140)*sscale+barSizeX,132*sscale+barSizeY),screen)
        quitButton = buttonify(quitButtonImage,200,100,((menuButtonX+140)*sscale+barSizeX,474*sscale+barSizeY),screen)
        
        resumeGameText = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Resume",True,resumeGameColor,((menuTextX+25)*sscale+barSizeX,168*sscale+barSizeY),screen)
        quitText = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),"Quit",True,quitColor,((menuTextX+55)*sscale+barSizeX,510*sscale+barSizeY),screen)

        if menuBoxX*sscale <= -460*sscale and fadeAlpha == 0:
            flags["ShowPopUpMenu"] = False
            flags["MenuGlideIn"] = True
            flags["MenuGlideOut"] = False
            menuGlideInitialize()

        if flags["QuitAnimation"]:
            flags["ShowPopUpMenu"] = False
            area = 1
            flags["PlayMusic"] = True
            nextRoom = "MainMenu"


        #HOVER CHECKS
        if flags["ResumeGameButtonPressed"] == False:
            resumeGameButtonImage = "Images/MENU/MENUBUTTON.png"
            if resumeGameButton[1].collidepoint(mouse):
                resumeGameColor = grayBlue
            else:
                resumeGameColor = white
        else:
            resumeGameButtonImage = "Images/MENU/MENUBUTTON2.png"
            resumeGameColor = darkGrayBlue

            if bpt >= 200:
                flags["ResumeGameButtonPressed"] = False
                
        if flags["QuitButtonPressed"] == False:
            quitButtonImage = "Images/MENU/MENUBUTTON.png"
            if quitButton[1].collidepoint(mouse):
                quitColor = grayBlue
            else:
                quitColor = white
        else:
            quitButtonImage = "Images/MENU/MENUBUTTON2.png"
            quitColor = darkGrayBlue
            
            flags["FadeOut"] = True
            
            if bpt >= 200:
                flags["QuitButtonPressed"] = False
                flags["QuitAnimation"] = True

        if resumeGameButton[1].collidepoint(mouse) or quitButton[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False

    #Fades from black to clear
    if flags["FadeIn"]:
        if fadeWait < ft:
            fadeWait += fadeSpeed
            if fadeAlpha > 0:
                fadeAlpha -= 10
        fadeSurface.set_alpha(fadeAlpha)
        fadeSurface.fill(black)
        screen.blit(fadeSurface,(0,0))
        if fadeAlpha == 0:
            flags["FadeIn"] = False
    #Fades from clear to black          
    if flags["FadeOut"]:
        if fadeWait < ft:
            fadeWait += fadeSpeed
            if fadeAlpha < 250:
                fadeAlpha += 10
        fadeSurface.set_alpha(fadeAlpha)
        fadeSurface.fill(black)
        screen.blit(fadeSurface,(0,0))
        if fadeAlpha == 250:
            flags["Blackout"] = True
            flags["FadeOut"] = False
    #When room changes the next room changes and Blackout happens when the screen fades entirely to black
    if flags["Blackout"]:
        print("Blackout")
        screen.fill(black)
        flags["CursorOverride"] = False
        #Initialize rooms
        if nextRoom == "LoadMenu":
            flags["ShowLoadMenu"] = True
            flags["ShowMenu"] = False
            flags["MenuGlideIn"] = True
            flags["MenuGlideOut"] = False
            menuGlideInitialize()
        elif nextRoom == "SettingsMenu":
            flags["ShowSettingsMenu"] = True
            flags["ShowMenu"] = False
            flags["ShowResolutionMenu"] = False
            flags["MenuGlideIn"] = True
            flags["MenuGlideOut"] = False
            menuGlideInitialize()
        elif nextRoom == "ResolutionMenu":
            flags["ShowResolutionMenu"] = True
            flags["ShowSettingsMenu"] = False
            flags["MenuGlideIn"] = True
            flags["MenuGlideOut"] = False
            menuGlideInitialize()
        elif nextRoom == "Intro":
            flags["ShowIntroCutscene"] = True
            flags["StopStartMusic"] = True
            flags["ShowMenu"] = False
            flags["IntroStage1"] = True
        elif nextRoom == "Start":
            flags["ShowStart"] = True
            flags["ShowMenu"] = False
        elif nextRoom == "MainMenu":
            flags = {"ShowStart":False,
                     "ShowMenu":True,
                     "ShowLoadMenu":False,
                     "ShowSettingsMenu":False,
                     "ShowIntroCutscene":False,
                     "ShowTutorialBridge":False,
                     "ShowTutorialEngine":False,
                     "StartButtonPressed":False,
                     "NewGameButtonPressed":False,
                     "LoadGameButtonPressed":False,
                     "SettingsButtonPressed":False,
                     "BackButtonPressed":False,
                     "LoadGameButton1Pressed":False,
                     "LoadGameButton2Pressed":False,
                     "LoadGameButton3Pressed":False,
                     "LoadBackButtonPressed":False,
                     "ResolutionMenuButtonPressed":False,
                     "SettingsBackButtonPressed":False,
                     "PlayMusic":False,
                     "StopMusic":False,
                     "IntroStage1":False,
                     "IntroStage2":False,
                     "FadeIn":False,
                     "FadeOut":False,
                     "Blackout":False,
                     "MenuGlideIn":True,
                     "MenuGlideOut":False,
                     "NextSong":False,
                     "CursorOverride":False,
                     "ShowTape":True,
                     "TapeActive":False,
                     "ShowPopUpMenu":False,
                     "ResumeGameButtonPressed":False,
                     "QuitButtonPressed":False,
                     "InitializeMenu":False,
                     "PopUpIn":False,
                     "PopUpOut":False,
                     "QuitAnimation":False,
                     "OpenButtonActive":False,
                     "CloseButtonActive":False,
                     "PushButtonActive":False,
                     "PullButtonActive":False,
                     "LookAtButtonActive":False,
                     "GiveButtonActive":False,
                     "TalkToButtonActive":False,
                     "PickUpButtonActive":False,
                     "UseButtonActive":False,
                     "ShowUserInterface":False,
                     "ResolutionButton1Pressed":False,
                     "ResolutionButton2Pressed":False,
                     "ResolutionButton3Pressed":False,
                     "ResolutionBackButtonPressed":False,
                     "ShowResolutionMenu":False}
            
            menuGlideInitialize()
        elif nextRoom == "TutorialBridge":
            flags["ShowIntroCutscene"] = False
            flags["ShowTutorialBridge"] = True
            area = 2
            flags["PlayMusic"] = True
            flags["MenuGlideIn"] = True
            flags["MenuGlideOut"] = False
            menuGlideInitialize()
        
        fadeInitialize(100,0,20,250)
        flags["FadeIn"] = True
        flags["Blackout"] = False
    #Draw Black Bars
    if barTop == False:
        leftBar = pygame.draw.rect(screen,black,(0,0,barSizeX,screenHeight))
        rightBar = pygame.draw.rect(screen,black,(screenWidth-barSizeX,0,barSizeX,screenHeight))
    else:
        leftBar = pygame.draw.rect(screen,black,(0,0,screenWidth,barSizeY))
        rightBar = pygame.draw.rect(screen,black,(0,screenHeight-barSizeY,screenWidth,barSizeY))

    #EVENT CHECKS
    for event in pygame.event.get():
        if event.type == QUIT: #Quis the window when redx is pressed
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN: # Checks for mouse press and depending on where the mouse is and the game state it has various effects
            #BUTTON CHECKS

            if flags["ShowStart"]:
                print("Menu")
                flags["StartButtonPressed"] = True
                fadeInitialize(100,0,20,0)
                flags["FadeOut"] = True
                bpt = 0
                
            if flags["ShowMenu"]:
                if newGameButton[1].collidepoint(mouse) and event.button == 1:
                    print("New Game")
                    flags["NewGameButtonPressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                elif loadGameButton[1].collidepoint(mouse) and event.button == 1:
                    print("Load Game")
                    flags["LoadGameButtonPressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                elif settingsButton[1].collidepoint(mouse) and event.button == 1:
                    print("Settings")
                    flags["SettingsButtonPressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                elif backButton[1].collidepoint(mouse) and event.button == 1:
                    print("Back")
                    flags["BackButtonPressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0

            if flags["ShowUserInterface"]:
                if openButton[1].collidepoint(mouse) and event.button == 1:
                    if flags["OpenButtonActive"] == False:
                        deactivateButtons()
                        flags["OpenButtonActive"] = True
                    else:
                        deactivateButtons()
                        
                if closeButton[1].collidepoint(mouse) and event.button == 1:
                    if flags["CloseButtonActive"] == False:
                        deactivateButtons()
                        flags["CloseButtonActive"] = True
                    else:
                        deactivateButtons()
                        
                if pushButton[1].collidepoint(mouse) and event.button == 1:
                    if flags["PushButtonActive"] == False:
                        deactivateButtons()
                        flags["PushButtonActive"] = True
                    else:
                        deactivateButtons()
                        
                if pullButton[1].collidepoint(mouse) and event.button == 1:
                    if flags["PullButtonActive"] == False:
                        deactivateButtons()
                        flags["PullButtonActive"] = True
                    else:
                        deactivateButtons()
                        
                if lookAtButton[1].collidepoint(mouse) and event.button == 1:
                    if flags["LookAtButtonActive"] == False:
                        deactivateButtons()
                        flags["LookAtButtonActive"] = True
                    else:
                        deactivateButtons()
                        
                if giveButton[1].collidepoint(mouse) and event.button == 1:
                    if flags["GiveButtonActive"] == False:
                        deactivateButtons()
                        flags["GiveButtonActive"] = True
                    else:
                        deactivateButtons()
                        
                if talkToButton[1].collidepoint(mouse) and event.button == 1:
                    if flags["TalkToButtonActive"] == False:
                        deactivateButtons()
                        flags["TalkToButtonActive"] = True
                    else:
                        deactivateButtons()
                        
                if pickUpButton[1].collidepoint(mouse) and event.button == 1:
                    if flags["PickUpButtonActive"] == False:
                        deactivateButtons()
                        flags["PickUpButtonActive"] = True
                    else:
                        deactivateButtons()
                        
                if useButton[1].collidepoint(mouse) and event.button == 1:
                    if flags["UseButtonActive"] == False:
                        deactivateButtons()
                        flags["UseButtonActive"] = True
                    else:
                        deactivateButtons()

            if flags["ShowPopUpMenu"]:
                if resumeGameButton[1].collidepoint(mouse) and event.button == 1:
                    print("Resume Game")
                    flags["ResumeGameButtonPressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                    fadeInitialize(100,0,20,0)
                    flags["PopUpOut"] = True
                elif quitButton[1].collidepoint(mouse) and event.button == 1:
                    print("Quit")
                    flags["QuitButtonPressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    fadeInitialize(100,0,20,0)
                    bpt = 0
                    
            if flags["ShowLoadMenu"]:
                if loadGameButton1[1].collidepoint(mouse) and event.button == 1:
                    print("Load - Save 1")
                    flags["LoadGameButton1Pressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                elif loadGameButton2[1].collidepoint(mouse) and event.button == 1:
                    print("Load - Save 2")
                    flags["LoadGameButton2Pressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                elif loadGameButton3[1].collidepoint(mouse) and event.button == 1:
                    print("Load - Save 3")
                    flags["LoadGameButton3Pressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                elif loadBackButton[1].collidepoint(mouse) and event.button == 1:
                    print("Back")
                    flags["LoadBackButtonPressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0

            if flags["ShowSettingsMenu"]:
                if resolutionMenuButton[1].collidepoint(mouse) and event.button == 1:
                    print("Change Resolution")
                    flags["ResolutionMenuButtonPressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                elif settingsBackButton[1].collidepoint(mouse) and event.button == 1:
                    print("Back")
                    flags["SettingsBackButtonPressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0

            if flags["ShowResolutionMenu"]:
                if resolutionButton1[1].collidepoint(mouse) and event.button == 1:
                    print("900x630") # Same as the original scaling but for set size
                    sscale = infoObject.current_h/700
                    if 1000*sscale < infoObject.current_w:
                        barTop = False
                        barSizeX = (infoObject.current_w - (1000*sscale))/2
                        barSizeY = 0
                        screenWidth = 1000*sscale+2*barSizeX
                        screenHeight = 700*sscale
                    else:
                        barTop = True
                        sscale = infoObject.current_w/1000
                        barSizeY = (infoObject.current_h-64 - (700*sscale))/2
                        barSizeX = 0
                        screenWidth = 1000*sscale
                        screenHeight = 700*sscale+2*barSizeY
                    screen = pygame.display.set_mode((int(screenWidth),int(screenHeight)))
                    fadeSurface = pygame.Surface((int(screenWidth),int(screenHeight)))
                    popUpScreen = pygame.display.set_mode((int(screenWidth),int(screenHeight)))
                    flags["ResolutionButton1Pressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                elif resolutionButton2[1].collidepoint(mouse) and event.button == 1:
                    print("1000x700")
                    sscale = 1
                    if 1000*sscale < infoObject.current_w:
                        barTop = False
                        barSizeX = (infoObject.current_w - (1000*sscale))/2
                        barSizeY = 0
                        screenWidth = 1000*sscale+2*barSizeX
                        screenHeight = 700*sscale
                    else:
                        barTop = True
                        sscale = infoObject.current_w/1000
                        barSizeY = (infoObject.current_h-64 - (700*sscale))/2
                        barSizeX = 0
                        screenWidth = 1000*sscale
                        screenHeight = 700*sscale+2*barSizeY
                    screen = pygame.display.set_mode((int(screenWidth),int(screenHeight)))
                    fadeSurface = pygame.Surface((int(screenWidth),int(screenHeight)))
                    popUpScreen = pygame.display.set_mode((int(screenWidth),int(screenHeight)))
                    flags["ResolutionButton2Pressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                elif resolutionButton3[1].collidepoint(mouse) and event.button == 1:
                    print("1200x840")
                    sscale = 1.2
                    if 1000*sscale < infoObject.current_w:
                        barTop = False
                        barSizeX = (infoObject.current_w - (1000*sscale))/2
                        barSizeY = 0
                        screenWidth = 1000*sscale+2*barSizeX
                        screenHeight = 700*sscale
                    else:
                        barTop = True
                        sscale = infoObject.current_w/1000
                        barSizeY = (infoObject.current_h-64 - (700*sscale))/2
                        barSizeX = 0
                        screenWidth = 1000*sscale
                        screenHeight = 700*sscale+2*barSizeY
                    screen = pygame.display.set_mode((int(screenWidth),int(screenHeight)))
                    fadeSurface = pygame.Surface((int(screenWidth),int(screenHeight)))
                    popUpScreen = pygame.display.set_mode((int(screenWidth),int(screenHeight)))
                    flags["ResolutionButton3Pressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0
                elif resolutionBackButton[1].collidepoint(mouse) and event.button == 1:
                    print("Back")
                    flags["ResolutionBackButtonPressed"] = True
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    bpt = 0

            if flags["ShowTutorialBridge"]: #Different active commands have different effects on what happens
                if flags["ShowPopUpMenu"] == False:
                    if Tape[1].collidepoint(mouse) and event.button == 1:
                        if flags["LookAtButtonActive"]:
                            print("You clicked a Tape, well done!")
                        if flags["PickUpButtonActive"]:
                            flags["ShowTape"] = False
                            print(Inventory)
                            Inventory.append({"Inventory Image":"Images/TUTORIAL/TapeI.png","Item Name":"Tape"})
                            print(Inventory)
                    
        elif event.type == KEYDOWN: # Detects Keypresses

            if event.key == K_ESCAPE:
                if flags["ShowMenu"] or flags["ShowStart"] or flags["ShowLoadMenu"]:
                    pygame.quit()
                    sys.exit()
                elif flags["ShowPopUpMenu"] == False:
                    print("Pop Up Menu")
                    menuGlideMult = 100
                    menuBoxX = -460
                    menuButtonX = -300
                    menuTextX = -345
                    flags["MenuGlideIn"] = True
                    flags["ShowPopUpMenu"] = True
                    flags["PopUpIn"] = True
                elif flags["ShowPopUpMenu"]:
                    print("Resume")
                    flags["MenuGlideOut"] = True
                    menuGlideMult = 100
                    fadeInitialize(100,0,20,100)
                    flags["PopUpOut"] = True

##        elif event.type == VIDEORESIZE:
##            screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)

        elif event.type == TRACK_END:
            flags["NextSong"] = True
        #Changes Song
        if flags["NextSong"]:
            track += 1
            flags["NextSong"] = False
            TRACKS = get_music(area)
            track = (track)%len(TRACKS)
            flags["PlayMusic"] = True
            
    #UPDATES
    #Changes timers
    if clock.get_time() != 0:
        if fpst >= 200:
            fpsText= (str(round(1000/loopTime)))
            fpst = 0
        fpsTextImage = textify(pygame.font.Font("Fonts/ROTG.otf",int(30*sscale)),fpsText,True,green,(0,0),screen)
    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
