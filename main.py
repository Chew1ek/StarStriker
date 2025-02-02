import os
import sys
from sys import exit

import pygame
import random
import csv



all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player = None
enemy = None


def ready():
    global flag, player_ready, end_game, player, enemy
    end_game = ''
    menu.deletemenu()
    all_sprites.remove(player)
    player = Player(300, 800, 'data/player_anim.png', 2, 1)
    enemy = Enemy(random.randint(50, width - 50), 0, 'data/enemy.png', 5, 2)
    all_sprites.add(player)
    player_ready = 1
    flag = 'play'

def create_player():
    global player
    all_sprites.remove(player)
    player = Player(300, 800, 'data/player_anim.png', 2, 1)
    all_sprites.add(player)
    player.create_new()


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


def level1():
    global player_ready, end_game, player, enemy
    end_game = ''
    menu.deletemenu()
    all_sprites.remove(player)
    player = Player(300, 800, 'data/player_anim.png', 2, 1)
    enemy = Enemy(random.randint(50, width - 50), 0, 'data/enemy.png', 5, 2)
    all_sprites.add(player)
    player_ready = 1

def level2():
    global flag, player_ready, end_game, player, level, enemy
    end_game = ''
    menu.deletemenu()
    all_sprites.remove(player)
    player = Player(300, 800, 'data/player_anim.png', 2, 1)
    enemy = Enemy(random.randint(50, width - 50), 0, 'data/enemy.png', 7, 4)
    all_sprites.add(player)
    player_ready = 1
    flag = 'play'
    level = 2

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


class Player(AnimatedSprite):
    def __init__(self, x, y, sheet_path, columns, rows, health=3):
        sheet = pygame.image.load(sheet_path)
        super().__init__(sheet, columns, rows, x, y)
        self.health = health
        self.is_be_damaged = False
        self.iter = 0
        self.player_damage = 0
        self.duration = 6

    def move(self):
        global key_pressed
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += 7
        if key_pressed[pygame.K_a]:
            self.rect.x -= 7
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
        global score, player_damage, game_over, flag, player_ready, death
        if pygame.sprite.spritecollideany(player, enemy_group):
            enemy.killed()
            if self.health < 1:
                menu.game_over()
                screen.fill((0, 0, 0))
                death = 1
                Lives.check_lives(3)
            else:
                self.health -= 1
                Lives.check_lives(self.health)
                score -= 25
                self.create_new()

    def create_new(self):
        global player, player_damage
        all_sprites.remove(player)
        player = Player(300, 800, 'data/player_anim.png', 2, 1, self.health)
        all_sprites.add(player)
        create_particles((self.rect.x, self.rect.y))
        player_damage = 1

    def update(self):
        global player_damage
        super().update()
        if self.iter > 30:
            if player_damage == 1:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.duration -= 1
                if self.duration == 0:
                    player_damage = 0
                self.iter = 0
        self.iter += tick




class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=5, health=2):
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
        global enemy, level
        if level == 1:
            enemy = Enemy(random.randint(50, width - 50), 0, 'data/enemy.png', 5)
        else:
            enemy = Enemy(random.randint(50, width - 50), 0, 'data/enemy.png', 7, 4)
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
    def __init__(self, pos, image, speed=-20, bullet_type=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speedy = speed
        self.type = bullet_type

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top < 0:
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
        self._option_surfaces.append(ARIAL_50.render(option, True ,(255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        global player_ready
        if player_ready == 0:
            self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, padding):
        global game_over
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, ('blue'), option_rect)
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
            global player, enemy, score, player_ready
            if player_ready == 0:
                score = 0
                enemy = Enemy(random.randint(0, width), 0, 'data/enemy.png')
                enemy_group.add(enemy)
                menu.select()
        if event.key == pygame.K_ESCAPE:
            exit()


    def leaderboard(self):
        global high_scores, flag
        flag = 'leader'
        menu.deletemenu()
        menu.append_option('', lambda: menu.back())
        menu.append_option('', lambda: menu.back())
        menu.append_option('', lambda: menu.back())
        menu.append_option('', lambda: menu.back())
        menu.append_option('', lambda: menu.back())
        menu.append_option('', lambda: menu.back())
        menu.append_option('Enter - выход', lambda: menu.back())




    def level_switcher(self):
        menu.deletemenu()
        menu.append_option('Уровень 1', lambda: level1())
        menu.append_option('Уровень 2', lambda: level2())
        menu.append_option('Назад', lambda: menu.back())

    def back(self):
        global player_ready, end_game, flag
        flag = 'menu'
        player_ready = 0
        end_game = ''
        self._option_surfaces = self.option_backup
        self._callbacks = self.callbacks_backup
        self._current_option_index = self.current_option_backup

    def name_input(self):
        global player_name, score, need_input, input_text, player_ready
        menu.deletemenu()
        menu.append_option('Назад', lambda: menu.back())
        need_input = True

        while need_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: # Ввод слов
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_SLASH:
                        need_input = False
                    else:
                        if len(input_text) < 10:
                            input_text += event.unicode
                            print(input_text)
                        else:
                            need_input = False

        menu.append_option(input_text, lambda: exit())
        print_text(input_text, 100, 400)



    def game_over(self):
        global player_ready, high_scores, end_game, flag
        menu.deletemenu()
        player_ready = 0
        flag = 'game_over'
        menu.append_option('Играть снова', lambda: ready())
        menu.append_option('Дальше', lambda: level2())
        menu.append_option('Выйти в меню', lambda: menu.create_main())



    def create_main(self):
        global end_game
        menu.deletemenu()
        end_game = ''
        menu.append_option('Старт', lambda: ready())
        menu.append_option('Выбор уровней', lambda: menu.level_switcher())
        menu.append_option('Таблица лидеров', lambda: menu.leaderboard())
        menu.append_option('Выход', lambda: exit())


class Particle(pygame.sprite.Sprite):
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


pygame.init()


need_input = False
input_text = ''

player_name = ''
score = 0
player_ready = 0
width, height = 600, 900
screen_rect = (0, 0, width, height)

level = 1
end_game = ''

GRAVITY = 2
ARIAL_50 = pygame.font.Font('PixelFont.ttf', 50)
font = pygame.font.Font('PixelFont.ttf', 35)
background = pygame.image.load('data/background.png')
background2 = pygame.image.load('data/background2.png')
game_over_font = pygame.font.Font('PixelFont.ttf', 80)
game_over_render = game_over_font.render('ИГРА ОКОНЧЕНА', 1, (205, 92, 92))
game_over = 0

pygame.display.set_icon(pygame.image.load("icon.ico"))

flag = 'menu'
death = 0

menu = Menu()
menu.create_main()

player_damage = 0

sound_strike = pygame.mixer.Sound('sounds/strike.wav')
pygame.mixer.music.load('sounds/fon.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

heart = Lives(550, 25, 'data/heart/heart_1.png')
bullet_image = pygame.image.load('data/bullet.png')

while True:
    tick = clock.tick()
    FPS = 60
    pygame.display.set_caption('Star Striker')
    pygame.display.update()
    clock.tick(FPS)
    follow = font.render(f'Счёт: {score}', 1, (139, 69, 19))
    key_pressed = pygame.key.get_pressed()

    if flag == 'menu':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                menu.menu_swap()

        if player_ready == 0:
            screen.fill((0, 0, 0))
            menu.draw(screen, 150, 450, 60)

    if flag == 'play':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                menu.menu_swap()

        if player_ready == 0:
            screen.fill((0, 0, 0))
            if end_game == 'end game':
                screen.blit(game_over_render, (15, 200))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    menu.menu_swap()

        elif player_ready == 1 and level < 2:
            screen.blit(background, (0, 0))
            if player is None:
                create_player()
            player.move()
            player.damage()
            menu.deletemenu()
            enemy.move()
            bullet_group.update()
            bullet_group.draw(screen)
            screen.blit(enemy.image, enemy.rect)
            screen.blit(player.image, player.rect)
            screen.blit(heart.image, heart.rect)
            screen.blit(follow, (0, 0))
            all_sprites.update()
            all_sprites.draw(screen)
            player.strike()

            if key_pressed:
                if key_pressed[pygame.K_TAB]:  # Ввод слов
                    input_check()

            if score >= 1000:
                screen.fill((0, 0, 0))
                menu.game_over()


        else:
            if player is None:
                create_player()

            player.move()
            player.damage()
            menu.deletemenu()
            enemy.move()
            screen.blit(background2, (0, 0))
            bullet_group.update()
            bullet_group.draw(screen)
            screen.blit(enemy.image, enemy.rect)
            screen.blit(player.image, player.rect)
            screen.blit(heart.image, heart.rect)
            screen.blit(follow, (0, 0))
            all_sprites.update()
            all_sprites.draw(screen)
            player.strike()

            if key_pressed:
                if key_pressed[pygame.K_TAB]:  # Ввод слов
                    input_check()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.strike()
                        sound_strike.play()

            if score >= 1500:
                game_over = 1
                menu.game_over()

    if flag == 'game_over':
        if player_ready == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        flag = 'menu'
                        menu.create_main()
                        with open('leader.csv', 'r',  newline='') as csvfile:
                            leader = csv.reader(csvfile, delimiter=';', quotechar='|')
                            spisok = []
                            for row in leader:
                                spisok.append([row[0], int(row[1])])
                            spisok.append([input_text, score])
                            spisok.sort(key=lambda x: x[1], reverse=True)

                        with open('leader.csv', 'w', newline='') as csvfile:
                           leader_writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                           a = 1
                           for row in spisok:
                               if a < 11:
                                   leader_writer.writerow(row)
                                   a += 1

                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 10:
                            input_text += event.unicode
                    screen.fill((0, 0, 0))
                    screen.blit((font.render(f'{input_text}', 1, (255, 255, 255))), (150, 600))
        screen.blit((ARIAL_50.render(f'Введите имя', 1, (255, 255, 255))), (150, 400))
        if death == 1:
            screen.blit((ARIAL_50.render(f'Вы умерли', 1, (250, 128, 114))), (150, 200))
            death = 0
        else:
            screen.blit((ARIAL_50.render(f'Уровень {level} пройден', 1, (250, 128, 114))), (100, 200))


    if flag == 'leader':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                menu.menu_swap()

        screen.blit((ARIAL_50.render(f'Таблица результатов', 1, (255, 255, 255))), (15, 50))
        with open('leader.csv', newline='') as csvfile:
            leader = csv.reader(csvfile, delimiter=';', quotechar='|')
            c = 1
            y = 200
            for row in leader:
                screen.blit((font.render(f'{c}. {", ".join(row)}', 1, (255, 255, 255))), (150, y))
                y += 40
                c += 1