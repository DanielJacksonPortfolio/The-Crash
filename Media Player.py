import sys, pygame
from pygame.locals import *

def get_music(area):
    playlist = []
    if area == 1:
        playlist = ["Sounds/OGG/LOADING.ogg","Sounds/OGG/MENU.ogg","Sounds/OGG/CREDITS.ogg","Sounds/OGG/CREDITS 2.ogg","Sounds/OGG/INTRO.ogg","Sounds/OGG/MEDIEVAL.ogg","Sounds/OGG/NIGHTCLUB.ogg","Sounds/OGG/RINGTONE2.ogg","Sounds/OGG/ROBOT.ogg","Sounds/OGG/SCI FI.ogg"]
    elif area == 2:
        playlist = ["Sounds/OGG/RINGTONE2.ogg"]
    elif area == 3:
        playlist = ["Sounds/OGG/WE BUILT THIS CITY.ogg"]
    elif area == 4:
        playlist = ["Sounds/OGG/HOOKED ON A FEELING.ogg","Sounds/OGG/GO ALL THE WAY.ogg","Sounds/OGG/SPIRIT IN THE SKY.ogg","Sounds/OGG/MOONAGE DAYDREAM.ogg","Sounds/OGG/FOOLED AROUND AND FELL IN LOVE.ogg","Sounds/OGG/IM NOT IN LOVE.ogg","Sounds/OGG/I WANT YOU BACK.ogg","Sounds/OGG/COME AND GET YOUR LOVE.ogg","Sounds/OGG/ESCAPE.ogg","Sounds/OGG/AINT NO MOUNTAIN.ogg"]
    elif area == 5:
        playlist = ["Sounds/OGG/AROUND THE WORLD.ogg","Sounds/OGG/DONT STOP BELEVIN.ogg","Sounds/OGG/WANTED DEAD OR ALIVE.ogg"]
    return playlist

def pause(playing):
    PPI = ""
    if playing == True:
        pygame.mixer.music.pause()
        playing = False
        PPI = "Images/MEDIA/PLAY.png"
    elif playing == False:
        pygame.mixer.music.unpause()
        playing = True
        PPI = "Images/MEDIA/PAUSE.png"
    return [playing, PPI]

def change_track(track,modifier):
    track += modifier
    return track

def change_area(area,modifier):
    area += modifier
    return area

def buttonify(Picture, coords, surface):
    image = pygame.image.load(Picture).convert_alpha()
    imagerect = image.get_rect()
    imagerect.topright = coords
    surface.blit(image,imagerect)
    return (image,imagerect)

pygame.init()
fullscreen = 1
screen = pygame.display.set_mode((1100,550),fullscreen)
clock = pygame.time.Clock()
fps = 60

TRACK_END = pygame.USEREVENT+1
track = 0
playing = True
area = 1
TRACKS = get_music(area)
default_text = True
next_song = False
text1 = "NOW PLAYING:"
temptext = (TRACKS[track])[11:(len(TRACKS[track])-4)]
text3 = (" "*(17-len(temptext))+temptext)
text2 = text3
track_changed = True
dt = 0

PPI = "Images/MEDIA/PAUSE.png"

pygame.mixer.music.set_endevent(TRACK_END)
pygame.mixer.music.load(TRACKS[track])
pygame.mixer.music.play()

myFont = pygame.font.Font("Fonts/DS-DIGI.TTF",70)

while 1:
    dt += clock.get_time()
    screen.fill((128,0,0))
    
    previousAreaButton = buttonify("Images/MEDIA/PAREA.png",(200,325),screen)
    previousSongButton = buttonify("Images/MEDIA/PSONG.png",(400,325),screen)
    playPauseButton = buttonify(PPI,(650,300),screen)
    nextSongButton = buttonify("Images/MEDIA/NSONG.png",(850,325),screen)
    nextAreaButton = buttonify("Images/MEDIA/NAREA.png",(1050,325),screen)
    
    outputrect1 = pygame.draw.rect(screen,(80,80,80),(50,50,1000,100),0)
    outputrect2 = pygame.draw.rect(screen,(0,0,0),(60,60,980,80),0)
    outputrect3 = pygame.draw.rect(screen,(80,80,80),(300,150,500,90),0)
    outputrect4 = pygame.draw.rect(screen,(0,0,0),(310,150,480,80),0)


    if playing:
        if dt >= 200:
            text1 = "NOW PLAYING:"
            temptext = (TRACKS[track])[11:(len(TRACKS[track])-4)]
            if len(temptext) >= 20:
                if track_changed == True:
                    text3 = (" "*5)+temptext
                    track_changed = False
                temptext = text3
                text3 = temptext[1:len(text3)]+temptext[0]
                text2 = text3[0:18]
            else:
                text2 = temptext
            dt = 0
    else:
        text1 = "PAUSED"
        text2 = ""
        
    timeText = str(pygame.mixer.music.get_pos()/1000)
    currentTime = int(round(float(timeText)))
    currentMinutes = currentTime//60
    currentSeconds = currentTime%60
    if currentSeconds < 10:
        currentSeconds = "0"+str(currentSeconds)
    else:
        currentSeconds = str(currentSeconds)
    if currentMinutes < 10:
        currentMinutes = "0"+str(currentMinutes)
    else:
        currentMinutes = str(currentMinutes)
    text4 = str(currentMinutes)+":"+currentSeconds
    
    textImage1 = myFont.render(text1,True,(0,255,0))
    textImage2 = myFont.render(text2,True,(0,255,0))
    textImage3 = myFont.render(text4,True,(0,255,0))
    screen.blit(textImage1,(70,65))
    screen.blit(textImage2,(440,65))
    screen.blit(textImage3,(470,155))
    
        
    for event in pygame.event.get():        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if playPauseButton[1].collidepoint(mouse):
                state_flip = pause(playing)
                playing = state_flip[0]
                PPI = state_flip[1]
            elif nextSongButton[1].collidepoint(mouse):
                track = change_track(track,1)
                next_song = True
            elif previousSongButton[1].collidepoint(mouse):
                track = change_track(track,-1)
                next_song = True
            elif nextAreaButton[1].collidepoint(mouse):
                if area <= 4:#Max Number of area - 1
                    area = change_area(area,1)
                else:
                    area = 1#Min Number of area
                track = 0
                next_song = True
            elif previousAreaButton[1].collidepoint(mouse):
                if area >= 2:#Min Number of area + 1
                    area = change_area(area,-1)
                else:
                    area = 5#Max number of area
                track = 0
                next_song = True

                
        elif event.type == TRACK_END:
            track = change_track(track,1)
            next_song = True
        
        if next_song == True:
            track_changed = True
            next_song = False
            TRACKS = get_music(area)
            track = (track)%len(TRACKS)
            pygame.mixer.music.load(TRACKS[track])
            pygame.mixer.music.play()
            if playing == False:
                state_flip = pause(playing)
                playing = state_flip[0]
                PPI = state_flip[1]

    pygame.display.flip()
    pygame.display.update()
    clock.tick(fps)
