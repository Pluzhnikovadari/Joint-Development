import pygame as pg
import sys
 
WHITE = (255, 255, 255)
BLUE = (0, 0, 225)
 
pg.init()
sc = pg.display.set_mode((400, 300))
sc.fill(WHITE)
pg.display.update()
 
pg.mouse.set_visible(False)
 
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
 
    sc.fill(WHITE)
 
    if pg.mouse.get_focused():
        pos = pg.mouse.get_pos()
        pg.draw.rect(
            sc, BLUE, (pos[0] - 10,
                       pos[1] - 10,
                       20, 20))
 
    pg.display.update()
    pg.time.delay(20)
 