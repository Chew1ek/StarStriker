import json
import os
import sys
import pygame
import random

pygame.init()

def input_check():
    global need_input
    if need_input == True:
        need_input = False
    else:
        need_input = True

def print_text(message, x, y, font_color=(255, 255, 255), font_type='PixelFont.ttf', font_size=50):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def ready():
    global player_ready
    player_ready = 1


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def create_particles(position):
    particle_count = 5
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))



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
                    sound_strike.play()
        if pygame.sprite.spritecollideany(enemy, bullet_group):
            bullet.killed()
            enemy.damage()

    def lose(self):
        global score
        score -= 50

    def damage(self):
        global score
        if pygame.sprite.spritecollideany(player, enemy_group):
            enemy.killed()
            if self.health < 1:
                menu.game_over()
                Lives.check_lives(3)
            else:
                self.health -= 1
                Lives.check_lives(self.health)
                score -= 25
                self.create_new()

    def create_new(self):
        global player
        player = Player(300, 800, 'data/player.png', self.health)
        create_particles((self.rect.x, self.rect.y))



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=3, health=3):
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
        enemy_group.add(enemy)

    def damage(self):
        global score
        if self.health > 0:
            self.health -= 1
        else:
            self.kill()
            self.create_new()
            score += 100

    def killed(self):
        self.kill()
        self.create_new()


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


class Lives(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(center = (x, y))

    def check_lives(lives):
        global heart
        if lives == 3:
            heart = Lives(550, 25, 'data/heart/heart_1.png')
        if lives == 2:
            heart = Lives(550, 25, 'data/heart/heart_2.png')
        if lives == 1:
            heart = Lives(550, 25, 'data/heart/heart_3.png')
        if lives == 0:
            heart = Lives(550, 25, 'data/heart/heart_4.png')


class Menu:
    def __init__(self):
        self.current_option_backup = 0
        self.callbacks_backup = []
        self.option_backup = []
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
            player_ready = 1

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

    def deletemenu(self):
        self.option_backup = self._option_surfaces
        self.callbacks_backup = self._callbacks
        self.current_option_backup = self._current_option_index
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def menu_swap(self):
        if event.key == pygame.K_w:
            menu.switch(-1)
        if event.key == pygame.K_s:
            menu.switch(1)
        if event.key == pygame.K_RETURN:
            global player, enemy, score
            score = 0
            enemy = Enemy(random.randint(0, width), 0, 'data/enemy.png')
            player = Player(300, 800, 'data/player.png')
            enemy_group.add(enemy)
            menu.select()
        if event.key == pygame.K_ESCAPE:
            quit()

    def leaderboard(self):
        global high_scores
        menu.deletemenu()
        menu.append_option(f'Лучший результат - {high_scores}', None)
        menu.append_option('Назад', lambda: menu.back())

    def level_switcher(self):
        menu.deletemenu()
        menu.append_option('Уровень 1', lambda: print('Уровень 1'))
        menu.append_option('Уровень 2', lambda: print('Уровень 2'))
        menu.append_option('Назад', lambda: menu.back())

    def back(self):
        global player_ready
        player_ready = 0
        self._option_surfaces = self.option_backup
        self._callbacks = self.callbacks_backup
        self._current_option_index = self.current_option_backup

    def name_input(self):
        global player_name
        print(1)
        player_name = input()

    def game_over(self):
        global player_ready, high_scores
        player_ready = 0
        screen.fill((255, 255, 255))
        menu.deletemenu()
        menu.draw(screen, 150, 200, 75)
        menu.append_option('Играть снова', lambda: ready())
        menu.append_option('Выйти в меню', lambda: menu.create_main())

    def create_main(self):
        menu.deletemenu()
        menu.append_option('Старт', lambda: ready())
        menu.append_option('Выбор уровней', lambda: menu.level_switcher())
        menu.append_option('Таблица лидеров', lambda: menu.leaderboard())
        menu.append_option('Выход', quit)



class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("scrap.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]



need_input = False
input_text = ''

player_name = ''
score = 0
player_ready = 0
width, height = 600, 900
screen_rect = (0, 0, width, height)

GRAVITY = 2
ARIAL_50 = pygame.font.Font('PixelFont.ttf', 50)
font = pygame.font.Font('PixelFont.ttf', 35)
background = pygame.image.load('data/background.png')
menu = Menu()

sound_strike = pygame.mixer.Sound('sounds/strike.wav')
pygame.mixer.music.load('sounds/fon.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

heart = Lives(550, 25, 'data/heart/heart_1.png')
bullet_image = pygame.image.load('data/bullet.png')
player = Player(300, 800, 'data/player.png')
enemy = Enemy(random.randint(0, 600), 0, 'data/enemy.png')

menu.append_option('Старт', lambda: ready())
menu.append_option('Выбор уровней', lambda: menu.level_switcher())
menu.append_option('Таблица лидеров', lambda: menu.leaderboard())
menu.append_option('Выход', quit)

all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

enemy_group.add(enemy)

while True:
    player.damage()
    FPS = 60
    pygame.display.set_caption('Star Striker')
    pygame.display.update()
    clock.tick(FPS)
    follow = font.render(f'Счёт: {score}', 1, (139, 69, 19))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            menu.menu_swap()


    if player_ready == 0:
        screen.fill((0, 0, 0))
        menu.draw(screen, 150, 200, 75)

    else:
        menu.deletemenu()
        enemy.move()
        screen.blit(background, (0, 0))
        key_pressed = pygame.key.get_pressed()

        if key_pressed:
            if key_pressed[pygame.K_TAB]: # Ввод слов
                input_check()
            player.move()
            player.strike()


            print_text(input_text, 100, 400)
        for event in pygame.event.get():
            if need_input and event.type == pygame.KEYDOWN: # Ввод слов
                if event.key == pygame.K_SLASH:
                    need_input = False
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 10:
                        input_text += event.unicode
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.strike()
                    sound_strike.play()


        all_sprites.update()
        all_sprites.draw(screen)
        bullet_group.update()
        bullet_group.draw(screen)
        screen.blit(enemy.image, enemy.rect)
        screen.blit(player.image, player.rect)
        screen.blit(heart.image, heart.rect)
        screen.blit(follow, (0, 0))