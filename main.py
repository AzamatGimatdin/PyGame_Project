import pygame, random


class Board:
    def __init__(self):
        # создаются размеры и координаты поля
        self.width = 12
        self.height = 22
        self.board = [[0] * self.width for _ in range(self.height)]
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
                                    self.cell_size), width=2)
                else:
                    pygame.draw.rect(screen, pygame.Color('black'), (self.left + partx, self.top + party, self.cell_size, 
                                    self.cell_size))
    
    # функция, которая будет обновлять поле каждый тик игры
    def update_field(self):
        pass

# класс, создающий кирпичики в тетрисе
class Bricks:
    def __init__(self):
        self.left = 40
        self.top = 10
        self.cell_size = 35
        # это список с кортежами всех существующих кирпичей в тетрисе
        # первый элемент - буква кирпича, форма которого похожа на него
        # второй элемент - цвет закрашивания самого квадратика кирпича
        # третий элемент - цвет закрашивания сторон квадратика кирпича
        # второй от третьего отличается немного, просто цвет сторон немного темнее
        # цвета я подбирал в rgb палитре, так что цифры могут показаться случайными
        self.bricks_list = [("I", (3, 240, 252), (7, 175, 184)), ("J", (7, 7, 184), (6, 6, 120)), 
                            ("L", (237, 142, 9), (201, 118, 2)), ("O", (237, 237, 5), (184, 184, 11)), 
                            ("S", (35, 232, 9), (22, 166, 3)), ("T", (132, 2, 219), (95, 0, 158)), 
                            ("Z", (219, 17, 2), (173, 12, 0))]
    # тут функция спавна кирпичей
    def spawn_brick(self):
        self.next_brick = self.bricks_list[random.randint(0, 3)]
        # тут просто определяю тип кирпича по букве и уже создаю сам кирпич
        if self.next_brick[0] == "I":
            # это число будет определять будет определять в по какому x заспавнится кирпичик
            self.random_x = random.randint(1, 10)
            for i in range(1, 5):
                pygame.draw.rect(screen, pygame.Color(self.next_brick[1]), (self.left + self.cell_size * self.random_x, 
                                self.top + self.cell_size * i, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color(self.next_brick[2]), (self.left + self.cell_size * self.random_x, 
                                self.top + self.cell_size * i, self.cell_size, self.cell_size), width=3)
        elif self.next_brick[0] == "J":
            self.random_x = random.randint(2, 10)
            for i in range(1, 4):
                pygame.draw.rect(screen, pygame.Color(self.next_brick[1]), (self.left + self.cell_size * self.random_x, 
                                self.top + self.cell_size * i, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color(self.next_brick[2]), (self.left + self.cell_size * self.random_x, 
                                self.top + self.cell_size * i, self.cell_size, self.cell_size), width=3)
            pygame.draw.rect(screen, pygame.Color(self.next_brick[1]), (self.left + self.cell_size * (self.random_x - 1), 
                            self.top + self.cell_size * 3, self.cell_size, self.cell_size))
            pygame.draw.rect(screen, pygame.Color(self.next_brick[2]), (self.left + self.cell_size * (self.random_x - 1), 
                            self.top + self.cell_size * 3, self.cell_size, self.cell_size), width=3)
        elif self.next_brick[0] == "L":
            self.random_x = random.randint(1, 9)
            for i in range(1, 4):
                pygame.draw.rect(screen, pygame.Color(self.next_brick[1]), (self.left + self.cell_size * self.random_x, 
                                self.top + self.cell_size * i, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color(self.next_brick[2]), (self.left + self.cell_size * self.random_x, 
                                self.top + self.cell_size * i, self.cell_size, self.cell_size), width=3)
            pygame.draw.rect(screen, pygame.Color(self.next_brick[1]), (self.left + self.cell_size * (self.random_x + 1), 
                            self.top + self.cell_size * 3, self.cell_size, self.cell_size))
            pygame.draw.rect(screen, pygame.Color(self.next_brick[2]), (self.left + self.cell_size * (self.random_x + 1), 
                            self.top + self.cell_size * 3, self.cell_size, self.cell_size), width=3)
        elif self.next_brick[0] == "O":
            self.random_x = random.randint(1, 9)
            for i in range(0, 2):
                pygame.draw.rect(screen, pygame.Color(self.next_brick[1]), (self.left + self.cell_size * (self.random_x + i), 
                                self.top + self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color(self.next_brick[2]), (self.left + self.cell_size * (self.random_x + i), 
                                self.top + self.cell_size, self.cell_size, self.cell_size), width=3)
            for i in range(0, 2):
                pygame.draw.rect(screen, pygame.Color(self.next_brick[1]), (self.left + self.cell_size * (self.random_x + i), 
                                self.top + self.cell_size * 2, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color(self.next_brick[2]), (self.left + self.cell_size * (self.random_x + i), 
                                self.top + self.cell_size * 2, self.cell_size, self.cell_size), width=3)
pygame.init()
board = Board()
bricks = Bricks()
pygame.display.set_caption('Тетрис')
size = width, height = 500, 800
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color((255, 255, 255)))
fps = 60
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
    if ticks == 100:
        bricks.spawn_brick()
        ticks = 0
    else:
        ticks += 1
    pygame.display.flip()
