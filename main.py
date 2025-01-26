import pygame, random


class Board:
    def __init__(self):
        self.num = -1
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
        self.score = 0
        self.game = True

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
                        pygame.draw.rect(screen, pygame.Color(self.bricks_dict[self.board[i - 1][j - 1][0]][0]), 
                                        (self.left + partx, self.top + party, self.cell_size, self.cell_size))
                        pygame.draw.rect(screen, pygame.Color(self.bricks_dict[self.board[i - 1][j - 1][0]][1]), 
                                        (self.left + partx, self.top + party, self.cell_size, self.cell_size), width=3)
    # функция, которая будет создавать кирпичи в self.board
    def spawn_brick(self):
        self.move = 1
        self.angle = 1
        self.num += 1
        temp = [i for i in self.bricks_dict]
        self.next_brick = random.choice(temp)
        # тут просто определяю тип кирпича и его координаты, а также проверяю, можно ли вообще создать кирпич
        if self.next_brick == "I":
            # это число будет определять будет определять в по какому x заспавнится кирпичик
            self.random_x = random.randint(1, 10)
            for i in range(1, 5):
                if self.board[i - 1][self.random_x - 1] != 0:
                    self.game = False
                    break
                self.board[i - 1][self.random_x - 1] = "I" + str(self.num)
        elif self.next_brick == "J":
            self.random_x = random.randint(2, 10)
            for i in range(1, 4):
                if self.board[i - 1][self.random_x - 1] != 0:
                    self.game = False
                    return
                self.board[i - 1][self.random_x - 1] = "J" + str(self.num)
            if self.board[2][self.random_x - 2] != 0:
                self.game = False
                return
            self.board[2][self.random_x - 2] = "J" + str(self.num)
        elif self.next_brick == "L":
            self.random_x = random.randint(1, 9)
            for i in range(1, 4):
                if self.board[i - 1][self.random_x - 1] != 0:
                    self.game = False
                    return
                self.board[i - 1][self.random_x - 1] = "L" + str(self.num)
            if self.board[2][self.random_x] != 0:
                    self.game = False
                    return
            self.board[2][self.random_x] = "L" + str(self.num)
        elif self.next_brick == "O":
            self.random_x = random.randint(1, 9)
            for i in range(0, 2):
                if self.board[0][self.random_x + i - 1] != 0:
                    self.game = False
                    return
                self.board[0][self.random_x + i - 1] = "O" + str(self.num)
            for i in range(0, 2):
                if self.board[1][self.random_x + i - 1] != 0:
                    self.game = False
                    return
                self.board[1][self.random_x + i - 1] = "O" + str(self.num)
        elif self.next_brick == "S":
            self.random_x = random.randint(2, 9)
            for i in range(0, 2):
                if self.board[0][self.random_x + i - 1] != 0:
                    self.game = False
                    return
                self.board[0][self.random_x + i - 1] = "S" + str(self.num)
            for i in range(0, 2):
                if self.board[1][self.random_x + i - 2] != 0:
                    self.game = False
                    return
                self.board[1][self.random_x + i - 2] = "S" + str(self.num)
        elif self.next_brick == "T":
            self.random_x = random.randint(1, 8)
            for i in range(0, 3):
                if self.board[0][self.random_x + i - 1] != 0:
                    self.game = False
                    return
                self.board[0][self.random_x + i - 1] = "T" + str(self.num)
            if self.board[1][self.random_x] != 0:
                    self.game = False
                    return
            self.board[1][self.random_x] = "T" + str(self.num)
        elif self.next_brick == "Z":
            self.random_x = random.randint(1, 8)
            for i in range(0, 2):
                if self.board[0][self.random_x + i - 1] != 0:
                    self.game = False
                    return
                self.board[0][self.random_x + i - 1] = "Z" + str(self.num)
            for i in range(0, 2):
                if self.board[1][self.random_x + i] != 0:
                    self.game = False
                    return
                self.board[1][self.random_x + i] = "Z" + str(self.num)
    # функция, которая будет обновлять поле каждый тик
    def update_field(self):
        flag = True
        temp = []
        # этими циклами я определяю, можно ли блоку двигаться
        for o in range(20):
            for n in range(10):
                if self.board[o][n] != 0 and self.board[o][n][1:] == str(self.num):
                    temp.append([o, n])
        for n in temp:
            if n[0] <= 18:
                if self.board[n[0] + 1][n[1]] != 0 and [n[0] + 1, n[1]] not in temp:
                    flag = False
                    break
            else:
                flag = False
        for i in range(18, -1, -1):
            for j in range(10):
                if self.board[i][j] != 0 and self.board[i][j][1:] == str(self.num) and flag:
                    self.board[i][j], self.board[i + 1][j] = self.board[i + 1][j], self.board[i][j]
        # функция возвращает, остановился блок или нет
        return flag
    # функция перемещения кирпичей вправо и влево
    def move_brick(self, key):
        temp = []
        flag = True
        for o in range(20):
            for n in range(10):
                if self.board[o][n] != 0 and self.board[o][n][1:] == str(self.num):
                    temp.append([o, n])
        if key == 97:
            for n in temp:
                if n[1] >= 1:
                    if self.board[n[0]][n[1] - 1] != 0 and [n[0], n[1] - 1] not in temp:
                        flag = False
                        break
                else:
                    flag = False
            for i in range(19, -1, -1):
                for j in range(1, 10):
                    if self.board[i][j] != 0 and self.board[i][j][1:] == str(self.num) and flag:
                        self.board[i][j], self.board[i][j - 1] = self.board[i][j - 1], self.board[i][j]
        elif key == 100:
            for n in temp:
                if n[1] < 9:
                    if self.board[n[0]][n[1] + 1] != 0 and [n[0], n[1] + 1] not in temp:
                        flag = False
                        break
                else:
                    flag = False
            for i in range(19, -1, -1):
                for j in range(8, -1, -1):
                    if self.board[i][j] != 0 and self.board[i][j][1:] == str(self.num) and flag:
                        self.board[i][j], self.board[i][j + 1] = self.board[i][j + 1], self.board[i][j]
    
    def rotate_brick(self):
        flag = True
        temp = []
        # этими циклом я определяю координаты блока 
        for o in range(20):
            for n in range(10):
                if self.board[o][n] != 0 and self.board[o][n][1:] == str(self.num):
                    letter = self.board[o][n][0]
                    temp.append([o, n])
        temp = sorted(temp)
        min_x = min([i[1] for i in temp])
        min_y = min([i[0] for i in temp])
        max_x = max([i[1] for i in temp])
        max_y = max([i[0] for i in temp])
        matrix = []
        matrix_copy = []
        for i in range(20):
            matrix_temp = []
            for j in range(10):
                if (i >= min_y and i <= max_y) and (j >= min_x and j <= max_x):
                    if self.board[i][j] != 0 and self.board[i][j][0] != letter:
                        flag = False
                        break
                    matrix_temp.append(self.board[i][j])
            if matrix_temp:
                matrix.append(matrix_temp)
        if flag:
            length = len(matrix[0])
            for i in range(length):
                matrix_temp = []
                for j in range(len(matrix)):
                    matrix_temp.append(matrix[j][length - i - 1])
                matrix_copy.append(matrix_temp)
            matrix = matrix_copy
            if self.move == 1:
                    if letter == "I":
                        min_x -= 1
                    elif letter == "J":
                        min_x -= 1
                    elif letter == "L":
                        min_y += 1
                    elif letter == "S":
                        min_x += 1
                    elif letter == "T":
                        min_x += 1
                        min_y -= 1
                    elif letter == "Z":
                        min_x += 1
            elif self.move == 0:
                if letter == "I":
                    min_x += 1
                    min_y += 1
                elif letter == "J":
                    min_x += 1
                    min_y -= 1
                elif letter == "L":
                    min_x += 1
                    min_y -= 1
                elif letter == "S":
                    min_x -= 1
                elif letter == "T":
                    min_x -= 1
                elif letter == "Z":
                    min_x -= 1
            for i in range(len(matrix)):
                    for j in range(len(matrix[i])):
                        if i + min_y <= 0 or j + min_x <= 0 or i + min_y > 18 or j + min_x > 9 or (self.board[i + min_y][j + min_x] != 0 and self.board[i + min_y][j + min_x][1:] != str(self.num)):
                            flag = False
            if flag:
                for i in range(20):
                    for j in range(10):
                        if self.board[i][j] != 0 and self.board[i][j][1:] == str(self.num):
                            self.board[i][j] = 0
                for i in range(len(matrix)):
                    for j in range(len(matrix[i])):
                        self.board[i + min_y][j + min_x], matrix[i][j] = matrix[i][j], self.board[i + min_y][j + min_x]
                if self.move == 1:
                    self.move = 2
                elif self.move == 2:
                    self.move = 1
        # удаление заполненных рядов и начисление за них баллов
    def delete_rows(self):
        count = 0
        last_row = False
        deleted = False
        self.first_row = False
        for i in range(20):
            if not 0 in self.board[i]:
                if not self.first_row:
                    self.first_row = i
                if not last_row:
                    last_row = True
                    if count == 1:
                        self.score += 100
                    elif count == 2:
                        self.score += 300
                    elif count == 3:
                        self.score += 700
                    elif count == 4:
                        self.score += 1500
                    count = 1
                else:
                    count += 1
                deleted = True
                for j in range(10):
                    self.board[i][j] = 0
            else:
                last_row = False
        if count == 1:
            self.score += 100
        elif count == 2:
            self.score += 300
        elif count == 3:
            self.score += 700
        elif count == 4:
            self.score += 1500
        if deleted:
            self.update_rows()
# обновление рядов именно при удалении
    def update_rows(self):
        for i in range(self.first_row, -1, -1):
            for j in range(10):
                if self.board[i][j] != 0 and self.board[i][j][1:]:
                    self.board[i][j], self.board[i + 1][j] = self.board[i + 1][j], self.board[i][j]
    
    # проверка может ли идти игра
    def check_game(self):
        if self.game:
            return True
        else:
            return False
    
    def end_game(self):
        return self.score


pygame.init()
board = Board()
pygame.display.set_caption('Тетрис')
size = width, height = 500, 800
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color((255, 255, 255)))
fps = 3
ticks = 1
running = True
clock = pygame.time.Clock()
board.render(screen)
while running:
    # я ввел условие, которое будет вызывать функцию спавна не каждый тик, а только когда предыдущий блок остановился
    if ticks == 1:
        board.delete_rows()
        board.spawn_brick()
        ticks = 0
    board.render(screen)
    # если блок остановился, то будет запускаться следующий
    flag = board.update_field()
    if  flag == False:
        ticks = 1
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if flag:
            # быстрое падение блока на ЛКМ
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                fps = 30
                while board.update_field() == True:
                    continue
                ticks = 1
                fps = 3
            # разворот блока
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                board.rotate_brick()
            # сдвиг блока влево
            if event.type == pygame.KEYDOWN and event.key == 97:
                board.move_brick(97)
            # сдвиг блока вправо
            if event.type == pygame.KEYDOWN and event.key == 100:
                board.move_brick(100)
    if not board.check_game():
        # должна останавливаться игра
        running = False
        # вывод результата
        print(board.end_game())
    pygame.display.flip()