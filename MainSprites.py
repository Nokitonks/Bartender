import pygame
#This file contains all the sprites for the main pygame game

#Change this to the path to your images folder
images = "/Users/stefan/Desktop/GIMP/"
#These are our sprite groups
Drinks = pygame.sprite.Group()
allSprites = pygame.sprite.Group()
Checks = pygame.sprite.Group()
Coasters = pygame.sprite.Group()
bars = pygame.sprite.Group()

#Drinks class that is a parent class for all 3 types of drinks
class Drink(pygame.sprite.Sprite):
    def __init__(self,filledAmount=0,capacity=100):
        super().__init__(Drinks,allSprites)
        self.filledAmount = filledAmount
        self.capacity = capacity

    def fill(self,amount):
        self.filledAmount+= amount

#NEED TO CHANGE THE PATH TO THE IMAGES HERE
class Martini(Drink):
    type = "Martini"
    def __init__(self,location,filledAmount):
        super().__init__(filledAmount)
        self.image = pygame.image.load(images + "Martini.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = location

class Cosmo(Drink):
    type = "Cosmo"
    def __init__(self,location,filledAmount):
        super().__init__(filledAmount)
        self.image = pygame.image.load(images + "Cosmo.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = location

class TequilaSunrise(Drink):
    type = "TequilaSunrise"
    def __init__(self,location,filledAmount):
        super().__init__(filledAmount)
        self.image = pygame.image.load(images + "TequilaSunrise.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = location

#AGAIN CHANGE PATH TO IMAGE
class Highlight(pygame.sprite.Sprite):

    def __init__(self,position):
        super().__init__(allSprites)
        self.position = position
        self.image = pygame.image.load(images + "Highlight.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = [50,50]

    def setLocation(self,coaster):
        self.rect.midbottom = coaster.location

#CHANGE IMAGE PATH
class Coaster(pygame.sprite.Sprite):

    def __init__(self,location,position):
        super().__init__(allSprites,Coasters)
        self.location = location
        self.image = pygame.image.load(images + "Coaster.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = location
        self.full = False
        self.drink = None
        self.position = position
        self.filledBar = None

#This is bar that represents how filled a drink on a coaster is
class filledBar(pygame.sprite.Sprite):

    height = 15

    #Changes width based on amount
    def __init__(self,location,amount):
        super().__init__(allSprites,bars)
        self.amount = amount
        self.image = pygame.Surface([self.amount, self.height])
        self.image.fill([255, 0, 20])
        self.rect = self.image.get_rect()
        self.rect.midleft = [location[0] - 25,location[1]]
        self.location = location

    #Checks to see if amount has changes and so changes its rect
    def update(self):

        self.image = pygame.Surface([self.amount, self.height])
        self.image.fill([255, 0, 20])
        self.rect = self.image.get_rect()
        self.rect.midleft = [self.location[0] - 25,self.location[1]]



#DONT FORGET TO CHANGE IMAGE PATHS
class Check(pygame.sprite.Sprite):


    def __init__(self,location,home,position,type="Martini"):
        super().__init__(allSprites,Checks)
        self.location = location
        if type =="Martini":
            self.image = pygame.image.load(images + "MartiniCheck.png")
        if type == "TequilaSunrise":
            self.image = pygame.image.load(images + "TequilaSunriseCheck.png")
        if type == "Cosmo":
            self.image = pygame.image.load(images + "CosmoCheck.png")
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.home = home
        self.position = position





