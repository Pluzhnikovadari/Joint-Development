import pygame as pg
import sys
 
WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)
 
sc = pg.display.set_mode((400, 300))
sc.fill(WHITE)
pg.display.update()
 
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                pg.draw.circle(
                    sc, RED, i.pos, 20)
                pg.display.update()
            elif i.button == 3:
                pg.draw.circle(
                    sc, BLUE, i.pos, 20)
                pg.draw.rect(
                    sc, GREEN,
                    (i.pos[0] - 10,
                     i.pos[1] - 10,
                     20, 20))
                pg.display.update()
            elif i.button == 2:
                sc.fill(WHITE)
                pg.display.update()
 
    pg.time.delay(20)