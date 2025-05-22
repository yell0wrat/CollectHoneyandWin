from settings import *
from player import Player
from sprites import *
from random import randint
#initalizing the game with pygane.init
#whenever starting a class as well, you must make a "__init__" funciton
class Game:
    def __init__(self):
        #setup for the games
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('the lion does not concern itself with titles')
        #we use this as the framerate for the game
        self.clock = pygame.time.Clock()
        self.running = True
        #groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        #sprites
        self.player = Player((400,300), self.all_sprites,self.collision_sprites)
        for i in range(6):
            #these wont matter in the future, just testing
            x,y = randint(0,WINDOW_WIDTH), randint(0,WINDOW_HEIGHT)
            w,h = randint(50,90), randint(60,80)
            #adding it to 2 seperate sprites, player is in all sprites NOT in collision, but has access to it to detect collision
            CollisionSprite((x,y), (w,h), (self.all_sprites,self.collision_sprites))

    def run(self):
        while self.running:
            #delta time, makes the game not dependent on the FPS of the system
            dt = self.clock.tick() / 1000
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            #update, updates sprites
            self.all_sprites.update(dt)
            #draw, to "draw" is to make the images visible to the user
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        pygame.quit()
#we have to now call the game class in order for it to run
if __name__ == '__main__':
    game = Game()
    game.run()




#these are for characters that will get their own py file
class Character:
    #you define the variables that are in () that aren't self
    def __init__(self, health: int, damage: int, speed: int):
        self.health=health
        #max health isn't in the vars but this is for future proofing
        self.health_max=health
        self.damage=damage
        self.speed = speed

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
