import pygame
import time
import random
 
pygame.init()
 
sc = (0, 0, 0)
snake = (102, 51, 0)
red = (139, 0, 0)
black = (0, 0, 0)
ground = (154, 205, 50)
food = [(139, 0, 0), (102, 0, 102), (0, 51, 51), (255, 204, 0)]
 
dis_width = 600
dis_height = 400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

inp = ''

def input_name():
    input_box = pygame.Rect(100, 100, 140, 32)
    color = pygame.Color('dodgerblue2')
    name = ''
    done = False
    global inp

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE and inp:
                    inp = inp[:-1]
                else:
                    inp += event.unicode

        dis.fill(ground)
        txt_surface = font_style.render(inp, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        dis.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(dis, color, input_box, 2)
        pygame.display.flip()
 
 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, sc)
    dis.blit(value, [0, 0])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, snake, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
 
def gameLoop():
    game_over = False
    game_close = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1

    col = random.choice(food)
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
 
        while game_close == True:
            dis.fill(ground)
            message("Your score: " + str(Length_of_snake - 1), red)

            file = open('score_snake.txt', 'r')
            data = file.readlines()
            table = []
            for el in data:
                if el:
                    name, s = el[:-1].split(" ")
                    table.append([int(s), name])
            table.append([Length_of_snake - 1, inp])
            table.sort()
            table = table[::-1]
            if len(table) > 5:
                table = table[:5]
            mesg = font_style.render("Best results:", True, black)
            dis.blit(mesg, [dis_width / 6, dis_height / 3 + 20])
            for i, elem in enumerate(table):
                mesg = font_style.render(elem[1] + " " + str(elem[0]), True, black)
                dis.blit(mesg, [dis_width / 6, dis_height / 3 + (i +2) * 20])
            pygame.display.update()


            time.sleep(3)

            file = open('score_snake.txt', 'w')
            text = ""
            for el in table:
                text += el[1] + " " + str(el[0]) + "\n"
            file.write(text)
            game_over = True
            game_close = False
            file.close()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(ground)
        pygame.draw.rect(dis, col, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            col = random.choice(food)
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
input_name()
gameLoop()