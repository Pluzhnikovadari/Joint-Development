import pygame as pg
import sys
 
WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)
FPS = 60

clock = pg.time.Clock()
 
sc = pg.display.set_mode((400, 300))
sc.fill(WHITE)
pg.display.update()

y_pos = x_pos = aim = 0
while 1:
    if y_pos != aim:
        y_pos += min(3, aim - y_pos)
        sc.fill(WHITE)
        pg.draw.circle(sc, RED, (x_pos, y_pos), 20)
        pg.display.update()
    elif aim != 0:
        sc.fill(WHITE)
        pg.draw.rect(sc, BLUE, (x_pos - 20, y_pos - 20, 40, 40))
        pg.display.update()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        if i.type == pg.MOUSEBUTTONDOWN and y_pos == aim:
            pg.draw.circle(sc, RED, (i.pos[0], 0), 20)
            pg.display.update()
            x_pos = i.pos[0]
            y_pos = 0
            aim = int(i.pos[1])
 
    clock.tick(FPS)