import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
    def __init__(self, xPos, yPos, wid, hei, im):
        self.x = xPos
        self.y = yPos
        self.w = wid
        self.h = hei
        self.image = pygame.image.load(im)
        self.vertFlip = False
        self.horzFlip = False
        self.vert_velocity = 1.2
        self.previousX = 0
        self.previousY = 0
    
    def isMario(self):
        return False
    def isPipe(self):
        return False
    def isGoomba(self):
        return False
    def isFireball(self):
        return False
    def isGround(self):
        return False   
    def update(self):
        return

class Mario(Sprite):
    def __init__(self):
        super().__init__(0,0,60,95,"mario1.png")
        self.numFramesInAir = 0
        self.marioImages = []
        self.marioImages.append(pygame.image.load("mario1.png"))
        self.marioImages.append(pygame.image.load("mario2.png"))
        self.marioImages.append(pygame.image.load("mario3.png"))
        self.marioImages.append(pygame.image.load("mario4.png"))
        self.marioImages.append(pygame.image.load("mario5.png"))
        self.imageNum = 0

    def previousPosition(self):
        self.previousX = self.x
        self.previousY = self.y
    
    def updateImageNum(self):
        self.imageNum += 1
        if self.imageNum >= len(self.marioImages):
            self.imageNum = 0
        self.image = self.marioImages[self.imageNum]
    
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.marioImages[self.imageNum], self.
        horzFlip, self.vertFlip), (self.x, self.y))
        
    def moveMario(self, newX, newY):
        self.x = self.x + newX
        self.y = self.y + newY
    
    def update(self):
        self.numFramesInAir += 1
        self.vert_velocity += 9.8
        self.y += self.vert_velocity
        
        if self.y > 575 - self.h:
            self.vert_velocity = 0
            self.y = 575 - self.h
            self.numFramesInAir = 0

        
    def isMario(self):
        return True
    
class Pipe(Sprite):
    def __init__(self, xPos, yPos):
        super().__init__(xPos, yPos, 55, 400, "pipe.png")
        
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.horzFlip,
        self.vertFlip), (self.x, self.y))
        
    def isPipe(self):
        return True

class Goomba(Sprite):
    def __init__(self, xPos, yPos):
        super().__init__(xPos, yPos, 37, 45, "goomba1.png")
        self.image = pygame.transform.scale(self.image, (37, 45))
        self.speed = 4
        self.direction = 1
        self.burn = False
        self.numFrames = 0
        
    def previousPosition(self):
        self.previousX = self.x
        self.previousY = self.y
            
    def isGoomba(self):
        return True
    
    def updateImage(self):
        self.image = pygame.image.load("goomba2.png")
        
    def update(self):
        self.previousPosition()
        #self.x += 1
        self.vert_velocity += 9.8
        self.y += self.vert_velocity
        self.x += self.speed * self.direction
        
        if self.y > 575 - self.h:
            self.y = 575 - self.h
            self.vert_velocity = 0
        
        if self.burn == True:
            self.speed = 0
            self.numFrames += 1
    
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.horzFlip,
        self.vertFlip), (self.x, self.y))

class Ground(Sprite):
    def __init__(self, xPos, yPos):
        super().__init__(xPos, yPos, 360, 27, "ground.png")
    
    def isGround(self):
        return True
    
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.horzFlip,
        self.vertFlip), (self.x, self.y))

class Fireball(Sprite):
    def __init__(self, xPos, yPos):
        super().__init__(xPos, yPos, 47, 47, "fireball.png")
        self.speed = 10
        self.direction = 1
        self.numFramesActive = 0
        
    def previousPosition(self):
        self.previousX = self.x
        self.previousY = self.y 
        
    def update(self):
        self.numFramesActive += 1
        self.previousPosition()
        self.vert_velocity += 9.8
        self.y += self.vert_velocity
        self.x += self.speed * self.direction
        
        if self.y > 575 - self.h:
            self.y = 575 - self.h
            self.vert_velocity = -60
    
    def isFireball(self):
        return True
    
    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.horzFlip,
        self.vertFlip), (self.x, self.y))
                       
class Model():
    def __init__(self):
        self.mario = Mario()
        self.sprites = []
        self.pipe1 = Pipe(200,350)
        self.pipe2 = Pipe(400,500)
        self.sprites.append(self.mario)
        self.sprites.append(self.pipe1)
        self.sprites.append(self.pipe2)
        self.sprites.append(Pipe(550,400))
        self.sprites.append(Goomba(300,0))
        self.sprites.append(Goomba(250,0))
        self.sprites.append(Goomba(475,0))
        self.sprites.append(Ground(0,575))
        self.sprites.append(Ground(360,575))
        self.sprites.append(Ground(720,575))
        
    def collisionCheck(self, spriteA, spriteB):
        if spriteA.x + spriteA.w < spriteB.x:
            return False
        if spriteA.x >= spriteB.x + spriteB.w:
            return False
        if spriteA.y + spriteA.h <= spriteB.y:
            return False
        if spriteA.y >= spriteB.y + spriteB.h:
            return False
        return True
    
    def spriteCollision(self, spriteA, spriteB):
        if spriteA.y + spriteA.h >= spriteB.y and spriteA.previousY + spriteA.h <= spriteB.y:
            spriteA.y = spriteB.y - spriteA.h
            if spriteA.isMario():
                self.mario.vert_velocity = 0
                self.mario.numFramesInAir = 0
                return
            return
        if spriteA.y <= spriteB.y + spriteB.h and spriteA.previousY >= spriteB.y + spriteB.h:
            spriteA.y = spriteB.y + spriteB.h
            return
        if spriteA.previousX + spriteA.w <= spriteB.x + spriteB.w and spriteA.x + spriteA.w >= spriteB.x:
            spriteA.x = spriteB.x - spriteA.w
            if spriteA.isGoomba():
                spriteA.direction *= -1
        if spriteA.previousX >= spriteB.x + spriteB.w and spriteA.x <= spriteB.x + spriteB.w:
            spriteA.x = spriteB.x + spriteB.w
            if spriteA.isGoomba():
                spriteA.direction *= -1

    def update(self):
        for i in self.sprites:
            i.update()
            if i.isGoomba():
                for j in self.sprites:
                    if j.isPipe():
                        if self.collisionCheck(i, j): #Goomba Pipe Collision
                            self.spriteCollision(i, j)
       
            if i.isFireball():
                if i.numFramesActive > 70: # Remove fireball after a certain amount of time
                    self.sprites.remove(i)
                for j in self.sprites:
                    if j.isGoomba():
                        self.check = self.collisionCheck(i, j) #Fireball Goomba Collision
                        if self.check:
                            j.burn = True
                            j.updateImage()
                        if j.numFrames > 30:
                            self.sprites.remove(j) # Remove goomba after 30 frame counts
                        
       
            for j in self.sprites:
                if j.isPipe():
                    if self.collisionCheck(self.mario, j):
                        self.spriteCollision(self.mario, j) # Mario Pipe Collision
    
    def shootFireball(self, ballX, ballY):
        self.fireball = Fireball(ballX, ballY)
        self.sprites.append(self.fireball)
        
        
    
class View():
    def __init__(self, model):
        screen_size = (800,600)
        self.screen = pygame.display.set_mode(screen_size, 32)
        self.mario_image = pygame.image.load("mario1.png")
        self.model = model

    def update(self):    
        self.screen.fill([0,200,100])
        for sprite in self.model.sprites:
            sprite.draw(self.screen)
        pygame.display.flip()

class Controller():
    def __init__(self, model):
        self.model = model
        self.keep_going = True

    def update(self):
        self.model.mario.previousPosition()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = False
            elif event.type == pygame.KEYUP:
                if event.key == K_LCTRL:
                    self.model.shootFireball(self.model.mario.x, self.model.mario.y)  
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.model.mario.x -= 10
            self.model.mario.horzFlip = True
            self.model.mario.updateImageNum()
        if keys[K_RIGHT]:
            self.model.mario.x += 10
            self.model.mario.horzFlip = False
            self.model.mario.updateImageNum()
        if keys[K_SPACE]:
            if self.model.mario.numFramesInAir < 4:
                self.model.mario.y -= 100   
       
print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye")