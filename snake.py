"""Snake game."""
import pygame
import time
import random
import sys
sc = (0, 0, 0)
snake = (102, 51, 0)
red = (139, 0, 0)
black = (0, 0, 0)
ground = (154, 205, 50)
food = [(139, 0, 0), (102, 0, 102), (0, 51, 51), (255, 204, 0)]
dis_width = 600
dis_height = 400
snake_block = 10
snake_speed = 15


def input_name(dis, font_style, inp):
    """Introdusing and options."""
    input_box = pygame.Rect(100, 100, 140, 32)
    color = pygame.Color('dodgerblue2')
    done = False

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
                    if len(inp) < 20:
                        inp += event.unicode

        dis.fill(ground)
        mesg = font_style.render("Input your name", True, black)
        dis.blit(mesg, [100, 80])
        mesg = font_style.render("For moving use arrows, for pause use space",
                                 True, black)
        dis.blit(mesg, [100, 40])
        txt_surface = font_style.render(inp, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        dis.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(dis, color, input_box, 2)
        pygame.display.flip()
    return inp


def Your_score(dis, score, score_font):
    """Visualization of score."""
    value = score_font.render("Your Score: " + str(score), True, sc)
    dis.blit(value, [0, 0])


def our_snake(dis, snake_block, snake_list):
    """Drawing snake."""
    for x in snake_list:
        pygame.draw.rect(dis, snake, [x[0], x[1], snake_block, snake_block])


def message(dis, msg, color, font_style):
    """Drawing system messages."""
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop(dis, clock, font_style, score_font, paused, inp):
    """Loop of game."""
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

        while game_close:
            dis.fill(ground)
            message(dis, "Your score: " + str(Length_of_snake - 1),
                    red, font_style)

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
                mesg = font_style.render(elem[1] + " " + str(elem[0]),
                                         True, black)
                dis.blit(mesg, [dis_width / 6, dis_height / 3 + (i + 2) * 20])
            pygame.display.update()

            time.sleep(3)

            file.close()
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
                pygame.quit()
                sys.exit()
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
                elif event.key == pygame.K_SPACE:
                    paused = not paused

        if paused:
            dis.fill(ground)
            mesg = font_style.render("Paused", True, black)
            dis.blit(mesg, [260, 200])
            pygame.display.update()
        else:
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True
            x1 += x1_change
            y1 += y1_change
            dis.fill(ground)
            pygame.draw.rect(dis, col, [foodx, foody,
                             snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            our_snake(dis, snake_block, snake_List)
            Your_score(dis, Length_of_snake - 1, score_font)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                col = random.choice(food)
                foodx = round(random.randrange(
                    0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(
                    0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


def main():
    """App starting function."""
    inp = ''
    paused = False
    pygame.init()
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)

    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    inp = input_name(dis, font_style, inp)
    gameLoop(dis, clock, font_style, score_font, paused, inp)


if __name__ == '__main__':
    main()
