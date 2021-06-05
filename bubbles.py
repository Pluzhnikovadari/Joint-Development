from random import randint, random
import pygame
import sys
 
WIN_WIDTH = 1500
WIN_HEIGHT = 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
 
 
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
        flag = True
        if self.pos[0] < 0 or self.pos[0] > WIN_WIDTH:
            self.pos = (0, self.pos[1]) if self.pos[0] < 0 \
                                        else (WIN_WIDTH, self.pos[1])
            self.dx *= -1
        elif self.pos[1] < 0 or self.pos[1] > WIN_HEIGHT:
            self.pos = (self.pos[0], 0) if self.pos[1] < 0 \
                                        else (self.pos[0], WIN_HEIGHT)
            self.dy *= -1
        else:
            for obj in objects:
                if (self.pos[0] + self.dx - obj.pos[0]) ** 2 \
                        + (self.pos[1] + self.dy - obj.pos[1]) ** 2 \
                        <= (self.radius + obj.radius) ** 2 \
                        and (self.pos[0] != obj.pos[0] or self.pos[1] != obj.pos[1]):
                    tmp = (self.dx, self.dy)
                    dif_rad = self.radius ** 2 - obj.radius ** 2
                    sum_rad = self.radius ** 2 + obj.radius ** 2
                    self.dx = (dif_rad * self.dx + \
                               2 * (obj.radius ** 2) * obj.dx) / sum_rad
                    self.dy = (dif_rad * self.dy + \
                               2 * (obj.radius ** 2) * obj.dy) / sum_rad
                    obj.dx = (-dif_rad * obj.dx + \
                              2 * (self.radius ** 2) * tmp[0]) / sum_rad
                    obj.dy = (-dif_rad * obj.dy + \
                              2 * (self.radius ** 2) * tmp[1]) / sum_rad
                    obj.pos = (obj.pos[0] + obj.dx, obj.pos[1] + obj.dy)
            self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)
        pygame.draw.circle(self.surf, self.color, self.pos, self.radius)
        return objects
 
 
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
sc.fill(BLACK)
pygame.display.update()
circle_list = []
motion = True
clock = pygame.time.Clock()

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
            for obj in circle_list:
                if (pos[0] - obj.pos[0]) ** 2 + (pos[1] - obj.pos[1]) ** 2 \
                        <= (radius + obj.radius) ** 2:
                    flag = False
                    break
            if flag:
                new_elem = Ball(sc, pos, color, radius)
                circle_list.append(new_elem)
        if i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
            motion = False if motion else True

    if motion:
        sc.fill((0, 0, 0))
        tmp = circle_list
        for elem in circle_list:
            tmp = elem.move(tmp)
        circle_list = tmp
    pygame.display.update()