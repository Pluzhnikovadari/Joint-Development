import pygame
import sys
 
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)

pygame.init()
sc = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

pygame.display.update()
 
r1 = pygame.Rect((150, 20, 100, 75))
 
pygame.draw.rect(sc, WHITE, (20, 20, 100, 75))
pygame.draw.rect(sc, LIGHT_BLUE, r1, 8)

pygame.draw.line(sc, WHITE, 
                 [10, 30], 
                 [290, 15], 3)
pygame.draw.line(sc, WHITE, 
                 [10, 50], 
                 [290, 35])
pygame.draw.aaline(sc, WHITE, 
                   [10, 70], 
                   [290, 55])
pygame.draw.lines(sc, WHITE, True,
                  [[10, 10], [140, 70],
                   [280, 20]], 2)
pygame.draw.aalines(sc, WHITE, False,
                    [[10, 100], [140, 170],
                     [280, 110]])
OFFSET = 200
pygame.draw.polygon(sc, WHITE, 
                    [[150 + OFFSET, 10], [180 + OFFSET, 50], 
                     [90 + OFFSET, 90], [30 + OFFSET, 30]])
pygame.draw.polygon(sc, WHITE, 
                    [[250 + OFFSET, 110], [280 + OFFSET, 150], 
                     [190 + OFFSET, 190], [130 + OFFSET, 130]])
pygame.draw.aalines(sc, WHITE, True, 
                    [[250 + OFFSET, 110], [280 + OFFSET, 150], 
                     [190 + OFFSET, 190], [130 + OFFSET, 130]])
pygame.draw.circle(sc, YELLOW, 
                   (100, 100), 50)
pygame.draw.circle(sc, PINK, 
                   (200, 100), 50, 10)
pygame.draw.ellipse(sc, GREEN, 
                    (10, 200, 280, 100))
pi = 3.14
pygame.draw.arc(sc, WHITE,
                (20, 100, 280, 100),
                0, pi)
pygame.draw.arc(sc, PINK,
                (100, 60, 200, 150),
                pi, 2*pi, 3)

cnt = 0
while True:

    clock.tick(FPS)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
    cnt += 1
    if cnt % 10 == 0:
        pygame.display.set_caption(str(cnt // 10))
