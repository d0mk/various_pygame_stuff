import pygame, os, sys


class Player:
    def __init__(self):
        self.load_sounds()

    def load_sounds(self, volume=0.25):
        # TODO: fix the crackling sound
        def load_helper(filename):
            audio_file = pygame.mixer.Sound(filename)
            audio_file.set_volume(volume)
            return audio_file

        self.walk_sound = load_helper('walk.wav')
        self.jump_sound = load_helper('jump.wav')

    def draw(self):
        pass

    def update(self, x):
        pass


def main():
    # recommended order of modules initialization,
    # calling pre_init fixes the sound delay
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.init()

    screen = pygame.display.set_mode((400, 400))
    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()

        player.update(pressed_keys)

        screen.fill((0, 0, 0))
        player.draw()

        if pressed_keys[pygame.K_w]:
            player.walk_sound.play()

        if pressed_keys[pygame.K_SPACE]:
            player.jump_sound.play()
        

if __name__ == '__main__':
    os.chdir(os.path.join(os.getcwd(), 'movement_sound'))
    main()