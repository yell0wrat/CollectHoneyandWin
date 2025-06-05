from math import atan2, degrees
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
        self.distance = 30
        self.player_direction = pygame.Vector2(1,0)

        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('Robot','gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x,self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance


class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.direction = direction.normalize() if direction.length() > 0 else direction

        # like we did with the gun itself
        angle = degrees(atan2(self.direction.x, self.direction.y)) - 90
        if self.direction.x > 0:
            self.image = pygame.transform.rotozoom(self.original_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.original_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_frect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 2000
        self.speed = 50
        self.pos = pygame.Vector2(pos)  # For precise movement

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()