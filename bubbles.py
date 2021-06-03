from random import randint, random
import pygame
import sys
 
WIN_WIDTH = 1980
WIN_HEIGHT = 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
 
 
class Circle:
    def __init__(self, surface, pos, color, radius, speed=None):
        """Конструктору необходимо передать
        поверхность, по которой будет летать
        ракета и цвет самой ракеты"""
        self.surf = surface
        self.pos = pos
        self.color = color
        self.radius = radius
        self.speed = 5 * random() if not speed else speed
        self.dx = 2 * self.speed * random() - self.speed
        self.dy = 2 * self.speed * random() - self.speed
        pygame.draw.circle(self.surf, self.color, self.pos, self.radius)

    def move(self):
        self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)
        if self.pos[0] < 0 or self.pos[0] > WIN_WIDTH:
            self.pos = (0, self.pos[1]) if self.pos[0] < 0 else (WIN_WIDTH, self.pos[1])
            self.dx *= -1
        if self.pos[1] < 0 or self.pos[1] > WIN_HEIGHT:
            self.pos = (self.pos[0], 0) if self.pos[1] < 0 else (self.pos[0], WIN_HEIGHT)
            self.dy *= -1
        pygame.draw.circle(self.surf, self.color, self.pos, self.radius)
 
 
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
sc.fill(BLACK)
pygame.display.update()
circle_list = []

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
            pos = pygame.mouse.get_pos()
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            radius = random() * 10 + 20
            new_elem = Circle(sc, pos, color, radius)
            circle_list.append(new_elem)

    sc.fill((0, 0, 0))
    for elem in circle_list:
        elem.move()
    pygame.display.update()
    pygame.time.delay(20)