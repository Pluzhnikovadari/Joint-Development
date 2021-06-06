"""Platform and ball game."""
import pygame
import time
import random
import sys
pygame.init()
pygame.key.set_repeat(10, 10)
FPS = 60
ball_color = (102, 0, 153)
paddle_color = (102, 51, 0)
red = (139, 0, 0)
black = (0, 0, 0)
ground = (154, 205, 50)
platforms = [(139, 0, 0), (102, 0, 102), (0, 51, 51), (255, 204, 0)]

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Paddle Game')
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

paddle_x = 250
ball = [150, 200]
move_ball = [-2, -2]
move = False
game_close = False
result = True


def message(msg, color):
    """System messages drawing."""
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 3, dis_height / 3])


def rect(start_x, start_y, color):
    """Rectangle drawing."""
    pygame.draw.rect(dis, color, (start_x, start_y, 50, 15))
    pygame.draw.rect(dis, black, (start_x, start_y, 50, 15), 1)


def ball_draw(ball):
    """Ball drawing."""
    pygame.draw.circle(dis, ball_color, ball, 7)
    pygame.draw.circle(dis, black, ball, 7, 1)


def paddle(x):
    """Paddle drawing."""
    pygame.draw.rect(dis, paddle_color, (x, 350, 100, 10))
    pygame.draw.rect(dis, black, (x, 350, 100, 10), 1)


def paddle_left(paddle_x):
    """Left movement."""
    return -5


def paddle_right(paddle_x):
    """Right movement."""
    return 5


def ball_move(ball, rectangl, fir):
    """Ball movement."""
    global game_close, result
    if ball[0] - 3.5 <= 0:
        move_ball[0] = 2
    if ball[0] + 3.5 >= dis_width:
        move_ball[0] = -2
    if ball[1] + 3.5 >= dis_height:
        game_close = True
        if rectangl:
            result = False
        else:
            result = True
    if ball[1] - 3.5 <= 0:
        move_ball[1] = 2
    if hit_paddle(ball):
        move_ball[1] = -2
    for i in range(len(rectangl)):
        if hit_rect_wi(rectangl, i, ball, fir):
            move_ball[1] = 2
    return move_ball


def hit_paddle(ball):
    """Ball and paddle collision handling."""
    global paddle_x
    if ball[0] >= paddle_x - 3.5 and ball[0] <= paddle_x + 100 + 3.5 \
       and ball[1] >= 350 - 3.5 and ball[1] <= 360 - 3.5:
        return True
    return False


def hit_rect_wi(rectangl, i, ball, fir):
    """Ball and rectangle collision handling."""
    if fir[i]:
        if ball[0] >= rectangl[i][0] - 3.5 \
           and ball[0] <= rectangl[i][0] + 50 + 3.5 \
           and ball[1] >= rectangl[i][1] + 3.5 \
           and ball[1] <= rectangl[i][1] + 15 + 3.5:
            fir[i] = False
            return True
        return False


def gameLoop():
    """Loop of game."""
    global paddle_x, ball, move, game_close
    game_over = False
    paddle_speed = 0

    rectangl = [(0, 0, random.choice(platforms)),
                (50, 0, random.choice(platforms)),
                (150, 0, random.choice(platforms)),
                (200, 0, random.choice(platforms)),
                (250, 0, random.choice(platforms)),
                (300, 0, random.choice(platforms)),
                (350, 0, random.choice(platforms)),
                (400, 0, random.choice(platforms)),
                (450, 0, random.choice(platforms)),
                (500, 0, random.choice(platforms)),
                (0, 15, random.choice(platforms)),
                (50, 15, random.choice(platforms)),
                (100, 15, random.choice(platforms)),
                (150, 15, random.choice(platforms)),
                (200, 15, random.choice(platforms)),
                (250, 15, random.choice(platforms)),
                (300, 15, random.choice(platforms)),
                (350, 15, random.choice(platforms)),
                (400, 15, random.choice(platforms)),
                (450, 15, random.choice(platforms)),
                (500, 15, random.choice(platforms)),
                (550, 15, random.choice(platforms)),
                (550, 0, random.choice(platforms)),
                (100, 0, random.choice(platforms))]

    fir = [True for i in range(len(rectangl))]

    while not game_over:
        if True not in fir:
            game_close = True
        while game_close:
            dis.fill(ground)
            if result:
                message("You win!", red)
            else:
                message("You lose!", red)
            pygame.display.update()
            time.sleep(3)
            game_over = True
            game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle_speed = paddle_left(paddle_x)
                    if not move:
                        move = True
                elif event.key == pygame.K_RIGHT:
                    paddle_speed = paddle_right(paddle_x)
                    if not move:
                        move = True

        paddle_x += paddle_speed
        if paddle_x + 100 >= dis_width:
            paddle_speed = 0
        if paddle_x <= 0:
            paddle_speed = 0

        dis.fill(ground)
        paddle(paddle_x)

        for i, elem in enumerate(rectangl):
            if fir[i]:
                rect(*elem)
        if move:
            move_ball = ball_move(ball, rectangl, fir)
            ball[0] += move_ball[0]
            ball[1] += move_ball[1]
        ball_draw(ball)

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()


gameLoop()
