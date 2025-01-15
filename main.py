import pygame

pygame.init()

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, file):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(center = (x, y))


w, h = 600, 900
screen_rect = (0, 0, w, h)

background = pygame.image.load('data/background.png')

screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

player = Object(300, 800, 'data/player.png')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    key = pygame.key.get_pressed()
    if key[pygame.K_d]:
        player.rect.x += 5
    if key[pygame.K_a]:
        player.rect.x -= 5
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > w:
        player.rect.right = w

    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)

    FPS = 60
    pygame.display.set_caption('Star Striker')
    pygame.display.update()
    clock.tick(FPS)