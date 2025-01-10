import pygame

pygame.init()

w, h = 800, 800

screen = pygame.display.set_mode((w, h))

clock = pygame.time.Clock()
FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    clock.tick(FPS)