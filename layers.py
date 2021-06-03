from random import randint
import pygame as pg
import sys
 
sc = pg.display.set_mode((400, 400))
 
background = pg.Surface((400, 200))
background.fill((0, 255, 0))
xb = 0
yb = 100
 
hero = pg.Surface((100, 100))
hero.fill((255, 0, 0))
x = 0
y = 50
 
# порядок прорисовки важен!
background.blit(hero, (x, y))
sc.blit(background, (xb, yb))
 
pg.display.update()
 
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        elif i.type == pg.MOUSEBUTTONUP:
            yb = randint(0, 200)
 
    if x < 400:
        x += 2
    else:
        x = 0
 
    sc.fill((0, 0, 0))
    background.fill((0, 255, 0))
 
    background.blit(hero, (x, y))
    sc.blit(background, (xb, yb))
 
    pg.display.update()
 
    pg.time.delay(30)
 