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
        self.board = [[0] * (self.width - 2) for _ in range(self.height - 2)]
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
                        print(self.bricks_dict[self.board[i - 1][j - 1]][0])
                        # если клетка не равна нулю, то в словаре по букве находятся цвета кирпичей и рисуются на доске
                        pygame.draw.rect(screen, pygame.Color(self.bricks_dict[self.board[i - 1][j - 1]][0]), 
                                        (self.left + partx, self.top + party, self.cell_size, self.cell_size))
                        pygame.draw.rect(screen, pygame.Color(self.bricks_dict[self.board[i - 1][j - 1]][1]), 
                                        (self.left + partx, self.top + party, self.cell_size, self.cell_size), width=3)
    # функция, которая будет создавать кирпичи в self.board
    def spawn_brick(self):
        self.brick = []
        temp = [i for i in self.bricks_dict]
        self.next_brick = random.choice(temp)
        # тут просто определяю тип кирпича и его координаты
        if self.next_brick == "I":
            # это число будет определять будет определять в по какому x заспавнится кирпичик
            self.random_x = random.randint(1, 10)
            for i in range(1, 5):
                self.board[i - 1][self.random_x - 1] = "I"
                self.brick.append([i - 1, self.random_x - 1]) 
            self.brick.append("I") 
        elif self.next_brick == "J":
            self.random_x = random.randint(2, 10)
            for i in range(1, 4):
                self.board[i - 1][self.random_x - 1] = "J"
                self.brick.append([i - 1, self.random_x - 1]) 
            self.board[2][self.random_x - 2] = "J"
            self.brick.append([2, self.random_x - 2]) 
            self.brick.append("J")
        elif self.next_brick == "L":
            self.random_x = random.randint(1, 9)
            for i in range(1, 4):
                self.board[i - 1][self.random_x - 1] = "L"
                self.brick.append([i - 1, self.random_x - 1]) 
            self.board[2][self.random_x] = "L"
            self.brick.append([2, self.random_x]) 
            self.brick.append("L")
        elif self.next_brick == "O":
            self.random_x = random.randint(1, 9)
            for i in range(0, 2):
                self.board[0][self.random_x + i - 1] = "O"
                self.brick.append([0, self.random_x + i - 1]) 
            for i in range(0, 2):
                self.board[1][self.random_x + i - 1] = "O"
                self.brick.append([1, self.random_x + i - 1]) 
            self.brick.append("O")
        elif self.next_brick == "S":
            self.random_x = random.randint(2, 9)
            for i in range(0, 2):
                self.board[0][self.random_x + i - 1] = "S"
                self.brick.append([0, self.random_x + i - 1]) 
            for i in range(0, 2):
                self.board[1][self.random_x + i - 2] = "S"
                self.brick.append([1, self.random_x + i - 1]) 
            self.brick.append("S")
        elif self.next_brick == "T":
            self.random_x = random.randint(1, 8)
            for i in range(0, 3):
                self.board[0][self.random_x + i - 1] = "T"
                self.brick.append([0, self.random_x + i - 1]) 
            self.board[1][self.random_x] = "T"
            self.brick.append([1, self.random_x]) 
            self.brick.append("T")
        elif self.next_brick == "Z":
            self.random_x = random.randint(1, 8)
            for i in range(0, 2):
                self.board[0][self.random_x + i - 1] = "Z"
                self.brick.append([0, self.random_x + i - 1]) 
            for i in range(0, 2):
                self.board[1][self.random_x + i] = "Z"
                self.brick.append([1, self.random_x + i]) 
            self.brick.append("Z")
    # функция, которая будет обновлять поле каждый тик
    def update_field(self):
        letter = self.brick.pop()
        self.brick = sorted(self.brick, key=lambda x:x[0], reverse=True)
        self.brick.append(letter)
        flag = True
        for i in range(len(self.brick) - 1):
            if self.brick[i][0] == 19:
                flag = False
                break
            else:
                if self.board[self.brick[i][0] + 1][self.brick[i][1]] != 0 and [self.brick[i][0] + 1, self.brick[i][1]] not in self.brick:
                    flag = False
                    break
        if flag:
            for i in range(len(self.brick) - 1):
                print([self.brick[i][0]][self.brick[i][1]])
                print([self.brick[i][0]][self.brick[i][1]])
                self.board[self.brick[i][0]][self.brick[i][1]], self.board[self.brick[i][0] + 1][self.brick[i][1]] = self.board[self.brick[i][0] + 1][self.brick[i][1]], self.board[self.brick[i][0]][self.brick[i][1]]
                self.brick[i][0] += 1
        for i in range(20):
            print(self.board[i])
        print("\n\n")
                        
      #  for i in range(18, -1, -1):
        #    for j in range(10):
       #         if self.board[i][j] != 0:
       #             for brick in self.field_bricks:
       #                 if (i, j) in brick and brick[4] == True:
       #                     self.board[i][j], self.board[i + 1][j] = self.board[i + 1][j], self.board[i][j]
        #                    for n in range(len(brick) - 1):
       #                         brick[n] = list(brick[n])
        #                        brick[n][0] += 1
        #                        brick[n] = tuple(brick[n])
        #        for b in self.board:
        #            print(b)
        #        print("\n\n")


pygame.init()
board = Board()
pygame.display.set_caption('Тетрис')
size = width, height = 500, 800
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color((255, 255, 255)))
fps = 5
ticks = 10
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
    board.update_field()
    board.render(screen)
    pygame.display.flip()
