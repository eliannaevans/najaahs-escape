import pygame
from pygame.locals import *
import os

pygame.init()

def main():

    windowWidth = 1300
    windowHeight = 700
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    player = Player()
    pygame.display.set_caption("Illegal Flowers")
    background = pygame.image.load('backgroundPlaceholderTest2.bmp').convert()
    while (player.dead == False):
        pygame.mouse.set_visible(False) #set mouse cursor visibility
        screen.blit(background, [0,0]) #draw background
        player.move() #move player if appropriate
        player.draw(screen) #draw player in correct position
        pygame.draw.rect(screen, (128, 0, 128), player.hitbox)
        pygame.display.update() #update screen

        #if the escape key is pressed, close screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player.dead = True

class Player(pygame.sprite.Sprite):
    #represents the player
    def __init__(self):
        #Sprite constructor
        super().__init__()

        #create the player's image
        self.image = pygame.image.load('player1.0.bmp').convert()
        #self.image = pygame.image.load('~/Downloads/CodeDayImages/finalImages/Najaah-blurry-right.png').convert()

        self.x = 50
        self.y = 40

        self.dead = False

        self.hitbox = Rect((self.x, self.y), (64, 128))

    def move(self):
        #allows player to move

        key = pygame.key.get_pressed()
        dist = 1 #can be changed to change the speed of the player
        if key[pygame.K_LEFT]: #left arrow
            self.x -= dist
            self.hitbox = self.hitbox.move(-dist, 0)
        elif key[pygame.K_RIGHT]: #right arrow
            self.x += dist
            self.hitbox = self.hitbox.move(dist, 0)

    def draw(self, surface):
        #draws player

        surface.blit(self.image, (self.x, self.y))

main()
