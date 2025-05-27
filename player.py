from settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'Up', 0
        self.image = pygame.image.load(join('Robot','Down','0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        # this makes the hitbox smaller. it less empty space for the player to be hit by
        self.hitbox_rect = self.rect.inflate(-40,-42)
        # movement
        self.direction = pygame.Vector2(0,0)
        self.max_health = 100 # may change later i dont know
        self.current_health = self.max_health
        self.speed = 400
        self.collision_sprites = collision_sprites
    # no eniemes in game but this is future proofing
    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def is_alive(self):
        return self.current_health > 0

    def draw_health_bar(self, surface):
        bar_width, bar_height = 200, 20
        pos_x, pos_y = 10, 10  # 10 px from top-left corner

        # current health percentage
        health_ratio = self.current_health / self.max_health
        fill_width = int(bar_width * health_ratio)

        # background of health bar (lost hp)
        pygame.draw.rect(surface, (40, 40, 40), (pos_x, pos_y, bar_width, bar_height))
        # current hp
        pygame.draw.rect(surface, (254, 172, 40), (pos_x, pos_y, fill_width, bar_height))
        #border of health bar
        pygame.draw.rect(surface, (255, 255, 255), (pos_x, pos_y, bar_width, bar_height), 2)

        # text for the health
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"Health: {int(self.current_health)}/{self.max_health}", True, (255, 255, 255))
        surface.blit(health_text, (pos_x + 10, pos_y + 2))

    def load_images(self):
        self.frames ={'Left':[], 'Down':[], 'Right':[],'Up':[] }
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('Robot',state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)


    def input(self):
        keys = pygame.key.get_pressed()
        # using pygame-ce, NOT regular pygame, you wont get the weird bug of slow movement for left and up
        self.direction.x = int(keys[pygame.K_d] - int(keys[pygame.K_a]))
        self.direction.y = int(keys[pygame.K_s] - int(keys[pygame.K_w]))
        # diagonal speeds are faster, this line makes it normal and checks if there is direction move than 0
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

    def animate(self, dt):
        # get state
        if self.direction.x != 0:
            self.state = 'Right' if self.direction.x > 0 else 'Left'
        if self.direction.y != 0:
            self.state = 'Down' if self.direction.y > 0 else 'Up'

        # animation
        # this the animation only happen when input occurs, index of the animation will be 0 unless there is input
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        # looking for the walking direction state of the animation,
        # where we get the remainder of frame_index and self frames and its state to make the animation occur
        # if u dont get the remainder the program will fucking crash bc u cant get .5 of a frame
        # this makes the animation look rather smooth for having only 4 frames of walking
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)

