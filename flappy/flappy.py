import pygame, led, sys, os, random, csv
from pygame.locals import *
from bmpfont import bmpfont
from led.PixelEventHandler import *

""" A flappy bird clone
"""

random.seed()

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

wing1font = bmpfont.BmpFont("bmpfont/wing1-5x5px-white.idx")

# detect if a serial/USB port is given as argument
hasSerialPortParameter = ( sys.argv.__len__() > 1 )

# use 90 x 20 matrix when no usb port for real display provided
fallbackSize = ( 90, 20 )

if hasSerialPortParameter:
    serialport = sys.argv[ 1 ]
    print "INITIALIZING WITH USB-PORT: "+serialport
    ledDisplay = led.dsclient.DisplayServerClientDisplay(serialport, 8123)
else:
    print "INITIALIZING WITH SIMULATOR ONLY."
    ledDisplay = led.dsclient.DisplayServerClientDisplay("localhost", 8123)

# use same size for sim and real LED panel
size = ledDisplay.size()
simDisplay = led.sim.SimDisplay(size)
screen = pygame.Surface(size)
gamestate = 1 #1=alive; 0=dead

class Flappy(pygame.sprite.Sprite):
    def __init__(self):
        super(Flappy, self).__init__()
        self.image = pygame.image.load("Sprites/flappy3.png").convert_alpha()
        self.rect = self.image.get_rect()

    def setPos(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.centery += 1

    def flap(self):
        self.rect.centery -= 3

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.image.load("Sprites/flappybackground.png").convert()
        self.rect = self.image.get_rect()

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super(Ground, self).__init__()
        self.image = pygame.Surface([90,1])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = 20

class Pipe(pygame.sprite.Sprite):
    def __init__(self, top=False, speed=1):
        super(Pipe, self).__init__()
        self.image = pygame.image.load("Sprites/pipe.png").convert_alpha()
        if top:
            self.image = pygame.transform.flip(self.image,False,True)
        self.rect = self.image.get_rect()
        self.passed = False
        self.speed = speed

    def setPos(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.centerx -= self.speed
        if self.rect.centerx < -9:
            self.passed = True
        else:
            self.passed = False
        #     self.rect.centerx = 99

    def isPassed(self):
        return self.passed

flappy = Flappy()
background = Background()
ground = Ground()
# pipebottom1 = Pipe(False)
# pipetop1 = Pipe(True)
# pipes = [pipebottom1, pipetop1]
pipes = []
baselevel = 1
level = baselevel
stage = 1
LevelDesc = []
LevelDesc.append([(98, 25), (98, -6)])
LevelDesc.append([(98, 25), (98, -6), (138, 23), (138, -8)])
LevelDesc.append([(98, 23), (98, -8), (128, 25), (128, -6), (158, 27), (158, -4)])
LevelDesc.append([(98, 24), (98, -7), (118, 25), (118, -6), (138, 24), (138, -7), (158, 23), (158, -8)])

def resetGame():
    global pipes
    global level
    flappy.setPos(10,10)
    level = baselevel
    pipes = []
    # for pipe in pipes:
    #     del pipe

    for i in range(baselevel):
        addPipes()
    # pipes[0].setPos(45,25)
    # pipes[1].setPos(45,-6)

def LevelPassed(lvl):
    global pipes
    # print lvl
    passedPipes = 0
    for pipe in pipes:
        if pipe.isPassed():
            passedPipes += 1
            # print passedPipes
            if (passedPipes / 2) >= lvl:
                return True
    return False

def addPipes():
    global pipes
    global level

    print pipes

    pipes.append(Pipe(False,stage))
    pipes.append(Pipe(True,stage))

    # if level == 2:
    i = 0
    for pipe in pipes:
        # print level
        pipe.setPos(LevelDesc[level-1][i][0],LevelDesc[level-1][i][1])
        i += 1

def main():
    pygame.init()
    pygame.joystick.init()
    # Initialize first joystick
    if pygame.joystick.get_count() > 0:
        stick = pygame.joystick.Joystick(0)
        stick.init()
    clock = pygame.time.Clock()
    
    global gamestate
    global pipes
    global level
    global stage

    scored = False

    resetGame()

    flappygroup = pygame.sprite.Group()
    backgroundgroup = pygame.sprite.Group()
    groundgroup = pygame.sprite.Group()
    pipegroup = pygame.sprite.Group()

    for pipe in pipes:
        pipegroup.add(pipe)

    flappygroup.add(flappy)
    # flappygroup.add(pipegroup.sprites())

    backgroundgroup.add(background)
    groundgroup.add(ground)

    while True:
        for pgevent in pygame.event.get():
            event = process_event(pgevent)
            # if event.type == QUIT:
            #     pygame.quit()
            #     sys.exit()

            if event.type == PUSH:
                if event.button == UP:
                    if gamestate == 0:
                        gamestate = 1
                        scored = False
                    else:
                        flappy.flap()
                elif event.button == DOWN:
                    pass
                elif event.button == LEFT:
                    pass
                elif event.button == RIGHT:
                    pass
                elif event.button == B1:
                    if gamestate == 0:
                        gamestate = 1
                        scored = False
                    else:
                        flappy.flap()
                elif event.button == P1:
                    pygame.quit()
                    sys.exit()

        if gamestate == 1:
            screen.fill(BLACK)

            backgroundgroup.draw(screen)
            groundgroup.draw(screen)

            pipegroup.update()
            pipegroup.draw(screen)

            flappygroup.update()
            flappygroup.draw(screen)

            text = ""
            text += "Stage "
            text += str(stage)
            text += " Level "
            text += str(level)
            wing1font.blit(text,screen)

            if pygame.sprite.spritecollideany(flappy, pipegroup) == None and pygame.sprite.spritecollideany(flappy, groundgroup) == None :
            # if pygame.sprite.spritecollideany(flappy, groundgroup) == None :
                # print pipes
                if LevelPassed(level):
                    wing1font.blit("Level passed",screen, (30,0))
                    level += 1
                    if level > len(LevelDesc):
                        stage += 1
                        pipegroup.empty()
                        resetGame()
                        for pipe in pipes:
                            pipegroup.add(pipe)
                        continue
                    addPipes()
                    for pipe in pipes:
                        pipegroup.add(pipe)
                    
            else:
                pipegroup.empty()
                resetGame()
                for pipe in pipes:
                    pipegroup.add(pipe)
                gamestate = 0
        else:
            pass

        simDisplay.update(screen)
        ledDisplay.update(screen)

        clock.tick(10)

main()
