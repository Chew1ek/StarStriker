import pygame
pygame.init()

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, file):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(center = (x, y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0 or self.rect.left > width or self.rect.top > height or self.rect.bottom < 0:
            self.kill()

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
        global player_ready
        if player_ready == 0:
            self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, ('blue'), option_rect)
            surf.blit(option, option_rect)


def ready():
    global player_ready
    player_ready += 1


player_ready = 0
width, height = 600, 900
screen_rect = (0, 0, width, height)
ARIAL_50 = pygame.font.SysFont('arial', 50)
background = pygame.image.load('data/background.png')
menu = Menu()
menu.append_option('Старт', lambda: ready())
menu.append_option('Выбор уровней', lambda: print('Выбор уровня'))
menu.append_option('Выход', quit)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

bullet_image = pygame.image.load('data/bullet.png')
player = Object(300, 800, 'data/player.png')
enemy = pygame.image.load('data/enemy.png')
enemy_y = -0

bullet_group = pygame.sprite.Group()


while True:
    FPS = 60
    pygame.display.set_caption('Star Striker')
    pygame.display.update()
    clock.tick(FPS)
    enemy_rect = enemy.get_rect(topleft=(300, enemy_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                menu.switch(-1)
            elif event.key == pygame.K_s:
                menu.switch(1)
            elif event.key == pygame.K_RETURN:
                menu.select()
            elif event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.center, bullet_image)
                bullet.speedy = -10
                bullet_group.add(bullet)



    if player_ready == 0:
        screen.fill((0, 0, 0))
        menu.draw(screen, 225, 200, 75)
    else:
        enemy_y += 2
        screen.blit(background, (0, 0))
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            player.rect.x += 5
        if key[pygame.K_a]:
            player.rect.x -= 5
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > width:
            player.rect.right = width

        bullet_group.update()
        bullet_group.draw(screen)
        screen.blit(player.image, player.rect)
        screen.blit(enemy, (300 ,enemy_y))