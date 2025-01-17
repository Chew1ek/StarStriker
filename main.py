import pygame

pygame.init()

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, file):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(center = (x, y))

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._option_surfaces.append(ARIAL_50.render(option, True ,('white')))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, ('blue'), option_rect)
            surf.blit(option, option_rect)


width, height = 600, 900
screen_rect = (0, 0, width, height)
ARIAL_50 = pygame.font.SysFont('arial', 50)
background = pygame.image.load('data/background.png')
menu = Menu()
menu.append_option('Старт', lambda: print('Hello'))
menu.append_option('Выход', quit)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

player = Object(300, 800, 'data/player.png')


while True:
    FPS = 60
    pygame.display.set_caption('Star Striker')
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                menu.switch(-1)
            elif event.key == pygame.K_DOWN:
                menu.switch(1)
            elif event.key == pygame.K_e:
                menu.select()



    key = pygame.key.get_pressed()
    if key[pygame.K_d]:
        player.rect.x += 5
    if key[pygame.K_a]:
        player.rect.x -= 5
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > width:
        player.rect.right = width

    screen.blit(background, (0, 0))
    menu.draw(screen, 100, 100, 75)
    screen.blit(player.image, player.rect)