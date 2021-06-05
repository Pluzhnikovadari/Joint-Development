import pygame
import sys


class Game:
    size_block = 100
    margin = 1
    width = heigth = size_block * 3 + margin * 3
    size_window = (width, heigth)
    black = (0, 0, 0)
    red = (255, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    end = ''
    mas = [[0] * 3 for _ in range(3)]
    query = 0
    screen = 1

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.size_window)
        pygame.display.set_caption('TicTacToe')
        self.game_loop()

    def mouse(self):

        x_mouse, y_mouse = pygame.mouse.get_pos()
        col = x_mouse // (Game.size_block + Game.margin)
        row = y_mouse // (Game.size_block + Game.margin)
        if not self.mas[row][col]:
            if self.query % 2:
                self.mas[row][col] = 'o'
            else:
                self.mas[row][col] = 'x'
            self.query += 1

    def space(self):
        self.query = 0
        self.mas = [[0] * 3 for _ in range(3)]
        self.end = ''
        self.screen.fill(Game.black)

    def draw_x(self, x, y):
        pygame.draw.line(self.screen, Game.white, (x + 2, y + 2),
                         (x + Game.size_block - 2, y + Game.size_block - 2), 3)
        pygame.draw.line(self.screen, Game.white,
                         (x + 2, y + Game.size_block - 2),
                         (x + Game.size_block - 2, y + 2), 3)

    def draw_o(self, x, y):
        pygame.draw.circle(self.screen, Game.white,
                           (x + Game.size_block // 2,
                            y + Game.size_block // 2),
                           Game.size_block // 2 - 3, 3)

    def check_winner(self):
        win = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (2, 4, 6),
               (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8)]
        for i in win:
            if self.mas[i[0] // 3][i[0] % 3] == \
                    self.mas[i[1] // 3][i[1] % 3] == \
                    self.mas[i[2] // 3][i[2] % 3] == 'x':
                return 'First player wins'
            if self.mas[i[0] // 3][i[0] % 3] == \
                    self.mas[i[1] // 3][i[1] % 3] == \
                    self.mas[i[2] // 3][i[2] % 3] == 'o':
                return 'Second player wins'
        if self.query == 9:
            return 'Draw'
        return 0

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.end:
                    self.mouse()
                elif event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_SPACE:
                    self.space()

            if not self.end:
                for row in range(3):
                    for col in range(3):
                        if self.mas[row][col] == 'x':
                            self.color = Game.green
                        elif self.mas[row][col] == 'o':
                            self.color = Game.red
                        else:
                            self.color = Game.white
                        x = col * Game.size_block + (col + 1) * Game.margin
                        y = row * Game.size_block + (row + 1) * Game.margin
                        pygame.draw.rect(self.screen, self.color,
                                         (x, y, Game.size_block,
                                          Game.size_block))
                        if self.color == Game.green:
                            self.draw_x(x, y)
                        elif self.color == Game.red:
                            self.draw_o(x, y)
            self.end = self.check_winner()
            if self.end:
                self.screen.fill(Game.black)
                font = pygame.font.SysFont('stxingkai', 20)
                text1 = font.render(self.end, True, Game.white)
                text_rect = text1.get_rect()
                text_x = self.screen.get_width() / 2 - text_rect.width / 2
                text_y = self.screen.get_height() / 2 - text_rect.height / 2
                self.screen.blit(text1, (text_x, text_y))
            pygame.display.update()


if __name__ == '__main__':
    Game().start()
