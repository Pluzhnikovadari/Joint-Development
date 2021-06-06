#-*-coding:utf-8-*-
import pygame, sys, time
from pygame.locals import *
# Блоки-ограничители рисуются как отдельные поверхности
# Между ними курсором перемещаем мячик
FPS = 30 # кадров в сек
# Размеры окна игры
width  = 500
height = 500
# Заголовок окна игры
title = "Collisions detection test"
# Сообщение в консоль игры
info = "Нет столкновений \n"
# Переменная - индикатор движения
direction = False
# Шаг движения
myStep = 2
pygame.init()
fpsClock = pygame.time.Clock()
mainSurface=pygame.display.set_mode((width,height),0,32)
pygame.display.set_caption(title)
background=pygame.image.load('images/car.png')     # Фон 
sprite = pygame.image.load('images/car.png')     # Подвижная картинка
# Начальные координаты подвижной картинки
# Важно, чтобы в начале работы она не перекрывала ни один блок
spriteX=mainSurface.get_width() - sprite.get_width()
spriteY=mainSurface.get_height() - sprite.get_height()
# Неподвижные блоки - все сохраняем в одном списке
# Структура списка blocks:
# каждый элемент - пара значений: (поверхность, область её размещения)
# blocks[0] - первый элемент списка, blocks[0][0] - surface первого элемента,blocks[0][1]  - Rect первого элемента
blocks = []
block1 = pygame.Surface((200,200))
block1.set_alpha(80)
block1.fill((255,0,0))
block1Rect = pygame.Rect(0,0,block1.get_width(), block1.get_height())
blocks.append((block1,block1Rect))
#
block2 = pygame.Surface((100,200))
block2.fill((0,255,0))
block2Rect = pygame.Rect(400,0,block2.get_width(), block2.get_height())
blocks.append((block2,block2Rect))
#
block3 = pygame.Surface((300,100))
block3.fill((0,0,255))
block3Rect = pygame.Rect(0,350,block3.get_width(), block3.get_height())
blocks.append((block3,block3Rect))
# закончили с описанием 3-х блоков
# *********>
def newPosition (direction, spriteX, spriteY):
    # Функция пересчитывает координаты новой позиции подвижного объекта
    # Проверяем столкновений со всеми блоками-границаи
    global myStep
    if direction:
        if direction == K_UP:
            spriteY -= myStep
        elif direction == K_DOWN:
            spriteY += myStep
        elif direction == K_LEFT:
            spriteX -= myStep
        elif direction == K_RIGHT:
            spriteX += myStep
    return spriteX, spriteY
# *********>
# *********>
def collisionDetected():
    global blocks
    global spriteRectNew
    colFlag = False
    # Проверка столкновений со всеми блоками в массиве блоков
    for block in blocks:
        if spriteRectNew.colliderect(block[1]):
            collisionDir = direction
            colFlag = True
    return colFlag
# *********>
# Цикл игры
while True:
    fpsClock.tick(FPS) # Частота обновления экрана
    
    # Обрабатываем очередь событий - начало 
    for event in pygame.event.get(): 
        # В цикле берём из очереди очередное событие, запоминаем в переменной event
        # Проверяем тип события и выполняем соответствующие лействия
        if event.type == QUIT:
            # Тип проверяемого события НАЖАТ Х В ОКНЕ ИГРЫ
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            # ESC key pressed
            pygame.quit()
            sys.exit()
        # Следующая строка получает управление только тогда, когда не отработали предыдущие проверки кода события
        # то есть произошло событие, отличное от перечисленных выше
        if event.type == KEYDOWN:
            direction = event.key
        if event.type == KEYUP:
            direction = False # Кнопка отпущена
    # Обрабатываем очередь событий - конец 
    # Текущее место расположения подвижной картинки 
    spriteRect = pygame.Rect(spriteX,spriteY,sprite.get_width(), sprite.get_height())
    # Сохраняем старые координаты
    oldPos = (spriteX, spriteY)
    
    # Вычмсляем новые координаты, анализируя нажатые кнопки
    spriteX, spriteY = newPosition(direction, spriteX, spriteY)
    # Вычисляем новое место расположения картинки
    spriteRectNew = pygame.Rect(spriteX,spriteY,sprite.get_width(), sprite.get_height())
    
    # Проверяем, не пересекает ли новое место блоки. Если пересекает, то вовращпни картинке старые координаты
    if collisionDetected():
        (spriteX, spriteY) = oldPos
        
    # Рисуем всё на экране
    #    Фон 
    mainSurface.blit(background,(0,0))
    #    Блоки 
    for block in blocks:
        mainSurface.blit(block[0],(block[1].x,block[1].y))
    #    Картинку 
    mainSurface.blit(sprite,(spriteRect.x,spriteRect.y))
    #    Обновляем экран
    pygame.display.update()