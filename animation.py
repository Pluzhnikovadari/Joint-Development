import pygame
import sys
 
FPS = 60
WIN_WIDTH = 400
WIN_HEIGHT = 400
BLACK = (0, 0, 0)
COLOR = (175, 238, 238)
 
clock = pygame.time.Clock()
sc = pygame.display.set_mode(
    (WIN_WIDTH, WIN_HEIGHT))

w = 100
h = w
x = 0 - w
y = WIN_HEIGHT // 2
 
while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
    sc.fill(BLACK)
    pygame.draw.rect(sc, COLOR, (x, y, w, h))
    pygame.display.update()
    if x >= WIN_WIDTH + w:
        x = 0 - w
    else:
        x += 2
 
    clock.tick(FPS)