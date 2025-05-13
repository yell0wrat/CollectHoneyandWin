import pygame
from pygame.locals import *
from sys import exit
#Hello smee I will show you what I will be doing for the coding
#initalizing the game with pygane.init
pygame.init()
#im going to start off with a character class
#whenever you do a class, it is usually named with a capital letter
#whenever starting a class as well, you must make a "__init__" funciton
class Character:
    #you define the variables that are in () that aren't self
    def __init__(self, health: int, damage: int, speed: int):
        self.health=health
        #max health isn't in the vars but this is for future proofing
        self.health_max=health
        self.damage=damage
        self.speed = speed
#okay im also gonna show you about class inheritance
#to inhert class you do something like: "class [new class](old class):"
class Robot(Character):
    def __init__(self, health: int, damage: int, speed: int):
        super().__init__(health=health, damage=damage, speed=speed)
    #we use the super init method to take what we have from the original class
#im gonna do this again but with the enemy class (we can have more than 1 enemy but for now i wanna just make it general
class Enemy(Character):
    def __init__(self, health: int, damage: int, speed: int):
        super().__init__(health=health, damage=damage, speed=speed)
#there is way more to do but hopfully i did good in giving u a mini lesson on what youll be learning in the future
screen = pygame.display.set_mode((640,480),0,32)
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
