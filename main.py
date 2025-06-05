from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
#from random import randint probably not needed anymore

# initalizing the game with pygane.init
# whenever starting a class as well, you must make a "__init__" funciton
class Game:
    def __init__(self):
        # setup for the games
        pygame.init()
        #made the game borderless, which speeds up loading into the game when compared to only doing fullscreen function
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
        pygame.display.set_caption('the lion does not concern itself with titles')
        # we use this as the framerate for the game
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_images()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.setup()

        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 150
        #font name
        self.font = pygame.font.SysFont('Corbel', 35)
        self.main_menu()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('Robot', 'bolt 3.png')).convert_alpha()


    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 30
            Bullet(self.bullet_surf, pos, self.gun.player_direction , (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
        elif pygame.mouse.get_pressed()[2]:
            print('slash')

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def main_menu(self):
            pygame.mixer.music.load('Music/Ambulance.mp3')
            pygame.mixer.music.set_volume(.5)
            pygame.mixer.music.play(-1)
            quit_text = self.font.render('Quit', True, 'white')
            start_text = self.font.render('Start', True, 'white')
            menu_active = True

            while menu_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return False  # false to indicate quitting

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        # start button click (top button)
                        if (WINDOW_WIDTH / 2 - 70 <= mouse[0] <= WINDOW_WIDTH / 2 + 70 and
                                WINDOW_HEIGHT / 2 - 50 <= mouse[1] <= WINDOW_HEIGHT / 2 - 10):
                            menu_active = False  # Exit menu
                            pygame.mixer.music.fadeout(500)
                            pygame.mixer.music.load('Music/RNB_song.mp3')
                            pygame.mixer.music.set_volume(0.1)
                            pygame.mixer.music.play(-1)

                            return True  # true to indicate starting game

                        # quit button click (bottom button)
                        elif (WINDOW_WIDTH / 2 - 70 <= mouse[0] <= WINDOW_WIDTH / 2 + 70 and
                              WINDOW_HEIGHT / 2 + 10 <= mouse[1] <= WINDOW_HEIGHT / 2 + 50):
                            pygame.quit()
                            return False  # false to indicate quitting

                # drawing
                self.display_surface.fill((254, 172, 40))
                mouse = pygame.mouse.get_pos()

                # drawing the start button
                start_color = 'light grey' if (WINDOW_WIDTH / 2 - 70 <= mouse[0] <= WINDOW_WIDTH / 2 + 70 and
                                               WINDOW_HEIGHT / 2 - 50 <= mouse[1] <= WINDOW_HEIGHT / 2 - 10) else 'grey'
                pygame.draw.rect(self.display_surface, start_color,
                                 [WINDOW_WIDTH / 2 - 70, WINDOW_HEIGHT / 2 - 50, 140, 40])

                # drawing the quit button
                quit_color = 'light grey' if (WINDOW_WIDTH / 2 - 70 <= mouse[0] <= WINDOW_WIDTH / 2 + 70 and
                                              WINDOW_HEIGHT / 2 + 10 <= mouse[1] <= WINDOW_HEIGHT / 2 + 50) else 'grey'
                pygame.draw.rect(self.display_surface, quit_color,
                                 [WINDOW_WIDTH / 2 - 70, WINDOW_HEIGHT / 2 + 10, 140, 40])

                # adds text to buttons
                self.display_surface.blit(start_text, (WINDOW_WIDTH / 2 - 35, WINDOW_HEIGHT / 2 - 40))
                self.display_surface.blit(quit_text, (WINDOW_WIDTH / 2 - 35, WINDOW_HEIGHT / 2 + 20))

                pygame.display.update()
            return True

    def setup(self):
        # loading in the map layer by layer, starting from 1 to x layer
        map = load_pygame(join('Data','untitled.tmx'))

        # layers with no collisions use .tiles and Sprite class
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)

        for x, y, image in map.get_layer_by_name('Elevated').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)

        for x, y, image in map.get_layer_by_name('No collisions').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)

        for x, y, image in map.get_layer_by_name('Shadow').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)

        for x, y, image in map.get_layer_by_name('Water foam').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        # layers with collisions use for obj and CollisionSprite class
        for obj in map.get_layer_by_name('Collisions'):
             CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        # this spawns player at the coords at layer
        for obj in map.get_layer_by_name('Player spawn'):
            self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            self.gun = Gun(self.player, self.all_sprites)



        #for obj in map.get_layer_by_name('Enemy spawn'):

    def run(self):
        while self.running:
            # delta time, makes the game not dependent on the FPS of the system
            dt = self.clock.tick() / 1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # update, updates sprites
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            # draw, to "draw" is to make the images visible to the user
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            self.player.draw_health_bar(self.display_surface)

            pygame.display.update()
        pygame.quit()
# we have to now call the game class in order for it to run
if __name__ == '__main__':
    game = Game()
    game.run()