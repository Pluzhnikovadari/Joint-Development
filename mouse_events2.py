import pygame as pg
import sys
 
WHITE = (255, 255, 255)
BLUE = (0, 0, 225)
 
sc = pg.display.set_mode((400, 300))
sc.fill(WHITE)
pg.display.update()
 
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
 
    pressed = pg.mouse.get_pressed()
    pos = pg.mouse.get_pos()
    if pressed[0]:
        pg.draw.circle(sc, BLUE, pos, 5)
        pg.display.update()
 
    pg.time.delay(20)