import pygame
#Hello smee I will show you what I will be doing for the coding
#im going to start off with a character class
#whenever you do a class, it is usually named with a capital letter
#whenever starting a class as well, you must make a "__init__" funciton
class Character:
    #you define the variables that are in () that aren't self
    def __init__(self, health: int, damage: int):
        self.health=health
        #max health isn't in the vars but this is for future proofing
        self.health_max=health
        self.damage=damage
#okay im also gonna show you about class inheritance
#to inhert class you do something like: "class [new class](old class):"
class Robot(Character):
    def __init__(self, health: int, damage: int):
        super().__init__(health=health, damage=damage)
    #we use the super init method to take what we have from the original class
#im gonna do this again but with the enemy class (we can have more than 1 enemy but for now i wanna just make it general
class Enemy(Character):
    def __init__(self, health: int, damage: int):
        super().__init__(health=health, damage=damage)
#there is way more to do but hopfully i did good in giving u a mini lesson on what youll be learning in the future

