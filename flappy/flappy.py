import pygame, led, sys, os, random, csv
from pygame.locals import *
from bmpfont import bmpfont

""" A flappy bird clone
"""

random.seed()

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

wing1font = bmpfont.BmpFont("bmpfont/wing2-3x3px-white.idx")

# detect if a serial/USB port is given as argument
hasSerialPortParameter = ( sys.argv.__len__() > 1 )

# use 90 x 20 matrix when no usb port for real display provided
fallbackSize = ( 90, 20 )

if hasSerialPortParameter:
    serialPort = sys.argv[ 1 ]
    print "INITIALIZING WITH USB-PORT: "+serialPort
    ledDisplay = led.teensy.TeensyDisplay( serialPort, fallbackSize )
else:
    print "INITIALIZING WITH SIMULATOR ONLY."
    ledDisplay = led.teensy.TeensyDisplay( None, fallbackSize )

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
    def __init__(self, top=False):
        super(Pipe, self).__init__()
        self.image = pygame.image.load("Sprites/pipe.png").convert_alpha()
        if top:
            self.image = pygame.transform.flip(self.image,False,True)
        self.rect = self.image.get_rect()
        self.passed = False

    def setPos(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.centerx -= 1
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
level = 1
LevelDesc = []
LevelDesc.append([(99, 25), (99, -6)])
LevelDesc.append([(99, 25), (99, -6), (140, 23), (140, -8)])

def resetGame():
    global pipes
    global level
    flappy.setPos(10,10)
    level = 1
    pipes = []
    # for pipe in pipes:
    #     del pipe

    addPipes()
    # pipes[0].setPos(45,25)
    # pipes[1].setPos(45,-6)

def LevelPassed(lvl):
    global pipes
    print lvl
    passedPipes = 0
    for pipe in pipes:
        if pipe.isPassed():
            passedPipes += 1
            print passedPipes
            if (passedPipes / 2) >= lvl:
                return True
    return False

def addPipes():
    global pipes
    global level

    print pipes

    pipes.append(Pipe(False))
    pipes.append(Pipe(True))

    # if level == 2:
    i = 0
    for pipe in pipes:
        # print level
        pipe.setPos(LevelDesc[level-1][i][0],LevelDesc[level-1][i][1])
        i += 1

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    global gamestate
    global pipes
    global level

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
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    pass
                elif event.key == K_DOWN:
                    pass
                elif event.key == K_LEFT:
                    pass
                elif event.key == K_RIGHT:
                    pass
                elif event.key == K_SPACE:
                    if gamestate == 0:
                        gamestate = 1
                        scored = False
                    else:
                        flappy.flap()

            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    pass

        if gamestate == 1:
            screen.fill(BLACK)

            backgroundgroup.draw(screen)
            groundgroup.draw(screen)

            pipegroup.update()
            pipegroup.draw(screen)

            flappygroup.update()
            flappygroup.draw(screen)

            wing1font.blit("Flappy",screen)

            # if pygame.sprite.spritecollideany(flappy, pipegroup) == None and pygame.sprite.spritecollideany(flappy, groundgroup) == None :
            if pygame.sprite.spritecollideany(flappy, groundgroup) == None :
                print pipes
                if LevelPassed(level):
                    wing1font.blit("Level passed",screen, (30,0))
                    level += 1
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
