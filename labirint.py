from random import randint, random
import pygame
import sys
import time


WIN_WIDTH = 1500
WIN_HEIGHT = 1000
WALL_WIDTH = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
END_TEXT_COLOR = (200, 20, 20)
START_TEXT_COLOR = (0, 139, 139)
WALL_COLOR = (139, 100, 50)
START_MENU_COLOR = (255, 140, 0)
BACKGROUND_COLOR = (154, 205, 50)
FPS = 60
PLAYER_START = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
PLAYER_SPEED = 5
GENERATOR_FREQ = 1
BALL_RADIUS = 20


def intercect_line_circle(x0, y0, r, x1, y1, x2, y2):
    '''проверяем есть ли решения у системы уравнений
    (y - y1) / (y2 - y1) = (x - x1) / (x2 - x1) и
    (x - x0)^2 + (y - y0)^2 = r^2'''

    if x1 == x2:
        b = -y0
        D = r**2 - (x1 - x0)**2
        if D < 0:
            return False
        res1, res2 = -b - D**0.5, -b + D**0.5
        if res2 < y1 or res1 > y2:
            return False

    else:
        a2 = (y1 - y2) / (x1 - x2)
        b2 = (x1 * y2 - x2 * y1) / (x1 - x2)
        b2 -= y0
        a = 1 + a2**2
        b = -x0 + a2 * b2
        c = x0**2 + b2**2 - r**2
        D = b**2 - a * c
        if D < 0:
            return False
        res1, res2 = (-b - D**0.5) / a, (-b + D**0.5) / a
        if x1 > x2:
            x1, x2 = x2, x1
        if res2 < x1 or res1 > x2:
            return False
    return True


def point_in_rect(pos, start, params):
    return start[0] <= pos[0] <= start[0] + params[0] and \
           start[1] <= pos[1] <= start[1] + params[1]


def point_in_circle(pos, start, radius):
    return (pos[0] - start[0])**2 + (pos[1] - start[1])**2 <= radius**2


class Wall:
    def __init__(self, surface, start, params, color):
        self.surf = surface
        self.start = start
        self.params = params
        self.color = color
        self.type = "wall"
        pygame.draw.rect(self.surf, self.color, self.start + self.params)

    def draw(self):
        pygame.draw.rect(self.surf, self.color, self.start + self.params)


class Ball:
    def __init__(self, surface, pos, color, radius,
                 speed=None, dx=None, dy=None):
        self.surf = surface
        self.pos = pos
        self.color = color
        self.radius = radius
        self.type = "ball"
        self.speed = 5 * random() + 2 if not speed else speed
        self.dx = 2 * self.speed * random() - self.speed if not dx else dx
        self.dy = 2 * self.speed * random() - self.speed if not dy else dy
        pygame.draw.circle(self.surf, self.color, self.pos, self.radius)

    def move(self, objects):
        for obj in objects:
            if obj.type == "ball":
                x = self.pos[0] + self.dx - obj.pos[0]
                y = self.pos[1] + self.dy - obj.pos[1]
                r = self.radius + obj.radius
                if x**2 + y**2 <= r**2 and \
                   (self.pos[0] != obj.pos[0] or self.pos[1] != obj.pos[1]):
                    tmp = (self.dx, self.dy)
                    dif_rad = self.radius ** 2 - obj.radius ** 2
                    sum_rad = self.radius ** 2 + obj.radius ** 2
                    self.dx = dif_rad * self.dx + 2 * (obj.radius ** 2) \
                                                    * obj.dx
                    self.dx /= sum_rad
                    self.dy = dif_rad * self.dy + 2 * (obj.radius ** 2) \
                                                    * obj.dy
                    self.dy /= sum_rad
                    obj.dx = -dif_rad * obj.dx + 2 * (self.radius ** 2) \
                                                   * tmp[0]
                    obj.dx /= sum_rad
                    obj.dy = -dif_rad * obj.dy + 2 * (self.radius ** 2) \
                                                   * tmp[1]
                    obj.dy /= sum_rad
                    obj.pos = (obj.pos[0] + obj.dx, obj.pos[1] + obj.dy)
            if obj.type == "wall":
                if intercect_line_circle(self.pos[0] + self.dx,
                                         self.pos[1] + self.dy,
                                         self.radius, *obj.start,
                                         obj.start[0] + obj.params[0],
                                         obj.start[1]) or \
                   intercect_line_circle(self.pos[0] + self.dx,
                                         self.pos[1] + self.dy,
                                         self.radius, obj.start[0],
                                         obj.start[1] + obj.params[1],
                                         obj.start[0] + obj.params[0],
                                         obj.start[1] + obj.params[1]):
                    self.dy *= -1
                if intercect_line_circle(self.pos[0] + self.dx,
                                         self.pos[1] + self.dy,
                                         self.radius, *obj.start, obj.start[0],
                                         obj.start[1] + obj.params[1]) or \
                   intercect_line_circle(self.pos[0] + self.dx,
                                         self.pos[1] + self.dy,
                                         self.radius,
                                         obj.start[0] + obj.params[0],
                                         obj.start[1],
                                         obj.start[0] + obj.params[0],
                                         obj.start[1] + obj.params[1]):
                    self.dx *= -1
            if obj.type == "player":
                dot1 = (obj.x - obj.surf.get_width() // 2,
                        obj.y - obj.surf.get_height() // 2)
                dot2 = (obj.x + obj.surf.get_width() // 2,
                        obj.y - obj.surf.get_height() // 2)
                dot3 = (obj.x - obj.surf.get_width() // 2,
                        obj.y + obj.surf.get_height() // 2)
                dot4 = (obj.x + obj.surf.get_width() // 2,
                        obj.y + obj.surf.get_height() // 2)
                if point_in_circle(dot1, self.pos, self.radius) or \
                   point_in_circle(dot2, self.pos, self.radius) or \
                   point_in_circle(dot3, self.pos, self.radius) or \
                   point_in_circle(dot4, self.pos, self.radius):
                    return False

        self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)
        pygame.draw.circle(self.surf, self.color, self.pos, self.radius)
        return objects


class Player:
    def __init__(self, parent_surf, pos, speed):
        self.sc = parent_surf
        self.surf = pygame.image.load('images/bug.png').convert()
        self.surf.set_colorkey((255, 255, 255))
        self.degree = 0
        self.type = "player"
        resize = (self.surf.get_width() // 12, self.surf.get_height() // 12)
        self.surf = pygame.transform.scale(self.surf, resize)
        self.x, self.y = pos
        self.speed = speed
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.sc.blit(self.surf, self.rect)

    def move(self, objects):
        keys = pygame.key.get_pressed()
        delta_x = delta_y = 0
        if keys[pygame.K_LEFT]:
            delta_x -= self.speed
            self.degree = 90
        elif keys[pygame.K_RIGHT]:
            delta_x += self.speed
            self.degree = 270
        elif keys[pygame.K_UP]:
            delta_y -= self.speed
            self.degree = 0
        elif keys[pygame.K_DOWN]:
            delta_y += self.speed
            self.degree = 180
        move = True
        rot = pygame.transform.rotate(self.surf, self.degree)
        rot_rect = rot.get_rect(center=(self.x + delta_x, self.y + delta_y))
        dot1 = (self.x - rot.get_width() // 2 + delta_x,
                self.y - rot.get_height() // 2 + delta_y)
        dot2 = (self.x - rot.get_width() // 2 + delta_x,
                self.y + rot.get_height() // 2 + delta_y)
        dot3 = (self.x + rot.get_width() // 2 + delta_x,
                self.y - rot.get_height() // 2 + delta_y)
        dot4 = (self.x + rot.get_width() // 2 + delta_x,
                self.y + rot.get_height() // 2 + delta_y)

        for obj in objects:
            if obj.type == "ball":
                if point_in_circle(dot1, obj.pos, obj.radius) or \
                   point_in_circle(dot2, obj.pos, obj.radius) or \
                   point_in_circle(dot3, obj.pos, obj.radius) or \
                   point_in_circle(dot4, obj.pos, obj.radius):
                    return False
            if obj.type == "wall":
                if point_in_rect(dot1, obj.start, obj.params) or \
                   point_in_rect(dot2, obj.start, obj.params) or \
                   point_in_rect(dot3, obj.start, obj.params) or \
                   point_in_rect(dot4, obj.start, obj.params):
                    move = False
                    break
        if move:
            self.x += delta_x
            self.y += delta_y
        else:
            rot = pygame.transform.rotate(self.surf, self.degree)
            rot_rect = rot.get_rect(center=(self.x, self.y))
        self.sc.blit(rot, rot_rect)
        return True


def init_walls(surface):
    wall_list = []
    wall_list.append(Wall(surface, (0, 0), (WALL_WIDTH, WIN_HEIGHT),
                          WALL_COLOR))
    wall_list.append(Wall(surface, (0, 0), (WIN_WIDTH, WALL_WIDTH),
                          WALL_COLOR))
    wall_list.append(Wall(surface, (WIN_WIDTH - WALL_WIDTH, 0),
                          (WALL_WIDTH, WIN_HEIGHT), WALL_COLOR))
    wall_list.append(Wall(surface, (WALL_WIDTH, WIN_HEIGHT - WALL_WIDTH),
                          (WIN_WIDTH, WALL_WIDTH), WALL_COLOR))

    wall_list.append(Wall(surface, (300, 200),
                          (50, 650), WALL_COLOR))
    wall_list.append(Wall(surface, (300, 200),
                          (900, 50), WALL_COLOR))
    wall_list.append(Wall(surface, (1150, 400),
                          (50, 500), WALL_COLOR))
    wall_list.append(Wall(surface, (1300, 400),
                          (100, 50), WALL_COLOR))
    wall_list.append(Wall(surface, (450, 850),
                          (400, 50), WALL_COLOR))
    wall_list.append(Wall(surface, (600, 450),
                          (50, 200), WALL_COLOR))
    wall_list.append(Wall(surface, (600, 650),
                          (200, 50), WALL_COLOR))
    wall_list.append(Wall(surface, (120, 650),
                          (120, 50), WALL_COLOR))
    wall_list.append(Wall(surface, (90, 450),
                          (210, 50), WALL_COLOR))
    wall_list.append(Wall(surface, (150, 230),
                          (70, 70), WALL_COLOR))
    wall_list.append(Wall(surface, (550, 85),
                          (125, 63), WALL_COLOR))
    wall_list.append(Wall(surface, (950, 90),
                          (50, 90), WALL_COLOR))
    wall_list.append(Wall(surface, (60, 90),
                          (70, 50), WALL_COLOR))
    wall_list.append(Wall(surface, (420, 700),
                          (70, 50), WALL_COLOR))
    return wall_list


def game_start(surface):
    surface.fill(START_MENU_COLOR)

    f = pygame.font.SysFont('arial', 48)
    text = f.render("Добро пожаловать в нашу увлекательную игру!", False,
                    START_TEXT_COLOR)
    text2 = f.render("Ваша задача: уклоняясь от шаров продержаться", False,
                     START_TEXT_COLOR)
    text3 = f.render("на поле как можно дольше", False,
                     START_TEXT_COLOR)
    text4 = f.render("Управление:", False,
                     START_TEXT_COLOR)
    text5 = f.render("Enter - начать игру", False,
                     START_TEXT_COLOR)
    text6 = f.render("Space - остановить игру", False,
                     START_TEXT_COLOR)

    surface.blit(text, (WIN_WIDTH * 0.2, WIN_HEIGHT * 0.3))
    surface.blit(text2, (WIN_WIDTH * 0.2, WIN_HEIGHT * 0.4))
    surface.blit(text3, (WIN_WIDTH * 0.2, WIN_HEIGHT * 0.45))
    surface.blit(text4, (WIN_WIDTH * 0.2, WIN_HEIGHT * 0.55))
    surface.blit(text5, (WIN_WIDTH * 0.2, WIN_HEIGHT * 0.6))
    surface.blit(text6, (WIN_WIDTH * 0.2, WIN_HEIGHT * 0.65))
    pygame.display.update()
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            break
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()


def end_of_game(surface, time):
    surface.fill(BLACK)

    f = pygame.font.SysFont('arial', 48)
    text = f.render("Вы проиграли! Продержавшись {:.2f} секунд".format(time),
                    False, END_TEXT_COLOR)
    text2 = f.render("Чтобы начать заново нажмите Enter", False,
                     END_TEXT_COLOR)

    surface.blit(text, (WIN_WIDTH * 0.3, WIN_HEIGHT * 0.3))
    surface.blit(text2, (WIN_WIDTH * 0.3, WIN_HEIGHT * 0.4))
    pygame.display.update()

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()


def game_restart(surface, wall_list):
    player = Player(sc, PLAYER_START, PLAYER_SPEED)
    obj_list = wall_list + [player]
    surface.fill(BLACK)
    surface.blit(player.surf, player.rect)
    return (time.time(), obj_list, player)


pygame.font.init()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
game_start(sc)
sc.fill(BACKGROUND_COLOR)
pygame.display.update()
game_stop = True
clock = pygame.time.Clock()
player = Player(sc, PLAYER_START, PLAYER_SPEED)
wall_list = init_walls(sc)
obj_list = wall_list + [player]
sc.blit(player.surf, player.rect)
last_gen = start_time = time.time()
dif_time = 0

pygame.display.update()
game_end = False
game_stop = False

while True:
    clock.tick(FPS)
    if game_end:
        end_of_game(sc, dif_time)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            start_time, obj_list, player = game_restart(sc, wall_list)
            dif_time = 0
            game_end = False
        continue
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        if i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
            game_stop = False if game_stop else True
            if game_stop:
                dif_time += time.time()
            else:
                dif_time -= time.time()
    cur_time = time.time()
    if not game_stop:
        if cur_time - last_gen > GENERATOR_FREQ:
            pos = (randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            radius = BALL_RADIUS
            while True:
                unable_create = False
                for obj in obj_list:
                    if obj.type == "ball" and \
                       (pos[0] - obj.pos[0]) ** 2 + \
                       (pos[1] - obj.pos[1])**2 <= (radius + obj.radius) ** 2:
                        unable_create = True
                        break
                    if obj.type == "wall":
                        dif = (pos[0] - obj.start[0], pos[1] - obj.start[1])
                        x1, x2 = obj.start[0], obj.start[0] + obj.params[0]
                        y1, y2 = obj.start[1], obj.start[1] + obj.params[1]
                        if 0 <= dif[0] <= obj.params[0] and \
                           0 <= dif[1] <= obj.params[1] or \
                           intercect_line_circle(*pos, radius, x1, y1,
                                                 x1, y2) or \
                           intercect_line_circle(*pos, radius, x2, y1,
                                                 x2, y2) or \
                           intercect_line_circle(*pos, radius, x1, y1,
                                                 x2, y1) or \
                           intercect_line_circle(*pos, radius, x1, y2,
                                                 x2, y2):
                            unable_create = True
                            break
                    if obj.type == "player":
                        dot1 = (obj.x - obj.surf.get_width() // 2,
                                obj.y - obj.surf.get_height() // 2)
                        dot2 = (obj.x - obj.surf.get_width() // 2,
                                obj.y + obj.surf.get_height() // 2)
                        dot3 = (obj.x + obj.surf.get_width() // 2,
                                obj.y - obj.surf.get_height() // 2)
                        dot4 = (obj.x + obj.surf.get_width() // 2,
                                obj.y + obj.surf.get_height() // 2)
                        if point_in_circle(dot1, pos, radius) or \
                           point_in_circle(dot2, pos, radius) or \
                           point_in_circle(dot3, pos, radius) or \
                           point_in_circle(dot4, pos, radius):
                            unable_create = True
                            break
                if not unable_create:
                    new_elem = Ball(sc, pos, color, radius)
                    obj_list.append(new_elem)
                    break
                pos = (randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT))
            last_gen = time.time()

        sc.fill(BACKGROUND_COLOR)
        tmp = obj_list
        if obj_list:
            if player.move(tmp):
                for elem in obj_list:
                    if elem.type == "ball":
                        tmp = elem.move(tmp)
                        if not tmp:
                            game_end = True
                            dif_time += time.time() - start_time
                            break
                    if elem.type == "wall":
                        elem.draw()
                obj_list = tmp
            else:
                game_end = True
                dif_time += time.time() - start_time

    pygame.display.update()
