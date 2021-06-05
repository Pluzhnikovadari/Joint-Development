from random import randint, random
import pygame
import sys

WIN_WIDTH = 1500
WIN_HEIGHT = 1000
WALL_WIDTH = 30
WALL_WIDTH_2 = 50
WALL_HEIGHT_2 = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60


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

        self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)
        pygame.draw.circle(self.surf, self.color, self.pos, self.radius)
        return objects


def init_walls(surface):
    wall_list = []
    wall_list.append(Wall(surface, (0, 0), (WALL_WIDTH, WIN_HEIGHT), RED))
    wall_list.append(Wall(surface, (0, 0), (WIN_WIDTH, WALL_WIDTH), RED))
    wall_list.append(Wall(surface, (WIN_WIDTH - WALL_WIDTH, 0),
                          (WALL_WIDTH, WIN_HEIGHT), RED))
    wall_list.append(Wall(surface, (WALL_WIDTH, WIN_HEIGHT - WALL_WIDTH),
                          (WIN_WIDTH, WALL_WIDTH), RED))
    wall_list.append(Wall(surface, (WIN_WIDTH // 2, WIN_HEIGHT // 2),
                          (WALL_WIDTH, WALL_WIDTH), RED))
    wall_list.append(Wall(surface, (WIN_WIDTH // 4, WIN_HEIGHT * 0.3),
                          (WALL_WIDTH_2, WALL_HEIGHT_2), RED))
    return wall_list

def description():
    print("Нажмите левой кнопкой мыши на экран, чтобы сгенирировать\n" + \
          "шар, который будет двигаться в случайном направлении.\n" + \
          "Чтобы остановить игру, нажмите Пробел")

description()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
sc.fill(BLACK)
pygame.display.update()
motion = True
clock = pygame.time.Clock()

obj_list = init_walls(sc)


while 1:
    clock.tick(FPS)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
            pos = pygame.mouse.get_pos()
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            radius = random() * 10 + 20
            flag = True
            for obj in obj_list:
                if obj.type == "ball" and \
                   (pos[0] - obj.pos[0]) ** 2 + \
                   (pos[1] - obj.pos[1])**2 <= (radius + obj.radius) ** 2:
                    flag = False
                    break
                if obj.type == "wall":
                    dif = (pos[0] - obj.start[0], pos[1] - obj.start[1])
                    if 0 <= dif[0] <= obj.params[0] and \
                       0 <= dif[1] <= obj.params[1] or \
                       intercect_line_circle(*pos, radius, *obj.start,
                                             obj.start[0],
                                             obj.start[1] + obj.params[1]) or \
                       intercect_line_circle(*pos, radius,
                                             obj.start[0] + obj.params[0],
                                             obj.start[1],
                                             obj.start[0] + obj.params[0],
                                             obj.start[1] + obj.params[1]) or \
                       intercect_line_circle(*pos, radius, *obj.start,
                                             obj.start[0] + obj.params[0],
                                             obj.start[1]) or \
                       intercect_line_circle(*pos, radius, obj.start[0],
                                             obj.start[1] + obj.params[1],
                                             obj.start[0] + obj.params[0],
                                             obj.start[1] + obj.params[1]):
                        flag = False
                        break
            if flag:
                new_elem = Ball(sc, pos, color, radius)
                obj_list.append(new_elem)
        if i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
            motion = False if motion else True

    if motion:
        sc.fill((0, 0, 0))
        tmp = obj_list
        for elem in obj_list:
            if elem.type == "ball":
                tmp = elem.move(tmp)
            if elem.type == "wall":
                elem.draw()
        obj_list = tmp

    pygame.display.update()
