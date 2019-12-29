import pygame
import sys, os
from itertools import cycle
from glob import glob


class Player:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.load_sounds()
        self.load_images()
        self.state = 'idle'
        self.image = None
        self.controls = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
        self.time_point = pygame.time.get_ticks()

    def load_images(self):
        def load_helper(*filenames):
            images = [pygame.image.load(filename).convert_alpha() for filename in filenames]
            return cycle(images)

        self.images = {
            'idle': load_helper('idle.png'),
            'moving': load_helper(*glob('move_*.png'))
        }

    def load_sounds(self, volume=0.25):
        # TODO: fix the crackling sound
        def load_helper(filename):
            audio_file = pygame.mixer.Sound(filename)
            audio_file.set_volume(volume)
            return audio_file

        self.walk_sound = load_helper('walk.wav')
        self.jump_sound = load_helper('jump.wav')

    def draw(self, surf):
        if self.state == 'idle':
            self.image = next(self.images['idle'])
            
        if self.state == 'moving':
            if pygame.time.get_ticks() - self.time_point > 200:
                self.image = next(self.images['moving'])
                self.time_point = pygame.time.get_ticks()

        surf.blit(self.image, (self.x, self.y))

    def move(self, pressed_keys):
        # TODO: add constraints
        if pressed_keys[pygame.K_UP]:
            self.y -= 1
        if pressed_keys[pygame.K_DOWN]:
            self.y += 1
        if pressed_keys[pygame.K_LEFT]:
            self.x -= 1
        if pressed_keys[pygame.K_RIGHT]:
            self.x += 1

    def update(self, pressed_keys):
        if any(pressed_keys[key] for key in self.controls):
            self.state = 'moving'
            # if pygame.time.get_ticks() - self.time_point > 100:
                # self.time_point = pygame.time.get_ticks()
            self.move(pressed_keys)
        else:
            self.state = 'idle'

        # if pygame.time.get_ticks() - self.time_point > 500:
        #     self.move(pressed_keys)
        #     self.time_point = pygame.time.get_ticks()
            
        # if pressed_keys[pygame.K_w]:
        #     player.walk_sound.play()

        # if pressed_keys[pygame.K_SPACE]:
        #     player.jump_sound.play()


def main():
    # recommended order of modules initialization,
    # calling pre_init fixes the sound delay
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.init()

    clock = pygame.time.Clock()

    tiles = (40, 40)
    scale_factor = 10

    surf = pygame.Surface(tiles)
    screen = pygame.display.set_mode((surf.get_width() * scale_factor, surf.get_height() * scale_factor))
    player = Player(0, 0)

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()

        player.update(pressed_keys)

        surf.fill((255, 255, 255))
        player.draw(surf)
        screen.blit(pygame.transform.scale(surf, screen.get_size()), (0, 0))
        pygame.display.update()
        

if __name__ == '__main__':
    os.chdir(os.path.join(os.getcwd(), 'movement_sound'))
    main()