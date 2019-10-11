#                                       TO FIX
#     ____________________________________________________________________________
#
#     _____________________________________________________________________________
#
#                                       TO DO
#     ____________________________________________________________________________
#                                   LOADING IMAGES
#                                   SKIP
#                                   POP UP MENU

import sys, pygame, time, os, pickle # Imports: Sys - Exiting, pygame - Interface, Time - Waiting ect., os - Positioning the Window, pickle - Saving.
from pygame.locals import *

os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(30)

# FUNCTIONS

def buttonify(Picture, coords, surface):     # This function creates a button. It returns the Image and rectangular hitbox of said button.
    imagerect = Picture.get_rect()             # It takes in an image, the coordinates of the button and the surface to blit it on.
    imagerect.topright = coords
    surface.blit(Picture, imagerect)
    return (Picture, imagerect)

def doorInDefault(x, y):     # This function sets all of the variables associated with an "IN" Door to their defaults, taking only the doors co-ordinates.
    global doorInTBX, doorInTBY, doorInTX, doorInTY, doorInBX, doorInBY, doorInSX, doorInSY, doorInCX, doorInCY, doorInDefaultX, doorInDefaultY
    doorInDefaultX = x
    doorInDefaultY = y
    doorInTBX = x
    doorInTBY = y
    doorInTX = x
    doorInTY = y
    doorInBX = x
    doorInBY = y
    doorInSX = x
    doorInSY = y
    doorInCX = x
    doorInCY = y

def doorOutDefault(x, y):     # This function sets all of the variables associated with an "OUT" Door to their defaults, taking only the doors co-ordinates.
    global doorOutTBX, doorOutTBY, doorOutTX, doorOutTY, doorOutBX, doorOutBY, doorOutSX, doorOutSY, doorOutCX, doorOutCY, doorOutDefaultX, doorOutDefaultY
    doorOutDefaultX = x
    doorOutDefaultY = y
    doorOutTBX = x
    doorOutTBY = y
    doorOutTX = x
    doorOutTY = y
    doorOutBX = x
    doorOutBY = y
    doorOutSX = x
    doorOutSY = y
    doorOutCX = x
    doorOutCY = y

def colorPulse(colorMult, fade):     # This function makes a color pulse form white to gray and back eternally. It takes a Integer to be pulsed and the direction of the fade
    if colorMult == 155:
        fade = True
    elif colorMult == 255:
        fade = False
    if fade == False:
        colorMult -= 1
    elif fade:
        colorMult += 1
    return (colorMult, fade)

def textify(fontSize, text, antiA, color, coords, surface):     # This function is used to generate a text surface. It takes in The size, string, anti-aliasing, color, coordinates and surface
    font = pygame.font.Font("Fonts/ROTG.otf", int(fontSize*scale))
    image = font.render(text, antiA, color)
    surface.blit(image, coords)
    return image

def buttonHover(buttonFlag, buttonImage, button, buttonColor, nextRoomInput): # This function is used to detect when the cursor is over a button.
    global grayBlue, white, darkGrayBlue, flags, bpt, nextRoom, button1Image1, button1Image2
    if flags[buttonFlag] == False:             # If the button hasn't been clicked it checks for the cursors position and changes the text color accordingly
        buttonImage = button1Image1
        if button[1].collidepoint(mouse):
            buttonColor = grayBlue
        else:
            buttonColor = white
    else:                                    # Else it changes the image of the button to the depressed one and begins a fade out.
        buttonImage = button1Image2
        buttonColor = darkGrayBlue
        fadeInitialize(100, 0, 20, 0)
        flags["FadeOut"] = True
        
        if bpt >= 200:                        # After 200 ms it changes the room to the next one specified as a parameter.
            flags[buttonFlag] = False
            nextRoom = nextRoomInput
    array = [buttonImage, buttonColor] 
    return array

def outputInitialize(gameTextV, textColorV, pageAmountV): # This fucntion prepares the output pack to default ready for a new output block
    global gameText, placeholder, textWait, gameTextImage, textX, it, flags, line, lineCount, textColor, textWaitModifier, pageAmount, currentPageNumber
    closeOutputButtonImage = closeOutputButtonImage1
    currentPageNumber = 0
    flags["CloseOutputButtonPressed"] = False
    flags["ShowOutput"] = True
    gameText = gameTextV
    it = 0
    line = 0
    lineCount = 0
    pageAmount = pageAmountV
    placeholder = 0
    textColor = textColorV
    textWait = 100
    textWaitModifier = 10
    textX = 100

def fadeInitialize(fadeWaitV, ftv, fadeSpeedV, fadeAlphaV): # This is used to initialize the fading of the screen after a click etc. It sets values to the corrseponding parameters
    global fadeWait, ft, fadeSpeed, fadeAlpha, fadeLimit
    fadeWait = fadeWaitV
    ft = ftv
    fadeSpeed = fadeSpeedV
    fadeAlpha = fadeAlphaV

def menuInitialize(): # This is a semi-redundant function as the menu no longer glides in/out however it still initializes the coordinates of the menu content
    global menuGlideMult, menuBoxX, menuButtonX, menuTextX
    
    menuGlideMult = 100
    menuBoxX = 0
    menuButtonX = 160
    menuTextX = 115

def get_music(area): # This is used to change the current song playing
    playlist = []
    if area == 1:
        playlist = ["Sounds/OGG/START.ogg"]
    elif area == 2:
        playlist = ["Sounds/Ambient.ogg"]
    return playlist

def deactivateCommandButtons(): # This is used to clear all of the white outlines around the command buttons
    global flags
    flags["OpenButtonActive"] = False
    flags["CloseButtonActive"] = False
    flags["PushButtonActive"] = False
    flags["PullButtonActive"] = False
    flags["ExamineButtonActive"] = False
    flags["GiveButtonActive"] = False
    flags["TalkToButtonActive"] = False
    flags["PickUpButtonActive"] = False
    flags["UseButtonActive"] = False

def deactivateInventoryButtons():# This is used to clear all of the white outlines around the inventory slots
    global flags, currentObject
    flags["IBox1ButtonActive"] = False
    flags["IBox2ButtonActive"] = False
    flags["IBox3ButtonActive"] = False
    flags["IBox4ButtonActive"] = False
    flags["IBox5ButtonActive"] = False
    flags["IBox6ButtonActive"] = False
    flags["IBox7ButtonActive"] = False
    flags["IBox8Button5Active"] = False
    currentObject = ""

# PYGAME STUFF

pygame.init()

infoObject = pygame.display.Info()
currentHeight, currentWidth = infoObject.current_h, infoObject.current_w

# This block of code is used to set the scale of the window and calculate the dimensions of the black bars which keep the window in proportion

#############################################################################
#############################################################################
#############################################################################

##currentHeight = 700
##currentWidth = 1000
##scale = currentHeight/700
##
##barSizeY = 0
##barSizeX = 0
##barTop = False
##
##screenWidth = 1000
##screenHeight = 700

#############################################################################
#############################################################################
#############################################################################

currentHeight -= 69
scale = currentHeight/700

if 1000*scale < currentWidth:
    barTop = False
    barSizeX = (currentWidth - (1000*scale))/2
    barSizeY = 0
    screenWidth = 1000*scale+2*barSizeX
    screenHeight = 700*scale
else:
    barTop = True
    scale = currentWidth/1000
    barSizeY = (currentHeight - (700*scale))/2
    barSizeX = 0
    screenWidth = 1000*scale
    screenHeight = 700*scale+2*barSizeY

# This initializes all of the key surfaces

screen = pygame.display.set_mode((int(screenWidth), int(screenHeight)),DOUBLEBUF)
fadeSurface = pygame.Surface((int(screenWidth), int(screenHeight)))
popUpScreen = pygame.display.set_mode((int(screenWidth), int(screenHeight)))

# Sets up the    FPS of the game

clock = pygame.time.Clock()
fps = 1000
textFPS = 100

# Counter Initialization

bpt = 0 # Button Pressed Timer
it = 0 # Intro Timer
fpst = 0 # FPS Timer
lft = 0 # Light Flicker Timer
cit = 500 # Code Input Timer

# FADING

fadeInitialize(100, 0, 20, 0)

# FLAGS

currentSlot = 0 # The current slot within the inventory

roomSide = 0 # This stores the actual value of the room Side e.g 124
currentRoomSide = 0 # This is the relative room side so it is always 0,1,2 or 3 e.g. 124 --> 0 because 124%4 is 0

KeypadCode = "" # Declares the keypad code variable
currentKey = "" # This stores the current key for the NPC interface

# The inventory consists of any items collected within the game. It is initialized with blank spaces which are skipped when outputting the inventory later on
Inventory = [{"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}, {"Item Name":"BLANK"}]
imod = 0 #    This is a future proofing variable for if the game got complex enough for the user to require more than 8 slots. It would basically move the inventory up or down 8 slots. However the arrows do not work as of this version

# FLAGS - These are the most important part of the code. The many flags dictate the exact game state based on a number of boolean values. If you were to change the flags you would change the game state.
# They control everything from what is displayed to what 'room' you are currently in and are vital to almost every aspect of my game

flags ={"BackButtonPressed":False, 
        "Blackout":False, 
        "BookcaseActive":True,
        "BookcaseBroken":False,
        "BookcaseExists":False,
        "CloseButtonActive":False, 
        "CloseButtonExists":False,
        "CloseKeypadButtonPressed":False,
        "CloseNPCButtonPressed":False,
        "CloseOuputButtonPressed":False,
        "ComputerActive":False,
        "ComputerFixed":False,
        "CursorOverride":False, 
        "DoorInActive":False,
        "DoorInClose":False, 
        "DoorInOpen":False,
        "DoorInOpened":False,
        "DoorOutActive":False,
        "DoorOutClose":False, 
        "DoorOutExists":False, 
        "DoorOutOpen":False,
        "DoorOutOpened":False,
        "DownArrowButtonActive":False, 
        "EngineActive":False, 
        "EngineExists":False,
        "EngineFixed":False,
        "EngineTaped":False,
        "ExamineButtonActive":False, 
        "FadeIn":False, 
        "FadeOut":False,
        "FusionCoreActive":False, 
        "GiveButtonActive":False, 
        "IBox1ButtonActive":False, 
        "IBox2ButtonActive":False, 
        "IBox3ButtonActive":False, 
        "IBox4ButtonActive":False, 
        "IBox5ButtonActive":False, 
        "IBox6ButtonActive":False, 
        "IBox7ButtonActive":False, 
        "IBox8ButtonActive":False, 
        "InitializeMenu":False, 
        "IntroStage1":False, 
        "IntroStage2":False, 
        "Key0Pressed":False,
        "Key1Pressed":False,
        "Key2Pressed":False,
        "Key3Pressed":False,
        "Key4Pressed":False,
        "Key5Pressed":False,
        "Key6Pressed":False,
        "Key7Pressed":False,
        "Key8Pressed":False,
        "Key9Pressed":False,
        "KeyBPressed":False,
        "KeypadActive":False,
        "KeypadUnlocked":False,
        "KeyTPressed":False,
        "LoadBackButtonPressed":False, 
        "LoadGameButton1Pressed":False, 
        "LoadGameButton2Pressed":False, 
        "LoadGameButton3Pressed":False, 
        "LoadGameButtonPressed":False, 
        "MenuGlideIn":True, 
        "MenuGlideOut":False, 
        "NewGameButtonPressed":False, 
        "NextSong":False, 
        "OpenButtonActive":False, 
        "PanelActive":False,
        "PanelExists":False,
        "PanelFixed":False,
        "PanelRemoved":False,
        "PanelWireFixed":False,
        "PanelWireTaped":False,
        "PickUpButtonActive":False, 
        "PlayMusic":True, 
        "PopUpIn":False, 
        "PopUpOut":False, 
        "PullButtonActive":False, 
        "PushButtonActive":False, 
        "QuitAnimation":False, 
        "QuitButtonPressed":False, 
        "ResolutionBackButtonPressed":False, 
        "ResolutionButton1Pressed":False, 
        "ResolutionButton2Pressed":False, 
        "ResolutionButton3Pressed":False, 
        "ResolutionMenuButtonPressed":False, 
        "ResumeGameButtonPressed":False, 
        "SaveBackButtonPressed":False, 
        "SaveGameButton1Pressed":False, 
        "SaveGameButton2Pressed":False, 
        "SaveGameButton3Pressed":False, 
        "SaveGameButtonPressed":False, 
        "ScrewdriverActive":False,
        "ScrewdriverExists":False,
        "SettingsBackButtonPressed":False, 
        "SettingsButtonPressed":False,
        "ShowBookcase":True,
        "ShowComputer":True,
        "ShowComputerInterface":False,
        "ShowDoorIn":True,
        "ShowDoorOut":True,
        "ShowEngine":True, 
        "ShowFusionCore":True, 
        "ShowIntroCutscene":False, 
        "ShowKeypad":True,
        "ShowKeypadInterface":False,
        "ShowLoadMenu":False, 
        "ShowMenu":False, 
        "ShowNPCInterface":False,
        "ShowOutput":False,
        "ShowPanel":True,
        "ShowPopUpMenu":False, 
        "ShowResolutionMenu":False, 
        "ShowRoom1":False,
        "ShowRoom2":False,
        "ShowSaveMenu":False, 
        "ShowScrewdriver":False,
        "ShowSettingsMenu":False, 
        "ShowSolder":True, 
        "ShowStart":True, 
        "ShowTape":True, 
        "ShowTutorial":False, 
        "ShowUserInterface":False,
        "SkipButtonActive":False,
        "SolderActive":False,
        "SolderExists":False,
        "StartButtonPressed":False,
        "StopMusic":False, 
        "TalkToButtonActive":False, 
        "TapeActive":False,
        "TextSkipped":False,
        "TutorialButtonPressed":False,
        "UpArrowButtonActive":False, 
        "UseButtonActive":False,
        "UpdateImages":True,    
        }

# An array of coordinates for the Y values of the text used in an output block

textHeight = [100,140,180,220,260,300,340,380,420,460,500,540,580,620]


colorMult = 250 # a value used to make a shade of gray
fade = True # used to discern the direction of color change

# COLORS - Some basic colors that i have assigned variables to for easy use

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grayBlue = (10, 85, 175)
darkGrayBlue = (5, 35, 70)
backgroundGray = (155, 155, 157)

# Button Colors - The color of the text on each menu button

button1Color = white
button2Color = white
button3Color = white
button4Color = white

backgroundColor = (255, 0, 0)
textColor = (250, 0, 0)

# TEXT
fpsText = "0"

# IMAGE VARIABLES

nextRoom = ""
loopTime = 0

menuInitialize()

# MUSIC

TRACK_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(TRACK_END)

track = 0
area = 1
TRACKS = get_music(area)
et = 0

while 1:
    
    # INITIALIZE
    screen.fill(red)
    mouse = pygame.mouse.get_pos()
    loopTime = clock.get_time()
    bpt += loopTime # Button Pressed Time
    fpst += loopTime # Frames Per Second Time
    ft += loopTime # Fade Time
    lft += loopTime # Light Flicker Time
    cit += loopTime # Code Input Time
    et -= loopTime

    # FLAG CHECKS

    if flags["UpdateImages"]: # This Flag is run whenever the window is resized including when the game is started. It loads every possible image into a variable
        print("Update Images")
        Arrow1Image1 = pygame.image.load("Images/UI/Arrow1.png").convert_alpha()
        Arrow1Image2 = pygame.image.load("Images/UI/Arrow2.png").convert_alpha()
        Arrow2Image1 = pygame.image.load("Images/UI/Arrow1.png").convert_alpha()
        Arrow2Image2 = pygame.image.load("Images/UI/Arrow2.png").convert_alpha()
        backgroundSegment1 = pygame.image.load("Images/TUTORIAL/SpaceshipSegment1.png").convert_alpha()
        backgroundSegment2 = pygame.image.load("Images/TUTORIAL/SpaceshipSegment2.png").convert_alpha()
        blankImage = pygame.image.load("Images/BLANK.png").convert_alpha()
        bookcaseImage1 = pygame.image.load("Images/TUTORIAL/Bookcase1.png").convert_alpha()
        bookcaseImage2 = pygame.image.load("Images/TUTORIAL/Bookcase2.png").convert_alpha()
        bookcaseImage3 = pygame.image.load("Images/TUTORIAL/Bookcase3.png").convert_alpha()
        button1Image1 = pygame.image.load("Images/MENU/MENUBUTTON.png").convert_alpha()
        button1Image2 = pygame.image.load("Images/MENU/MENUBUTTON2.png").convert_alpha()
        button2Image1 = pygame.image.load("Images/MENU/MENUBUTTON.png").convert_alpha()
        button2Image2 = pygame.image.load("Images/MENU/MENUBUTTON2.png").convert_alpha()
        button3Image1 = pygame.image.load("Images/MENU/MENUBUTTON.png").convert_alpha()
        button3Image2 = pygame.image.load("Images/MENU/MENUBUTTON2.png").convert_alpha()
        button4Image1 = pygame.image.load("Images/MENU/MENUBUTTON.png").convert_alpha()
        button4Image2 = pygame.image.load("Images/MENU/MENUBUTTON2.png").convert_alpha()
        closeButtonImage1 = pygame.image.load("Images/UI/Close1.png").convert_alpha()
        closeButtonImage2 = pygame.image.load("Images/UI/Close2.png").convert_alpha()
        closeKeypadButtonImage1 = pygame.image.load("Images/UI/X1.png").convert_alpha()
        closeKeypadButtonImage2 = pygame.image.load("Images/UI/X2.png").convert_alpha()
        closeNPCButtonImage1 = pygame.image.load("Images/UI/X1.png").convert_alpha()
        closeNPCButtonImage2 = pygame.image.load("Images/UI/X2.png").convert_alpha()
        closeOutputButtonImage1 = pygame.image.load("Images/UI/X1.png").convert_alpha()
        closeOutputButtonImage2 = pygame.image.load("Images/UI/X2.png").convert_alpha()
        computerImage1 = pygame.image.load("Images/ROOM2/Computer1.png").convert_alpha()
        computerImage2 = pygame.image.load("Images/ROOM2/Computer2.png").convert_alpha()
        computerImage3 = pygame.image.load("Images/ROOM2/Computer3.png").convert_alpha()
        computerImage4 = pygame.image.load("Images/ROOM2/Computer4.png").convert_alpha()
        doorA24WImage = pygame.image.load("Images/TUTORIAL/A-24.png").convert_alpha()
        doorA25WImage = pygame.image.load("Images/BLANK.png").convert_alpha()
        doorBImage = pygame.image.load("Images/TUTORIAL/DoorB.png").convert_alpha()
        doorCImage = pygame.image.load("Images/TUTORIAL/DoorC.png").convert_alpha()
        doorSImage = pygame.image.load("Images/TUTORIAL/DoorS.png").convert_alpha()
        doorTBImage1 = pygame.image.load("Images/TUTORIAL/DoorTB1.png").convert_alpha()
        doorTBImage2 = pygame.image.load("Images/TUTORIAL/DoorTB2.png").convert_alpha()
        doorTImage = pygame.image.load("Images/TUTORIAL/DoorT.png").convert_alpha()
        engineImage1 = pygame.image.load("Images/TUTORIAL/EngineObject1.png").convert_alpha()
        engineImage2 = pygame.image.load("Images/TUTORIAL/EngineObject2.png").convert_alpha()
        engineImage3 = pygame.image.load("Images/TUTORIAL/EngineObject3.png").convert_alpha()
        engineImage4 = pygame.image.load("Images/TUTORIAL/EngineObject4.png").convert_alpha()
        engineImage5 = pygame.image.load("Images/TUTORIAL/EngineObject5.png").convert_alpha()
        examineButtonImage1 = pygame.image.load("Images/UI/Examine1.png").convert_alpha()
        examineButtonImage2 = pygame.image.load("Images/UI/Examine2.png").convert_alpha()
        fusionCoreImage1 = pygame.image.load("Images/TUTORIAL/Fusion Core1.png").convert_alpha()
        fusionCoreImage2 = pygame.image.load("Images/TUTORIAL/Fusion Core2.png").convert_alpha()
        fusionCoreImage3 = pygame.image.load("Images/TUTORIAL/Fusion Core3.png").convert_alpha()
        giveButtonImage1 = pygame.image.load("Images/UI/Give1.png").convert_alpha()
        giveButtonImage2 = pygame.image.load("Images/UI/Give2.png").convert_alpha()
        IBox1Image1 = pygame.image.load("Images/UI/Inventory Box1.png").convert_alpha()
        IBox1Image2 = pygame.image.load("Images/UI/Inventory Box2.png").convert_alpha()
        IBox2Image1 = pygame.image.load("Images/UI/Inventory Box1.png").convert_alpha()
        IBox2Image2 = pygame.image.load("Images/UI/Inventory Box2.png").convert_alpha()
        IBox3Image1 = pygame.image.load("Images/UI/Inventory Box1.png").convert_alpha()
        IBox3Image2 = pygame.image.load("Images/UI/Inventory Box2.png").convert_alpha()
        IBox4Image1 = pygame.image.load("Images/UI/Inventory Box1.png").convert_alpha()
        IBox4Image2 = pygame.image.load("Images/UI/Inventory Box2.png").convert_alpha()
        IBox5Image1 = pygame.image.load("Images/UI/Inventory Box1.png").convert_alpha()
        IBox5Image2 = pygame.image.load("Images/UI/Inventory Box2.png").convert_alpha()
        IBox6Image1 = pygame.image.load("Images/UI/Inventory Box1.png").convert_alpha()
        IBox6Image2 = pygame.image.load("Images/UI/Inventory Box2.png").convert_alpha()
        IBox7Image1 = pygame.image.load("Images/UI/Inventory Box1.png").convert_alpha()
        IBox7Image2 = pygame.image.load("Images/UI/Inventory Box2.png").convert_alpha()
        IBox8Image1 = pygame.image.load("Images/UI/Inventory Box1.png").convert_alpha()
        IBox8Image2 = pygame.image.load("Images/UI/Inventory Box2.png").convert_alpha()
        key0Image1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons01.png").convert_alpha()
        key0Image2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons02.png").convert_alpha()
        key0Image3 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons03.png").convert_alpha()
        key1Image1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons11.png").convert_alpha()
        key1Image2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons12.png").convert_alpha()
        key1Image3 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons13.png").convert_alpha()
        key2Image1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons21.png").convert_alpha()
        key2Image2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons22.png").convert_alpha()
        key2Image3 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons23.png").convert_alpha()
        key3Image1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons31.png").convert_alpha()
        key3Image2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons32.png").convert_alpha()
        key3Image3 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons33.png").convert_alpha()
        key4Image1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons41.png").convert_alpha()
        key4Image2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons42.png").convert_alpha()
        key4Image3 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons43.png").convert_alpha()
        key5Image1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons51.png").convert_alpha()
        key5Image2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons52.png").convert_alpha()
        key5Image3 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons53.png").convert_alpha()
        key6Image1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons61.png").convert_alpha()
        key6Image2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons62.png").convert_alpha()
        key6Image3 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons63.png").convert_alpha()
        key7Image1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons71.png").convert_alpha()
        key7Image2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons72.png").convert_alpha()
        key7Image3 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons73.png").convert_alpha()
        key8Image1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons81.png").convert_alpha()
        key8Image2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons82.png").convert_alpha()
        key8Image3 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons83.png").convert_alpha()
        key9Image1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons91.png").convert_alpha()
        key9Image2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons92.png").convert_alpha()
        key9Image3 = pygame.image.load("Images/TUTORIAL/KEYPAD/Buttons93.png").convert_alpha()
        keyBImage1 = pygame.image.load("Images/TUTORIAL/KEYPAD/ButtonsB1.png").convert_alpha()
        keyBImage2 = pygame.image.load("Images/TUTORIAL/KEYPAD/ButtonsB2.png").convert_alpha()
        keyBImage3 = pygame.image.load("Images/TUTORIAL/KEYPAD/ButtonsB3.png").convert_alpha()
        keypadBackgroundImage = pygame.image.load("Images/TUTORIAL/KEYPAD/Background.png").convert_alpha()
        keypadImage1 = pygame.image.load("Images/TUTORIAL/KEYPAD/Keypad1.png").convert_alpha()
        keypadImage2 = pygame.image.load("Images/TUTORIAL/KEYPAD/Keypad2.png").convert_alpha()
        keyTImage1 = pygame.image.load("Images/TUTORIAL/KEYPAD/ButtonsT1.png").convert_alpha()
        keyTImage2 = pygame.image.load("Images/TUTORIAL/KEYPAD/ButtonsT2.png").convert_alpha()
        keyTImage3 = pygame.image.load("Images/TUTORIAL/KEYPAD/ButtonsT3.png").convert_alpha()
        leftSideImage1 = pygame.image.load("Images/UI/Left Side1.png").convert_alpha()
        leftSideImage2 = pygame.image.load("Images/UI/Left Side2.png").convert_alpha()
        menuBackgroundImage = pygame.image.load("Images/MENU/MENU.png").convert_alpha()
        menuBoxImage = pygame.image.load("Images/MENU/MENUBOX.png").convert_alpha()
        numberImage = pygame.image.load("Images/TUTORIAL/Number.png")
        openButtonImage1 = pygame.image.load("Images/UI/Open1.png").convert_alpha()
        openButtonImage2 = pygame.image.load("Images/UI/Open2.png").convert_alpha()
        outputBox = pygame.image.load("Images/UI/OutputBox.png").convert_alpha()
        panelImage1 = pygame.image.load("Images/TUTORIAL/PanelBroken1.png").convert_alpha()
        panelImage10 = pygame.image.load("Images/TUTORIAL/PanelInventory.png").convert_alpha()
        panelImage2 = pygame.image.load("Images/TUTORIAL/PanelBroken2.png").convert_alpha()
        panelImage3 = pygame.image.load("Images/TUTORIAL/PanelOpen1.png").convert_alpha()
        panelImage4 = pygame.image.load("Images/TUTORIAL/PanelOpen2.png").convert_alpha()
        panelImage5 = pygame.image.load("Images/TUTORIAL/PanelWeld1.png").convert_alpha()
        panelImage6 = pygame.image.load("Images/TUTORIAL/PanelWeld2.png").convert_alpha()
        panelImage7 = pygame.image.load("Images/TUTORIAL/PanelFixed1.png").convert_alpha()
        panelImage8 = pygame.image.load("Images/TUTORIAL/PanelFixed2.png").convert_alpha()
        panelImage9 = pygame.image.load("Images/TUTORIAL/PanelClosed.png").convert_alpha()
        pickUpButtonImage1 = pygame.image.load("Images/UI/Pick Up1.png").convert_alpha()
        pickUpButtonImage2 = pygame.image.load("Images/UI/Pick Up2.png").convert_alpha()
        pullButtonImage1 = pygame.image.load("Images/UI/Pull1.png").convert_alpha()
        pullButtonImage2 = pygame.image.load("Images/UI/Pull2.png").convert_alpha()
        pushButtonImage1 = pygame.image.load("Images/UI/Push1.png").convert_alpha()
        pushButtonImage2 = pygame.image.load("Images/UI/Push2.png").convert_alpha()
        rightSideImage1 = pygame.image.load("Images/UI/Right Side1.png").convert_alpha()
        rightSideImage2 = pygame.image.load("Images/UI/Right Side2.png").convert_alpha()
        screwdriverImage1 = pygame.image.load("Images/TUTORIAL/Screwdriver1.png").convert_alpha()
        screwdriverImage2 = pygame.image.load("Images/TUTORIAL/Screwdriver2.png").convert_alpha()
        screwdriverImage3 = pygame.image.load("Images/TUTORIAL/Screwdriver3.png").convert_alpha()
        skipButtonImage1 = pygame.image.load("Images/UI/Skip1.png").convert_alpha()
        skipButtonImage2 = pygame.image.load("Images/UI/Skip2.png").convert_alpha()
        skipButtonImage3 = pygame.image.load("Images/UI/Skip3.png").convert_alpha()
        skipButtonImage4 = pygame.image.load("Images/UI/Skip4.png").convert_alpha()
        solderImage1 = pygame.image.load("Images/TUTORIAL/Solder1.png").convert_alpha()
        solderImage2 = pygame.image.load("Images/TUTORIAL/Solder2.png").convert_alpha()
        solderImage3 = pygame.image.load("Images/TUTORIAL/Solder3.png").convert_alpha()
        talkToButtonImage1 = pygame.image.load("Images/UI/Talk To1.png").convert_alpha()
        talkToButtonImage2 = pygame.image.load("Images/UI/Talk To2.png").convert_alpha()
        tapeImage1 = pygame.image.load("Images/TUTORIAL/Tape1.png").convert_alpha()
        tapeImage2 = pygame.image.load("Images/TUTORIAL/Tape2.png").convert_alpha()
        tapeImage3 = pygame.image.load("Images/TUTORIAL/Tape3.png").convert_alpha()
        titleImage = pygame.image.load("Images/MENU/Title.png").convert_alpha()
        UIBackgroundImage = pygame.image.load("Images/UI/UIBackground.png").convert_alpha()
        useButtonImage1 = pygame.image.load("Images/UI/Use1.png").convert_alpha()
        useButtonImage2 = pygame.image.load("Images/UI/Use2.png").convert_alpha()


        Arrow1Image1 = pygame.transform.scale(Arrow1Image1, (round(Arrow1Image1.get_width()*scale), round(Arrow1Image1.get_height()*scale)))
        Arrow1Image2 = pygame.transform.scale(Arrow1Image2, (round(Arrow1Image2.get_width()*scale), round(Arrow1Image2.get_height()*scale)))
        Arrow2Image1 = pygame.transform.scale(Arrow2Image1, (round(Arrow2Image1.get_width()*scale), round(Arrow2Image1.get_height()*scale)))
        Arrow2Image2 = pygame.transform.scale(Arrow2Image2, (round(Arrow2Image2.get_width()*scale), round(Arrow2Image2.get_height()*scale)))
        backgroundSegment1 = pygame.transform.scale(backgroundSegment1, (round(backgroundSegment1.get_width()*scale), round(backgroundSegment1.get_height()*scale)))
        backgroundSegment2 = pygame.transform.scale(backgroundSegment2, (round(backgroundSegment2.get_width()*scale), round(backgroundSegment2.get_height()*scale)))
        blankImage = pygame.transform.scale(blankImage, (round(blankImage.get_width()*scale), round(blankImage.get_height()*scale)))
        bookcaseImage1 = pygame.transform.scale(bookcaseImage1, (round(bookcaseImage1.get_width()*scale), round(bookcaseImage1.get_height()*scale)))
        bookcaseImage2 = pygame.transform.scale(bookcaseImage2, (round(bookcaseImage2.get_width()*scale), round(bookcaseImage2.get_height()*scale)))
        bookcaseImage3 = pygame.transform.scale(bookcaseImage3, (round(bookcaseImage3.get_width()*scale), round(bookcaseImage3.get_height()*scale)))        
        button1Image1 = pygame.transform.scale(button1Image1, (round(button1Image1.get_width()*scale), round(button1Image1.get_height()*scale)))
        button1Image2 = pygame.transform.scale(button1Image2, (round(button1Image2.get_width()*scale), round(button1Image2.get_height()*scale)))
        button2Image1 = pygame.transform.scale(button2Image1, (round(button2Image1.get_width()*scale), round(button2Image1.get_height()*scale)))
        button2Image2 = pygame.transform.scale(button2Image2, (round(button2Image2.get_width()*scale), round(button2Image2.get_height()*scale)))
        button3Image1 = pygame.transform.scale(button3Image1, (round(button3Image1.get_width()*scale), round(button3Image1.get_height()*scale)))
        button3Image2 = pygame.transform.scale(button3Image2, (round(button3Image2.get_width()*scale), round(button4Image2.get_height()*scale)))
        button4Image1 = pygame.transform.scale(button4Image1, (round(button4Image1.get_width()*scale), round(button4Image1.get_height()*scale)))
        button4Image2 = pygame.transform.scale(button4Image2, (round(button4Image2.get_width()*scale), round(button4Image2.get_height()*scale)))
        closeButtonImage1 = pygame.transform.scale(closeButtonImage1, (round(closeButtonImage1.get_width()*scale), round(closeButtonImage1.get_height()*scale)))
        closeButtonImage2 = pygame.transform.scale(closeButtonImage2, (round(closeButtonImage2.get_width()*scale), round(closeButtonImage2.get_height()*scale)))
        closeKeypadButtonImage1 = pygame.transform.scale(closeKeypadButtonImage1, (round(closeKeypadButtonImage1.get_width()*scale), round(closeKeypadButtonImage1.get_height()*scale)))
        closeKeypadButtonImage2 = pygame.transform.scale(closeKeypadButtonImage2, (round(closeKeypadButtonImage2.get_width()*scale), round(closeKeypadButtonImage2.get_height()*scale)))
        closeNPCButtonImage1 = pygame.transform.scale(closeNPCButtonImage1, (round(closeNPCButtonImage1.get_width()*scale), round(closeNPCButtonImage1.get_height()*scale)))
        closeNPCButtonImage2 = pygame.transform.scale(closeNPCButtonImage2, (round(closeNPCButtonImage2.get_width()*scale), round(closeNPCButtonImage2.get_height()*scale)))
        closeOutputButtonImage1 = pygame.transform.scale(closeOutputButtonImage1, (round(closeOutputButtonImage1.get_width()*scale), round(closeOutputButtonImage1.get_height()*scale)))
        closeOutputButtonImage2 = pygame.transform.scale(closeOutputButtonImage2, (round(closeOutputButtonImage2.get_width()*scale), round(closeOutputButtonImage2.get_height()*scale)))
        computerImage1 = pygame.transform.scale(computerImage1, (round(computerImage1.get_width()*scale), round(computerImage1.get_height()*scale)))
        computerImage2 = pygame.transform.scale(computerImage2, (round(computerImage2.get_width()*scale), round(computerImage2.get_height()*scale)))
        computerImage3 = pygame.transform.scale(computerImage3, (round(computerImage3.get_width()*scale), round(computerImage3.get_height()*scale)))
        computerImage4 = pygame.transform.scale(computerImage4, (round(computerImage4.get_width()*scale), round(computerImage4.get_height()*scale)))
        doorA24WImage = pygame.transform.scale(doorA24WImage, (round(doorA24WImage.get_width()*scale), round(doorA24WImage.get_height()*scale)))
        doorA25WImage = pygame.transform.scale(doorA25WImage, (round(doorA25WImage.get_width()*scale), round(doorA25WImage.get_height()*scale)))
        doorBImage = pygame.transform.scale(doorBImage, (round(doorBImage.get_width()*scale), round(doorBImage.get_height()*scale)))
        doorCImage = pygame.transform.scale(doorCImage, (round(doorCImage.get_width()*scale), round(doorCImage.get_height()*scale)))
        doorSImage = pygame.transform.scale(doorSImage, (round(doorSImage.get_width()*scale), round(doorSImage.get_height()*scale)))
        doorTImage = pygame.transform.scale(doorTImage, (round(doorTImage.get_width()*scale), round(doorTImage.get_height()*scale)))
        doorTBImage1 = pygame.transform.scale(doorTBImage1, (round(doorTBImage1.get_width()*scale), round(doorTBImage1.get_height()*scale)))
        doorTBImage2 = pygame.transform.scale(doorTBImage2, (round(doorTBImage2.get_width()*scale), round(doorTBImage2.get_height()*scale)))
        engineImage1 = pygame.transform.scale(engineImage1, (round(engineImage1.get_width()*scale), round(engineImage1.get_height()*scale)))
        engineImage2 = pygame.transform.scale(engineImage2, (round(engineImage2.get_width()*scale), round(engineImage2.get_height()*scale)))
        engineImage3 = pygame.transform.scale(engineImage3, (round(engineImage3.get_width()*scale), round(engineImage3.get_height()*scale)))
        engineImage4 = pygame.transform.scale(engineImage4, (round(engineImage4.get_width()*scale), round(engineImage4.get_height()*scale)))
        engineImage5 = pygame.transform.scale(engineImage5, (round(engineImage5.get_width()*scale), round(engineImage5.get_height()*scale)))
        examineButtonImage1 = pygame.transform.scale(examineButtonImage1, (round(examineButtonImage1.get_width()*scale), round(examineButtonImage1.get_height()*scale)))
        examineButtonImage2 = pygame.transform.scale(examineButtonImage2, (round(examineButtonImage2.get_width()*scale), round(examineButtonImage2.get_height()*scale)))
        fusionCoreImage1 = pygame.transform.scale(fusionCoreImage1, (round(fusionCoreImage1.get_width()*scale), round(fusionCoreImage1.get_height()*scale)))
        fusionCoreImage2 = pygame.transform.scale(fusionCoreImage2, (round(fusionCoreImage2.get_width()*scale), round(fusionCoreImage2.get_height()*scale)))
        fusionCoreImage3 = pygame.transform.scale(fusionCoreImage3, (round(fusionCoreImage3.get_width()*scale), round(fusionCoreImage3.get_height()*scale)))
        giveButtonImage1 = pygame.transform.scale(giveButtonImage1, (round(giveButtonImage1.get_width()*scale), round(giveButtonImage1.get_height()*scale)))
        giveButtonImage2 = pygame.transform.scale(giveButtonImage2, (round(giveButtonImage2.get_width()*scale), round(giveButtonImage2.get_height()*scale)))
        IBox1Image1 = pygame.transform.scale(IBox1Image1, (round(IBox1Image1.get_width()*scale), round(IBox1Image1.get_height()*scale)))
        IBox1Image2 = pygame.transform.scale(IBox1Image2, (round(IBox1Image2.get_width()*scale), round(IBox1Image2.get_height()*scale)))
        IBox2Image1 = pygame.transform.scale(IBox2Image1, (round(IBox2Image1.get_width()*scale), round(IBox2Image1.get_height()*scale)))
        IBox2Image2 = pygame.transform.scale(IBox2Image2, (round(IBox2Image2.get_width()*scale), round(IBox2Image2.get_height()*scale)))
        IBox3Image1 = pygame.transform.scale(IBox3Image1, (round(IBox3Image1.get_width()*scale), round(IBox3Image1.get_height()*scale)))
        IBox3Image2 = pygame.transform.scale(IBox3Image2, (round(IBox3Image2.get_width()*scale), round(IBox3Image2.get_height()*scale)))
        IBox4Image1 = pygame.transform.scale(IBox4Image1, (round(IBox4Image1.get_width()*scale), round(IBox4Image1.get_height()*scale)))
        IBox4Image2 = pygame.transform.scale(IBox4Image2, (round(IBox4Image2.get_width()*scale), round(IBox4Image2.get_height()*scale)))
        IBox5Image1 = pygame.transform.scale(IBox5Image1, (round(IBox5Image1.get_width()*scale), round(IBox5Image1.get_height()*scale)))
        IBox5Image2 = pygame.transform.scale(IBox5Image2, (round(IBox5Image2.get_width()*scale), round(IBox5Image2.get_height()*scale)))
        IBox6Image1 = pygame.transform.scale(IBox6Image1, (round(IBox6Image1.get_width()*scale), round(IBox6Image1.get_height()*scale)))
        IBox6Image2 = pygame.transform.scale(IBox6Image2, (round(IBox6Image2.get_width()*scale), round(IBox6Image2.get_height()*scale)))
        IBox7Image1 = pygame.transform.scale(IBox7Image1, (round(IBox7Image1.get_width()*scale), round(IBox7Image1.get_height()*scale)))
        IBox7Image2 = pygame.transform.scale(IBox7Image2, (round(IBox7Image2.get_width()*scale), round(IBox7Image2.get_height()*scale)))
        IBox8Image1 = pygame.transform.scale(IBox8Image1, (round(IBox8Image1.get_width()*scale), round(IBox8Image1.get_height()*scale)))
        IBox8Image2 = pygame.transform.scale(IBox8Image2, (round(IBox8Image2.get_width()*scale), round(IBox8Image2.get_height()*scale)))
        key0Image1 = pygame.transform.scale(key0Image1, (round(key0Image1.get_width()*scale*3), round(key0Image1.get_height()*scale*3)))
        key0Image2 = pygame.transform.scale(key0Image2, (round(key0Image2.get_width()*scale*3), round(key0Image2.get_height()*scale*3)))
        key0Image3 = pygame.transform.scale(key0Image3, (round(key0Image3.get_width()*scale*3), round(key0Image3.get_height()*scale*3)))
        key1Image1 = pygame.transform.scale(key1Image1, (round(key1Image1.get_width()*scale*3), round(key1Image1.get_height()*scale*3)))
        key1Image2 = pygame.transform.scale(key1Image2, (round(key1Image2.get_width()*scale*3), round(key1Image2.get_height()*scale*3)))
        key1Image3 = pygame.transform.scale(key1Image3, (round(key1Image3.get_width()*scale*3), round(key1Image3.get_height()*scale*3)))
        key2Image1 = pygame.transform.scale(key2Image1, (round(key2Image1.get_width()*scale*3), round(key2Image1.get_height()*scale*3)))
        key2Image2 = pygame.transform.scale(key2Image2, (round(key2Image2.get_width()*scale*3), round(key2Image2.get_height()*scale*3)))
        key2Image3 = pygame.transform.scale(key2Image3, (round(key2Image3.get_width()*scale*3), round(key2Image3.get_height()*scale*3)))
        key3Image1 = pygame.transform.scale(key3Image1, (round(key3Image1.get_width()*scale*3), round(key3Image1.get_height()*scale*3)))
        key3Image2 = pygame.transform.scale(key3Image2, (round(key3Image2.get_width()*scale*3), round(key3Image2.get_height()*scale*3)))
        key3Image3 = pygame.transform.scale(key3Image3, (round(key3Image3.get_width()*scale*3), round(key3Image3.get_height()*scale*3)))
        key4Image1 = pygame.transform.scale(key4Image1, (round(key4Image1.get_width()*scale*3), round(key4Image1.get_height()*scale*3)))
        key4Image2 = pygame.transform.scale(key4Image2, (round(key4Image2.get_width()*scale*3), round(key4Image2.get_height()*scale*3)))
        key4Image3 = pygame.transform.scale(key4Image3, (round(key4Image3.get_width()*scale*3), round(key4Image3.get_height()*scale*3)))
        key5Image1 = pygame.transform.scale(key5Image1, (round(key5Image1.get_width()*scale*3), round(key5Image1.get_height()*scale*3)))
        key5Image2 = pygame.transform.scale(key5Image2, (round(key5Image2.get_width()*scale*3), round(key5Image2.get_height()*scale*3)))
        key5Image3 = pygame.transform.scale(key5Image3, (round(key5Image3.get_width()*scale*3), round(key5Image3.get_height()*scale*3)))
        key6Image1 = pygame.transform.scale(key6Image1, (round(key6Image1.get_width()*scale*3), round(key6Image1.get_height()*scale*3)))
        key6Image2 = pygame.transform.scale(key6Image2, (round(key6Image2.get_width()*scale*3), round(key6Image2.get_height()*scale*3)))
        key6Image3 = pygame.transform.scale(key6Image3, (round(key6Image3.get_width()*scale*3), round(key6Image3.get_height()*scale*3)))
        key7Image1 = pygame.transform.scale(key7Image1, (round(key7Image1.get_width()*scale*3), round(key7Image1.get_height()*scale*3)))
        key7Image2 = pygame.transform.scale(key7Image2, (round(key7Image2.get_width()*scale*3), round(key7Image2.get_height()*scale*3)))
        key7Image3 = pygame.transform.scale(key7Image3, (round(key7Image3.get_width()*scale*3), round(key7Image3.get_height()*scale*3)))
        key8Image1 = pygame.transform.scale(key8Image1, (round(key8Image1.get_width()*scale*3), round(key8Image1.get_height()*scale*3)))
        key8Image2 = pygame.transform.scale(key8Image2, (round(key8Image2.get_width()*scale*3), round(key8Image2.get_height()*scale*3)))
        key8Image3 = pygame.transform.scale(key8Image3, (round(key8Image3.get_width()*scale*3), round(key8Image3.get_height()*scale*3)))
        key9Image1 = pygame.transform.scale(key9Image1, (round(key9Image1.get_width()*scale*3), round(key9Image1.get_height()*scale*3)))
        key9Image2 = pygame.transform.scale(key9Image2, (round(key9Image2.get_width()*scale*3), round(key9Image2.get_height()*scale*3)))
        key9Image3 = pygame.transform.scale(key9Image3, (round(key9Image3.get_width()*scale*3), round(key9Image3.get_height()*scale*3)))
        keyBImage1 = pygame.transform.scale(keyBImage1, (round(keyBImage1.get_width()*scale*3), round(keyBImage1.get_height()*scale*3)))
        keyBImage2 = pygame.transform.scale(keyBImage2, (round(keyBImage2.get_width()*scale*3), round(keyBImage2.get_height()*scale*3)))
        keyBImage3 = pygame.transform.scale(keyBImage3, (round(keyBImage3.get_width()*scale*3), round(keyBImage3.get_height()*scale*3)))
        keypadBackgroundImage = pygame.transform.scale(keypadBackgroundImage, (round(keypadBackgroundImage.get_width()*scale), round(keypadBackgroundImage.get_height()*scale)))
        keypadImage1 = pygame.transform.scale(keypadImage1, (round(keypadImage1.get_width()*scale), round(keypadImage1.get_height()*scale)))
        keypadImage2 = pygame.transform.scale(keypadImage2, (round(keypadImage2.get_width()*scale), round(keypadImage2.get_height()*scale)))
        keyTImage1 = pygame.transform.scale(keyTImage1, (round(keyTImage1.get_width()*scale*3), round(keyTImage1.get_height()*scale*3)))
        keyTImage2 = pygame.transform.scale(keyTImage2, (round(keyTImage2.get_width()*scale*3), round(keyTImage2.get_height()*scale*3)))
        keyTImage3 = pygame.transform.scale(keyTImage3, (round(keyTImage3.get_width()*scale*3), round(keyTImage3.get_height()*scale*3)))
        leftSideImage1 = pygame.transform.scale(leftSideImage1, (round(leftSideImage1.get_width()*scale), round(leftSideImage1.get_height()*scale)))
        leftSideImage2 = pygame.transform.scale(leftSideImage2, (round(leftSideImage2.get_width()*scale), round(leftSideImage2.get_height()*scale)))
        menuBackgroundImage = pygame.transform.scale(menuBackgroundImage, (round(menuBackgroundImage.get_width()*scale+1), round(menuBackgroundImage.get_height()*scale)))
        menuBox = pygame.transform.scale(menuBoxImage, (round(menuBoxImage.get_width()*scale), round(menuBoxImage.get_height()*scale)))
        numberImage = pygame.transform.scale(numberImage, (round(numberImage.get_width()*scale), round(numberImage.get_height()*scale)))
        openButtonImage1 = pygame.transform.scale(openButtonImage1, (round(openButtonImage1.get_width()*scale), round(openButtonImage1.get_height()*scale)))
        openButtonImage2 = pygame.transform.scale(openButtonImage2, (round(openButtonImage2.get_width()*scale), round(openButtonImage2.get_height()*scale)))
        outputBox = pygame.transform.scale(outputBox, (round(outputBox.get_width()*scale), round(outputBox.get_height()*scale)))
        panelImage1 = pygame.transform.scale(panelImage1, (round(panelImage1.get_width()*scale), round(panelImage1.get_height()*scale)))
        panelImage10 = pygame.transform.scale(panelImage10, (round(panelImage10.get_width()*scale), round(panelImage10.get_height()*scale)))
        panelImage2 = pygame.transform.scale(panelImage2, (round(panelImage2.get_width()*scale), round(panelImage2.get_height()*scale)))
        panelImage3 = pygame.transform.scale(panelImage3, (round(panelImage3.get_width()*scale), round(panelImage3.get_height()*scale)))
        panelImage4 = pygame.transform.scale(panelImage4, (round(panelImage4.get_width()*scale), round(panelImage4.get_height()*scale)))
        panelImage5 = pygame.transform.scale(panelImage5, (round(panelImage5.get_width()*scale), round(panelImage5.get_height()*scale)))
        panelImage6 = pygame.transform.scale(panelImage6, (round(panelImage6.get_width()*scale), round(panelImage6.get_height()*scale)))
        panelImage7 = pygame.transform.scale(panelImage7, (round(panelImage7.get_width()*scale), round(panelImage7.get_height()*scale)))
        panelImage8 = pygame.transform.scale(panelImage8, (round(panelImage8.get_width()*scale), round(panelImage8.get_height()*scale)))
        panelImage9 = pygame.transform.scale(panelImage9, (round(panelImage9.get_width()*scale), round(panelImage9.get_height()*scale)))
        pickUpButtonImage1 = pygame.transform.scale(pickUpButtonImage1, (round(pickUpButtonImage1.get_width()*scale), round(pickUpButtonImage1.get_height()*scale)))
        pickUpButtonImage2 = pygame.transform.scale(pickUpButtonImage2, (round(pickUpButtonImage2.get_width()*scale), round(pickUpButtonImage2.get_height()*scale)))
        pullButtonImage1 = pygame.transform.scale(pullButtonImage1, (round(pullButtonImage1.get_width()*scale), round(pullButtonImage1.get_height()*scale)))
        pullButtonImage2 = pygame.transform.scale(pullButtonImage2, (round(pullButtonImage2.get_width()*scale), round(pullButtonImage2.get_height()*scale)))
        pushButtonImage1 = pygame.transform.scale(pushButtonImage1, (round(pushButtonImage1.get_width()*scale), round(pushButtonImage1.get_height()*scale)))
        pushButtonImage2 = pygame.transform.scale(pushButtonImage2, (round(pushButtonImage2.get_width()*scale), round(pushButtonImage2.get_height()*scale)))
        rightSideImage1 = pygame.transform.scale(rightSideImage1, (round(rightSideImage1.get_width()*scale), round(rightSideImage1.get_height()*scale)))
        rightSideImage2 = pygame.transform.scale(rightSideImage2, (round(rightSideImage2.get_width()*scale), round(rightSideImage2.get_height()*scale)))
        screwdriverImage1 = pygame.transform.scale(screwdriverImage1, (round(screwdriverImage1.get_width()*scale), round(screwdriverImage1.get_height()*scale)))
        screwdriverImage2 = pygame.transform.scale(screwdriverImage2, (round(screwdriverImage2.get_width()*scale), round(screwdriverImage2.get_height()*scale)))
        screwdriverImage3 = pygame.transform.scale(screwdriverImage3, (round(screwdriverImage3.get_width()*scale), round(screwdriverImage3.get_height()*scale)))
        skipButtonImage1 = pygame.transform.scale(skipButtonImage1, (round(skipButtonImage1.get_width()*scale), round(skipButtonImage1.get_height()*scale)))
        skipButtonImage2 = pygame.transform.scale(skipButtonImage2, (round(skipButtonImage2.get_width()*scale), round(skipButtonImage2.get_height()*scale)))
        solderImage1 = pygame.transform.scale(solderImage1, (round(solderImage1.get_width()*scale), round(solderImage1.get_height()*scale)))
        solderImage2 = pygame.transform.scale(solderImage2, (round(solderImage2.get_width()*scale), round(solderImage2.get_height()*scale)))
        solderImage3 = pygame.transform.scale(solderImage3, (round(solderImage3.get_width()*scale), round(solderImage3.get_height()*scale)))
        talkToButtonImage1 = pygame.transform.scale(talkToButtonImage1, (round(talkToButtonImage1.get_width()*scale), round(talkToButtonImage1.get_height()*scale)))
        talkToButtonImage2 = pygame.transform.scale(talkToButtonImage2, (round(talkToButtonImage2.get_width()*scale), round(talkToButtonImage2.get_height()*scale)))
        tapeImage1 = pygame.transform.scale(tapeImage1, (round(tapeImage1.get_width()*scale), round(tapeImage1.get_height()*scale)))
        tapeImage2 = pygame.transform.scale(tapeImage2, (round(tapeImage2.get_width()*scale), round(tapeImage2.get_height()*scale)))
        tapeImage3 = pygame.transform.scale(tapeImage3, (round(tapeImage3.get_width()*scale), round(tapeImage3.get_height()*scale)))
        titleImage = pygame.transform.scale(titleImage, (round(titleImage.get_width()*scale), round(titleImage.get_height()*scale)))
        UIBackgroundImage = pygame.transform.scale(UIBackgroundImage, (round(UIBackgroundImage.get_width()*scale), round(UIBackgroundImage.get_height()*scale)))
        useButtonImage1 = pygame.transform.scale(useButtonImage1, (round(useButtonImage1.get_width()*scale), round(useButtonImage1.get_height()*scale)))
        useButtonImage2 = pygame.transform.scale(useButtonImage2, (round(useButtonImage2.get_width()*scale), round(useButtonImage2.get_height()*scale)))

        bookcaseImage = bookcaseImage1
        Arrow1Image = Arrow1Image1
        Arrow2Image = Arrow2Image1
        button1Image = button1Image1
        button2Image = button2Image1
        button3Image = button3Image1
        button4Image = button4Image1
        closeButtonImage = closeButtonImage1
        closeKeypadButtonImage = closeKeypadButtonImage1
        closeNPCButtonImage = closeNPCButtonImage1
        closeOutputButtonImage = closeOutputButtonImage1
        computerImage = computerImage1
        doorTBImage = doorTBImage1
        engineImage = engineImage1
        examineButtonImage = examineButtonImage1
        fusionCoreImage = fusionCoreImage1
        giveButtonImage = giveButtonImage1
        IBox1Image = IBox1Image1
        IBox2Image = IBox2Image1
        IBox3Image = IBox3Image1
        IBox4Image = IBox4Image1
        IBox5Image = IBox5Image1
        IBox6Image = IBox6Image1
        IBox7Image = IBox7Image1
        IBox8Image = IBox8Image1
        key0Image = key0Image1
        key1Image = key1Image1
        key2Image = key2Image1
        key3Image = key3Image1
        key4Image = key4Image1
        key5Image = key5Image1
        key6Image = key6Image1
        key7Image = key7Image1
        key8Image = key8Image1
        key9Image = key9Image1
        keyBImage = keyBImage1
        keypadImage = keypadImage1
        keyTImage = keyTImage1
        leftSideImage = leftSideImage1
        openButtonImage = openButtonImage1
        panelImage = panelImage1
        pickUpButtonImage = pickUpButtonImage1
        pullButtonImage = pullButtonImage1
        pushButtonImage = pushButtonImage1
        rightSideImage = rightSideImage1
        screwdriverImage = screwdriverImage1
        skipButtonImage = skipButtonImage1
        solderImage = solderImage1
        talkToButtonImage = talkToButtonImage1
        tapeImage = tapeImage1
        useButtonImage = useButtonImage1
        
        flags["UpdateImages"] = False

    if flags["DoorInOpen"]: # This flag is a simple selection in which the "In Door" is progressively opened whilst it is active
        if doorInTY != doorInDefaultY-142:
            doorInTY-=1
            doorInBY+=1
        else:
            flags["DoorInOpen"] = False
            flags["DoorInOpened"] = True
            
    if flags["DoorInClose"]: # Same as above but closing
        flags["DoorInOpened"] = False
        if doorInTY != doorInDefaultY:
            doorInTY+=1
            doorInBY-=1
        else:
            flags["DoorInClose"] = False

    if flags["DoorOutOpen"]: # Same as above but for the door out which is the door that leads outwards from the centre
        if doorOutTY != doorOutDefaultY-142:
            doorOutTY-=1
            doorOutBY+=1
        else:
            flags["DoorOutOpen"] = False
            flags["DoorOutOpened"] = True
            
    if flags["DoorOutClose"]: # Same as above but closing
        flags["DoorOutOpened"] = False
        if doorOutTY != doorOutDefaultY:
            doorOutTY+=1
            doorOutBY-=1
        else:
            flags["DoorOutClose"] = False

    if flags["CursorOverride"]: #Simp,e selection statement that determines the state of the cursor (what it looks like)
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)

    if flags["PlayMusic"]: # Runs once to play music
        TRACKS = get_music(area)
        pygame.mixer.music.load(TRACKS[track])
        pygame.mixer.music.play()
        flags["PlayMusic"] = False
        
    if flags["StopMusic"]: # Will pause playing music however it is currently unused
        pygame.mixer.music.pause()
        flags["StopMusic"] = False
    
    if flags["ShowStart"]: # First complex flag. This flag begins as active and sets the screen to the inital "Click anywhere to begin" state. All of the following scenes begin with a similar structure
        pygame.display.set_caption("The Crash - Start") # Sets Caption
        screen.blit(menuBackgroundImage, (0+barSizeX, 0+barSizeY)) # Sets background to the space image
        screen.blit(titleImage, (0+barSizeX, 33+barSizeY)) # Blitts the title
        playTextImage = textify(30, "Click anywhere to continue...", True, (colorMult, colorMult, colorMult), (round(25*scale)+barSizeX, round(200*scale)+barSizeY), screen) # Blits text that alternates in color on the screen
        colorPulseData = colorPulse(colorMult, fade) # Gets data from colorPulse function and assigns it to relevant varaibles
        colorMult = colorPulseData[0]
        fade = colorPulseData[1]
        
        if flags["StartButtonPressed"]: # Checks to see if the screen has been pressed
            if bpt >= 200: # After 0.2 seconds the room is set to main menu which will be changed in Blackout Flag
                flags["StartButtonPressed"] = False
                nextRoom = "MainMenu"

    if flags["ShowMenu"]: # The menu flag sets all of the structure of the Main menu. The following menus are identical except for the actions/names of the buttons so they do not require commenting
        pygame.display.set_caption("The Crash - Menu")
        screen.blit(menuBackgroundImage, (0+barSizeX, 0+barSizeY))
        screen.blit(menuBox, (round(menuBoxX*scale+barSizeX), round(108*scale+barSizeY)))# Blits menu background

        newGameButton = buttonify(button1Image, ((menuButtonX+140)*scale+barSizeX, 132*scale+barSizeY), screen) # Initalizes all of the buttons
        loadGameButton = buttonify(button2Image, ((menuButtonX+140)*scale+barSizeX, 246*scale+barSizeY), screen)
        settingsButton = buttonify(button3Image, ((menuButtonX+140)*scale+barSizeX, 360*scale+barSizeY), screen)
        backButton = buttonify(button4Image, ((menuButtonX+140)*scale+barSizeX, 474*scale+barSizeY), screen)
        
        newGameText = textify(30, "New Game", True, button1Color, ((menuTextX)*scale+barSizeX, 168*scale+barSizeY), screen) # Puts text on each of the buttons
        loadGameText = textify(30, "Load Game", True, button2Color, ((menuTextX)*scale+barSizeX, 282*scale+barSizeY), screen)
        settingsText = textify(30, "Settings", True, button3Color, ((menuTextX+20)*scale+barSizeX, 396*scale+barSizeY), screen)
        backText = textify(30, "Back", True, button4Color, ((menuTextX+45)*scale+barSizeX, 510*scale+barSizeY), screen)

        # HOVER CHECKS - Sets up the buttons and states and will change appearance if hovered or clicked

        tempArray = buttonHover("NewGameButtonPressed", button1Image, newGameButton, button1Color, "Intro")
        button1Image = tempArray[0]
        button1Color = tempArray[1]

        tempArray = buttonHover("LoadGameButtonPressed", button2Image, loadGameButton, button2Color, "LoadMenu")
        button2Image = tempArray[0]
        button2Color = tempArray[1]

        tempArray = buttonHover("SettingsButtonPressed", button3Image, settingsButton, button3Color, "SettingsMenu")
        button3Image = tempArray[0]
        button3Color = tempArray[1]

        tempArray = buttonHover("BackButtonPressed", button4Image, backButton, button4Color, "Start")
        button4Image = tempArray[0]
        button4Color = tempArray[1]

        #Checks to see if cursor is over any of the butttons and changes cursor accordingly

        if newGameButton[1].collidepoint(mouse) or loadGameButton[1].collidepoint(mouse) or backButton[1].collidepoint(mouse) or settingsButton[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False

    if flags["ShowLoadMenu"]:#Exact same structure as ShowMenu
        pygame.display.set_caption("The Crash - Load Game")
        bpt += loopTime
        screen.blit(menuBackgroundImage, (0+barSizeX, 0+barSizeY))
        screen.blit(menuBox, (round(menuBoxX*scale+barSizeX), round(108*scale+barSizeY)))

        loadGameButton1 = buttonify(button1Image, ((menuButtonX+140)*scale+barSizeX, 132*scale+barSizeY), screen)
        loadGameButton2 = buttonify(button2Image, ((menuButtonX+140)*scale+barSizeX, 246*scale+barSizeY), screen)
        loadGameButton3 = buttonify(button3Image, ((menuButtonX+140)*scale+barSizeX, 360*scale+barSizeY), screen)
        loadBackButton = buttonify(button4Image, ((menuButtonX+140)*scale+barSizeX, 474*scale+barSizeY), screen)
        
        loadGameButton1Text = textify(30, "Save 1", True, button1Color, ((menuTextX+35)*scale+barSizeX, 168*scale+barSizeY), screen)
        loadGameButton2Text = textify(30, "Save 2", True, button2Color, ((menuTextX+35)*scale+barSizeX, 282*scale+barSizeY), screen)
        loadGameButton3Text = textify(30, "Save 3", True, button3Color, ((menuTextX+35)*scale+barSizeX, 396*scale+barSizeY), screen)
        loadBackText = textify(30, "Back", True, button4Color, ((menuTextX+45)*scale+barSizeX, 510*scale+barSizeY), screen)

        # HOVER CHECKS

        tempArray = buttonHover("LoadGameButton1Pressed", button1Image, loadGameButton1, button1Color, "LoadSave")
        button1Image = tempArray[0]
        button1Color = tempArray[1]

        tempArray = buttonHover("LoadGameButton2Pressed", button2Image, loadGameButton2, button2Color, "LoadSave")
        button2Image = tempArray[0]
        button2Color = tempArray[1]

        tempArray = buttonHover("LoadGameButton3Pressed", button3Image, loadGameButton3, button3Color, "LoadSave")
        button3Image = tempArray[0]
        button3Color = tempArray[1]

        tempArray = buttonHover("LoadBackButtonPressed", button4Image, loadBackButton, button4Color, "MainMenu")
        button4Image = tempArray[0]
        button4Color = tempArray[1]
                
        if loadGameButton1[1].collidepoint(mouse) or loadGameButton2[1].collidepoint(mouse) or loadBackButton[1].collidepoint(mouse) or loadGameButton3[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False

    if flags["ShowSettingsMenu"]:#Exact same structure as ShowMenu with less buttons
        pygame.display.set_caption("The Crash - Settings")
        bpt += loopTime
        screen.blit(menuBackgroundImage,(0+barSizeX, 0+barSizeY))
        screen.blit(menuBox, (round(menuBoxX*scale+barSizeX), round(108*scale+barSizeY)))

        resolutionMenuButton = buttonify(button1Image, ((menuButtonX+140)*scale+barSizeX, 132*scale+barSizeY), screen)
        settingsBackButton = buttonify(button4Image, ((menuButtonX+140)*scale+barSizeX, 474*scale+barSizeY), screen)
        
        resolutionMenuButtonText1 = textify(25, "Change", True, button1Color, ((menuTextX+35)*scale+barSizeX, 148*scale+barSizeY), screen)
        resolutionMenuButtonText2 = textify(25, "Resolution", True, button1Color, ((menuTextX+20)*scale+barSizeX, 188*scale+barSizeY), screen)
        settingsBackText = textify(30, "Back", True, button4Color, ((menuTextX+45)*scale+barSizeX, 510*scale+barSizeY), screen)

        # HOVER CHECKS

        tempArray = buttonHover("ResolutionMenuButtonPressed", button1Image, resolutionMenuButton, button1Color, "ResolutionMenu")
        button1Image = tempArray[0]
        button1Color = tempArray[1]

        tempArray = buttonHover("SettingsBackButtonPressed", button4Image, settingsBackButton, button4Color, "MainMenu")
        button4Image = tempArray[0]
        button4Color = tempArray[1]
                
        if resolutionMenuButton[1].collidepoint(mouse) or settingsBackButton[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False

    if flags["ShowResolutionMenu"]:#Exact same structure as ShowMenu
        pygame.display.set_caption("The Crash - Resolution Menu")
        bpt += loopTime
        screen.blit(menuBackgroundImage, (0+barSizeX, 0+barSizeY))
        screen.blit(menuBox, (round(menuBoxX*scale+barSizeX), round(108*scale+barSizeY)))

        resolutionButton1 = buttonify(button1Image, ((menuButtonX+140)*scale+barSizeX, 132*scale+barSizeY), screen)
        resolutionButton2 = buttonify(button2Image, ((menuButtonX+140)*scale+barSizeX, 246*scale+barSizeY), screen)
        resolutionButton3 = buttonify(button3Image, ((menuButtonX+140)*scale+barSizeX, 360*scale+barSizeY), screen)
        resolutionBackButton = buttonify(button4Image, ((menuButtonX+140)*scale+barSizeX, 474*scale+barSizeY), screen)
        
        resolutionButton1Text = textify(30, "Auto", True, button1Color, ((menuTextX+45)*scale+barSizeX, 168*scale+barSizeY), screen)
        resolutionButton2Text = textify(30, "1000x700", True, button2Color, ((menuTextX+5)*scale+barSizeX, 282*scale+barSizeY), screen)
        resolutionButton3Text = textify(30, "1200x840", True, button3Color, ((menuTextX+5)*scale+barSizeX, 396*scale+barSizeY), screen)
        resolutionBackText = textify(30, "Back", True, button4Color, ((menuTextX+45)*scale+barSizeX, 510*scale+barSizeY), screen)

        # HOVER CHECKS

        tempArray = buttonHover("ResolutionButton1Pressed", button1Image, resolutionButton1, button1Color, "")
        button1Image = tempArray[0]
        button1Color = tempArray[1]

        tempArray = buttonHover("ResolutionButton2Pressed", button2Image, resolutionButton2, button2Color, "")
        button2Image = tempArray[0]
        button2Color = tempArray[1]

        tempArray = buttonHover("ResolutionButton3Pressed", button3Image, resolutionButton3, button3Color, "")
        button3Image = tempArray[0]
        button3Color = tempArray[1]

        tempArray = buttonHover("ResolutionBackButtonPressed", button4Image, resolutionBackButton, button4Color, "SettingsMenu")
        button4Image = tempArray[0]
        button4Color = tempArray[1]
                
        if resolutionButton1[1].collidepoint(mouse) or resolutionButton2[1].collidepoint(mouse) or resolutionBackButton[1].collidepoint(mouse) or resolutionButton3[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False

    if flags["ShowIntroCutscene"]: # Thi flag contains the intro which works based on a time that is tracked constantly
        pygame.display.set_caption("The Crash - Intro")
        screen.fill(black)#Sets screen to be black
        it += loopTime
        if it < 3000:#After 3 seconds it begins firstg set of scrolling text
            gameText = "THIS IS A"
            placeholder = 0
            textWait = 100
            gameTextImage = pygame.font.Font("Fonts/ROTG.otf", int(30*scale)).render("", True, white)
            
        if it >= 3000 and it < 4000:#Between 3 and 4 seconds it leaves text on screen
            gameTextImage = textify(50, gameText[:placeholder], True, green, (250*scale+barSizeX, 325*scale+barSizeY), screen)
            if textWait < it and placeholder != len(gameText):
                textWait = it+100
                placeholder+=1
                
        if it >= 4000 and it < 4500:
            gameTextImage = textify(50, "THIS IS A", True, green, (250*scale+barSizeX, 325*scale+barSizeY), screen)
            gameText = "TEMPORARY INTRO!"
            placeholder = 0
            textWait = 100
        if it >= 4500 and it < 6000:
            gameTextImage = textify(50, gameText[:placeholder], True, green, (250*scale+barSizeX, 325*scale+barSizeY), screen)
            if textWait < it and placeholder != len(gameText):
                textWait = it+100
                placeholder+=1
        if it >= 6000 and it < 7000:
            gameTextImage = textify(50, "TEMPORARY INTRO!", True, green, (250*scale+barSizeX, 325*scale+barSizeY), screen)
        if flags["IntroStage1"] and it >= 0:#Changes music to Intro
            pygame.mixer.music.load("Sounds/LOADING.ogg")
            pygame.mixer.music.play()
            flags["IntroStage1"] = False
        if flags["IntroStage2"] and it >= 6200:#Begins fade to game
            flags["FadeOut"] = True
            lft = 0
            it = 0
            flags["IntroStage2"] = False

        elif it >= 6500:#Changes room to Room1
            nextRoom = "Room1"
            flags["IntroStage2"] = True

    if flags["ShowTutorial"]:#Blits the tutorial information onto the screen
        outputInitialize([["Welcome to 'The Crash', a point and click"," adventure game that places you in"," the wreckage of a spaceship. You must","repair the ship and escape","into the vast expanse of space.","Each room has 4 walls each containing a","puzzle to solve, varying in difficulty.","The Goal","Open the door in each room to progress."],["TUTORIAL","Interact with the world by forming sentences.","You choose a command and then an interactable","object in the environment.","The use command can be used directly on the","environment or on an object first","For Example: use wrench on pipe.","You can rotate 90 degrees by clicking the sides","of the screen.","Escape by solving puzzles. Everything that can be","interacted with has a purpose..."],["This is a test build.","The game currently has just one room with content.","All the objects in the room are required to","continue currently"]],grayBlue,3)
        flags["ShowTutorial"] = False

    if flags["ShowRoom1"]:#The most complex of all of the flags this contains all of the content related to the starting room
        screen.fill(backgroundGray)
        
        if flags["ShowKeypadInterface"] == False:#Checks to see if the keypad is in use
            flags["ShowUserInterface"] = True

        if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
            pygame.display.set_caption("The Crash - Engine Room")

        if currentRoomSide == 0:#If direction is north...

            if flags["ShowDoorIn"]:#Shows Door. all futurge objects folow the same structure with there own unique code. The objects that can be picked up are almost identical. The constamnt objects are more unique as they react to specific objects
                screen.blit(doorCImage, (doorInCX*scale+barSizeX, doorInCY*scale+barSizeY))
                screen.blit(doorSImage, (doorInSX*scale+barSizeX, doorInSY*scale+barSizeY))
                screen.blit(doorTImage, (doorInTX*scale+barSizeX, doorInTY*scale+barSizeY))                     
                screen.blit(doorA24WImage, (doorInTX*scale+barSizeX, doorInTY*scale+barSizeY))                        
                screen.blit(doorBImage, (doorInBX*scale+barSizeX, doorInBY*scale+barSizeY))                     
                doorInTB = buttonify(doorTBImage, ((doorInTBX+150)*scale+barSizeX, doorInTBY*scale+barSizeY), screen)

                if flags["DoorInActive"]:
                    doorTBImage = doorTBImage2
                else:
                    doorTBImage = doorTBImage1
                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if doorInTB[1].collidepoint(mouse):
                        flags["DoorInActive"] = True
                    else:
                        flags["DoorInActive"] = False

            #This is in every room and makes the background which is constructed in segments
            screen.blit(backgroundSegment1, (-200*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (80*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (360*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment2, (639*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (918*scale+barSizeX, 0*scale+barSizeY))

            if flags["ShowKeypad"]:#Keypad Code
                keypad = buttonify(keypadImage,(530*scale+barSizeX, 140*scale+barSizeY), screen)
                if flags["KeypadActive"]:
                    keypadImage = keypadImage2
                else:
                    keypadImage = keypadImage1
                if flags["ShowPopUpMenu"] == False and flags["KeypadUnlocked"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if keypad[1].collidepoint(mouse):
                        flags["KeypadActive"] = True
                    else:
                        flags["KeypadActive"] = False
                else:
                    keypadImage = keypadImage1

            if flags["ShowFusionCore"]:#Fusion Core Code
                fusionCore = buttonify(fusionCoreImage,(300*scale+barSizeX, 206*scale+barSizeY), screen)
                if flags["FusionCoreActive"]:
                    fusionCoreImage = fusionCoreImage2
                else:
                    fusionCoreImage = fusionCoreImage1
                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if fusionCore[1].collidepoint(mouse):
                        flags["FusionCoreActive"] = True
                    else:
                        flags["FusionCoreActive"] = False

            if flags["ShowTape"]:
                tape = buttonify(tapeImage,(200*scale+barSizeX, 270*scale+barSizeY), screen)
                if flags["TapeActive"]:
                    tapeImage = tapeImage2
                else:
                    tapeImage = tapeImage1
                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if tape[1].collidepoint(mouse):
                        flags["TapeActive"] = True
                    else:
                        flags["TapeActive"] = False

        if currentRoomSide == 1:#EAST
            screen.blit(backgroundSegment1, (-200*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (80*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (360*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (639*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (918*scale+barSizeX, 0*scale+barSizeY))

            if flags["ShowPanel"]:#A more complex Environmental Object. Depending in the state of the panel different objects will have different effects. This can be seen in the if statement
                panel = buttonify(panelImage,(575*scale+barSizeX, 125*scale+barSizeY), screen)
                flags["PanelExists"] = True
                if flags["PanelFixed"] == False:
                    if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                        if panel[1].collidepoint(mouse):
                            flags["PanelActive"] = True
                        else:
                            flags["PanelActive"] = False
                if flags["PanelRemoved"] == False:
                    if flags["PanelActive"]:
                        panelImage = panelImage2
                    else:
                        panelImage = panelImage1
                else:
                    if flags["PanelWireFixed"] == False:
                        if flags["PanelActive"]:
                            panelImage = panelImage4
                        else:
                            panelImage = panelImage3
                    else:
                        if flags["PanelWireTaped"] == False:
                            if flags["PanelActive"]:
                                panelImage = panelImage6
                            else:
                                panelImage = panelImage5
                        else:
                            if flags["PanelFixed"] == False:
                                if flags["PanelActive"]:
                                    panelImage = panelImage8
                                else:
                                    panelImage = panelImage7
                            else:
                                panelImage = panelImage9

        if currentRoomSide == 2:
            screen.blit(backgroundSegment1, (-200*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (80*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (360*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (639*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (918*scale+barSizeX, 0*scale+barSizeY))
            if flags["ShowEngine"]: # As with the panel the negine reacts differently at different stages
                engine = buttonify(engineImage,(346*scale+barSizeX, 30*scale+barSizeY), screen)
                flags["EngineExists"] = True
                if flags["EngineFixed"] == False:
                    if flags["EngineTaped"] == False:
                        if flags["EngineActive"]:
                            engineImage = engineImage2
                        else:
                            engineImage = engineImage1
                    else:
                        if flags["EngineActive"]:
                            engineImage = engineImage4
                        else:
                            engineImage = engineImage3

                    if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                        if engine[1].collidepoint(mouse):
                            flags["EngineActive"] = True
                        else:
                            flags["EngineActive"] = False
                else:
                    engineImage = engineImage5

            if flags["ShowSolder"]:
                solder = buttonify(solderImage,(523*scale+barSizeX, 223*scale+barSizeY), screen)
                flags["SolderExists"] = True
                if flags["SolderActive"]:
                    solderImage = solderImage2
                else:
                    solderImage = solderImage1
                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if solder[1].collidepoint(mouse):
                        flags["SolderActive"] = True
                    else:
                        flags["SolderActive"] = False

        if currentRoomSide == 3:
            screen.blit(backgroundSegment1, (-200*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (80*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (360*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (639*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (918*scale+barSizeX, 0*scale+barSizeY))

            if flags["ShowScrewdriver"]:
                screwdriver = buttonify(screwdriverImage,(428*scale+barSizeX, 400*scale+barSizeY), screen)
                flags["ScrewdriverExists"] = True
                if flags["ScrewdriverActive"]:
                    screwdriverImage = screwdriverImage2
                else:
                    screwdriverImage = screwdriverImage1
                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if screwdriver[1].collidepoint(mouse):
                        flags["ScrewdriverActive"] = True
                    else:
                        flags["ScrewdriverActive"] = False

            if flags["ShowBookcase"]:
                if flags["BookcaseBroken"] == False:
                    bookcase = buttonify(bookcaseImage,(312*scale+barSizeX, 90*scale+barSizeY), screen)
                    flags["BookcaseExists"] = True
                    if flags["BookcaseActive"]:
                        bookcaseImage = bookcaseImage2
                    else:
                        bookcaseImage = bookcaseImage1 
                    if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                        if bookcase[1].collidepoint(mouse):
                            flags["BookcaseActive"] = True
                        else:
                            flags["BookcaseActive"] = False
                else:
                    screen.blit(numberImage, (138*scale+barSizeX, 99*scale+barSizeY))
                    screen.blit(bookcaseImage, (128*scale+barSizeX, 182*scale+barSizeY))

    if flags["ShowRoom2"]: #Second Room. Structurely identical to the first except it has a door back the way you ame and an NPC
        screen.fill(backgroundGray)

        if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
            pygame.display.set_caption("The Crash - Bridge")

        if currentRoomSide == 0:

            if flags["ShowDoorIn"]:
                screen.blit(doorCImage, (doorInCX*scale+barSizeX, doorInCY*scale+barSizeY))
                screen.blit(doorSImage, (doorInSX*scale+barSizeX, doorInSY*scale+barSizeY))
                screen.blit(doorTImage, (doorInTX*scale+barSizeX, doorInTY*scale+barSizeY))                     
                screen.blit(doorA25WImage, (doorInTX*scale+barSizeX, doorInTY*scale+barSizeY))                        
                screen.blit(doorBImage, (doorInBX*scale+barSizeX, doorInBY*scale+barSizeY))                     
                doorInTB = buttonify(doorTBImage, ((doorInTBX+150)*scale+barSizeX, doorInTBY*scale+barSizeY), screen)

                if flags["DoorInActive"]:
                    doorTBImage = doorTBImage2
                else:
                    doorTBImage = doorTBImage1
                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if doorInTB[1].collidepoint(mouse):
                        flags["DoorInActive"] = True
                    else:
                        flags["DoorInActive"] = False
                        
            screen.blit(backgroundSegment1, (-200*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (80*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (360*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment2, (639*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (918*scale+barSizeX, 0*scale+barSizeY))

            if flags["ShowComputer"]:#NPC
                computer = buttonify(computerImage,(282*scale+barSizeX, 83*scale+barSizeY), screen)
                if flags["ComputerFixed"] == False:
                    if flags["ComputerActive"]:
                        computerImage = computerImage2
                    else:
                        computerImage = computerImage1
                else:
                    if flags["ComputerActive"]:
                        computerImage = computerImage4
                    else:
                        computerImage = computerImage3

                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if computer[1].collidepoint(mouse):
                        flags["ComputerActive"] = True
                    else:
                        flags["ComputerActive"] = False


        if currentRoomSide == 1:
            screen.blit(backgroundSegment1, (-200*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (80*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (360*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (639*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (918*scale+barSizeX, 0*scale+barSizeY))

        if currentRoomSide == 2:

            if flags["ShowDoorOut"]:
                screen.blit(doorCImage, (doorOutCX*scale+barSizeX, doorOutCY*scale+barSizeY))
                screen.blit(doorSImage, (doorOutSX*scale+barSizeX, doorOutSY*scale+barSizeY))
                screen.blit(doorTImage, (doorOutTX*scale+barSizeX, doorOutTY*scale+barSizeY))                     
                screen.blit(doorA24WImage, (doorOutTX*scale+barSizeX, doorOutTY*scale+barSizeY))                        
                screen.blit(doorBImage, (doorOutBX*scale+barSizeX, doorOutBY*scale+barSizeY))                     
                doorOutTB = buttonify(doorTBImage, ((doorInTBX+150)*scale+barSizeX, doorOutTBY*scale+barSizeY), screen)
                flags["DoorOutExists"] = True

                if flags["DoorOutActive"]:
                    doorTBImage = doorTBImage2
                else:
                    doorTBImage = doorTBImage1
                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if doorOutTB[1].collidepoint(mouse):
                        flags["DoorOutActive"] = True
                    else:
                        flags["DoorOutActive"] = False

            screen.blit(backgroundSegment1, (-200*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment2, (80*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (360*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (639*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (918*scale+barSizeX, 0*scale+barSizeY))

        if currentRoomSide == 3:
            screen.blit(backgroundSegment1, (-200*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (80*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (360*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (639*scale+barSizeX, 0*scale+barSizeY))
            screen.blit(backgroundSegment1, (918*scale+barSizeX, 0*scale+barSizeY))

    if flags["ShowUserInterface"]:#This blits all of the UI to the screen

        screen.blit(UIBackgroundImage, (0*scale+barSizeX, 500*scale+barSizeY))
        screen.blit(leftSideImage, (0*scale+barSizeX, 0*scale+barSizeY))
        screen.blit(rightSideImage, (926*scale+barSizeX, 0*scale+barSizeY))
        rightSide = buttonify(blankImage,(1000*scale+barSizeX,0+barSizeY),screen)
        leftSide = buttonify(blankImage,(74+barSizeX,0+barSizeY),screen)
        openButton = buttonify(openButtonImage,(133*scale+barSizeX, 510*scale+barSizeY), screen)
        closeButton = buttonify(closeButtonImage,(145*scale+barSizeX, 560*scale+barSizeY), screen)
        giveButton = buttonify(giveButtonImage,(123*scale+barSizeX, 610*scale+barSizeY), screen)
        examineButton = buttonify(examineButtonImage, (327*scale+barSizeX, 510*scale+barSizeY), screen)
        talkToButton = buttonify(talkToButtonImage, (327*scale+barSizeX, 560*scale+barSizeY), screen)
        pickUpButton = buttonify(pickUpButtonImage, (317*scale+barSizeX, 610*scale+barSizeY), screen)
        pushButton = buttonify(pushButtonImage, (447*scale+barSizeX, 510*scale+barSizeY), screen)
        pullButton = buttonify(pullButtonImage, (447*scale+barSizeX, 560*scale+barSizeY), screen)
        useButton = buttonify(useButtonImage, (430*scale+barSizeX, 610*scale+barSizeY), screen)
        upArrowButton = buttonify(Arrow1Image, (530*scale+barSizeX, 546*scale+barSizeY), screen)
        downArrowButton = buttonify(pygame.transform.rotate(Arrow2Image, 180),(530*scale+barSizeX, 592*scale+barSizeY), screen)
        IBox1Button = buttonify(IBox1Image, (650*scale+barSizeX, 510*scale+barSizeY), screen)
        IBox2Button = buttonify(IBox2Image, (760*scale+barSizeX, 510*scale+barSizeY), screen)
        IBox3Button = buttonify(IBox3Image, (870*scale+barSizeX, 510*scale+barSizeY), screen)
        IBox4Button = buttonify(IBox4Image, (980*scale+barSizeX, 510*scale+barSizeY), screen)
        IBox5Button = buttonify(IBox5Image, (650*scale+barSizeX, 590*scale+barSizeY), screen)
        IBox6Button = buttonify(IBox6Image, (760*scale+barSizeX, 590*scale+barSizeY), screen)
        IBox7Button = buttonify(IBox7Image, (870*scale+barSizeX, 590*scale+barSizeY), screen)
        IBox8Button = buttonify(IBox8Image, (980*scale+barSizeX, 590*scale+barSizeY), screen)

        for i in range(0, currentSlot):#This constructs the inventory removing any empty slots inbetween objects and placing them on the end of the list
            if Inventory[i]["Item Name"] == "BLANK":
                Inventory.append(Inventory[i])
                Inventory.remove(Inventory[i])
            else:
                screen.blit(Inventory[i]["Inventory Image"], ((544+(110*(i%4)))*scale+barSizeX, (519+(80*(i//4)))*scale+barSizeY))
    
        if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:#Initializes the hovering of the buttons in the UI
            if rightSide[1].collidepoint(mouse):
                rightSideImage = rightSideImage2
            else:
                rightSideImage = rightSideImage1

            if leftSide[1].collidepoint(mouse):
                leftSideImage = leftSideImage2
            else:
                leftSideImage = leftSideImage1

            if flags["OpenButtonActive"] == False:
                if openButton[1].collidepoint(mouse):
                    openButtonImage = openButtonImage2
                else:
                    openButtonImage = openButtonImage1
            else:
                openButtonImage = openButtonImage2
                

            if flags["CloseButtonActive"] == False:
                if closeButton[1].collidepoint(mouse):
                    closeButtonImage = closeButtonImage2
                else:
                    closeButtonImage = closeButtonImage1
            else:
                closeButtonImage = closeButtonImage2
                
            if flags["PushButtonActive"] == False:
                if pushButton[1].collidepoint(mouse):
                    pushButtonImage = pushButtonImage2
                else:
                    pushButtonImage = pushButtonImage1
            else:
                pushButtonImage = pushButtonImage2
                
            if flags["PullButtonActive"] == False:
                if pullButton[1].collidepoint(mouse):
                    pullButtonImage = pullButtonImage2
                else:
                    pullButtonImage = pullButtonImage1
            else:
                pullButtonImage = pullButtonImage2
                
            if flags["ExamineButtonActive"] == False:
                if examineButton[1].collidepoint(mouse):
                    examineButtonImage = examineButtonImage2
                else:
                    examineButtonImage = examineButtonImage1
            else:
                examineButtonImage = examineButtonImage2
                
            if flags["GiveButtonActive"] == False:
                if giveButton[1].collidepoint(mouse):
                    giveButtonImage = giveButtonImage2
                else:
                    giveButtonImage = giveButtonImage1
            else:
                giveButtonImage = giveButtonImage2

            if flags["TalkToButtonActive"] == False:
                if talkToButton[1].collidepoint(mouse):
                    talkToButtonImage = talkToButtonImage2
                else:
                    talkToButtonImage = talkToButtonImage1
            else:
                talkToButtonImage = talkToButtonImage2

            if flags["PickUpButtonActive"] == False:
                if pickUpButton[1].collidepoint(mouse):
                    pickUpButtonImage = pickUpButtonImage2
                else:
                    pickUpButtonImage = pickUpButtonImage1
            else:
                pickUpButtonImage = pickUpButtonImage2

            if flags["UseButtonActive"] == False:
                if useButton[1].collidepoint(mouse):
                    useButtonImage = useButtonImage2
                else:
                    useButtonImage = useButtonImage1
            else:
                useButtonImage = useButtonImage2
            if flags["UpArrowButtonActive"] == False:
                if upArrowButton[1].collidepoint(mouse):
                    Arrow1Image = Arrow1Image2
                else:
                    Arrow1Image = Arrow1Image1
            else:
                Arrow1Image = Arrow1Image2
            if flags["DownArrowButtonActive"] == False:
                if downArrowButton[1].collidepoint(mouse):
                    Arrow2Image = Arrow2Image2
                else:
                    Arrow2Image = Arrow2Image1
            else:
                Arrow2Image = Arrow2Image2
            if flags["IBox1ButtonActive"] == False:
                if IBox1Button[1].collidepoint(mouse):
                    IBox1Image = IBox1Image2
                else:
                    IBox1Image = IBox1Image1
            else:
                IBox1Image = IBox1Image2
            if flags["IBox2ButtonActive"] == False:
                if IBox2Button[1].collidepoint(mouse):
                    IBox2Image = IBox2Image2
                else:
                    IBox2Image = IBox2Image1
            else:
                IBox2Image = IBox2Image2
            if flags["IBox3ButtonActive"] == False:
                if IBox3Button[1].collidepoint(mouse):
                    IBox3Image = IBox3Image2
                else:
                    IBox3Image = IBox3Image1
            else:
                IBox3Image = IBox3Image2
            if flags["IBox4ButtonActive"] == False:
                if IBox4Button[1].collidepoint(mouse):
                    IBox4Image = IBox4Image2
                else:
                    IBox4Image = IBox4Image1
            else:
                IBox4Image = IBox4Image2
            if flags["IBox5ButtonActive"] == False:
                if IBox5Button[1].collidepoint(mouse):
                    IBox5Image = IBox5Image2
                else:
                    IBox5Image = IBox5Image1
            else:
                IBox5Image = IBox5Image2
            if flags["IBox6ButtonActive"] == False:
                if IBox6Button[1].collidepoint(mouse):
                    IBox6Image = IBox6Image2
                else:
                    IBox6Image = IBox6Image1
            else:
                IBox6Image = IBox6Image2
            if flags["IBox7ButtonActive"] == False:
                if IBox7Button[1].collidepoint(mouse):
                    IBox7Image = IBox7Image2
                else:
                    IBox7Image = IBox7Image1
            else:
                IBox7Image = IBox7Image2
            if flags["IBox8ButtonActive"] == False:
                if IBox8Button[1].collidepoint(mouse):
                    IBox8Image = IBox8Image2
                else:
                    IBox8Image = IBox8Image1
            else:
                IBox8Image = IBox8Image2

    if flags["ShowKeypadInterface"]: # Shows the keypad interface
        fadeSurface.set_alpha(200)
        fadeSurface.fill(black)
        screen.blit(fadeSurface, (0, 0))
        screen.blit(keypadBackgroundImage, (314*scale+barSizeX, 52*scale+barSizeY))
        
        key1 = buttonify(key1Image, (446*scale+barSizeX,201*scale+barSizeY+2),screen)
        key2 = buttonify(key2Image, (551*scale+barSizeX+1,201*scale+barSizeY+2),screen)
        key3 = buttonify(key3Image, (656*scale+barSizeX,201*scale+barSizeY+2),screen)
        key4 = buttonify(key4Image, (446*scale+barSizeX,306*scale+barSizeY+3),screen)
        key5 = buttonify(key5Image, (551*scale+barSizeX+1,306*scale+barSizeY+3),screen)
        key6 = buttonify(key6Image, (656*scale+barSizeX,306*scale+barSizeY+3),screen)
        key7 = buttonify(key7Image, (446*scale+barSizeX,411*scale+barSizeY+2),screen)
        key8 = buttonify(key8Image, (551*scale+barSizeX+1,411*scale+barSizeY+2),screen)
        key9 = buttonify(key9Image, (656*scale+barSizeX,411*scale+barSizeY+2),screen)
        keyB = buttonify(keyBImage, (446*scale+barSizeX,516*scale+barSizeY+2),screen)
        key0 = buttonify(key0Image, (551*scale+barSizeX+1,516*scale+barSizeY+2),screen)
        keyT = buttonify(keyTImage, (656*scale+barSizeX,516*scale+barSizeY+2),screen)

        KeypadText = ""

        if flags["KeypadUnlocked"] == False:#This creates the keypads display
            if cit >= 2000:
                for i in range(0,len(KeypadCode)):
                    KeypadText += KeypadCode[i]
                KeypadText += ((4-len(KeypadCode))*"*")

                outputTextImage1 = textify(80, KeypadText[0], True, (25,90,15), (round(370*scale)+barSizeX, round(94*scale)+barSizeY), screen)
                outputTextImage2 = textify(80, KeypadText[1], True, (25,90,15), (round(440*scale)+barSizeX, round(94*scale)+barSizeY), screen)
                outputTextImage3 = textify(80, KeypadText[2], True, (25,90,15), (round(510*scale)+barSizeX, round(94*scale)+barSizeY), screen)
                outputTextImage4 = textify(80, KeypadText[3], True, (25,90,15), (round(580*scale)+barSizeX, round(94*scale)+barSizeY), screen)
            else:
                outputTextImage1 = textify(32, "Incorrect", True, (25,90,15), (round(370*scale)+barSizeX, round(118*scale)+barSizeY), screen)

        else:
            if cit <= 2000:
                outputTextImage1 = textify(32, "Access Granted", True, (25,90,15), (round(370*scale)+barSizeX, round(118*scale)+barSizeY), screen)
            else:
                flags["ShowKeypadInterface"] = False

        closeKeypadButton = buttonify(closeKeypadButtonImage, (900*scale+barSizeX, 100*scale+barSizeY), screen)

        if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowOutput"] == False:#Controls the keypads hovering and clicking graphical changes
                    
            if flags["CloseKeypadButtonPressed"] == False:
                if closeKeypadButton[1].collidepoint(mouse):
                    closeKeypadButtonImage = closeKeypadButtonImage2
                else:
                    closeKeypadButtonImage = closeKeypadButtonImage1

            if flags["Key0Pressed"] == False:
                if key0[1].collidepoint(mouse):
                    key0Image = key0Image2
                else:
                    key0Image = key0Image1
            else:
                key0Image = key0Image3
                if bpt >= 200:
                    flags["Key0Pressed"] = False

            if flags["Key1Pressed"] == False:
                if key1[1].collidepoint(mouse):
                    key1Image = key1Image2
                else:
                    key1Image = key1Image1
            else:
                key1Image = key1Image3
                if bpt >= 200:
                    flags["Key1Pressed"] = False

            if flags["Key2Pressed"] == False:
                if key2[1].collidepoint(mouse):
                    key2Image = key2Image2
                else:
                    key2Image = key2Image1
            else:
                key2Image = key2Image3
                if bpt >= 200:
                    flags["Key2Pressed"] = False

            if flags["Key3Pressed"] == False:
                if key3[1].collidepoint(mouse):
                    key3Image = key3Image2
                else:
                    key3Image = key3Image1
            else:
                key3Image = key3Image3
                if bpt >= 200:
                    flags["Key3Pressed"] = False

            if flags["Key4Pressed"] == False:
                if key4[1].collidepoint(mouse):
                    key4Image = key4Image2
                else:
                    key4Image = key4Image1
            else:
                key4Image = key4Image3
                if bpt >= 200:
                    flags["Key4Pressed"] = False

            if flags["Key5Pressed"] == False:
                if key5[1].collidepoint(mouse):
                    key5Image = key5Image2
                else:
                    key5Image = key5Image1
            else:
                key5Image = key5Image3
                if bpt >= 200:
                    flags["Key5Pressed"] = False

            if flags["Key6Pressed"] == False:
                if key6[1].collidepoint(mouse):
                    key6Image = key6Image2
                else:
                    key6Image = key6Image1
            else:
                key6Image = key6Image3
                if bpt >= 200:
                    flags["Key6Pressed"] = False

            if flags["Key7Pressed"] == False:
                if key7[1].collidepoint(mouse):
                    key7Image = key7Image2
                else:
                    key7Image = key7Image1
            else:
                key7Image = key7Image3
                if bpt >= 200:
                    flags["Key7Pressed"] = False

            if flags["Key8Pressed"] == False:
                if key8[1].collidepoint(mouse):
                    key8Image = key8Image2
                else:
                    key8Image = key8Image1
            else:
                key8Image = key8Image3
                if bpt >= 200:
                    flags["Key8Pressed"] = False

            if flags["Key9Pressed"] == False:
                if key9[1].collidepoint(mouse):
                    key9Image = key9Image2
                else:
                    key9Image = key9Image1
            else:
                key9Image = key9Image3
                if bpt >= 200:
                    flags["Key9Pressed"] = False

            if flags["KeyTPressed"] == False:
                if keyT[1].collidepoint(mouse):
                    keyTImage = keyTImage2
                else:
                    keyTImage = keyTImage1
            else:
                keyTImage = keyTImage3
                if bpt >= 200:
                    flags["KeyTPressed"] = False

            if flags["KeyBPressed"] == False:
                if keyB[1].collidepoint(mouse):
                    keyBImage = keyBImage2
                else:
                    keyBImage = keyBImage1
            else:
                keyBImage = keyBImage3
                if bpt >= 200:
                    flags["KeyBPressed"] = False

    if flags["ShowNPCInterface"]:#This creates the interface for the Experimental NPC
        screen.fill(black)
        answerText = [""]*3
        file = open(("NPCS/"+currentNPC+"/File.txt"),"r")
        lines = file.readlines()

        for i in range(0,len(lines)):#It checks for the NPC code in the text file (the line begining with C.../) and stores it
            if (lines[i].split("/")[0]) == ("C"+currentKey):
                NPCOutput = lines[i].split("/")[1]
                break
        for i in range(0,len(lines)): # It then stores all of the options for player responses in the same way
            if (lines[i].split("/")[0]) == ("P"+currentKey):
                if len(lines[i].split("/")[1]) > 1:
                    for j in range(0,3):
                        if answerText[j] == "":
                            answerText[j] = lines[i].split("/")[1]
                            break
                else:
                    currentKey = ""
                    flags["ShowNPCInterface"] = False
                    break

        for i in range(0,(len(NPCOutput)//50)+1):#It then displays the two pieces of information
            outputTextImage = textify(30, NPCOutput[50*i:(50*i)+50], True, white, (round(25*scale)+barSizeX, round((25+(i*35))*scale)+barSizeY), screen)
        font = pygame.font.Font("Fonts/ROTG.otf", int(30*scale))
        answer1Image = font.render(answerText[0], True, white)
        answer2Image = font.render(answerText[1], True, white)
        answer3Image = font.render(answerText[2], True, white)

        answer1 = buttonify(pygame.transform.scale(answer1Image,(pygame.Surface.get_width(answer1Image),pygame.Surface.get_height(answer1Image))),(pygame.Surface.get_width(answer1Image)*scale+barSizeX,450+barSizeY),screen)
        answer2 = buttonify(pygame.transform.scale(answer2Image,(pygame.Surface.get_width(answer2Image),pygame.Surface.get_height(answer2Image))),(pygame.Surface.get_width(answer2Image)*scale+barSizeX,525+barSizeY),screen)
        answer3 = buttonify(pygame.transform.scale(answer3Image,(pygame.Surface.get_width(answer3Image),pygame.Surface.get_height(answer3Image))),(pygame.Surface.get_width(answer3Image)*scale+barSizeX,600+barSizeY),screen)

        closeNPCButton = buttonify(closeKeypadButtonImage, (950*scale+barSizeX, 50*scale+barSizeY), screen)

        if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowOutput"] == False:    
            if flags["CloseNPCButtonPressed"] == False:
                if closeNPCButton[1].collidepoint(mouse):
                    closeNPCButtonImage = closeNPCButtonImage2
                else:
                    closeNPCButtonImage = closeNPCButtonImage1

    if flags["ShowSaveMenu"]:#Exact same structure as ShowMenu
        pygame.display.set_caption("The Crash - Save Game")
                    
        fadeSurface.set_alpha(fadeAlpha)
        popUpScreen.set_alpha(0)
        fadeSurface.fill(black)
        screen.blit(pygame.transform.scale(fadeSurface, (int(1000*scale+barSizeX), int(700*scale+barSizeY))), (0, 0))
        screen.blit(pygame.transform.scale(popUpScreen, (int(1000*scale+barSizeX), int(700*scale+barSizeY))), (0, 0))
        popUpScreen.blit(menuBox, (round(menuBoxX*scale+barSizeX), round(108*scale+barSizeY)))

        saveGameButton1 = buttonify(button1Image, ((menuButtonX+140)*scale+barSizeX, 132*scale+barSizeY), screen)
        saveGameButton2 = buttonify(button2Image, ((menuButtonX+140)*scale+barSizeX, 246*scale+barSizeY), screen)
        saveGameButton3 = buttonify(button3Image, ((menuButtonX+140)*scale+barSizeX, 360*scale+barSizeY), screen)
        saveBackButton = buttonify(button4Image, ((menuButtonX+140)*scale+barSizeX, 474*scale+barSizeY), screen)
        
        saveGameButton1Text = textify(30, "Save 1", True, button1Color, ((menuTextX+35)*scale+barSizeX, 168*scale+barSizeY), screen)
        saveGameButton2Text = textify(30, "Save 2", True, button2Color, ((menuTextX+35)*scale+barSizeX, 282*scale+barSizeY), screen)
        saveGameButton3Text = textify(30, "Save 3", True, button3Color, ((menuTextX+35)*scale+barSizeX, 396*scale+barSizeY), screen)
        saveBackText = textify(30, "Back", True, button4Color, ((menuTextX+45)*scale+barSizeX, 510*scale+barSizeY), screen)

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
        # HOVER CHECKS

        tempArray = buttonHover("SaveGameButton1Pressed", button1Image, saveGameButton1, button1Color, "")
        button1Image = tempArray[0]
        button1Color = tempArray[1]

        tempArray = buttonHover("SaveGameButton2Pressed", button2Image, saveGameButton2, button2Color, "")
        button2Image = tempArray[0]
        button2Color = tempArray[1]

        tempArray = buttonHover("SaveGameButton3Pressed", button3Image, saveGameButton3, button3Color, "")
        button3Image = tempArray[0]
        button3Color = tempArray[1]

        tempArray = buttonHover("SaveBackButtonPressed", button4Image, saveBackButton, button4Color, "PopUpMenu")
        button4Image = tempArray[0]
        button4Color = tempArray[1]
                
        if saveGameButton1[1].collidepoint(mouse) or saveGameButton2[1].collidepoint(mouse) or saveBackButton[1].collidepoint(mouse) or saveGameButton3[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False
            
    if flags["ShowPopUpMenu"]:#Exact same structure as ShowMenu
        pygame.display.set_caption("The Crash - Pop Up Menu")

        screen.blit(pygame.transform.scale(fadeSurface, (int(1000*scale+barSizeX), int(700*scale+barSizeY))), (0, 0))
        screen.blit(pygame.transform.scale(popUpScreen, (int(1000*scale+barSizeX), int(700*scale+barSizeY))), (0, 0))
        popUpScreen.blit(menuBox, (round(menuBoxX*scale+barSizeX), round(108*scale+barSizeY)))

        resumeGameButton = buttonify(button1Image, ((menuButtonX+140)*scale+barSizeX, 132*scale+barSizeY), screen)
        saveGameButton = buttonify(button2Image, ((menuButtonX+140)*scale+barSizeX, 246*scale+barSizeY), screen)
        tutorialButton = buttonify(button3Image, ((menuButtonX+140)*scale+barSizeX, 360*scale+barSizeY), screen)
        quitButton = buttonify(button4Image, ((menuButtonX+140)*scale+barSizeX, 474*scale+barSizeY), screen)

        resumeGameText = textify(30, "Resume", True, button1Color, ((menuTextX+25)*scale+barSizeX, 168*scale+barSizeY), screen)
        saveGameButtonText = textify(30, "Save Game", True, button2Color, ((menuTextX)*scale+barSizeX, 282*scale+barSizeY), screen)
        tutorialButtonText = textify(30, "Help", True, button3Color, ((menuTextX+55)*scale+barSizeX, 396*scale+barSizeY), screen)
        quitText = textify(30, "Quit", True, button4Color, ((menuTextX+55)*scale+barSizeX, 510*scale+barSizeY), screen)

        # HOVER CHECKS

        tempArray = buttonHover("ResumeGameButtonPressed", button1Image, resumeGameButton, button1Color, "")
        button1Image = tempArray[0]
        button1Color = tempArray[1]

        tempArray = buttonHover("SaveGameButtonPressed", button2Image, saveGameButton, button2Color, "SaveMenu")
        button2Image = tempArray[0]
        button2Color = tempArray[1]

        tempArray = buttonHover("QuitButtonPressed", button4Image, quitButton, button4Color, "MainMenu")
        button4Image = tempArray[0]
        button4Color = tempArray[1]

        tempArray = buttonHover("TutorialButtonPressed", button3Image, tutorialButton, button3Color, "")
        button3Image = tempArray[0]
        button3Color = tempArray[1]

        if resumeGameButton[1].collidepoint(mouse) or saveGameButton[1].collidepoint(mouse) or quitButton[1].collidepoint(mouse):
            flags["CursorOverride"] = True
        else:
            flags["CursorOverride"] = False

    if flags["FadeIn"]:#Fades from black to transparent
        if fadeWait < ft:
            fadeWait += fadeSpeed
            if fadeAlpha > 0:
                fadeAlpha -= 10
        fadeSurface.set_alpha(fadeAlpha)
        fadeSurface.fill(black)
        screen.blit(fadeSurface, (0, 0))
        if fadeAlpha == 0:
            flags["FadeIn"] = False
            
    if flags["FadeOut"]:#Fades from transpaarent to black
        if fadeWait < ft:
            fadeWait += fadeSpeed
            if fadeAlpha < 250:
                fadeAlpha += 10
        fadeSurface.set_alpha(fadeAlpha)
        fadeSurface.fill(black)
        screen.blit(fadeSurface, (0, 0))
        if fadeAlpha == 250:
            flags["Blackout"] = True
            flags["FadeOut"] = False

    if flags["Blackout"]:#occurs after fadeOut it changes the active room depending on what the nextRoom variable is set to.
        print("Blackout")
        screen.fill(black)
        flags["CursorOverride"] = False
        
        if nextRoom == "LoadMenu":
            flags["ShowLoadMenu"] = True
            flags["ShowMenu"] = False
            flags["MenuGlideIn"] = True
            flags["MenuGlideOut"] = False
            menuInitialize()
        elif nextRoom == "SettingsMenu":
            flags["ShowSettingsMenu"] = True
            flags["ShowMenu"] = False
            flags["ShowResolutionMenu"] = False
            flags["MenuGlideIn"] = True
            flags["MenuGlideOut"] = False
            menuInitialize()
        elif nextRoom == "ResolutionMenu":
            flags["ShowResolutionMenu"] = True
            flags["ShowSettingsMenu"] = False
            flags["MenuGlideIn"] = True
            flags["MenuGlideOut"] = False
            menuInitialize()
        elif nextRoom == "Intro":
            flags["ShowIntroCutscene"] = True
            flags["StopStartMusic"] = True
            flags["ShowMenu"] = False
            flags["IntroStage1"] = True
        elif nextRoom == "Start":
            flags["ShowStart"] = True
            flags["ShowMenu"] = False
        elif nextRoom == "SaveMenu":
            flags["ShowSaveMenu"] = True
            flags["ShowPopUpMenu"] = False
        elif nextRoom == "PopUpMenu":
            flags["ShowSaveMenu"] = False
            flags["ShowPopUpMenu"] = True
        elif nextRoom == "MainMenu":
            flags= {"BackButtonPressed":False, 
                    "Blackout":False, 
                    "BookcaseActive":True,
                    "BookcaseBroken":False,
                    "BookcaseExists":False,
                    "CloseButtonActive":False, 
                    "CloseButtonExists":False,
                    "CloseKeypadButtonPressed":False,
                    "CloseNPCButtonPressed":False,
                    "CloseOuputButtonPressed":False,
                    "ComputerActive":False,
                    "ComputerFixed":False,
                    "CursorOverride":False, 
                    "DoorInActive":False, 
                    "DoorInClose":False, 
                    "DoorInOpen":False, 
                    "DoorInOpened":False,
                    "DoorOutActive":False,
                    "DoorOutClose":False, 
                    "DoorOutExists":False,
                    "DoorOutOpen":False, 
                    "DoorOutOpened":False,
                    "DownArrowButtonActive":False, 
                    "EngineActive":False, 
                    "EngineExists":False,
                    "EngineFixed":False,
                    "EngineTaped":False, 
                    "ExamineButtonActive":False, 
                    "FadeIn":False, 
                    "FadeOut":False, 
                    "FusionCoreActive":False, 
                    "GiveButtonActive":False, 
                    "IBox1ButtonActive":False, 
                    "IBox2ButtonActive":False, 
                    "IBox3ButtonActive":False, 
                    "IBox4ButtonActive":False, 
                    "IBox5ButtonActive":False, 
                    "IBox6ButtonActive":False, 
                    "IBox7ButtonActive":False, 
                    "IBox8ButtonActive":False, 
                    "InitializeMenu":False, 
                    "IntroStage1":False, 
                    "IntroStage2":False, 
                    "Key0Pressed":False,
                    "Key1Pressed":False,
                    "Key2Pressed":False,
                    "Key3Pressed":False,
                    "Key4Pressed":False,
                    "Key5Pressed":False,
                    "Key6Pressed":False,
                    "Key7Pressed":False,
                    "Key8Pressed":False,
                    "Key9Pressed":False,
                    "KeyBPressed":False,
                    "KeypadActive":False,
                    "KeypadUnlocked":False,
                    "KeyTPressed":False,
                    "LoadBackButtonPressed":False, 
                    "LoadGameButton1Pressed":False, 
                    "LoadGameButton2Pressed":False, 
                    "LoadGameButton3Pressed":False, 
                    "LoadGameButtonPressed":False, 
                    "MenuGlideIn":True, 
                    "MenuGlideOut":False, 
                    "NewGameButtonPressed":False, 
                    "NextSong":False, 
                    "OpenButtonActive":False, 
                    "PanelActive":False,
                    "PanelExists":False,
                    "PanelFixed":False,
                    "PanelRemoved":False,
                    "PanelWireFixed":False,
                    "PanelWireTaped":False,
                    "PickUpButtonActive":False, 
                    "PlayMusic":False, 
                    "PopUpIn":False, 
                    "PopUpOut":False, 
                    "PullButtonActive":False, 
                    "PushButtonActive":False, 
                    "QuitAnimation":False, 
                    "QuitButtonPressed":False, 
                    "ResolutionBackButtonPressed":False, 
                    "ResolutionButton1Pressed":False, 
                    "ResolutionButton2Pressed":False, 
                    "ResolutionButton3Pressed":False, 
                    "ResolutionMenuButtonPressed":False, 
                    "ResumeGameButtonPressed":False, 
                    "SaveBackButtonPressed":False, 
                    "SaveGameButton1Pressed":False, 
                    "SaveGameButton2Pressed":False, 
                    "SaveGameButton3Pressed":False, 
                    "SaveGameButtonPressed":False, 
                    "ScrewdriverActive":False,
                    "ScrewdriverExists":False,
                    "SettingsBackButtonPressed":False, 
                    "SettingsButtonPressed":False, 
                    "ShowBookcase":True,
                    "ShowComputer":True,
                    "ShowComputerInterface":False,
                    "ShowDoorIn":True,
                    "ShowDoorOut":True,
                    "ShowEngine":True, 
                    "ShowFusionCore":True, 
                    "ShowIntroCutscene":False, 
                    "ShowKeypad":True,
                    "ShowKeypadInterface":False,
                    "ShowLoadMenu":False, 
                    "ShowMenu":True,
                    "ShowNPCInterface":False,
                    "ShowOutput":False,
                    "ShowPanel":True,
                    "ShowPopUpMenu":False, 
                    "ShowResolutionMenu":False, 
                    "ShowRoom1":False,
                    "ShowRoom2":False,
                    "ShowSaveMenu":False, 
                    "ShowScrewdriver":False,
                    "ShowSettingsMenu":False,
                    "ShowSolder":True, 
                    "ShowStart":False, 
                    "ShowTape":True, 
                    "ShowTutorial":False,
                    "ShowUserInterface":False,
                    "SkipButtonActive":False,
                    "SolderActive":False, 
                    "SolderExists":False,
                    "StartButtonPressed":False,
                    "StartConversation":True,
                    "StopMusic":False, 
                    "TalkToButtonActive":False, 
                    "TapeActive":False,
                    "TextSkipped":False,
                    "TutorialButtonPressed":False,
                    "UpArrowButtonActive":False, 
                    "UseButtonActive":False,
                    "UpdateImages":False,

                    }
            
            menuInitialize()
        elif nextRoom == "Room1":
            if flags["ShowIntroCutscene"]:
                flags["ShowIntroCutscene"] = False
                flags["ShowTutorial"] = True
                area = 2
                flags["PlayMusic"] = True
            flags["ShowRoom2"] = False
            flags["ShowRoom1"] = True
            flags["DoorInOpened"] = False
            flags["DoorOutOpened"] = False
            doorInDefault(705, 83)
        elif nextRoom == "Room2":
            flags["ShowRoom1"] = False
            flags["ShowRoom2"] = True
            flags["DoorOutOpened"] = False
            flags["DoorInOpened"] = False
            doorInDefault(705, 83)
            doorOutDefault(145, 83)
        elif nextRoom == "LoadSave":
            flags = tempflags
            print(Inventory)
            print()
            Inventory = tempInventory
            print(Inventory)
            print()
            print(tempInventory)
            print()
            for i in range (1,3):
                if flags[("ShowRoom"+str(i))] == True:
                    roomNumber = i
                    break
                elif i == (3-1) and flags[("ShowRoom"+str(i))] != True:
                    roomNumber = 0
            if roomNumber == 1:
                flags["DoorInOpened"] = False
                flags["DoorOutOpened"] = False
                doorInDefault(705, 83)
                area = 2
                flags["PlayMusic"] = True
            elif roomNumber == 2:
                flags["DoorOutOpened"] = False
                flags["DoorInOpened"] = False
                doorInDefault(705, 83)
                doorOutDefault(145, 83)
                area = 2
                flags["PlayMusic"] = True
            flags["ShowSaveMenu"] = False
            flags["CloseButtonExists"] = False
            flags["ShowUserInterface"] = True
            flags["ShowOutput"] = False
            flags["ShowKeypadInterface"] = False




        flags["FadeIn"] = True
        flags["Blackout"] = False

    if flags["ShowOutput"]:#Generates an output box and the text on it.

        screen.blit(outputBox, (0+barSizeX, 0+barSizeY))
        it += loopTime

        #The following is what makes the text scroll

        if textWait < it and placeholder != len(gameText[currentPageNumber][line]):
            textWait += textWaitModifier
            placeholder += 1
            gameTextImage = textify(30, gameText[currentPageNumber][line][:placeholder], True, textColor, (textX*scale+barSizeX, textHeight[line]*scale+barSizeY), screen)
        if placeholder == len(gameText[currentPageNumber][line]) and len(gameText[currentPageNumber][line]) > 1:
            if line +1 != len(gameText[currentPageNumber]):
                line +=1
                textHeight[line] = textHeight[line-1]+40
                placeholder = 1
            lineCount +=1
        if lineCount > len(gameText[currentPageNumber]) or flags["SkipButtonActive"]:
            for i in range(0,line+1):
                gameTextImage = textify(30, gameText[currentPageNumber][i], True, textColor, (textX*scale+barSizeX, textHeight[i]*scale+barSizeY), screen)
            flags["SkipButtonActive"] = False
            flags["TextSkipped"] = True
        else:
            for i in range(0,line):
                gameTextImage = textify(30, gameText[currentPageNumber][i], True, textColor, (textX*scale+barSizeX, textHeight[i]*scale+barSizeY), screen)

        closeOutputButton = buttonify(closeOutputButtonImage, ((900)*scale+barSizeX, 90*scale+barSizeY), screen)
        flags["CloseButtonExists"] = True
        if flags["CloseOutputButtonPressed"] == False:
            if closeOutputButton[1].collidepoint(mouse):
                closeOutputButtonImage = closeOutputButtonImage2
            else:
                closeOutputButtonImage = closeOutputButtonImage1

        if flags["TextSkipped"] == False:
            skipButton = buttonify(skipButtonImage, (850*scale+barSizeX, 550*scale+barSizeY), screen)
            if skipButton[1].collidepoint(mouse):
                skipButtonImage = skipButtonImage2
            else:
                skipButtonImage = skipButtonImage1
        else:
            if currentPageNumber + 1 <= pageAmount - 1:
                skipButton = buttonify(skipButtonImage,(850*scale+barSizeX, 550*scale+barSizeY), screen)
                if skipButton[1].collidepoint(mouse):
                    skipButtonImage = skipButtonImage4
                else:
                    skipButtonImage = skipButtonImage3
                #This if statement determines the position of the two black bars that appear on the screen in order to maximise used space without akward window shapes
    if barTop == False:
        leftBar = pygame.draw.rect(screen, black, (0, 0, barSizeX, screenHeight))
        rightBar = pygame.draw.rect(screen, black, (screenWidth-barSizeX, 0, barSizeX+1, screenHeight))
    else:
        leftBar = pygame.draw.rect(screen, black, (0, 0, screenWidth, barSizeY))
        rightBar = pygame.draw.rect(screen, black, (0, screenHeight-barSizeY, screenWidth, barSizeY))

    # EVENT CHECKS
    for event in pygame.event.get():
        if event.type == QUIT:#Checks to see if red cross is pressed
            pygame.quit()
            sys.exit()
            break

        if event.type == MOUSEBUTTONDOWN: # Does different actions depending on what is active and what is clicked
            # BUTTON CHECKS

            if flags["CloseButtonExists"]:
                if closeOutputButton[1].collidepoint(mouse) and event.button == 1:
                    print("Close Output")
                    flags["CloseOutputButtonPressed"] = True
                    flags["TextSkipped"] = False
                    flags["ShowOutput"] = False

            if flags["ShowKeypadInterface"]:
                if closeKeypadButton[1].collidepoint(mouse) and event.button == 1:
                    print("Close Keypad")
                    flags["CloseKeypadButtonPressed"] = True
                    flags["ShowKeypadInterface"] = False
                    flags["ShowUserInterface"] = True
                if key0[1].collidepoint(mouse) and event.button == 1:#If keypad button pressed...
                    print("0")
                    flags["Key0Pressed"] = True 
                    if len(KeypadCode) < 4:
                        KeypadCode += "0"#Add a 0 to the current code string
                    print(KeypadCode)
                    bpt = 0
                if key1[1].collidepoint(mouse) and event.button == 1:#Same as above for 1 etc.
                    print("1")
                    flags["Key1Pressed"] = True 
                    if len(KeypadCode) < 4:
                        KeypadCode += "1"
                    print(KeypadCode)
                    bpt = 0
                if key2[1].collidepoint(mouse) and event.button == 1:
                    print("2")
                    flags["Key2Pressed"] = True 
                    if len(KeypadCode) < 4:
                        KeypadCode += "2"
                    print(KeypadCode)
                    bpt = 0
                if key3[1].collidepoint(mouse) and event.button == 1:
                    print("3")
                    flags["Key3Pressed"] = True 
                    if len(KeypadCode) < 4:
                        KeypadCode += "3"
                    print(KeypadCode)
                    bpt = 0
                if key4[1].collidepoint(mouse) and event.button == 1:
                    print("4")
                    flags["Key4Pressed"] = True 
                    if len(KeypadCode) < 4:
                        KeypadCode += "4"
                    print(KeypadCode)
                    bpt = 0
                if key5[1].collidepoint(mouse) and event.button == 1:
                    print("5")
                    flags["Key5Pressed"] = True 
                    if len(KeypadCode) < 4:
                        KeypadCode += "5"
                    print(KeypadCode)
                    bpt = 0
                if key6[1].collidepoint(mouse) and event.button == 1:
                    print("6")
                    flags["Key6Pressed"] = True 
                    if len(KeypadCode) < 4:
                        KeypadCode += "6"
                    print(KeypadCode)
                    bpt = 0
                if key7[1].collidepoint(mouse) and event.button == 1:
                    print("7")
                    flags["Key7Pressed"] = True 
                    if len(KeypadCode) < 4:
                        KeypadCode += "7"
                    print(KeypadCode)
                    bpt = 0
                if key8[1].collidepoint(mouse) and event.button == 1:
                    print("8")
                    flags["Key8Pressed"] = True 
                    if len(KeypadCode) < 4:
                        KeypadCode += "8"
                    print(KeypadCode)
                    bpt = 0
                if key9[1].collidepoint(mouse) and event.button == 1:
                    print("9")
                    flags["Key9Pressed"] = True 
                    if len(KeypadCode) < 4:
                        KeypadCode += "9"
                    print(KeypadCode)
                    bpt = 0
                if keyT[1].collidepoint(mouse) and event.button == 1:#The 'enter' key. Checks if the code is correct and then either unlocks the keypad or doesnt
                    print("Enter")
                    flags["KeyTPressed"] = True 
                    if len(KeypadCode) == 4:
                        if KeypadCode == "4297":
                            flags["KeypadUnlocked"] = True
                            print("Correct")
                            cit = 0
                        else:
                            cit = 0
                            KeypadCode = ""


                    bpt = 0
                if keyB[1].collidepoint(mouse) and event.button == 1:#Backspace Key
                    print("Backspace")
                    flags["KeyBPressed"] = True 
                    if len(KeypadCode) != 0:
                        KeypadCode = KeypadCode[:-1]
                    print(KeypadCode)
                    bpt = 0

            if flags["ShowMenu"]:#Button presses for Menu
                if newGameButton[1].collidepoint(mouse) and event.button == 1:
                    print("New Game")
                    flags["NewGameButtonPressed"] = True

                    menuGlideMult = 100
                    bpt = 0
                elif loadGameButton[1].collidepoint(mouse) and event.button == 1:
                    print("Load Game")
                    flags["LoadGameButtonPressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif settingsButton[1].collidepoint(mouse) and event.button == 1:
                    print("Settings")
                    flags["SettingsButtonPressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif backButton[1].collidepoint(mouse) and event.button == 1:
                    print("Back")
                    flags["BackButtonPressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0

            if flags["ShowNPCInterface"]:#Button presses for NPC. Ita edits the identifer code depending on the option picked
                if answer1[1].collidepoint(mouse) and event.button == 1:
                    currentKey+="A"
                    print("+A")
                    print(currentKey)
                elif answer2[1].collidepoint(mouse) and event.button == 1:
                    currentKey+="B"
                    print("+B")
                    print(currentKey)
                elif answer3[1].collidepoint(mouse) and event.button == 1:
                    currentKey+="C"
                    print("+C")
                    print(currentKey)

                if closeNPCButton[1].collidepoint(mouse) and event.button == 1:
                    print("Close NPC")
                    flags["CloseNPCButtonPressed"] = True
                    flags["ShowNPCInterface"] = False

            if flags["ShowOutput"]:#Button presses for Output
                if skipButton[1].collidepoint(mouse) and event.button == 1:
                    if flags["TextSkipped"] == False:
                        flags["SkipButtonActive"] = True
                        line = len(gameText[currentPageNumber]) - 1
                    else: # Resets the output
                        currentPageNumber += 1
                        it = 0
                        line = 0
                        lineCount = 0
                        placeholder = 0
                        textWait = 100
                        textWaitModifier = 10
                        textX = 100
                        flags["TextSkipped"] = False

            if flags["ShowPopUpMenu"]:#Button presses for PopUp Menu
                if resumeGameButton[1].collidepoint(mouse) and event.button == 1:
                    print("Resume Game")
                    flags["ResumeGameButtonPressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                    flags["ShowPopUpMenu"] = False
                elif saveGameButton[1].collidepoint(mouse) and event.button == 1:
                    print("Save Game")
                    flags["SaveGameButtonPressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0

                elif tutorialButton[1].collidepoint(mouse) and event.button == 1:
                    print("Tutorial")
                    flags["TutorialButtonPressed"] = True
                    flags["ShowTutorial"] = True
                    
                    menuGlideMult = 100
                    bpt = 0

                elif quitButton[1].collidepoint(mouse) and event.button == 1:
                    print("Quit")
                    flags["QuitButtonPressed"] = True
                    area = 1
                    flags["PlayMusic"] = True
                    
                    menuGlideMult = 100
                    fadeInitialize(100, 0, 20, 0)
                    bpt = 0
                    nextRoom = "MainMenu"

            if flags["ShowResolutionMenu"]:#Button presses for Resolution Menu. Each button scales the window in a distinct way or Automatically the largest
                if resolutionButton1[1].collidepoint(mouse) and event.button == 1:
                    print("Auto")
                    scale = currentHeight/700#Same as inital scale calculation
                    if 1000*scale < currentWidth:
                        barTop = False
                        barSizeX = (currentWidth - (1000*scale))/2
                        barSizeY = 0
                        screenWidth = 1000*scale+2*barSizeX
                        screenHeight = 700*scale
                    else:
                        barTop = True
                        scale = currentWidth/1000
                        barSizeY = (currentHeight - (700*scale))/2
                        barSizeX = 0
                        screenWidth = 1000*scale
                        screenHeight = 700*scale+2*barSizeY

                    screen = pygame.display.set_mode((int(screenWidth), int(screenHeight)),DOUBLEBUF)
                    fadeSurface = pygame.Surface((int(screenWidth), int(screenHeight)))
                    popUpScreen = pygame.display.set_mode((int(screenWidth), int(screenHeight)))

                    flags["UpdateImages"] = True
                    flags["ResolutionButton1Pressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif resolutionButton2[1].collidepoint(mouse) and event.button == 1:
                    print("1000x700")
                    scale = 1
                    currentHeight, currentWidth = infoObject.current_h, infoObject.current_w
                    currentHeight -= 69
                    if 1000*scale < currentWidth:
                        barTop = False
                        barSizeX = (currentWidth - (1000*scale))/2
                        barSizeY = 0
                        screenWidth = 1000*scale+2*barSizeX
                        screenHeight = 700*scale
                    else:
                        barTop = True
                        scale = currentWidth/1000
                        barSizeY = (currentHeight-64 - (700*scale))/2
                        barSizeX = 0
                        screenWidth = 1000*scale
                        screenHeight = 700*scale+2*barSizeY
                    screen = pygame.display.set_mode((int(screenWidth), int(screenHeight)),DOUBLEBUF)
                    fadeSurface = pygame.Surface((int(screenWidth), int(screenHeight)))
                    popUpScreen = pygame.display.set_mode((int(screenWidth), int(screenHeight)))

                    flags["UpdateImages"] = True
                    flags["ResolutionButton2Pressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif resolutionButton3[1].collidepoint(mouse) and event.button == 1:
                    print("1200x840")
                    scale = 1.2
                    currentHeight, currentWidth = infoObject.current_h, infoObject.current_w
                    currentHeight -= 69
                    if 1000*scale < currentWidth:
                        barTop = False
                        barSizeX = (currentWidth - (1000*scale))/2
                        barSizeY = 0
                        screenWidth = 1000*scale+2*barSizeX
                        screenHeight = 700*scale
                    else:
                        barTop = True
                        scale = currentWidth/1000
                        barSizeY = (currentHeight - (700*scale))/2
                        barSizeX = 0
                        screenWidth = 1000*scale
                        screenHeight = 700*scale+2*barSizeY
                    screen = pygame.display.set_mode((int(screenWidth), int(screenHeight)),DOUBLEBUF)
                    fadeSurface = pygame.Surface((int(screenWidth), int(screenHeight)))
                    popUpScreen = pygame.display.set_mode((int(screenWidth), int(screenHeight)))

                    flags["UpdateImages"] = True                    
                    flags["ResolutionButton3Pressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif resolutionBackButton[1].collidepoint(mouse) and event.button == 1:
                    print("Back")
                    flags["ResolutionBackButtonPressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0

            if flags["ShowRoom1"]:#Button presses for Room1. Especially important for the EnviroObjects as they will change depending on which object is active. Else it depends on the command selected
                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if currentRoomSide == 0:
                        if flags["ShowFusionCore"]:
                            if fusionCore[1].collidepoint(mouse):
                                if event.button == 1:
                                    if flags["ExamineButtonActive"]:
                                        outputInitialize([["This is a fusion core. They power every","interstellar transport vessel in the known","universe."]],grayBlue,1)
                                    if flags["PickUpButtonActive"]:
                                        flags["ShowFusionCore"] = False
                                        Inventory[currentSlot] = {"Inventory Image":fusionCoreImage3, "Item Name":"FusionCore", "Item Description":["This is a fusion core. They power every","interstellar transport vessel in the known","universe."]}
                                        currentSlot+=1
                                elif event.button == 3:
                                    flags["ShowFusionCore"] = False
                                    Inventory[currentSlot] = {"Inventory Image":fusionCoreImage3, "Item Name":"FusionCore", "Item Description":["This is a fusion core. They power every","interstellar transport vessel in the known","universe."]}
                                    currentSlot+=1

                        if keypad[1].collidepoint(mouse): 
                            if event.button == 1:
                                if flags["ExamineButtonActive"]:
                                    outputInitialize([["This appears to be a keypad lock for the","door to your right. It requires a 4 digit code."]],grayBlue,1)
                                if flags["UseButtonActive"]:
                                    if flags["EngineFixed"] and flags["PanelFixed"]:
                                        if flags["KeypadUnlocked"] == False:
                                            flags["ShowUserInterface"] = False
                                            flags["ShowKeypadInterface"] = True
                                            closeKeypadButtonImage = closeKeypadButtonImage1
                                    else:
                                        outputInitialize([["There is no response. It appears that there is","no power."]],grayBlue,1)
                            elif event.button == 3:
                                if flags["EngineFixed"] and flags["PanelFixed"]:
                                    if flags["KeypadUnlocked"] == False:
                                        flags["ShowUserInterface"] = False
                                        flags["ShowKeypadInterface"] = True
                                        closeKeypadButtonImage = closeKeypadButtonImage1
                                else:
                                    outputInitialize([["There is no response. It appears that there is","no power."]],grayBlue,1)
                        
                        if flags["ShowTape"]:
                            if tape[1].collidepoint(mouse):
                                if event.button == 1:
                                    if flags["ExamineButtonActive"]:
                                        outputInitialize([["A reel of universal standard space tape perfect","for all your space needs."]],grayBlue,1)
                                    if flags["PickUpButtonActive"]:
                                        flags["ShowTape"] = False
                                        Inventory[currentSlot] = {"Inventory Image":tapeImage3, "Item Name":"Tape", "Item Description":["A reel of universal standard space tape perfect","for all your space needs."]}
                                        currentSlot+=1
                                elif event.button == 3:
                                    flags["ShowTape"] = False
                                    Inventory[currentSlot] = {"Inventory Image":tapeImage3, "Item Name":"Tape", "Item Description":["A reel of universal standard space tape perfect","for all your space needs."]}
                                    currentSlot+=1
                                
                        if doorInTB[1].collidepoint(mouse):
                            if event.button == 1:
                                if flags["ExamineButtonActive"]:
                                    outputInitialize([["A door that leads deeper into the ship's depths.","You'll need to open it to progress."]],grayBlue,1)
                                if flags["UseButtonActive"]:
                                    if flags["DoorInOpened"]:
                                        flags["FadeOut"] = True
                                        lft = 0
                                        it = 0
                                        nextRoom = "Room2"

                                if flags["OpenButtonActive"]:
                                    if flags["EngineFixed"] and flags["PanelFixed"]:
                                        if flags["KeypadUnlocked"]:
                                            flags["DoorInOpen"] = True
                                            flags["DoorInClose"] = False
                                            outputInitialize([["Sector A-24","Bulkhead now opening"]],grayBlue,1)
                                        else:
                                            outputInitialize([["The door is locked. There must be some way of","overriding the security..."]],grayBlue,1)
                                    else:
                                        outputInitialize([["There is no response. It appears there is no power"]],grayBlue,1)
                                if flags["CloseButtonActive"]:
                                    if flags["EngineFixed"]:
                                        flags["DoorInClose"] = True
                                        flags["DoorInOpen"] = False
                                        outputInitialize([["Sector A-24","Bulkhead now closing"]],grayBlue,1)
                                    else:
                                        outputInitialize([["There is no response. It appears there is no power."]],grayBlue,1)
                            if event.button == 3:
                                flags["FadeOut"] = True
                                lft = 0
                                it = 0
                                nextRoom = "Room2"

                    if currentRoomSide == 1:
                        if flags["PanelExists"]:
                            if panel[1].collidepoint(mouse):
                                if event.button == 1:
                                    if flags["ExamineButtonActive"]:
                                        if flags["PanelFixed"] == False:
                                            outputInitialize([["It's a standard wall panel, although the crash","seems to have broken it."]],grayBlue,1)
                                        else:
                                            outputInitialize([["It's a wall panel. What you were expecting a","detailed description. Well this is it."]],grayBlue,1)
                                    if flags["PanelFixed"] == False:
                                        if flags["PanelRemoved"] == False:
                                            if flags["UseButtonActive"] and currentObject == "Screwdriver":
                                                print("Panel Removed")
                                                flags["PanelRemoved"] = True
                                                Inventory[currentSlot] = {"Inventory Image":panelImage10, "Item Name":"WallPanel", "Item Description":["One of thousands of wall panels that make","up the ship's interior."]}
                                                currentSlot+=1
                                                Inventory = [element for element in Inventory if element.get('Item Name', '') != 'Screwdriver']
                                                deactivateInventoryButtons()
                                        else:
                                            if flags["PanelWireFixed"] == False:
                                                if flags["UseButtonActive"] and currentObject == "Solder":
                                                    print("Wire Welded")
                                                    flags["PanelWireFixed"] = True
                                                    Inventory = [element for element in Inventory if element.get('Item Name', '') != 'Solder']
                                                    deactivateInventoryButtons()
                                            else:
                                                if flags["PanelWireTaped"] == False:
                                                    if flags["UseButtonActive"]:
                                                        if currentObject == "Tape":
                                                            print("Wire Taped")
                                                            flags["PanelWireTaped"] = True
                                                            if flags["EngineTaped"]:
                                                                Inventory = [element for element in Inventory if element.get('Item Name', '') != 'Tape']
                                                            deactivateInventoryButtons()
                                                else:
                                                    if flags["UseButtonActive"]:
                                                        print("Panel Fixed")
                                                        if currentObject == "WallPanel":
                                                            flags["PanelFixed"] = True
                                                            if flags["EngineFixed"]:
                                                                outputInitialize([["Panel Repaired - Power has been restored."]],grayBlue,1)
                                                            else:
                                                                outputInitialize([["Panel Repaired"]],grayBlue,1)
                                                            Inventory = [element for element in Inventory if element.get('Item Name', '') != 'WallPanel']
                                                            deactivateInventoryButtons()
                                elif event.button == 3:
                                    if flags["PanelFixed"] == False:
                                        outputInitialize([["It's a standard wall panel, although the crash","seems to have broken it."]],grayBlue,1)
                                    else:
                                        outputInitialize([["It's a wall panel. What you were expecting a","detailed description. Well this is it."]],grayBlue,1)

                    if currentRoomSide == 2:
                        if flags["ShowSolder"]:
                            if flags["SolderExists"]:
                                if solder[1].collidepoint(mouse) and event.button == 1:
                                    if flags["ExamineButtonActive"]:
                                        outputInitialize([["It's a soldering iron. This can be used to","fix broken wires and circuitry with intricate","precision."]],grayBlue,1)
                                    if flags["PickUpButtonActive"]:
                                        flags["ShowSolder"] = False
                                        Inventory[currentSlot] = {"Inventory Image":solderImage3, "Item Name":"Solder", "Item Description":["It's a soldering iron. This can be used to","fix broken wires and circuitry with intricate","precision."]}
                                        currentSlot+=1

                        if flags["EngineExists"]:
                            if engine[1].collidepoint(mouse) and event.button == 1:
                                if flags["ExamineButtonActive"]:
                                    if flags["EngineFixed"] == False:
                                        if flags["EngineTaped"] == False: 
                                            outputInitialize([["The Core of the Ship. This is what makes","dimensional travel possible. It was invented by","Dr. E. Blue. He was hanging a digital clock in","his air lock when he slipped and fell. When he","came too he saw this, the fluxed tranisistor. It","looks like the fuel core is missing and there","is a crack in the glass!"]],grayBlue,1)
                                        else:
                                             outputInitialize([["The Core of the Ship. This is what makes","dimensional travel possible. It was invented by","Dr. E. Blue. He was hanging a digital clock in","his air lock when he slipped and fell. When he","came too he saw this, the fluxed tranisistor. It","looks like the fuel core is missing!"]],grayBlue,1)
                                    else:
                                        outputInitialize([["The Core of the Ship. This is what makes","dimensional travel possible. It was invented by","Dr. E. Blue. He was hanging a digital clock in","his air lock when he slipped and fell. When he","came too he saw this, the fluxed tranisistor. It appears to be fully functional."]],grayBlue,1)

                                if flags["EngineFixed"] == False:
                                    if flags["EngineTaped"]:
                                        if flags["UseButtonActive"] and currentObject == "FusionCore":
                                            flags["EngineFixed"] = True
                                            outputInitialize([["Core Systems have been restored."]],grayBlue,1)
                                            Inventory = [element for element in Inventory if element.get('Item Name', '') != 'FusionCore']
                                            deactivateInventoryButtons()
                                    else:
                                        if flags["UseButtonActive"] and currentObject == "FusionCore":
                                            outputInitialize([["Warning! Fix fluxed containment breach before","inserting fusion core."]],grayBlue,1)
                                            deactivateInventoryButtons()

                                        if flags["UseButtonActive"] and currentObject == "Tape":
                                            flags["EngineTaped"] = True
                                            if flags["PanelWireTaped"]:
                                                Inventory = [element for element in Inventory if element.get('Item Name', '') != 'Tape']
                                            deactivateInventoryButtons()

                    if currentRoomSide == 3:
                        if flags["ShowScrewdriver"]:
                            if flags["ScrewdriverExists"]:
                                if screwdriver[1].collidepoint(mouse) and event.button == 1:
                                    if flags["ExamineButtonActive"]:
                                        outputInitialize([["It's a screwdriver. Its a tool found in almost","every dimension used for - you guessed","it - screwing things. I suppose it can unscrew","things as well but that besides the point."]],grayBlue,1)
                                    if flags["PickUpButtonActive"]:
                                        flags["ShowScrewdriver"] = False
                                        Inventory[currentSlot] = {"Inventory Image":screwdriverImage3, "Item Name":"Screwdriver", "Item Description":["It's a screwdriver. Its a tool found in almost","every dimension used for - you guessed","it - screwing things. I suppose it can unscrew","things as well but that besides the point."]}
                                        currentSlot+=1
                        if flags["BookcaseBroken"] == False:
                            if flags["BookcaseExists"]:
                                if bookcase[1].collidepoint(mouse) and event.button == 1:
                                    if flags["ExamineButtonActive"]:
                                        outputInitialize([["It's a large storage cabinet. Both the doors and","glass case are locked although the glass looks","fragile."]],grayBlue,1)
                                    elif flags["OpenButtonActive"]:
                                        outputInitialize([["It's locked and the doors are securely attached."]],grayBlue,1)
                                    elif flags["PushButtonActive"]:
                                        flags["ShowScrewdriver"] = True
                                        flags["BookcaseBroken"] = True
                                        bookcaseImage = bookcaseImage3
                                    else:
                                        outputInitialize([["That's not a good idea."]],grayBlue,1)             

            if flags["ShowRoom2"]:#Button presses for Room 2. similar to Room 1 yet unique.
                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if currentRoomSide == 0:
                        if doorInTB[1].collidepoint(mouse):
                            if event.button == 1:
                                if flags["ExamineButtonActive"]:
                                    outputInitialize([["A door that leads deeper into the ship's depths.","You'll need to open it to progress."]],grayBlue,1)
                                if flags["OpenButtonActive"]:
                                    flags["DoorInOpen"] = True
                                    flags["DoorInClose"] = False
                                    outputInitialize([["Sector A-25","Bulkhead now opening"]],grayBlue,1)
                                if flags["CloseButtonActive"]:
                                    flags["DoorInClose"] = True
                                    flags["DoorInOpen"] = False
                                    outputInitialize([["Sector A-25","Bulkhead now closing"]],grayBlue,1)
                            if event.button == 3:
                                flags["DoorInOpen"] = True
                                flags["DoorInClose"] = False

                        if flags["ShowComputer"]:
                            if computer[1].collidepoint(mouse) and event.button == 1:
                                if flags["ExamineButtonActive"]:
                                    if flags["ComputerFixed"] == False:
                                        outputInitialize([["It's an access terminal for the ship's computer","system. It looks like the terminal's connections","are shot based on the condition of the screen"]],grayBlue,1)
                                    else:
                                        outputInitialize([["A fully functional access terminal to the","ship's mainframe. It can be used to communicate","with the ships's AI to gather information."]],grayBlue,1)
                                if flags["UseButtonActive"]:
                                    if flags["ComputerFixed"] == False:
                                        outputInitialize([["There is little to be gained from the terminal","in this state. There must be some way to repair","it..."]],grayBlue,1)
                                    else:
                                        flags["ShowComputerInterface"] = True
                                if flags["TalkToButtonActive"]:
                                    if flags["ComputerFixed"] == False:
                                        flags["ComputerFixed"] = True
                                    else:
                                        flags["ShowNPCInterface"] = True
                                        currentNPC = "ROOM2/COMPUTER"
                                        currentLine = 0


                    if currentRoomSide == 2:
                        if flags["DoorOutExists"]:
                            if doorOutTB[1].collidepoint(mouse):
                                if event.button == 1:
                                    if flags["ExamineButtonActive"]:
                                        outputInitialize([["A door that leads back the way you've come."]],grayBlue,1)
                                    if flags["UseButtonActive"]:
                                        if flags["DoorOutOpened"]:
                                            flags["FadeOut"] = True
                                            lft = 0
                                            it = 0
                                            nextRoom = "Room1"

                                    if flags["OpenButtonActive"]:
                                        print("Open")
                                        flags["DoorOutOpen"] = True
                                        flags["DoorOutClose"] = False
                                        outputInitialize([["Sector A-24","Bulkhead now opening"]],grayBlue,1)
                                    if flags["CloseButtonActive"]:
                                        flags["DoorOutClose"] = True
                                        flags["DoorOutOpen"] = False
                                        outputInitialize([["Sector A-24","Bulkhead now closing"]],grayBlue,1)
                                elif event.button == 3:
                                    flags["FadeOut"] = True
                                    lft = 0
                                    it = 0
                                    nextRoom = "Room1"

            if flags["ShowSaveMenu"]:#Button presses for Save Menu
                if saveGameButton1[1].collidepoint(mouse) and event.button == 1:
                    print("Save - Save 1")
                    with open("SAVES/SAVE1/flags.p", "wb") as f:
                        pickle.dump(flags,f)
                    with open("SAVES/SAVE1/inventory.p", "wb") as f:
                        pickle.dump(Inventory,f)
                    with open("SAVES/SAVE1/current_slot.p", "wb") as f:
                        pickle.dump(currentSlot,f)
                    flags["SaveGameButton1Pressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif saveGameButton2[1].collidepoint(mouse) and event.button == 1:
                    print("Save - Save 2")
                    with open("SAVES/SAVE2/flags.p", "wb") as f:
                        pickle.dump(flags,f)
                    with open("SAVES/SAVE2/inventory.p", "wb") as f:
                        pickle.dump(Inventory,f)
                    flags["SaveGameButton2Pressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif saveGameButton3[1].collidepoint(mouse) and event.button == 1:
                    print("Save - Save 3")
                    with open("SAVES/SAVE3/flags.p", "wb") as f:
                        pickle.dump(flags,f)
                    with open("SAVES/SAVE3/inventory.p", "wb") as f:
                        pickle.dump(Inventory,f)
                    flags["SaveGameButton3Pressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif saveBackButton[1].collidepoint(mouse) and event.button == 1:
                    print("Back")
                    flags["SaveBackButtonPressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                    nextRoom = "PopUpMenu"

            if flags["ShowSettingsMenu"]:#Button presses for Settings Menu
                if resolutionMenuButton[1].collidepoint(mouse) and event.button == 1:
                    print("Change Resolution")
                    flags["ResolutionMenuButtonPressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif settingsBackButton[1].collidepoint(mouse) and event.button == 1:
                    print("Back")
                    flags["SettingsBackButtonPressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0

            if flags["ShowStart"]:#Button presses for the Start Screen
                print("Menu")
                flags["StartButtonPressed"] = True
                fadeInitialize(100, 0, 20, 0)
                flags["FadeOut"] = True
                bpt = 0

            if flags["ShowUserInterface"]:#Button presses for UI. Important for interacting with objects

                if flags["ShowPopUpMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False and flags["ShowKeypadInterface"] == False and flags["ShowOutput"] == False:
                    if rightSide[1].collidepoint(mouse) and event.button == 1:
                        roomSide += 1
                        currentRoomSide = roomSide%4
                    if leftSide[1].collidepoint(mouse) and event.button == 1:
                        roomSide -= 1
                        currentRoomSide = roomSide%4

                    if openButton[1].collidepoint(mouse) and event.button == 1:
                        if flags["OpenButtonActive"] == False:
                            deactivateCommandButtons()
                            flags["OpenButtonActive"] = True
                        else:
                            deactivateCommandButtons()
                            
                    if closeButton[1].collidepoint(mouse) and event.button == 1:
                        if flags["CloseButtonActive"] == False:
                            deactivateCommandButtons()
                            flags["CloseButtonActive"] = True
                        else:
                            deactivateCommandButtons()
                            
                    if pushButton[1].collidepoint(mouse) and event.button == 1:
                        if flags["PushButtonActive"] == False:
                            deactivateCommandButtons()
                            flags["PushButtonActive"] = True
                        else:
                            deactivateCommandButtons()
                            
                    if pullButton[1].collidepoint(mouse) and event.button == 1:
                        if flags["PullButtonActive"] == False:
                            deactivateCommandButtons()
                            flags["PullButtonActive"] = True
                        else:
                            deactivateCommandButtons()
                            
                    if examineButton[1].collidepoint(mouse) and event.button == 1:
                        if flags["ExamineButtonActive"] == False:
                            deactivateCommandButtons()
                            flags["ExamineButtonActive"] = True
                        else:
                            deactivateCommandButtons()
                            
                    if giveButton[1].collidepoint(mouse) and event.button == 1:
                        if flags["GiveButtonActive"] == False:
                            deactivateCommandButtons()
                            flags["GiveButtonActive"] = True
                        else:
                            deactivateCommandButtons()
                            
                    if talkToButton[1].collidepoint(mouse) and event.button == 1:
                        if flags["TalkToButtonActive"] == False:
                            deactivateCommandButtons()
                            flags["TalkToButtonActive"] = True
                        else:
                            deactivateCommandButtons()
                            
                    if pickUpButton[1].collidepoint(mouse) and event.button == 1:
                        if flags["PickUpButtonActive"] == False:
                            deactivateCommandButtons()
                            flags["PickUpButtonActive"] = True
                        else:
                            deactivateCommandButtons()
                            
                    if useButton[1].collidepoint(mouse) and event.button == 1:
                        if flags["UseButtonActive"] == False:
                            deactivateCommandButtons()
                            flags["UseButtonActive"] = True
                        else:
                            deactivateCommandButtons()

                    #The arrows do not work but are also not currently necessary
                    if upArrowButton[1].collidepoint(mouse) and event.button == 1:
                        if imod > 0:
                            imod -=1
                            
                    if downArrowButton[1].collidepoint(mouse) and event.button == 1:
                        imod +=1
 
                    if flags["UseButtonActive"]:
                        if IBox1Button[1].collidepoint(mouse) and event.button == 1:
                            if flags["IBox1ButtonActive"] == False:
                                deactivateInventoryButtons()
                                flags["IBox1ButtonActive"] = True
                                activeISlot = 0
                            else:
                                deactivateInventoryButtons()
                        if IBox2Button[1].collidepoint(mouse) and event.button == 1:
                            if flags["IBox2ButtonActive"] == False:
                                deactivateInventoryButtons()
                                flags["IBox2ButtonActive"] = True
                                activeISlot = 1
                            else:
                                deactivateInventoryButtons()
                        if IBox3Button[1].collidepoint(mouse) and event.button == 1:
                            if flags["IBox3ButtonActive"] == False:
                                deactivateInventoryButtons()
                                flags["IBox3ButtonActive"] = True
                                activeISlot = 2
                            else:
                                deactivateInventoryButtons()
                        if IBox4Button[1].collidepoint(mouse) and event.button == 1:
                            if flags["IBox4ButtonActive"] == False:
                                deactivateInventoryButtons()
                                flags["IBox4ButtonActive"] = True
                                activeISlot = 3
                            else:
                                deactivateInventoryButtons()
                        if IBox5Button[1].collidepoint(mouse) and event.button == 1:
                            if flags["IBox5ButtonActive"] == False:
                                deactivateInventoryButtons()
                                flags["IBox5ButtonActive"] = True
                                activeISlot = 4
                            else:
                                deactivateInventoryButtons()
                        if IBox6Button[1].collidepoint(mouse) and event.button == 1:
                            if flags["IBox6ButtonActive"] == False:
                                deactivateInventoryButtons()
                                flags["IBox6ButtonActive"] = True
                                activeISlot = 5
                            else:
                                deactivateInventoryButtons()
                        if IBox7Button[1].collidepoint(mouse) and event.button == 1:
                            if flags["IBox7ButtonActive"] == False:
                                deactivateInventoryButtons()
                                flags["IBox7ButtonActive"] = True
                                activeISlot = 6
                            else:
                                deactivateInventoryButtons()
                        if IBox8Button[1].collidepoint(mouse) and event.button == 1:
                            if flags["IBox8ButtonActive"] == False:
                                deactivateInventoryButtons()
                                flags["IBox8ButtonActive"] = True
                                activeISlot = 7
                            else:
                                deactivateInventoryButtons()
                    else:
                        deactivateInventoryButtons()

                    #Checks for differnt Commands on each of the inventory slots.
                        
                    if flags["ExamineButtonActive"]: 
                        if IBox1Button[1].collidepoint(mouse) and event.button == 1:
                            outputInitialize(Inventory[0+8*imod]["Item Description"],grayBlue,1)
                        elif IBox2Button[1].collidepoint(mouse) and event.button == 1:
                            outputInitialize(Inventory[1+8*imod]["Item Description"],grayBlue,1)
                        elif IBox3Button[1].collidepoint(mouse) and event.button == 1:
                            outputInitialize(Inventory[2+8*imod]["Item Description"],grayBlue,1)
                        elif IBox4Button[1].collidepoint(mouse) and event.button == 1:
                            outputInitialize(Inventory[3+8*imod]["Item Description"],grayBlue,1)
                        elif IBox5Button[1].collidepoint(mouse) and event.button == 1:
                            outputInitialize(Inventory[4+8*imod]["Item Description"],grayBlue,1)
                        elif IBox6Button[1].collidepoint(mouse) and event.button == 1:
                            outputInitialize(Inventory[5+8*imod]["Item Description"],grayBlue,1)
                        elif IBox7Button[1].collidepoint(mouse) and event.button == 1:
                            outputInitialize(Inventory[6+8*imod]["Item Description"],grayBlue,1)
                        elif IBox8Button[1].collidepoint(mouse) and event.button == 1:
                            outputInitialize(Inventory[7+8*imod]["Item Description"],grayBlue,1)
                            
                    if flags["UseButtonActive"]:
                        if IBox1Button[1].collidepoint(mouse) and event.button == 1:
                            currentObject = Inventory[0+8*imod]["Item Name"]
                        elif IBox2Button[1].collidepoint(mouse) and event.button == 1:
                            currentObject = Inventory[1+8*imod]["Item Name"]
                        elif IBox3Button[1].collidepoint(mouse) and event.button == 1:
                            currentObject = Inventory[2+8*imod]["Item Name"]
                        elif IBox4Button[1].collidepoint(mouse) and event.button == 1:
                            currentObject = Inventory[3+8*imod]["Item Name"]
                        elif IBox5Button[1].collidepoint(mouse) and event.button == 1:
                            currentObject = Inventory[4+8*imod]["Item Name"]
                        elif IBox6Button[1].collidepoint(mouse) and event.button == 1:
                            currentObject = Inventory[5+8*imod]["Item Name"]
                        elif IBox7Button[1].collidepoint(mouse) and event.button == 1:
                            currentObject = Inventory[6+8*imod]["Item Name"]
                        elif IBox8Button[1].collidepoint(mouse) and event.button == 1:
                            currentObject = Inventory[7+8*imod]["Item Name"]
                    else:
                        currentObject = ""

            if flags["ShowLoadMenu"]:#Button Presses for Load menu
                if loadGameButton1[1].collidepoint(mouse) and event.button == 1:
                    print("Load - Save 1")
                    with open("SAVES/SAVE1/flags.p", "rb") as f:
                        tempflags = pickle.load(f)
                    with open("SAVES/SAVE1/inventory.p", "rb") as g:
                        tempInventory = pickle.load(g)
                    with open("SAVES/SAVE1/current_slot.p", "rb") as g:
                        currentSlot = pickle.load(g)

                    flags["LoadGameButton1Pressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif loadGameButton2[1].collidepoint(mouse) and event.button == 1:
                    print("Load - Save 2")
                    with open("SAVES/SAVE2/flags.p", "rb") as f:
                        tempflags = pickle.load(f)
                    with open("SAVES/SAVE2/inventory.p", "rb") as g:
                        tempInventory = pickle.load(g)
                    flags["LoadGameButton2Pressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif loadGameButton3[1].collidepoint(mouse) and event.button == 1:
                    print("Load - Save 3")
                    with open("SAVES/SAVE3/flags.p", "rb") as f:
                        tempflags = pickle.load(f)
                    with open("SAVES/SAVE3/inventory.p", "rb") as g:
                        tempInventory = pickle.load(g)
                    flags["LoadGameButton3Pressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0
                elif loadBackButton[1].collidepoint(mouse) and event.button == 1:
                    print("Back")
                    flags["LoadBackButtonPressed"] = True
                    
                    menuGlideMult = 100
                    bpt = 0

        elif event.type == KEYDOWN:#Checks key inputs

            if event.key == K_SPACE:#Developer Key for refreshing images on screen
                flags["UpdateImages"] = True
            elif event.key == K_ESCAPE:#Pause Key
                flags["CursorOverride"] = True
                if flags["ShowMenu"] == False and flags["ShowLoadMenu"] == False and flags["ShowPopUpMenu"] == False and flags["ShowResolutionMenu"] == False and flags["ShowSettingsMenu"] == False and flags["ShowSaveMenu"] == False and flags["ShowNPCInterface"] == False:

                    popUpScreen.set_alpha(0)
                    flags["ShowPopUpMenu"] = True

                elif flags["ShowPopUpMenu"]:
                    flags["ShowPopUpMenu"] = False
            else:
                et = 500
                efont = pygame.font.Font("Fonts/ROTG.otf", int(50*scale))
                emessage = chr(event.key)+" does nothing"
                    
        #Moves the song on when the previous one ends
        elif event.type == TRACK_END:
            flags["NextSong"] = True

        if flags["NextSong"]:
            track += 1
            flags["NextSong"] = False
            TRACKS = get_music(area)
            track = (track)%len(TRACKS)
            flags["PlayMusic"] = True

    # UPDATES
    #Blits current dircetion to the screen
    if currentRoomSide == 0:
        directionText = "North"
    elif currentRoomSide == 1:
        directionText = "East"
    elif currentRoomSide == 2:
        directionText = "South"
    elif currentRoomSide == 3:
        directionText = "West"
                #Blits FPS    to screen
    if clock.get_time() != 0:
        if fpst >= 200:
            fpsText= (str(round(1000/loopTime)))
            fpst = 0
        fpsTextImage = textify(30, fpsText, True, green, (0, 0), screen)
        if flags["ShowUserInterface"]:
            directionTextImage = textify(30, directionText, True, green, (0, 50), screen)
                #Updates game state
    if et>0:
        error = efont.render(emessage, True, green)
        error.set_alpha(et-275)
        screen.blit(error, ((((screenWidth-(barSizeX*2)-error.get_width())/2)*scale+barSizeX, 168*scale+barSizeY)))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
