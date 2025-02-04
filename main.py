import pygame
import random


pygame.init()
size = width, height = 500, 800
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("Arial", 72)
small_font = pygame.font.SysFont("Arial", 48) 
clock = pygame.time.Clock()

screen.fill((0, 0, 0))


class Button:
    def __init__(self, y, text, action):
        self.rect = pygame.Rect((width // 2) - (200 // 2), y, 200, 60)
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, (70, 100, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3)
        text_surf = small_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Главное меню
class MainMenu:
    def __init__(self, start_game, show_instructions, exit_game):
        self.title = font.render("TETRIS", True, (98, 124, 208))
        self.title_rect = self.title.get_rect(center=(width // 2, 100))
        self.buttons = [
            Button(300, "Play", start_game),
            Button(400, "Controls", show_instructions),
            Button(500, "Quit", exit_game)
        ]

    def draw(self, screen):
        screen.fill((0, 0, 0))
        x_offset = (width // 2) - 90
        screen.blit(self.title, self.title_rect.topleft)
        for button in self.buttons:
            button.draw(screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.is_clicked(event.pos):
                    button.action()

# Экран "Управление"
class Controls:
    def __init__(self, back_to_menu):
        self.text_lines = [
            "ЛКМ - поставить блок",
            "ПКМ - вращать блок",
            "A/D - двигать блок"
        ]
        self.back_button = Button(600, "Back", back_to_menu)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        y_offset = 250
        for line in self.text_lines:
            text_surf = small_font.render(line, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(width // 2, y_offset))
            screen.blit(text_surf, text_rect)
            y_offset += 50
        self.back_button.draw(screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.back_button.is_clicked(event.pos):
            self.back_button.action()

# Экран завершения игры
class EndMenu:
    def __init__(self, exit_game):
        self.text = small_font.render(f"Final Score: {board.score}", True, (255, 255, 255))
        self.exit_button = Button(500, "Quit", exit_game)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text_rect = self.text.get_rect(center=(width // 2, 300))
        screen.blit(self.text, text_rect)
        self.exit_button.draw(screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.exit_button.is_clicked(event.pos):
            self.exit_button.action()

# Функции управления меню
def start_game():
    global running, game_running
    game_running = True
    running = False

def show_instructions():
    global current_menu
    current_menu = Controls(lambda: set_main_menu())

def set_main_menu():
    global current_menu
    current_menu = main_menu

def exit_game():
    pygame.quit()
    exit()

main_menu = MainMenu(start_game, show_instructions, exit_game)
current_menu = main_menu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        current_menu.handle_event(event)
    current_menu.draw(screen)
    pygame.display.flip()
    clock.tick(60)


# Основной игровой цикл
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
        self.angle_x = 1
        self.angle_y = 1
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
    # функция разворота блока
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
        # крайние точки матрицы блока
        min_x = min([i[1] for i in temp])
        min_y = min([i[0] for i in temp])
        max_x = max([i[1] for i in temp])
        max_y = max([i[0] for i in temp])
        matrix = []
        matrix_copy = []
        # проверяю, нет ли клеток других блоков в моей матрице
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
            # циклами разворачиваю матрицу на 90 градусов
            for i in range(length):
                matrix_temp = []
                for j in range(len(matrix)):
                    matrix_temp.append(matrix[j][length - i - 1])
                matrix_copy.append(matrix_temp)
            matrix = matrix_copy
            # проверяю можно ли будет вставить матрицу на предыдущее место с нужным смещением
            for i in range(len(matrix)):
                    for j in range(len(matrix[i])):
                        if i + min_y < 0 or j + min_x <= 0 or i + min_y > 18 or j + min_x > 9 or (self.board[i + min_y][j + min_x] != 0 and self.board[i + min_y][j + min_x][1:] != str(self.num)):
                            flag = False
            if flag:
                # тут я определяю смещение для матрицы отдельно для каждого блока
                # в зависимости от того поварачивается блок по x или y, и вправо или влево
                if self.move == 1:
                    if self.angle_x == 1:
                        if letter == "I":
                            min_x -= 1
                            min_y += 1
                        elif letter == "J":
                            min_y += 1
                        elif letter == "L":
                            min_x -= 1
                        elif letter == "T":
                            min_x += 1
                            min_y -= 1
                    elif self.angle_x == -1:
                        if letter == "I":
                            min_x -= 1
                            min_y += 1
                        elif letter == "J":
                            min_x -= 1
                        elif letter == "L":
                            min_y += 1
                        elif letter == "S":
                            min_x += 1
                            min_y -= 1
                        elif letter == "Z":
                            min_x += 1
                            min_y -= 1
                    # меняю разворот вправо или влево
                    if self.angle_x == -1:
                        self.angle_x = 1
                    elif self.angle_x == 1:
                        self.angle_x = -1
                elif self.move == 0:
                    if self.angle_y == 1:
                        if letter == "I":
                            min_x += 1
                            min_y -= 1
                        elif letter == "J":
                            min_y -= 1
                            min_x += 1
                        elif letter == "S":
                            min_y += 1
                        elif letter == "T":
                            min_x -= 1
                        elif letter == "Z":
                            min_y += 1
                    elif self.angle_y == -1:
                        if letter == "I":
                            min_x += 1
                            min_y -= 1
                        elif letter == "L":
                            min_x += 1
                            min_y -= 1
                        elif letter == "S":
                            min_x -= 1
                        elif letter == "Z":
                            min_x -= 1
                        elif letter == "T":
                            min_y += 1
                    # меняю разворот вправо или влево
                    if self.angle_y == -1:
                        self.angle_y = 1
                    elif self.angle_y == 1:
                        self.angle_y = -1
                # очищаю предыдущее место матрицы
                for i in range(20):
                    for j in range(10):
                        if self.board[i][j] != 0 and self.board[i][j][1:] == str(self.num):
                            self.board[i][j] = 0
                # вставляю в поле развернутую матрицу
                for i in range(len(matrix)):
                    for j in range(len(matrix[i])):
                        self.board[i + min_y][j + min_x], matrix[i][j] = matrix[i][j], self.board[i + min_y][j + min_x]
                # меняю разворот по x или y
                if self.move == 0:
                    self.move = 1
                elif self.move == 1:
                    self.move = 0
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
    # вывод итоговых очков
    def end_game(self):
        return self.score


pygame.init()
board = Board()
pygame.display.set_caption('Тетрис')
size = width, height = 500, 800
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color((255, 255, 255)))
fps = 4
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
    # если блок остановился, то будет запускаться следующий
    flag = board.update_field()
    if  flag == False:
        ticks = 1
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
                fps = 4
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
    clock.tick(fps)
    board.render(screen)
    pygame.display.flip()


end_menu = EndMenu(exit_game)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        end_menu.handle_event(event)
    end_menu.draw(screen)
    clock.tick(60)
