import pygame
from random import choice


class App:
    """
    Класс приложения
    """

    def __init__(self):
        """
        Инициализация приложения
        """
        self.running = True

        pygame.init()  # Инициализация pygame

        self.screen = pygame.display.set_mode((576, 640))  # Создание окна
        pygame.display.set_caption('Игра "Трубопровод"')  # Название окна
        pygame.display.set_icon(pygame.image.load('images/icon.png'))  # Иконка окна

        self.clock = pygame.time.Clock()  # Создание объекта для отслеживания времени

        self.state = MainMenu(self, self.screen, self.clock, 9, 9)  # Начальное состояние

    def execute(self):
        while self.running:  # Основной цикл приложения
            for event in pygame.event.get():  # Получение событий
                if event.type == pygame.QUIT:  # Пользователь закрыл окно
                    self.running = False
                else:
                    self.state.event_handler(event)  # Обработка событий текущего состояния
            self.state.loop()  # Цикл текущего состояния
            self.state.render()  # Отрисовка текущего состояния
        pygame.quit()  # Завершение работы pygame


class Button:
    """
    Класс кнопки
    """

    def __init__(self, text):
        """
        Инициализация кнопки
        """
        self.text = text  # Текст кнопки
        self.font = pygame.font.Font('fonts/OpenSans-Regular.ttf', 32)  # Загрузка шрифта
        self.image = pygame.image.load(f'images/button.png').convert_alpha()  # Загрузка изображения кнопки

    def draw(self, screen, x, y):
        """
        Отрисовка кнопки
        """
        screen.blit(self.image, (x, y))  # Отрисовка изображения кнопки
        button_text = self.font.render(self.text, True, 'black')
        button_text_x = x + ((320 - button_text.get_width()) // 2)
        button_text_y = y + 8
        screen.blit(button_text, (button_text_x, button_text_y))  # Отрисовка текста кнопки


class SizeButton(Button):
    """
    Класс кнопки изменения размера поля
    """

    def __init__(self, text):
        """
        Инициализация кнопки изменения размера поля
        """
        super().__init__(text)
        self.image = pygame.image.load(f'images/size_button.png').convert_alpha()  # Загрузка изображения кнопки

    def draw(self, screen, x, y):
        """
        Отрисовка кнопки изменения размера поля
        """
        screen.blit(self.image, (x, y))  # Отрисовка изображения кнопки
        button_text = self.font.render(self.text, True, 'black')
        button_text_x = x + ((211 - button_text.get_width()) // 2)
        button_text_y = y + 8
        screen.blit(button_text, (button_text_x, button_text_y))  # Отрисовка текста кнопки


class MainMenu:
    """
    Класс главного меню
    """

    def __init__(self, application, screen, clock, rows, cols):
        """
        Инициализация главного меню
        """
        self.app = application  # Экземпляр приложения
        self.screen = screen  # Окно приложения
        self.clock = clock  # Отслеживание времени
        self.rows = rows  # Количество строк
        self.cols = cols  # Количество столбцов

        self.width, self.height = self.screen.get_size()  # Размеры окна

        self.title_font = pygame.font.Font('fonts/OpenSans-Regular.ttf', 64)  # Загрузка шрифта названия
        self.font = pygame.font.Font('fonts/OpenSans-Regular.ttf', 32)  # Загрузка шрифта

        self.buttons = [  # Кнопки главного меню
            Button('Играть'),
            SizeButton('Размер поля'),
            Button('Таблица рекордов'),
            Button('Выйти из игры')
        ]

        self.button_x = (self.width - 320) // 2  # Положение кнопок по оси X

    def event_handler(self, event):
        """
        Обработка событий
        """
        if event.type == pygame.MOUSEBUTTONDOWN:  # Нажата клавиша мыши
            x, y = pygame.mouse.get_pos()  # Получение координат курсора

            if self.button_x <= x <= self.button_x + 320:

                if 128 <= y <= 192 and event.button == 1:  # Нажатие ЛКМ по кнопке "Играть"
                    self.app.state = Game(self.app, self.screen, self.clock, self.rows, self.cols)

                elif self.button_x + 209 <= x <= self.button_x + 252 and 224 <= y <= 240:  # Увеличение числа строк
                    if event.button == 1 and self.rows + 1 <= 18:  # Нажатие ЛКМ по кнопке "▲"
                        self.rows += 1
                    elif event.button == 3:  # Нажатие ПКМ по кнопке "▲"
                        if self.rows + 5 <= 18:
                            self.rows += 5
                        else:
                            self.rows = 18

                elif self.button_x + 209 <= x <= self.button_x + 252 and 272 <= y <= 288:  # Уменьшение числа строк
                    if event.button == 1 and self.rows - 1 >= 9:  # Нажатие ЛКМ по кнопке "▼"
                        self.rows -= 1
                    elif event.button == 3:  # Нажатие ПКМ по кнопке "▼"
                        if self.rows - 5 >= 9:
                            self.rows -= 5
                        else:
                            self.rows = 9

                elif self.button_x + 277 <= x <= self.button_x + 320 and 224 <= y <= 240:  # Увеличение числа столбцов
                    if event.button == 1 and self.cols + 1 <= 36:  # Нажатие ЛКМ по кнопке "▲"
                        self.cols += 1
                    elif event.button == 3:  # Нажатие ПКМ по кнопке "▲"
                        if self.cols + 5 <= 36:
                            self.cols += 5
                        else:
                            self.cols = 36

                elif self.button_x + 277 <= x <= self.button_x + 320 and 272 <= y <= 288:  # Уменьшение числа столбцов
                    if event.button == 1 and self.cols - 1 >= 9:  # Нажатие ЛКМ по кнопке "▼"
                        self.cols -= 1
                    elif event.button == 3:  # Нажатие ПКМ по кнопке "▼"
                        if self.cols - 5 >= 9:
                            self.cols -= 5
                        else:
                            self.cols = 9

                elif 320 <= y <= 384 and event.button == 1:  # Нажатие ЛКМ по кнопке "Таблица рекордов"
                    # TODO: Таблица рекордов
                    pass

                elif 416 <= y <= 480 and event.button == 1:  # Нажатие ЛКМ по кнопке "Выйти из игры"
                    self.app.running = False

    def loop(self):
        """
        Цикл главного меню
        """
        self.clock.tick(60)  # Ограничение FPS до 60

    def render(self):
        """
        Отрисовка главного меню
        """
        self.screen.fill('white')  # Заливка экрана белым цветом, чтобы избавиться от прошлого кадра

        title_text = self.title_font.render('Трубопровод', True, 'black')
        self.screen.blit(title_text, ((self.width - title_text.get_width()) // 2, 8))  # Отрисовка названия

        for i, button in enumerate(self.buttons):
            button.draw(self.screen, self.button_x, 128 + 96 * i)  # Отрисовка кнопок
        rows_text = self.font.render(f'{self.rows}', True, 'black')
        self.screen.blit(rows_text, (self.button_x + 230 - rows_text.get_width() // 2, 232))  # Отрисовка числа строк
        cols_text = self.font.render(f'{self.cols}', True, 'black')
        self.screen.blit(cols_text, (self.button_x + 298 - cols_text.get_width() // 2, 232))  # Отрисовка числа столбцов

        pygame.display.flip()  # Отображение изменений на экране


class Tile:
    """
    Класс фишки
    """

    def __init__(self, pipe, angle):
        """
        Инициализация фишки
        """
        self.pipe = pipe  # Тип трубы
        self.angle = angle  # Угол поворота фишки
        self.image = pygame.image.load(f'images/{pipe}.png').convert_alpha()  # Загрузка изображения фишки

    def __add__(self, angle):
        """
        Поворот фишки против часовой стрелки
        """
        self.angle = (self.angle + angle) % 360

    def __sub__(self, angle):
        """
        Поворот фишки по часовой стрелке
        """
        self.angle = (self.angle - angle) % 360

    def water_direction(self, direction):
        """
        Определение направления, в котором будет двигаться вода
        """
        if self.pipe == 'straight':  # Фишка с прямой трубой
            if direction == 'right' and self.angle % 180 == 0:
                return 'right'
            elif direction == 'left' and self.angle % 180 == 0:
                return 'left'
            elif direction == 'down' and self.angle % 180 == 90:
                return 'down'
            elif direction == 'up' and self.angle % 180 == 90:
                return 'up'

        elif self.pipe == 'bend':  # Фишка с коленом
            if direction == 'right' and self.angle == 0 or direction == 'left' and self.angle == 90:
                return 'down'
            elif direction == 'right' and self.angle == 270 or direction == 'left' and self.angle == 180:
                return 'up'
            elif direction == 'down' and self.angle == 180 or direction == 'up' and self.angle == 90:
                return 'right'
            elif direction == 'down' and self.angle == 270 or direction == 'up' and self.angle == 0:
                return 'left'

        elif self.pipe == 'cross':  # Фишка с двумя противоположными коленами
            if direction == 'right' and self.angle % 180 == 0 or direction == 'left' and self.angle % 180 == 90:
                return 'down'
            elif direction == 'right' and self.angle % 180 == 90 or direction == 'left' and self.angle % 180 == 0:
                return 'up'
            elif direction == 'down' and self.angle % 180 == 0 or direction == 'up' and self.angle % 180 == 90:
                return 'right'
            elif direction == 'down' and self.angle % 180 == 90 or direction == 'up' and self.angle % 180 == 0:
                return 'left'

        elif self.pipe == 'end' and (direction == 'right' and self.angle == 0 or  # Фишка с концом трубы
                                     direction == 'left' and self.angle == 180 or
                                     direction == 'down' and self.angle == 270 or
                                     direction == 'up' and self.angle == 90):
            return 'end'

        else:
            return None


class Game:
    """
    Класс игры
    """

    def __init__(self, application, screen, clock, rows, cols):
        """
        Инициализация игры
        """
        self.app = application  # Экземпляр приложения
        self.screen = screen  # Окно приложения
        self.clock = clock  # Отслеживание времени
        self.rows = rows  # Количество строк
        self.cols = cols  # Количество столбцов

        self.pause = False  # Пауза
        self.win = False  # Победа

        self.scale = 16 * (min(576 // self.rows, 1152 // self.cols) // 16)  # Размер фишки
        self.grid_width, self.grid_height = self.cols * self.scale, self.rows * self.scale  # Размеры игрового поля
        self.width, self.height = max(self.grid_width, 512), max(self.grid_height, 512) + 64  # Размеры окна
        self.grid_x = (self.width - self.grid_width) // 2  # Положение игрового поля по оси X
        self.grid_y = (self.height - self.grid_height + 64) // 2  # Положение игрового поля по оси Y

        if pygame.display.get_window_size() != (self.width, self.height):  # Размер окна не соответствует требуемому
            pygame.display.quit()  # Закрытие окна
            self.screen = pygame.display.set_mode((self.width, self.height))  # Создание окна
            pygame.display.set_caption('Игра "Трубопровод"')  # Название окна
            pygame.display.set_icon(pygame.image.load('images/icon.png'))  # Иконка окна

        self.start_x, self.start_y = 0, 0  # Положение начальной фишки
        self.end_x, self.end_y = self.cols - 1, self.rows - 1  # Положение конечной фишки

        self.tiles = [[Tile(choice(['straight', 'bend', 'cross']), choice([0, 90, 180, 270]))  # Генерация фишек
                       for _ in range(self.cols)] for _ in range(self.rows)]
        self.tiles[self.start_y][self.start_x] = Tile('start', 0)  # Начальная фишка
        self.tiles[self.end_y][self.end_x] = Tile('end', 0)  # Конечная фишка

        self.water = []  # Список координат труб с водой

        self.water_images = {  # Загрузка изображений труб с водой
            'start': pygame.image.load('images/start_water.png').convert_alpha(),
            'straight': pygame.image.load('images/straight_water.png').convert_alpha(),
            'bend': pygame.image.load('images/bend_water.png').convert_alpha(),
            'cross': pygame.image.load('images/cross_water.png').convert_alpha(),
            'end': pygame.image.load('images/end_water.png').convert_alpha()
        }

        self.font = pygame.font.Font('fonts/OpenSans-Regular.ttf', 45)  # Загрузка шрифта

        self.pause_icon = pygame.image.load('images/pause_icon.png').convert_alpha()  # Загрузка иконки паузы
        self.time_icon = pygame.image.load('images/time_icon.png').convert_alpha()  # Загрузка иконки счетчика времени
        self.turns_icon = pygame.image.load('images/turns_icon.png').convert_alpha()  # Загрузка иконки счетчика ходов

        self.pause_tint = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Затемнение экрана
        self.pause_tint.fill((0, 0, 0, 128))
        self.pause_bg = pygame.image.load('images/pause_bg.png').convert_alpha()  # Загрузка фона меню паузы
        self.pause_buttons = [  # Кнопки меню паузы
            Button('Продолжить'),
            Button('Выйти в меню')
        ]

        self.button_x = (self.width - 320) // 2  # Положение кнопок по оси X

        self.win_image = pygame.image.load('images/victory.png').convert_alpha()  # Загрузка изображения победы

        self.time = 0  # Счетчик времени
        self.turns = 0  # Счетчик ходов

        self.check_win()  # Проверка победной ситуации

    def event_handler(self, event):
        """
        Обработка событий
        """
        if event.type == pygame.MOUSEBUTTONDOWN:  # Нажата клавиша мыши
            x, y = pygame.mouse.get_pos()  # Получение координат курсора

            if (self.grid_x <= x <= self.grid_x + self.grid_width and self.grid_y <= y <= self.grid_y + self.grid_height
                    and not self.pause and not self.win):  # Курсор находится в пределах игрового поля
                tile_x, tile_y = (x - self.grid_x) // self.scale, (y - self.grid_y) // self.scale

                if event.button == 1:  # Левая клавиша мыши
                    _ = self.tiles[tile_y][tile_x] - 90  # Поворот фишки на 90 градусов по часовой стрелке
                    self.turns += 1  # Увеличение счетчика ходов
                    self.check_win()  # Проверка победной ситуации

                elif event.button == 3:  # Правая клавиша мыши
                    _ = self.tiles[tile_y][tile_x] + 90  # Поворот фишки на 90 градусов против часовой стрелки
                    self.turns += 1  # Увеличение счетчика ходов
                    self.check_win()  # Проверка победной ситуации

            elif 0 <= x <= 64 and 0 <= y <= 64 and event.button == 1 and not self.pause:  # Нажатие ЛКМ по кнопке паузы
                self.pause = True

            elif self.pause and self.button_x <= x <= self.button_x + 320 and event.button == 1:
                if 160 <= y <= 224:  # Нажатие ЛКМ по кнопке "Продолжить"
                    self.pause = False
                elif 256 <= y <= 320:  # Нажатие ЛКМ по кнопке "Выйти в меню"
                    self.app.state = MainMenu(self.app, self.screen, self.clock, self.rows, self.cols)

    def check_win(self):
        """
        Проверка победной ситуации
        """
        direction = None  # Направление движения воды
        x, y = self.start_x, self.start_y  # Начальные координаты воды
        self.water = [[x, y, 'start']]  # Список координат труб с водой

        if self.tiles[y][x].angle == 0:
            direction = 'right'  # Вода движется вправо
            x += 1
        elif self.tiles[y][x].angle == 90:
            direction = 'up'  # Вода движется вверх
            y -= 1
        elif self.tiles[y][x].angle == 180:
            direction = 'left'  # Вода движется влево
            x -= 1
        elif self.tiles[y][x].angle == 270:
            direction = 'down'  # Вода движется вниз
            y += 1

        while 0 <= x <= self.cols - 1 and 0 <= y <= self.rows - 1 and direction is not None and direction != 'win':

            direction = self.tiles[y][x].water_direction(direction)  # Определение направления движения воды

            if direction is not None:

                pipe = self.tiles[y][x].pipe  # Тип трубы

                if pipe == 'cross' and (self.tiles[y][x].angle == 0 and (direction in ['down', 'left']) or
                                        self.tiles[y][x].angle == 90 and (direction in ['down', 'right']) or
                                        self.tiles[y][x].angle == 180 and (direction in ['up', 'right']) or
                                        self.tiles[y][x].angle == 270 and (direction in ['up', 'left'])):
                    pipe = 'bend'  # Вода движется по нижнему колену (в остальных случаях - по верхнему)

                self.water.append([x, y, pipe])  # Добавление координат трубы с водой в список

                if direction == 'right':  # Вода движется вправо
                    x += 1
                elif direction == 'left':  # Вода движется влево
                    x -= 1
                elif direction == 'up':  # Вода движется вверх
                    y -= 1
                elif direction == 'down':  # Вода движется вниз
                    y += 1
                elif direction == 'end':  # Вода достигла конечной фишки
                    self.win = True

    def loop(self):
        """
        Цикл игры
        """
        self.clock.tick(60)  # Ограничение FPS до 60

        if not self.pause and not self.win:
            self.time += 1  # Увеличение счетчика времени

    def render(self):
        """
        Отрисовка игры
        """
        self.screen.fill('white')  # Заливка экрана белым цветом, чтобы избавиться от прошлого кадра

        self.screen.blit(self.pause_icon, (16, 16))  # Отрисовка кнопки паузы

        time_text = self.font.render(f'{self.time // 60}', True, 'black')
        time_x = (self.width - time_text.get_width() - 40) // 2
        self.screen.blit(self.time_icon, (time_x, 16))  # Отрисовка иконки счетчика времени
        self.screen.blit(time_text, (time_x + 40, -1))  # Отрисовка счетчика времени

        turns_text = self.font.render(f'{self.turns}', True, 'black')
        turns_x = self.width - turns_text.get_width() - 56
        self.screen.blit(self.turns_icon, (turns_x, 16))  # Отрисовка иконки счетчика ходов
        self.screen.blit(turns_text, (turns_x + 40, -1))  # Отрисовка счетчика ходов

        for tile_y, row in enumerate(self.tiles):
            for tile_x, tile in enumerate(row):
                x, y = self.grid_x + tile_x * self.scale, self.grid_y + tile_y * self.scale
                scaled_image = pygame.transform.scale(pygame.transform.rotate(tile.image, tile.angle),
                                                      (self.scale, self.scale))

                self.screen.blit(scaled_image, (x, y))  # Отрисовка фишки

        for tile_x, tile_y, pipe in self.water:
            x, y = self.grid_x + tile_x * self.scale, self.grid_y + tile_y * self.scale
            scaled_water = pygame.transform.scale(pygame.transform.rotate(
                self.water_images[pipe], self.tiles[tile_y][tile_x].angle), (self.scale, self.scale))

            self.screen.blit(scaled_water, (x, y))  # Отрисовка воды

        if self.win:
            # TODO: Меню конца игры
            self.screen.blit(self.win_image, (self.width // 2 - 256, 64))  # Отрисовка изображения победы

        if self.pause:
            self.screen.blit(self.pause_tint, (0, 0))  # Отрисовка затемнения экрана
            self.screen.blit(self.pause_bg, ((self.width - 384) // 2, 64))  # Отрисовка фона меню паузы
            pause_text = self.font.render('Пауза', True, 'black')
            self.screen.blit(pause_text, ((self.width - pause_text.get_width()) // 2, 63))  # Отрисовка текста "Пауза"
            for i, button in enumerate(self.pause_buttons):
                button.draw(self.screen, self.button_x, 160 + 96 * i)  # Отрисовка кнопок меню паузы

        pygame.display.flip()  # Отображение изменений на экране


if __name__ == '__main__':
    app = App()  # Создание экземпляра приложения
    app.execute()  # Запуск приложения
