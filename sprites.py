import pygame.sprite

from settings import *
# made so the ground layer does not do collision with the player
class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.ground = True
# this is for any object that should have collision
class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(center=pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # connect player
        self.player = player
        self.distance = 100
        self.player_direction = pygame.Vector2(1,0)

        super().__init__(groups)
        self.gun_surf = pygame.image.load(join())
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)
