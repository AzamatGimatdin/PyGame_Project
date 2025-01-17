import pygame, random


class Board:
    def __init__(self):
        # это список с кортежами всех существующих кирпичей в тетрисе
        # первый элемент - буква кирпича, форма которого похожа на него
        # второй элемент - цвет закрашивания самого квадратика кирпича
        # третий элемент - цвет закрашивания сторон квадратика кирпича
        # второй от третьего отличается немного, просто цвет сторон немного темнее
        # цвета я подбирал в rgb палитре, так что цифры могут показаться случайными
        self.bricks_dict = {"I":[(3, 240, 252), (7, 175, 184)], "J": [(7, 7, 184), (6, 6, 120)], 
                            "L": [(237, 142, 9), (201, 118, 2)], "O": [(237, 237, 5), (184, 184, 11)], 
                            "S": [(35, 232, 9), (22, 166, 3)], "T": [(132, 2, 219), (95, 0, 158)], 
                            "Z": [(219, 17, 2), (173, 12, 0)]}
        # создаются размеры и координаты поля
        self.width = 12
        self.height = 22
        self.board = [[0] * (self.width - 2) for _ in range(self.height - 2)]
        # это отход поля от левой стороны
        self.left = 40
        # это отход поля от верхней стороны
        self.top = 10
        # это размер каждого квадрата
        self.cell_size = 35

    def render(self, screen):
        for i in range(self.height):
            party = self.cell_size * i
            for j in range(self.width):
                partx = self.cell_size * j
                # это условие для крайних клеток, если выполняется, то они рисуются серыми, если нет - заполняются черным
                if i == 0 or i == 21 or j == 0 or j == 11:
                    pygame.draw.rect(screen, pygame.Color((62, 68, 79)), (self.left + partx, self.top + party, self.cell_size, 
                                    self.cell_size))
                    pygame.draw.rect(screen, pygame.Color((23, 25, 31)), (self.left + partx, self.top + party, self.cell_size, 
                                    self.cell_size), width=3)
                else:
                    if self.board[i - 1][j - 1] == 0:
                        pygame.draw.rect(screen, pygame.Color('black'), (self.left + partx, self.top + party, self.cell_size, 
                                        self.cell_size))
                    else:
                        # если клетка не равна нулю, то в словаре по букве находятся цвета кирпичей и рисуются на доске
                        pygame.draw.rect(screen, pygame.Color(self.bricks_dict[self.board[i - 1][j - 1]][0]), 
                                        (self.left + partx, self.top + party, self.cell_size, self.cell_size))
                        pygame.draw.rect(screen, pygame.Color(self.bricks_dict[self.board[i - 1][j - 1]][1]), 
                                        (self.left + partx, self.top + party, self.cell_size, self.cell_size), width=3)
    # функция, которая будет создавать кирпичи в self.board
    def spawn_brick(self):
        temp = [i for i in self.bricks_dict]
        self.next_brick = random.choice(temp)
        # тут просто определяю тип кирпича и его координаты
        if self.next_brick == "I":
            # это число будет определять будет определять в по какому x заспавнится кирпичик
            self.random_x = random.randint(1, 10)
            for i in range(1, 5):
                self.board[i - 1][self.random_x - 1] = "I" 
        elif self.next_brick == "J":
            self.random_x = random.randint(2, 10)
            for i in range(1, 4):
                self.board[i - 1][self.random_x - 1] = "J"
            self.board[2][self.random_x - 2] = "J"
        elif self.next_brick == "L":
            self.random_x = random.randint(1, 9)
            for i in range(1, 4):
                self.board[i - 1][self.random_x - 1] = "L"
            self.board[2][self.random_x] = "L"
        elif self.next_brick == "O":
            self.random_x = random.randint(1, 9)
            for i in range(0, 2):
                self.board[0][self.random_x + i - 1] = "O"
            for i in range(0, 2):
                self.board[1][self.random_x + i - 1] = "O"
        elif self.next_brick == "S":
            self.random_x = random.randint(2, 9)
            for i in range(0, 2):
                self.board[0][self.random_x + i - 1] = "S"
            for i in range(0, 2):
                self.board[1][self.random_x + i - 2] = "S"
        elif self.next_brick == "T":
            self.random_x = random.randint(1, 8)
            for i in range(0, 3):
                self.board[0][self.random_x + i - 1] = "T"
            self.board[1][self.random_x] = "T"
        elif self.next_brick == "Z":
            self.random_x = random.randint(1, 8)
            for i in range(0, 2):
                self.board[0][self.random_x + i - 1] = "Z"
            for i in range(0, 2):
                self.board[1][self.random_x + i] = "Z"
    # функция, которая будет обновлять поле каждый тик
    def update_field(self):
        for i in range(18, -1, -1):
            for j in range(10):
                if self.board[i][j] != 0 and self.board[i + 1][j] == 0:
                    self.board[i][j], self.board[i + 1][j] = self.board[i + 1][j], self.board[i][j]

pygame.init()
board = Board()
pygame.display.set_caption('Тетрис')
size = width, height = 500, 800
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color((255, 255, 255)))
fps = 5
ticks = 0
running = True
clock = pygame.time.Clock()
board.render(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(fps)
    # я ввел условие, которое будет вызывать функцию спавна не каждый тик, а только раз в несколько
    if ticks == 10:
        board.spawn_brick()
        ticks = 0
    else:
        ticks += 1
    board.render(screen)
    board.update_field()
    pygame.display.flip()
