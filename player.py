from settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('Smaller Robot.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        #this makes the hitbox smaller. it less empty space for the player to be hit by
        self.hitbox_rect = self.rect.inflate(-40,-42)
        #movement
        self.direction = pygame.Vector2(0,0)
        self.speed = 500
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        #using pygame-ce, NOT regular pygame, you wont get the weird bug of slow movement for left and up
        #@smee use pycharm terminal to install pygame-ce "pip install pygame-ce"
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        #diagonal speeds are faster, this line makes it normal and checks if there is direction move than 0
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center=self.hitbox_rect.center

    def collision(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    # > 0 = movement to right, < 0 = movement to left. we move the player back to the side theyre trying to run through
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    # > 0 = movement up, < 0 = movement down. we move the player back to the side theyre trying to run through
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top


    def update(self,dt):
        self.input()
        self.move(dt)

