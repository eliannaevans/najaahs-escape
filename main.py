import pygame
from pygame.locals import *
import time
import datetime

pygame.init()

torchObtained = False
pause = 0.2
def intro():
    # musicWindow()
    x = 0
    while x <= 50:
        print('')
        x = x + 1


    '''backstory'''
    for char in 'Welcome to Najaah\'s Escape':
        print(char, end='')
        time.sleep(pause)
    print()
    for char in 'Press enter to continue...':
        print(char, end='')
        time.sleep(pause)
    input()
    print()
    for char in 'You are an imp that has been captured by beings of light':
        print(char, end='')
        time.sleep(pause)
    print()
    for char in 'Your name is Najaah "Cow Soup" Jo Supercalafragalisticexpialidocious':
        print(char, end='')
        time.sleep(pause)
    print()
    for char in 'You have been framed for selling illegal flowers':
        print(char, end='')
        time.sleep(pause)
    print()
    for char in 'You are now in the dungeon of the castle of the Light King':
        print(char, end='')
        time.sleep(pause)
    print()
    print()
    for char in 'Use the left and right arrow keys to move. To interact with doors or ladders, press the up arrow. Please press enter to continue, then switch windows.':
        print(char, end='')
        time.sleep(pause)

def dungeonScene():

    windowWidth = 1300
    windowHeight = 700
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    player = Player() #player
    wallLeft = Object(0,0, True, False, False, False, 1, 700, False)  # wall 1
    wallRight = Object(1300, 0, True, False, False, False, 1, 700, False)  # wall 2
    door = Object(500, 200, False, True, True, False, 130, 205, False)  # door
    torch = Object(740, 280, False, False, False, False, 50, 50, True, 'torch-blurry.png')  # lone torch
    cellWall = Object(825, 0, True, False, False, False, 1, 400, False)
    passageDoor = Object(1175, 314, False, True, False, False, 115, 75, False)  # passage door
    ladderWall = Object(85, 425, True, False, False, False, 1, 300, False)  # end of passage
    ladder = Object(88, 420, False, False, False, True, 1, 300, False)  # ladder
    ladderWall2 = Object(200, 420, True, False, False, False, 1,60, False)
    pygame.display.set_caption("Illegal Flowers")
    background = pygame.image.load('background2.2.png').convert()
    while (player.dead == False):
        pygame.mouse.set_visible(False)  # set mouse cursor visibility
        screen.blit(background, [0,0])  # draw background

        # walls
        #pygame.draw.rect(screen, (30, 0, 0), wallLeft.hitbox)
        #pygame.draw.rect(screen, (30, 0, 0), wallRight.hitbox)
        #pygame.draw.rect(screen, (30, 0, 0), cellWall.hitbox)
        #pygame.draw.rect(screen, (30, 0, 0), ladderWall.hitbox)
        #pygame.draw.rect(screen, (30, 0, 0), ladder.hitbox)
        #pygame.draw.rect(screen, (30, 0, 0), ladderWall2.hitbox)

        # door
        #pygame.draw.rect(screen, (0, 0, 50), door.hitbox)
        #pygame.draw.rect(screen, (30, 0, 0), passageDoor.hitbox)

        #torch
        torch.draw(screen)

        player.collideCheck(door)
        player.collideCheck(wallLeft)
        player.collideCheck(wallRight)
        player.collideCheck(torch)
        player.collideCheck(cellWall)
        player.collideCheck(passageDoor)
        player.collideCheck(ladderWall)
        player.collideCheck(ladder)
        player.collideCheck(ladderWall2)

        player.move()  # move player if appropriate
        player.draw(screen)  # draw player in correct position
        #pygame.draw.rect(screen, (128, 0, 128), player.hitbox)

        pygame.display.update()  # update screen

        # if the escape key is pressed, close screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    player.dead = True
    pygame.display.quit()
    return player.torchObtained

class Player(pygame.sprite.Sprite):
    #represents the player
    def __init__(self):
        # Sprite constructor
        super().__init__()

        # create the player's image
        self.imageR = pygame.image.load('Najaah-blurry-right.png').convert_alpha()
        self.imageL = pygame.image.load('Najaah-blurry-left.png').convert_alpha()

        self.x = 900
        self.y = 218

        self.torchObtained = False

        self.dist = 1  # can be changed to change the speed of the player

        self.dead = False
        self.rightQ = False
        self.collide = False

        self.hitbox = Rect((self.x, self.y), (100, 200))

        self.inventory = []

    def move(self):
        # allows player to move

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:  # left arrow
            self.rightQ = False
            self.x -= self.dist
            self.hitbox = self.hitbox.move(-self.dist, 0)
        elif key[pygame.K_RIGHT]:  # right arrow
            self.rightQ = True
            self.x += self.dist
            self.hitbox = self.hitbox.move(self.dist, 0)

    def draw(self, surface):
        #draws player

        if self.rightQ:
            surface.blit(self.imageR, (self.x, self.y))
        else:
            surface.blit(self.imageL, (self.x, self.y))

    def collideCheck(self, object):
        #checks for collisions

        if object.isWall:
            if self.hitbox.colliderect(object.hitbox):
                if self.rightQ:
                    self.x -= self.dist
                    self.hitbox = self.hitbox.move(-self.dist, 0)
                else:
                    self.x += self.dist
                    self.hitbox = self.hitbox.move(self.dist, 0)
        elif object.isDoor:
            if self.hitbox.colliderect(object.hitbox):
                key = pygame.key.get_pressed()
                if key[K_UP]:
                    if object.isFinalDoor:
                        self.dead = True
                    else:
                        self.y = 488
                        self.hitbox = self.hitbox.move(0, 270)
        elif object.isLadder:
            if self.hitbox.colliderect(object.hitbox):
                key = pygame.key.get_pressed()
                if key[K_UP]:
                    self.y -= 1
                    self.hitbox = self.hitbox.move(0, -1)
        else:
            if self.hitbox.colliderect(object.hitbox):
                self.torchObtained = True
                if object.delete == False:
                    self.addToInventory(object)
                    object.delete = True


    def addToInventory(self, item):
        # adds item to inventory

        self.inventory.append(item)


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, isWall, isDoor, isFinalDoor, isLadder, width, height, imageQ, imageName = None):
        # initializes an object
        super().__init__()

        self.isWall = isWall
        self.isDoor = isDoor
        self.isFinalDoor = isFinalDoor
        self.isLadder = isLadder
        self.x = x
        self.y = y
        self.delete = False
        self.height = height
        self.width = width
        self.hitbox = Rect((x, y), (width, height))

        if imageQ:
            self.image = pygame.image.load(imageName).convert_alpha()

    def draw(self, surface):
       #draws the object


       if self.delete == False:
           surface.blit(self.image, (self.x, self.y))


def firstDoor(torchObtained):
    print("Congratulations, you have reached the first door!")
    time.sleep(1)
    print("Items picked up in your flee:")
    time.sleep(.5)
    if torchObtained:
        print("You put a flaming torch in your pocket. Great idea.")
    else:
        print("You haven't picked up any items yet.")
    time.sleep(1)
    print("You pull at the door, but it refuses to budge")
    time.sleep(2)
    print("Suddenly, an inscription appears on the door!")
    time.sleep(.5)
    print("The inscription reads:")
    time.sleep(.5)
    print("esolc eht ta nepo I")
    for num in {1,1,1,1,1}:
        time.sleep(.3)
        print("...")
    time.sleep(.5)
    puzzleLoop = True
    while puzzleLoop:
        print('What do you do?')
        puzzleInput1 = input(">>> ")
        if "close" in puzzleInput1:
            puzzleLoop = False
        elif "hint" in puzzleInput1:
            print("Hint: backwards")
            time.sleep(1)
        else:
            print("Incorrect. Try Again. type \"hint\" for a hint")
            time.sleep(1)
    print("You have made it through!")
    time.sleep(1)
    print("However, you haven't escaped yet. Try to get to the next door")
    time.sleep(2)
    input("Press enter to continue...")


def credits():
    input("Press enter to continue...")
    print('')
    print("*****Credits******")
    time.sleep(.5)
    print("The Coder Who Is Always Correct: Anna Evans")
    time.sleep(1)
    print("The Coder Who Is Sometimes Correct: Nathan Broyles")
    time.sleep(1)
    print("The Esteemed Chief Of Design and Graphics: Emily Broyles")
    time.sleep(1)
    # print("Music Dude: Nathan Broyles")
    # time.sleep(2)
    print("Story Development By: Anna Evans, Emily Broyles, Nathan Broyles")
    time.sleep(1)
    print("Chief of Distractions: Anna Evans")
    time.sleep(.5)
    print("Chief Of Supposed Awesomeness: Nathan Broyles")
    time.sleep(1)
    print("Captain of Rationality: Emily Broyles")
    time.sleep(3.14)
    print("Developers: Emily Broyles, Anna Evans, Nathan Broyles")
    time.sleep(3.14)
    print("*****")
    time.sleep(.5)
    print("Thank you for playing Najaah's Escape!")
    time.sleep(.5)
    print("*****")
    time.sleep(4)
    input("Press enter to exit >>>")


# def musicWindow():
#     screen = pygame.display.set_mode((5, 5))
#     pygame.mixer.init()
#     pygame.mixer.music.load("tiptoe8bitMP3.mp3")
#     pygame.mixer.music.play(-1, 0.0)


def command():
    return input('>>> ')


def nextPuzzle(torchObtained):
    path = 0
    while path == 0:

        print('You are now in the hallway.')
        time.sleep(1)
        print('You walk into a room. There is a guard with their back turned to you, a table with a bottle of some liquid you can\'t make out, a pile of hay in to corner, and a doorway past the guard. What would you like to do?')
        time.sleep(0.72)
        print('A: Talk to the guard nicely and ask them to not stab you')
        time.sleep(0.72)
        print('B: Fight guard')
        if torchObtained:
            time.sleep(0.72)
            print('C: Throw torch at pile of hay')
        time.sleep(1)
        choice = command()
        time.sleep(0.72)
        if torchObtained:
            if choice.lower() == 'c':
                path = 3
                print('You throw the torch at the pile of hay and distract the guard. You run past and get to the next door.')
                return path
        if choice.lower() == 'a':
            path = 1
            print('the guard stabs you and you die a horrible death')
            return path
        elif choice.lower() == 'b':
            path = 2
            print('You run at the guard and try to strangle them from behind, but the guard turns just as you get to them')
            time.sleep(1.25)
            print('You decide to make a break for it. As you run away, the guard swings their sword at you and just grazes you. ')
            time.sleep(1.25)
            print('When you look back, you realize your wings are gone. You make it to the next door, but the guard is just behind you.')
            time.sleep(1.25)
            print('You have 1 minute to solve the next puzzle')
            return path
        else:
            print('The rest of the alphabet is not authorized.')


def addSecs(tm, secs):
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()


def finalPuzzle(chosenPath):
    time.sleep(1)
    print('You come across a drawbridge, but the trunnion (the spinny turny thing that lowers the drawbridge) is stuck')
    time.sleep(4)
    print('you see the letters:')
    print('tqfbl gsjfoe boe foufs')
    if chosenPath == 2:
        time.sleep(0.72)
        print('You have 1 minute to solve the puzzle before the guard catches up to you. Type in your answer. After a minute, you will either live or die.')
        time.sleep(.5)
        print('(Oh, and no hints for you. They take too long.)')
        a = datetime.datetime.now().time()
        b = addSecs(a, 60000)
        userInput = input('>>> ')
        if b <= datetime.datetime.now().time():
            if userInput.lower() == 'friend':
                return True
        else:
          print('You have failed. The guard catches up to you, and promptly dismembers you. You have died a painful death.')
    elif chosenPath == 3:
        answered = False
        while not answered:
            userInput = input('>>> ')
            if userInput.lower() == 'hint':
                print("Caesar shift (1 to the right)")
            elif userInput.lower() == 'friend':
                answered = True
                notDead = True
                return notDead

    elif chosenPath == 1:
        print('')
    else:
        print('I don\'t know how, but you seem to have broken the game. please consult the administrators of life to have your soul deleted.')


wings = True
intro()
torchObtained = dungeonScene()
firstDoor(torchObtained)
path = nextPuzzle(torchObtained)
death = False

if path == 1:
    death = True
elif path == 2:
    wings = False
elif path == 3:
    wings = True
if not death:
    if finalPuzzle(path) == True:
        if wings == True:
            print('You have escaped the castle and can go back to your normal flower dealing life.')
        else:
            print('You have escaped the castle, but you no longer have your wings. You go on to live a life of sorrow and depression')
        time.sleep(1)
else:
    print('GAME OVER')

credits()
quit('the end')
