import pygame
import time
import random
import os
import sys
import datetime
 
pygame.init()

FPS = 60


white = (255, 255, 255)
black = (0, 0, 0)
ground = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
player_speed = 5
yellow = (255, 204, 0)

move = False

dis_width = 1000
dis_height = 600
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Meteor Game')
 
clock = pygame.time.Clock()
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


game_folder = os.path.dirname("../Joint-Development/meteor.py")
img_folder = os.path.join(game_folder, 'images')
player_img = pygame.image.load(os.path.join(img_folder, 'ship.png')).convert_alpha()
healf_img = pygame.image.load(os.path.join(img_folder, 'healf.png')).convert_alpha()
healf_img_m = pygame.image.load(os.path.join(img_folder, 'healf_m.png')).convert_alpha()
asteriod_img = pygame.image.load(os.path.join(img_folder, 'asteroid.png')).convert_alpha()
background = pygame.image.load(os.path.join(img_folder, 'kos.jpg')).convert()
background_rect = background.get_rect()


explode = [pygame.image.load(os.path.join(img_folder, 'ex0.png')).convert_alpha(), pygame.image.load(os.path.join(img_folder, 'ex1.png')).convert_alpha(),
    pygame.image.load(os.path.join(img_folder, 'ex2.png')).convert_alpha(), pygame.image.load(os.path.join(img_folder, 'ex3.png')).convert_alpha(),
    pygame.image.load(os.path.join(img_folder, 'ex4.png')).convert_alpha(), pygame.image.load(os.path.join(img_folder, 'ex5.png')).convert_alpha(),
    pygame.image.load(os.path.join(img_folder, 'ex6.png')).convert_alpha(), pygame.image.load(os.path.join(img_folder, 'ex7.png')).convert_alpha(),
    pygame.image.load(os.path.join(img_folder, 'ex8.png')).convert_alpha()]


game_close = False

bul_speed = -10

score = 0

inp = ''

healf = 4


def input_name():
    pygame.display.update()
    input_box = pygame.Rect(100, 100, 140, 32)
    color = pygame.Color('dodgerblue2')
    name = ''
    done = False
    global inp

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE and inp:
                    inp = inp[:-1]
                else:
                    inp += event.unicode

        dis.fill(ground)
        mesg = font_style.render("Input your name", True, white)
        dis.blit(mesg, [100, 80])
        txt_surface = font_style.render(inp, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        dis.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(dis, color, input_box, 2)
        pygame.display.flip()

def draw_expl(x, y, i):
    global explode
    rect = explode[i].get_rect(center=(x, y))
    dis.blit(explode[i], rect)



def pr_healf(healf):
    global healf_img, healf_img_m
    if healf > 0:
        if healf > 2:
            rect = healf_img.get_rect(center=(980, 20))
            dis.blit(healf_img, rect)
        else:
            rect = healf_img_m.get_rect(center=(980, 20))
            dis.blit(healf_img_m, rect)
    if healf > 1:
        if healf > 2:
            rect = healf_img.get_rect(center=(960, 20))
            dis.blit(healf_img, rect)
        else:
            rect = healf_img_m.get_rect(center=(960, 20))
            dis.blit(healf_img_m, rect)
    if healf > 2:
        rect = healf_img.get_rect(center=(940, 20))
        dis.blit(healf_img, rect)
    if healf > 3:
        rect = healf_img.get_rect(center=(920, 20))
        dis.blit(healf_img, rect)



def pr_score():
    global score
    value = score_font.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def ship_draw(start_x, start_y):
    global player_img
    rect = player_img.get_rect(center=(start_x, start_y))
    dis.blit(player_img, rect)

def asteroid_draw(start_x, start_y):
    global asteriod_img
    rect = asteriod_img.get_rect(center=(start_x, start_y))
    dis.blit(asteriod_img, rect)

def update(gamer):
    gamer_speed = [0, 0]
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT] and gamer[0] - 35 > 0:
        gamer_speed[0] = -8
    if keystate[pygame.K_RIGHT] and gamer[0] + 35 < dis_width:
        gamer_speed[0] = 8
    if keystate[pygame.K_UP] and gamer[1] - 35 > 0:
        gamer_speed[1] = -8
    if keystate[pygame.K_DOWN] and gamer[1] + 35 < dis_height:
        gamer_speed[1] = 8
    
    gamer[0] += gamer_speed[0]
    gamer[1] += gamer_speed[1]


def create_met():
    x = random.randrange(dis_width - 25)
    y = random.randrange(-100, -40)
    speed_y = random.randrange(1, 8)
    speed_x = random.randrange(-3, 3)
    return [[x, y], [speed_x, speed_y]]


def updete_met(met, met_speed):
    met[0] += met_speed[0]
    met[1] += met_speed[1]
    if met[1] > dis_height + 25 or met[0] < -25 or met[0] > dis_width + 25:
        met[0] = random.randrange(dis_width - 25)
        met[1] = random.randrange(-100, -40)
        met_speed[1] = random.randrange(1, 8)
        met_speed[0] = random.randrange(-3, 3)

def hit_meteor(gamer, met, met_speed):
    if met[0] + 25 > gamer[0] - 35 and met[0] - 25 < gamer[0] + 35 and \
        met[1] + 25 > gamer[1] - 35 and met[1] - 25 < gamer[1] + 35:
        met[0] = random.randrange(dis_width - 25)
        met[1] = random.randrange(-100, -40)
        met_speed[1] = random.randrange(1, 8)
        met_speed[0] = random.randrange(-3, 3)
        return True
    return False


def bullet_draw(x, y):
    pygame.draw.circle(dis, yellow, (x, y), 3)


def hit_bullet(bul, asteroids, e, exp):
    global score
    for ast in asteroids:
        if ast[0][0] + 25 > bul[0] - 3.5 and ast[0][0] - 25 < bul[0] + 3.5 and \
            ast[0][1] + 25 > bul[1] - 3.5 and ast[0][1] - 25 < bul[1] + 3.5:
            e.append(0)
            exp.append(ast[0][::])
            ast[0][0] = random.randrange(dis_width - 25)
            ast[0][1] = random.randrange(-100, -40)
            ast[1][1] = random.randrange(1, 8)
            ast[0][0] = random.randrange(-3, 3)
            score += 1
            return True
    return False


def gameLoop():
    global game_close, move, healf
    game_over = False

    gamer = [250, 350]
    asteroids = []
    for i in range(8):
        asteroids.append(create_met())

    bullet = []

    cur_time = 0

    now_time = datetime.datetime.now()
    now_time_healf = datetime.datetime.now()

    e = []
    exp = []
 
    while not game_over:

        while game_close == True:
            dis.fill(ground)

            message("Your score: " + str(score), red)

            file = open('meteor.txt', 'r')
            data = file.readlines()
            table = []
            for el in data:
                if el:
                    name, s = el[:-1].split(" ")
                    table.append([int(s), name])
            table.append([score, inp])
            table.sort()
            table = table[::-1]
            if len(table) > 5:
                table = table[:5]
            mesg = font_style.render("Best results:", True, white)
            dis.blit(mesg, [dis_width / 6, dis_height / 3 + 40])
            for i, elem in enumerate(table):
                mesg = font_style.render(elem[1] + " " + str(elem[0]), True, white)
                dis.blit(mesg, [dis_width / 6, dis_height / 3 + (i + 3) * 20])
            pygame.display.update()

            time.sleep(3)
            
            file = open('meteor.txt', 'w')
            text = ""
            for el in table:
                text += el[1] + " " + str(el[0]) + "\n"
            file.write(text)
            
            game_over = True
            game_close = False
            file.close()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                cur_time = datetime.datetime.now()
                difference = cur_time - now_time
                if divmod(difference.seconds * 60 + difference.microseconds, 60)[1] > 50:
                    bullet.append([gamer[0], gamer[1]])
                    now_time = cur_time
            update(gamer)

        dis.fill(ground)
        dis.blit(background, background_rect)

        for elem in asteroids:
            updete_met(*elem)
            asteroid_draw(*elem[0])

        bul_update = []
        for elem in bullet:
            elem[1] += bul_speed
            if elem[1] > -20 and not hit_bullet(elem, asteroids, e, exp):
                bul_update.append(elem)
        bullet = bul_update[::]
        for elem in bullet:
            bullet_draw(*elem)

        ship_draw(*gamer)

        res = False
        for elem in asteroids:
            explosions = elem[0][::]
            res = hit_meteor(gamer, elem[0], elem[1])
            if res:
                exp.append(explosions)
                e.append(0)
                healf -=  1
                if healf <= 0:
                    game_close = True

        pr_healf(healf)

        pr_score()

        update_e = []
        update_exp = []
        for i, el in enumerate(e):
            if el < 9:
                update_e.append(el + 1)
                draw_expl(exp[i][0], exp[i][1], el)
                update_exp.append(exp[i])
        e = update_e[::]
        exp = update_exp[::]
 
        pygame.display.update()
 
        clock.tick(FPS)
    pygame.quit()
    quit()

input_name()
pygame.key.set_repeat(10, 10)
gameLoop()