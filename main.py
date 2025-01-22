import pygame
import random

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, health=3):
        pygame.sprite.Sprite.__init__(self)

        self.health = health
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center = (x, y))

    def move(self):
        if key_pressed[pygame.K_d]:
            self.rect.x += 5
        if key_pressed[pygame.K_a]:
            self.rect.x -= 5
        if player.rect.left < 0:
            self.rect.left = 0
        if player.rect.right > width:
            self.rect.right = width

    def strike(self):
        global bullet
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.center, bullet_image)
                    bullet_group.add(bullet)
        if pygame.sprite.spritecollideany(enemy, bullet_group):
            bullet.killed()
            enemy.damage()

    def lose(self):
        global player_ready
        if self.health <= 0:
            player_ready = 2
        else:
            self.health -= 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=1, health=10):
        pygame.sprite.Sprite.__init__(self)

        self.speed = speed
        self.health= health
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center = (x, y))

    def move(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            player.lose()
            self.kill()
            self.create_new()

    def create_new(self):
        global enemy
        enemy = Enemy(random.randint(0, width), 0, 'data/enemy.png')

    def damage(self):
        global score
        if self.health > 0:
            self.health -= 1
        else:
            self.kill()
            self.create_new()
            score += 100


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, image, speed=-10, bullet_type=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (pos)
        self.speedy = speed
        self.type = bullet_type

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height or self.rect.bottom < 0:
            self.kill()

    def killed(self):
        self.kill()

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        if player_ready == 0:
            self._option_surfaces.append(ARIAL_50.render(option, True ,('white')))
            self._callbacks.append(callback)
        else:
            pass

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
                if player_ready == 0:
                    pygame.draw.rect(surf, ('blue'), option_rect)
                else:
                    pygame.draw.rect(surf, ('red'), option_rect)
            surf.blit(option, option_rect)


def ready():
    global player_ready
    player_ready = 1


score = 0
player_ready = 0
width, height = 600, 900
screen_rect = (0, 0, width, height)

ARIAL_50 = pygame.font.SysFont('arial', 50)
font = pygame.font.SysFont('arial', 35)
background = pygame.image.load('data/background.png')
menu = Menu()

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

bullet_image = pygame.image.load('data/bullet.png')
player = Player(300, 800, 'data/player.png')
enemy = Enemy(random.randint(0, 600), 0, 'data/enemy.png')

menu.append_option('Старт', lambda: ready())
menu.append_option('Выбор уровней', lambda: print('Выбор уровня'))
menu.append_option('Выход', quit)

bullet_group = pygame.sprite.Group()

while True:
    FPS = 60
    pygame.display.set_caption('Star Striker')
    pygame.display.update()
    clock.tick(FPS)
    follow = font.render(f'Счёт: {score}', 1, ('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                menu.switch(-1)
            if event.key == pygame.K_s:
                menu.switch(1)
            if event.key == pygame.K_RETURN:
                menu.select()
            if event.key == pygame.K_ESCAPE:
                quit()


    if player_ready == 0:
        screen.fill((0, 0, 0))
        menu.draw(screen, 225, 200, 75)
    else:
        enemy.move()
        screen.blit(background, (0, 0))
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            player.move()
            player.strike()
            if key_pressed[pygame.K_ESCAPE]:
                quit()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.strike()

        bullet_group.update()
        bullet_group.draw(screen)
        screen.blit(enemy.image, enemy.rect)
        screen.blit(player.image, player.rect)
        screen.blit(follow, (0, 0))