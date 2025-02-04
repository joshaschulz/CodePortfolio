import pygame
import time
import random
from os import path

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()


pygame.mixer.music.load("Jerry Five.mp3")
pygame.mixer.music.set_volume(0.3)
passive_sounds = pygame.mixer.Sound("Urban Traffic.wav")
passive_sounds.set_volume(0.2)
crash_sound2 = pygame.mixer.Sound("Crash Sound.wav")
crash_sound = pygame.mixer.Sound("Crash Sound2.wav")
crash_sound.set_volume(1)
ding_sound = pygame.mixer.Sound("Ding.wav")
button_sound = pygame.mixer.Sound("Button Sound.wav")
engine_sound1 = pygame.mixer.Sound("Engine Sound 1.wav")
engine_sound2 = pygame.mixer.Sound("Engine Sound 2.wav")
money_sound = pygame.mixer.Sound("Money Sound.wav")

display_width = 1000
display_height = 800

black = (0,0,0)
grey = (150,150,150)
white = (255,255,255)
red = (255,0,0)
dark_red = (200,0,0)
dark_green = (0,200,0)
green = (0,255,0)
blue = (0,0,255)

clock = pygame.time.Clock()


car_width = 113
exitNum = 180

pause = False
offRampPause = False

#highscore
def get_high_score():
    high_score = 0

    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
    except IOError:
        print("IOError. Ask Josh to fix.")
    except ValueError:
        print("ValueError. Ask Josh to fix.")
    return high_score
def save_high_score(new_high_score):
    try:
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        print("IOError. Ask Josh to fix.")

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Swerve")

#gas
gasFull = pygame.image.load('GasFull.png')
gas78 = pygame.image.load('Gas78.png')
gas68 = pygame.image.load('Gas68.png')
gas58 = pygame.image.load('Gas58.png')
gas48 = pygame.image.load('Gas48.png')
gas38 = pygame.image.load('Gas38.png')
gas28 = pygame.image.load('Gas28.png')
gas18 = pygame.image.load('Gas18.png')
gasEmpty = pygame.image.load('GasEmpty.png')
#gas
speedometer = pygame.image.load('Speedometer.png')

crash1 = pygame.image.load('crash1.png')
crash2 = pygame.image.load('crash2.png')

carArray = pygame.image.load('CarArray.png')
PINKcarImg = pygame.image.load('racecarPINK.png')
REDcarImg = pygame.image.load('racecarRED.png')
GREENcarImg = pygame.image.load('racecarGREEN.png')
YELLOWcarImg = pygame.image.load('racecarYELLOW.png')
BLUEcarImg = pygame.image.load('racecarBLUE.png')
gameIcon = pygame.image.load('racecar ICON.png')
backgroundImg = pygame.image.load('Freeway BackgroundLONG2.png')
backgroundEXIT = pygame.image.load('Freeway EXIT.png')
overlayIMG = pygame.image.load('Overlay.png')

pygame.display.set_icon(gameIcon)

carImg = PINKcarImg


#def things_dodged(count):
#    font = pygame.font.SysFont(None, 30)
#    text = font.render("Dodged: "+str(count), True, black)
#    gameDisplay.blit(text,(20,20))

def speed(count):
    gameDisplay.blit(speedometer,(((display_width*.99) - 85),(display_height*.9)))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects((str(count)), smallText, white)
    textRect.center = (((display_width*.99) - 43),(display_height*.927))
    gameDisplay.blit(textSurf, textRect)
    
def multiplier(count):
    font = pygame.font.SysFont(None, 30)
    text = font.render("Multiplier: "+str(count), True, black)
    gameDisplay.blit(text,(20,40))

#def timer():
    #global gameStartTime
    #font = pygame.font.SysFont(None, 30)
    #text = font.render("Time: "+str(gameStartTime), True, black)
    #gameDisplay.blit(text,(20,60))

def things(carImg2, thingx, thingy, thingw, thingh):    
    gameDisplay.blit(carImg2, [thingx, thingy, thingw, thingh])

def background(image,x,y, bkgStarty):
    gameDisplay.blit(image, (x,y), [0, bkgStarty, 1000, 1700])
    
def overlay(image,x,y):
    gameDisplay.blit(image, (x,y))
    
def car(carImg,x,y,crashCount):
    gameDisplay.blit(carImg, (x,y))
    if crashCount >= 1:
        gameDisplay.blit(crash1, (x,y))
        if crashCount == 2:
            gameDisplay.blit(crash2, (x,y))


def gas(tank,x,y):
    gameDisplay.blit(tank, (x,y))

def nextExitSoon():
    font = pygame.font.SysFont(None, 65)
    text = font.render("Exit Approaching", True, black)
    gameDisplay.blit(text,(310,40))


def onRampFuel():
    global score
    global tank
    if tank == gas58:
        if score <= 500:
            smallText = pygame.font.Font("freesansbold.ttf",25)
            textSurf, textRect = text_objects("Insufficient Funds", smallText, red)
            textRect.center = ( (250+(150/2)), (625) )
            gameDisplay.blit(textSurf, textRect) 
        else:
            global offRampPause
            global thing_speed
            global gameStartTime

            score -= 500
            gameStartTime = pygame.time.get_ticks()
            
            thing_speed = 4
            pygame.mixer.music.unpause()
            pygame.mixer.Sound.play(passive_sounds, loops = -1)
            offRampPause = False
    if tank == gas18:
        if score <= 1000:
            smallText = pygame.font.Font("freesansbold.ttf",25)
            textSurf, textRect = text_objects("Insufficient Funds", smallText, red)
            textRect.center = ( (250+(150/2)), (625) )
            gameDisplay.blit(textSurf, textRect) 
        else:
            score -= 1000
            gameStartTime = pygame.time.get_ticks()
            
            thing_speed = 4
            pygame.mixer.music.unpause()
            pygame.mixer.Sound.play(passive_sounds, loops = -1)
            offRampPause = False
    if tank == gasFull:
        smallText = pygame.font.Font("freesansbold.ttf",25)
        textSurf, textRect = text_objects("Full Tank", smallText, red)
        textRect.center = ( (250+(150/2)), (625) )
        gameDisplay.blit(textSurf, textRect)
            
def onRampRepair():
    global score
    global crashCount
    if crashCount == 0:
        smallText = pygame.font.Font("freesansbold.ttf",25)
        textSurf, textRect = text_objects("No Damage", smallText, red)
        textRect.center = ( (250+(150/2)), (625) )
        gameDisplay.blit(textSurf, textRect)
    if crashCount == 1:
        if score <= 1000:
            smallText = pygame.font.Font("freesansbold.ttf",25)
            textSurf, textRect = text_objects("Insufficient Funds", smallText, red)
            textRect.center = ( (250+(150/2)), (625) )
            gameDisplay.blit(textSurf, textRect) 
        else:
            global offRampPause
            global thing_speed

            score -= 1000
            crashCount = 0
            
            thing_speed = 4
            pygame.mixer.music.unpause()
            pygame.mixer.Sound.play(passive_sounds, loops = -1)
            offRampPause = False
    if crashCount == 2:
        if score <= 2000:
            smallText = pygame.font.Font("freesansbold.ttf",25)
            textSurf, textRect = text_objects("Insufficient Funds", smallText, red)
            textRect.center = ( (250+(150/2)), (625) )
            gameDisplay.blit(textSurf, textRect) 
        else:
            score -= 2000
            crashCount = 0
            
            thing_speed = 4
            pygame.mixer.music.unpause()
            pygame.mixer.Sound.play(passive_sounds, loops = -1)
            offRampPause = False
    
def onRamp():
    global offRampPause
    global thing_speed
    global gameStartTime
    global pausedTime
    global unpausedTime

    thing_speed = 4
    pygame.mixer.music.unpause()
    pygame.mixer.Sound.play(passive_sounds, loops = -1)
    offRampPause = False
    unpausedTime = pygame.time.get_ticks()
    #gameStartTime += pausedTime
    
def offRamp():
    global exitNum
    pygame.mixer.music.pause()
    pygame.mixer.Sound.stop(passive_sounds)

    exitNum += 1
    
    while offRampPause:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit_game()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    unpause()
                
        gameDisplay.fill(white)

        pygame.draw.rect(gameDisplay, grey, (250,400,150,100))
        pygame.draw.rect(gameDisplay, grey, (600,400,150,100))
        pygame.draw.rect(gameDisplay, dark_green, (425,525,150,100))

            
        largeText = pygame.font.Font('freesansbold.ttf',70)
        TextSurf, TextRect = text_objects(("Exit "+str(exitNum)), largeText, black)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)

        button("Gas Station",250,400,150,100,grey,gasStation)
        button("Repair Shop",600,400,150,100,grey,repairShop)
        button("Continue",425,525,150,100,dark_green,onRamp)

        smallText = pygame.font.Font("freesansbold.ttf",22)
        textSurf, textRect = text_objects("Gas Station", smallText, black)
        textRect.center = ( (250+(150/2)), (400+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",22)
        textSurf, textRect = text_objects("Repair Shop", smallText, black)
        textRect.center = ( (600+(150/2)), (400+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("Continue", smallText, black)
        textRect.center = ( (425+(150/2)), (525+(100/2)) )
        gameDisplay.blit(textSurf, textRect)
        
        pygame.display.update()
        clock.tick(15)
        
def repairShop():
    global score
    global crashCount

    pygame.mixer.music.pause()
    pygame.mixer.Sound.stop(passive_sounds)

    while offRampPause:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit_game()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                
        gameDisplay.fill(white)

        pygame.draw.rect(gameDisplay, dark_green, (600,500,150,100))
        pygame.draw.rect(gameDisplay, grey, (250,500,150,100))
        
        largeText = pygame.font.Font('freesansbold.ttf',70)
        TextSurf, TextRect = text_objects("Repair Shop", largeText, black)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)

        button("Continue",600,500,150,100,dark_green,onRamp)
        button("Repair",250,500,150,100,grey,onRampRepair)
        

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("Continue", smallText, black)
        textRect.center = ( (600+(150/2)), (500+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("Repair", smallText, black)
        textRect.center = ( (250+(150/2)), (500+(100/2)) )
        gameDisplay.blit(textSurf, textRect)
        if crashCount == 1:    
            smallText = pygame.font.Font("freesansbold.ttf",25)
            textSurf, textRect = text_objects("Cost: 1000", smallText, black)
            textRect.center = ( (250+(150/2)), (480) )
            gameDisplay.blit(textSurf, textRect)
        if crashCount == 2:
            smallText = pygame.font.Font("freesansbold.ttf",25)
            textSurf, textRect = text_objects("Cost: 2000", smallText, black)
            textRect.center = ( (250+(150/2)), (480) )
            gameDisplay.blit(textSurf, textRect)
        
        pygame.display.update()
        clock.tick(15)
        
def gasStation():
    global tank
    global score

    pygame.mixer.music.pause()
    pygame.mixer.Sound.stop(passive_sounds)

    while offRampPause:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit_game()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                
        gameDisplay.fill(white)

        pygame.draw.rect(gameDisplay, dark_green, (600,500,150,100))
        pygame.draw.rect(gameDisplay, grey, (250,500,150,100))
        
        largeText = pygame.font.Font('freesansbold.ttf',70)
        TextSurf, TextRect = text_objects("Gas Station", largeText, black)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)

        button("Continue",600,500,150,100,dark_green,onRamp)
        button("Refuel",250,500,150,100,grey,onRampFuel)
        

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("Continue", smallText, black)
        textRect.center = ( (600+(150/2)), (500+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("Refuel", smallText, black)
        textRect.center = ( (250+(150/2)), (500+(100/2)) )
        gameDisplay.blit(textSurf, textRect)
        if tank == gas58:    
            smallText = pygame.font.Font("freesansbold.ttf",25)
            textSurf, textRect = text_objects("Cost: 500", smallText, black)
            textRect.center = ( (250+(150/2)), (480) )
            gameDisplay.blit(textSurf, textRect)
        if tank == gas18:
            smallText = pygame.font.Font("freesansbold.ttf",25)
            textSurf, textRect = text_objects("Cost: 1000", smallText, black)
            textRect.center = ( (250+(150/2)), (480) )
            gameDisplay.blit(textSurf, textRect)
        
        pygame.display.update()
        clock.tick(15)

        
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

##def message_display(text):
##    largeText = pygame.font.Font('freesansbold.ttf',70)
##    TextSurf, TextRect = text_objects(text, largeText)
##    TextRect.center = ((display_width/2),(display_height/2))
##    gameDisplay.blit(TextSurf, TextRect)

def total_score(count):
    font = pygame.font.SysFont(None, 30)
    text = font.render("Score: "+str(count), True, black)
    gameDisplay.blit(text,(20,80))


def crash(score):

    pygame.mixer.music.stop()
    pygame.mixer.Sound.stop(passive_sounds)
    pygame.mixer.Sound.play(crash_sound)
    
    while True:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit_game()

        high_score = get_high_score()
        if score > high_score:
            save_high_score(score)

                
        gameDisplay.fill(white)

        pygame.draw.rect(gameDisplay, dark_green, (250,400,150,100))
        pygame.draw.rect(gameDisplay, dark_red, (600,400,150,100))
        
        largeText = pygame.font.Font('freesansbold.ttf',70)
        TextSurf, TextRect = text_objects("You Crashed!", largeText, black)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)

        button("Play Again",250,400,150,100,dark_green,game_loop)
        button("Quit",600,400,150,100,dark_red,quit_game)

        smallText = pygame.font.Font("freesansbold.ttf",35)
        textSurf, textRect = text_objects(("Score: "+str(score)), smallText, black)
        textRect.center = ((display_width/2),(display_height/2.6))
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",35)
        textSurf, textRect = text_objects(("Highscore: "+str(high_score)), smallText, black)
        textRect.center = ((display_width/2),(display_height/2.35))
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",25)
        textSurf, textRect = text_objects("Play Again", smallText, black)
        textRect.center = ( (250+(150/2)), (400+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("Quit", smallText, black)
        textRect.center = ( (600+(150/2)), (400+(100/2)) )
        gameDisplay.blit(textSurf, textRect)
        
        pygame.display.update()
        clock.tick(15)

def OutOfGas(score):
    
    pygame.mixer.music.stop()
    pygame.mixer.Sound.stop(passive_sounds)

    while True:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit_game()

        high_score = get_high_score()
        if score > high_score:
            save_high_score(score)

            
        gameDisplay.fill(white)

        pygame.draw.rect(gameDisplay, dark_green, (250,400,150,100))
        pygame.draw.rect(gameDisplay, dark_red, (600,400,150,100))
        
        largeText = pygame.font.Font('freesansbold.ttf',70)
        TextSurf, TextRect = text_objects("Out of Gas!", largeText, black)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)

        button("Play Again",250,400,150,100,dark_green,game_loop)
        button("Quit",600,400,150,100,dark_red,quit_game)
        
        smallText = pygame.font.Font("freesansbold.ttf",35)
        textSurf, textRect = text_objects(("Score: "+str(score)), smallText, black)
        textRect.center = ((display_width/2),(display_height/2.6))
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",35)
        textSurf, textRect = text_objects(("Highscore: "+str(high_score)), smallText, black)
        textRect.center = ((display_width/2),(display_height/2.35))
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",25)
        textSurf, textRect = text_objects("Play Again", smallText, black)
        textRect.center = ( (250+(150/2)), (400+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("Quit", smallText, black)
        textRect.center = ( (600+(150/2)), (400+(100/2)) )
        gameDisplay.blit(textSurf, textRect)
        
        pygame.display.update()
        clock.tick(15)

def buttonUp(msg,x,y,w,h,c,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(mouse)
        
    if x+w > mouse[0] > x and  y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, black, (x-5,y-5,w+10,h+10))
        pygame.draw.rect(gameDisplay, c, (x,y,w,h))
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP and action != None:
                action()
            
def button(msg,x,y,w,h,c,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(mouse)
        
    if x+w > mouse[0] > x and  y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, black, (x-5,y-5,w+10,h+10))
        pygame.draw.rect(gameDisplay, c, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
def buttonBox(x,y,w,h,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(mouse)
        
    if x+w > mouse[0] > x and  y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, black, [x,y,w,h], 2)
        if click[0] == 1 and action != None:
            action()
def buttonOutline(x,y,w,h):
    pygame.draw.rect(gameDisplay, black, [x,y,w,h], 2)


def quit_game():
    pygame.quit()
    quit()

def unpause():
    global pause
    global unpausedTime
    pygame.mixer.music.unpause()
    pygame.mixer.Sound.play(passive_sounds, loops = -1)
    unpausedTime = pygame.time.get_ticks()
    pause = False
    
def paused():
    
    pygame.mixer.music.pause()
    pygame.mixer.Sound.stop(passive_sounds)

    while pause:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit_game()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    unpause()
                if event.key == pygame.K_ESCAPE:
                    unpause()
                
        gameDisplay.fill(white)

        pygame.draw.rect(gameDisplay, dark_green, (250,400,150,100))
        pygame.draw.rect(gameDisplay, dark_red, (600,400,150,100))
        
        largeText = pygame.font.Font('freesansbold.ttf',70)
        TextSurf, TextRect = text_objects("Paused", largeText, black)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)

        button("Continue",250,400,150,100,dark_green,unpause)
        button("Quit",600,400,150,100,dark_red,quit_game)
        

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("Continue", smallText, black)
        textRect.center = ( (250+(150/2)), (400+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("Quit", smallText, black)
        textRect.center = ( (600+(150/2)), (400+(100/2)) )
        gameDisplay.blit(textSurf, textRect)       
        
        pygame.display.update()
        clock.tick(15)
def blueCar():
    global carImg
    print("Chooses blue car")
    carImg = BLUEcarImg
    randomSound = random.choice(range(1,3))
    if randomSound == 1:
        pygame.mixer.Sound.play(engine_sound1)
    if randomSound == 2:
        pygame.mixer.Sound.play(engine_sound2)
def greenCar():
    global carImg
    print("Chooses green car")
    carImg = GREENcarImg
    randomSound = random.choice(range(1,3))
    if randomSound == 1:
        pygame.mixer.Sound.play(engine_sound1)
    if randomSound == 2:
        pygame.mixer.Sound.play(engine_sound2)
def pinkCar():
    global carImg
    print("Chooses pink car")
    carImg = PINKcarImg
    randomSound = random.choice(range(1,3))
    if randomSound == 1:
        pygame.mixer.Sound.play(engine_sound1)
    if randomSound == 2:
        pygame.mixer.Sound.play(engine_sound2)
def redCar():
    global carImg
    print("Chooses red car")
    carImg = REDcarImg
    randomSound = random.choice(range(1,3))
    if randomSound == 1:
        pygame.mixer.Sound.play(engine_sound1)
    if randomSound == 2:
        pygame.mixer.Sound.play(engine_sound2)
def yellowCar():
    global carImg
    print("Chooses yellow car")
    carImg = YELLOWcarImg
    randomSound = random.choice(range(1,3))
    if randomSound == 1:
        pygame.mixer.Sound.play(engine_sound1)
    if randomSound == 2:
        pygame.mixer.Sound.play(engine_sound2)
def car_chooser():
    if carImg == BLUEcarImg:
        buttonOutline(170,530,134,155)

    if carImg == GREENcarImg:
        buttonOutline(303,530,131,155)

    if carImg == PINKcarImg:
        buttonOutline(433,530,134,155)

    if carImg == REDcarImg:
        buttonOutline(566,530,132,155)

    if carImg == YELLOWcarImg:
        buttonOutline(697,530,134,155)

    
    gameDisplay.blit(carArray, (182,550))
    
    buttonBox(170,530,134,155,blueCar)
    buttonBox(303,530,131,155,greenCar)
    buttonBox(433,530,134,155,pinkCar)
    buttonBox(566,530,132,155,redCar)
    buttonBox(697,530,134,155,yellowCar)

def game_intro():
    
    intro = True

    while intro:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    quit_game()

        gameDisplay.fill(white)


        car_chooser()

        pygame.draw.rect(gameDisplay, dark_green, (200,350,150,100))
        pygame.draw.rect(gameDisplay, dark_red, (650,350,150,100))
        pygame.draw.rect(gameDisplay, grey, (400,350,200,100))
        
        largeText = pygame.font.Font('freesansbold.ttf',140)
        TextSurf, TextRect = text_objects("Swerve", largeText, black)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)

        button("START",200,350,150,100,dark_green,game_loop)
        button("QUIT",650,350,150,100,dark_red,quit_game)
        button("HOW TO PLAY",400,350,200,100,grey,how_to_play)
        
        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("START", smallText, black)
        textRect.center = ( (200+(150/2)), (350+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("QUIT", smallText, black)
        textRect.center = ( (650+(150/2)), (350+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",25)
        textSurf, textRect = text_objects("HOW TO PLAY", smallText, black)
        textRect.center = ( (400+(200/2)), (350+(100/2)) )
        gameDisplay.blit(textSurf, textRect)
            
        pygame.display.update()
        clock.tick(15)


def how_to_play():
    
    howToPlay = True

    while howToPlay:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_intro()
                if event.key == pygame.K_ESCAPE:
                    game_intro()

        gameDisplay.fill(white)

        pygame.draw.rect(gameDisplay, dark_green, (250,600,150,100))
        pygame.draw.rect(gameDisplay, dark_red, (600,600,150,100))
        
        largeText = pygame.font.Font('freesansbold.ttf',100)
        TextSurf, TextRect = text_objects("How To Play", largeText, black)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)
        
            ##Instructions
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Use 'A' and 'D' or the LEFT and RIGHT arrow keys to move horizontally.", smallText, black)
        textRect.center = ( (500), (300+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Use 'W' and 'S' or the UP and DOWN arrow keys to accelerate/deceletrate.", smallText, black)
        textRect.center = ( (500), (350+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Avoid cars to increase your score, the faster you are moving, the greater your score.", smallText, black)
        textRect.center = ( (500), (400+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("To refuel or repair, enter the right lane and slow your speed when you approach an exit.", smallText, black)
        textRect.center = ( (500), (450+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("You lose the game by crashing or running out of gas.", smallText, black)
        textRect.center = ( (500), (500+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        button("START",250,600,150,100,dark_green,game_loop)
        button("QUIT",600,600,150,100,dark_red,quit_game)
            

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("START", smallText, black)
        textRect.center = ( (250+(150/2)), (600+(100/2)) )
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf",30)
        textSurf, textRect = text_objects("QUIT", smallText, black)
        textRect.center = ( (600+(150/2)), (600+(100/2)) )
        gameDisplay.blit(textSurf, textRect)
            
        pygame.display.update()
        clock.tick(15)



def game_loop():

    global pause
    global offRampPause
    global thing_speed
    global dodged
    global tank
    global score
    global crashCount
    global collision
    global gameStartTime
    global pausedTime
    global unpausedTime
    pausedTime = 0
    unpausedTime = 0
    gameStartTime = pygame.time.get_ticks()

    pygame.mixer.music.play(-1)
    pygame.mixer.Sound.play(passive_sounds, loops = -1)

    x = (display_width * .445)
    y = (display_height * .8)
    x_change = 0

    randomx = range(1,6)
    thing_startx = (random.choice(randomx)*150)+(random.choice(randomx)*3)-(random.choice(randomx)*3)
    thing_starty = -600
    thing_speed = 4
    thing_width = 113
    thing_height = 121
    
    randomCAR = random.choice(range(1,6))
    if randomCAR == 1:
        carImg2 = PINKcarImg
    if randomCAR == 2:
        carImg2 = REDcarImg
    if randomCAR == 3:
        carImg2 = GREENcarImg
    if randomCAR == 4:
        carImg2 = YELLOWcarImg
    if randomCAR == 5:
        carImg2 = BLUEcarImg

    bkgStarty = 0
   
    
    key_right = False
    key_left = False
    key_up = False
    key_down = False
    
    dodged = 0
    score = 0

    multi = 1
    tank = gasFull
    nextExit = 0

    crashCount = 0
    collision = False
    collision_time = 0
    collision_immune = False

    
    

    
    
    gameExit = False

    while not gameExit:
                #Quit Condition
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
                
                #Horizontal Movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    key_left = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    key_right = True
                #check for pause
                if event.key == pygame.K_p:
                    pause = True
                    pausedTime = pygame.time.get_ticks()
                    paused()
                if event.key == pygame.K_ESCAPE:
                    pause = True
                    pausedTime = pygame.time.get_ticks()
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    key_left = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    key_right = False

            if not key_left or key_right:
                x_change = 0
            if key_left:
                x_change = -10
            if key_right:
                x_change = 10
            #Speed Control
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    #key_up = True
                    thing_speed += 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    #key_down = True
                    thing_speed += -1
            #if event.type == pygame.KEYUP:
                #if event.key == pygame.K_UP:
                    #key_up = False
                #if event.key == pygame.K_DOWN:
                    #key_down = False

            #if key_up:
                #thing_speed += 1
            #if key_down:
                #thing_speed += -1
            if thing_speed < 0:
                thing_speed += 1
        x += x_change

        if thing_speed < 8:
            multi = 1
        if thing_speed >= 8:
            multi = 2
        if thing_speed >= 16:
            multi = 4
        if thing_speed >= 24:
            multi = 8
        if thing_speed >= 32:
            multi = 16
        if thing_speed >= 40:
            multi = 32
        if thing_speed >= 48:
            multi = 64
    #Gas
        gameCurrentTime = pygame.time.get_ticks() - (unpausedTime - pausedTime)
        if gameCurrentTime - gameStartTime < 10000:
            tank = gasFull
            nextExit = 0
        if gameCurrentTime - gameStartTime >= 10000:
            tank = gas78
            nextExit = 0
        if gameCurrentTime - gameStartTime >= 20000:
            tank = gas68
            nextExit = 0
        if gameCurrentTime - gameStartTime >= 30000:
            tank = gas58
            nextExit = 1
        if gameCurrentTime - gameStartTime >= 40000:
            tank = gas48
            nextExit = 0
        if gameCurrentTime - gameStartTime >= 50000:
            tank = gas38
            nextExit = 0
        if gameCurrentTime - gameStartTime >= 60000:
            tank = gas28
            nextExit = 0
        if gameCurrentTime - gameStartTime >= 70000:
            tank = gas18
            nextExit = 1
        if gameCurrentTime - gameStartTime >= 80000:
            tank = gasEmpty
            nextExit = 0
        if gameCurrentTime - gameStartTime >= 90000:
            OutOfGas(score)

        #gameDisplay.fill(white)
        #background


        thing_starty += thing_speed
        
        
        bkgStarty += -(thing_speed+10)
        if nextExit == 0:
            background(backgroundImg,0,-800,bkgStarty)
        elif nextExit == 1:
            background(backgroundEXIT,0,-800,bkgStarty)
            if thing_speed == 0 and x > 710:
                offRampPause = True
                pausedTime = pygame.time.get_ticks()
                offRamp()
                
        things(carImg2, thing_startx, thing_starty, thing_width, thing_height)
        #overlay(overlayIMG,0,0)
        car(carImg,x,y, crashCount)
        gas(tank,(display_width*.01),(display_height*.9))



        if pygame.time.get_ticks() - collision_time > 1000:
            collision_immune = False
        
        
        #things_dodged(dodged)
        speed(((thing_speed)*2)+52)
        #speed(thing_speed)
        total_score(score)
        multiplier(multi)
        #timer()
        

        if nextExit == 1:
            nextExitSoon()
        
        if bkgStarty < -display_height:
            bkgStarty = 0 
        
        if x > 910 - thing_width or x < 90:
            crash(score)


        if thing_starty > display_height:
            pygame.mixer.Sound.play(ding_sound)
            thing_starty = 0 - thing_height
            
            randomx = range(1,6)
            thing_startx = (random.choice(randomx)*150)+(random.choice(randomx)*3)-(random.choice(randomx)*3)
            dodged += 1

            randomCAR = random.choice(range(1,6))
            if randomCAR == 1:
                carImg2 = PINKcarImg
            if randomCAR == 2:
                carImg2 = REDcarImg
            if randomCAR == 3:
                carImg2 = GREENcarImg
            if randomCAR == 4:
                carImg2 = YELLOWcarImg
            if randomCAR == 5:
                carImg2 = BLUEcarImg
            
            score += (thing_speed*multi)

        if y < thing_starty+thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                if collision_immune == False:
                    crashCount += 1
                    pygame.mixer.Sound.play(crash_sound2)
                    collision_immune = True
                    collision_time = pygame.time.get_ticks()
                    if crashCount == 3:
                        crash(score)

                
        pygame.display.update()
        clock.tick(60)

game_intro()


###   To-Be Implemented
# 
# 
# 
# bonus points for 'Swerving'
# improved scoring system(score vs currency)
# ability to upgrade horizontal movement
# achievments
# MULTIPLAYER!!!
# 
###
