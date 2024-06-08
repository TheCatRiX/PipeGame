import pygame
import pickle
import os
from random import choice


class App:
    """
    Класс приложения
    """

    def __init__(self):
        """
        Инициализация приложения
        """
        self.running = True  # Флаг работы приложения

        pygame.init()  # Инициализация pygame

        try:
            with open('data/records.dat', 'rb') as f:
                self.records = pickle.load(f)  # Загрузка списка рекордов
        except FileNotFoundError:
            self.records = []  # Создание пустого списка рекордов

        self.player_name = ''  # Имя игрока

        self.screen = pygame.display.set_mode((576, 640))  # Создание окна
        pygame.display.set_caption('Игра "Трубопровод"')  # Название окна
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))  # Иконка окна

        self.rows, self.cols = 9, 9  # Начальное количество строк и столбцов
        self.min_rows, self.max_rows = 9, 18  # Минимальное и максимальное количество строк
        self.min_cols, self.max_cols = 9, 36  # Минимальное и максимальное количество столбцов

        self.clock = pygame.time.Clock()  # Создание объекта для отслеживания времени

        self.state = MainMenu(self)  # Начальное состояние

    def execute(self):
        while self.running:  # Основной цикл приложения
            for event in pygame.event.get():  # Получение событий
                if event.type == pygame.QUIT:  # Игрок закрыл окно
                    self.running = False  # Завершение работы приложения
                else:
                    self.state.event_handler(event)  # Обработка событий текущего состояния
            self.state.loop()  # Цикл текущего состояния
            self.state.render()  # Отрисовка текущего состояния

        if not os.path.exists('data'):  # Папка для данных не существует
            os.mkdir('data')  # Создание папки для данных
        with open('data/records.dat', 'wb') as f:
            pickle.dump(self.records, f)  # Сохранение списка рекордов

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
        self.font = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 32)  # Загрузка шрифта
        self.image = pygame.image.load(f'assets/button.png').convert_alpha()  # Загрузка изображения кнопки

    def draw(self, screen, x, y):
        """
        Отрисовка кнопки
        """
        screen.blit(self.image, (x, y))  # Отрисовка изображения кнопки

        button_text = self.font.render(self.text, True, 'black')
        button_text_x = x + ((320 - button_text.get_width()) // 2)
        button_text_y = y + 8
        screen.blit(button_text, (button_text_x, button_text_y))  # Отрисовка текста кнопки


class GridSizeButton(Button):
    """
    Класс кнопки изменения размера поля
    """

    def __init__(self, text):
        """
        Инициализация кнопки изменения размера поля
        """
        super().__init__(text)  # Вызов конструктора родительского класса Button
        self.image = pygame.image.load(f'assets/size_button.png').convert_alpha()  # Загрузка изображения кнопки

    def draw(self, screen, x, y):
        """
        Отрисовка кнопки изменения размера поля
        """
        screen.blit(self.image, (x, y))  # Отрисовка изображения кнопки

        button_text = self.font.render(self.text, True, 'black')
        button_text_x = x + ((211 - button_text.get_width()) // 2)
        button_text_y = y + 8
        screen.blit(button_text, (button_text_x, button_text_y))  # Отрисовка текста кнопки


def value_increase(value, step, max_value):
    """
    Возвращает значение, увеличенное на шаг, с учётом максимального значения
    """
    if value + step <= max_value:
        return value + step
    else:
        return max_value


def value_decrease(value, step, min_value):
    """
    Возвращает значение, уменьшенное на шаг, с учётом минимального значения
    """
    if value - step >= min_value:
        return value - step
    else:
        return min_value


class MainMenu:
    """
    Класс главного меню
    """

    def __init__(self, application):
        """
        Инициализация главного меню
        """
        self.app = application  # Экземпляр приложения

        self.width, self.height = self.app.screen.get_size()  # Размер окна

        self.title_font = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 64)  # Загрузка шрифта названия
        self.font = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 32)  # Загрузка шрифта

        self.buttons = [  # Кнопки главного меню
            Button('Играть'),
            GridSizeButton('Размер поля'),
            Button('Таблица рекордов'),
            Button('Выйти из игры')
        ]

        self.menu_button_x = (self.width - 320) // 2  # Положение кнопок меню по оси X

    def event_handler(self, event):
        """
        Обработка событий
        """
        if event.type == pygame.MOUSEBUTTONDOWN:  # Нажатие клавиши мыши
            x, y = pygame.mouse.get_pos()  # Получение координат курсора

            if self.menu_button_x <= x <= self.menu_button_x + 320:

                if 128 <= y <= 192 and event.button == 1:  # Нажатие ЛКМ по кнопке "Играть"
                    self.app.state = Game(self.app)  # Начало новой игры

                elif self.menu_button_x + 209 <= x <= self.menu_button_x + 252 and 224 <= y <= 240:
                    if event.button == 1:  # Нажатие ЛКМ по кнопке "▲"
                        self.app.rows = value_increase(self.app.rows, 1, 18)  # Увеличение числа строк на 1
                    elif event.button == 3:  # Нажатие ПКМ по кнопке "▲"
                        self.app.rows = value_increase(self.app.rows, 5, 18)  # Увеличение числа строк на 5

                elif self.menu_button_x + 209 <= x <= self.menu_button_x + 252 and 272 <= y <= 288:
                    if event.button == 1:  # Нажатие ЛКМ по кнопке "▼"
                        self.app.rows = value_decrease(self.app.rows, 1, 9)  # Уменьшение числа строк на 1
                    elif event.button == 3:  # Нажатие ПКМ по кнопке "▼"
                        self.app.rows = value_decrease(self.app.rows, 5, 9)  # Уменьшение числа строк на 5

                elif self.menu_button_x + 277 <= x <= self.menu_button_x + 320 and 224 <= y <= 240:
                    if event.button == 1:  # Нажатие ЛКМ по кнопке "▲"
                        self.app.cols = value_increase(self.app.cols, 1, 36)  # Увеличение числа столбцов на 1
                    elif event.button == 3:  # Нажатие ПКМ по кнопке "▲"
                        self.app.cols = value_increase(self.app.cols, 5, 36)  # Увеличение числа столбцов на 5

                elif self.menu_button_x + 277 <= x <= self.menu_button_x + 320 and 272 <= y <= 288:
                    if event.button == 1:  # Нажатие ЛКМ по кнопке "▼"
                        self.app.cols = value_decrease(self.app.cols, 1, 9)  # Уменьшение числа столбцов на 1
                    elif event.button == 3:  # Нажатие ПКМ по кнопке "▼"
                        self.app.cols = value_decrease(self.app.cols, 5, 9)  # Уменьшение числа столбцов на 5

                elif 320 <= y <= 384 and event.button == 1:  # Нажатие ЛКМ по кнопке "Таблица рекордов"
                    # TODO: Таблица рекордов
                    print('Таблица рекордов:')
                    print(*self.app.records, sep='\n', end='\n\n')

                elif 416 <= y <= 480 and event.button == 1:  # Нажатие ЛКМ по кнопке "Выйти из игры"
                    self.app.running = False  # Завершение работы приложения

        elif event.type == pygame.KEYDOWN:  # Нажатие клавиши клавиатуры

            if event.key == pygame.K_RETURN:  # Нажатие клавиши Enter
                self.app.state = Game(self.app)  # Начало новой игры

            elif event.key == pygame.K_UP:  # Нажатие клавиши вверх
                self.app.rows = value_increase(self.app.rows, 1, 18)  # Увеличение числа строк на 1

            elif event.key == pygame.K_DOWN:  # Нажатие клавиши вниз
                self.app.rows = value_decrease(self.app.rows, 1, 9)  # Уменьшение числа строк на 1

            elif event.key == pygame.K_RIGHT:  # Нажатие клавиши вправо
                self.app.cols = value_increase(self.app.cols, 1, 36)  # Увеличение числа столбцов на 1

            elif event.key == pygame.K_LEFT:  # Нажатие клавиши влево
                self.app.cols = value_decrease(self.app.cols, 1, 9)  # Уменьшение числа столбцов на 1

            elif event.key == pygame.K_TAB:  # Нажатие клавиши Tab
                print('Таблица рекордов:')
                print(*self.app.records, sep='\n', end='\n\n')

            elif event.key == pygame.K_ESCAPE:  # Нажатие клавиши Escape
                self.app.running = False  # Завершение работы приложения

    def loop(self):
        """
        Цикл главного меню
        """
        self.app.clock.tick(60)  # Ограничение FPS до 60

    def render(self):
        """
        Отрисовка главного меню
        """
        self.app.screen.fill('white')  # Заливка экрана белым цветом, чтобы избавиться от прошлого кадра

        title_text = self.title_font.render('Трубопровод', True, 'black')
        self.app.screen.blit(title_text, ((self.width - title_text.get_width()) // 2, 8))  # Отрисовка названия

        for i, button in enumerate(self.buttons):
            button.draw(self.app.screen, self.menu_button_x, 128 + 96 * i)  # Отрисовка кнопок

        rows_text = self.font.render(f'{self.app.rows}', True, 'black')
        rows_x = self.menu_button_x + 230 - rows_text.get_width() // 2
        self.app.screen.blit(rows_text, (rows_x, 232))  # Отрисовка числа строк

        cols_text = self.font.render(f'{self.app.cols}', True, 'black')
        cols_x = self.menu_button_x + 298 - cols_text.get_width() // 2
        self.app.screen.blit(cols_text, (cols_x, 232))  # Отрисовка числа столбцов

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
        self.image = pygame.image.load(f'assets/pipes/{pipe}.png').convert_alpha()  # Загрузка изображения фишки

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
                return 'right'  # Вода движется вправо
            elif direction == 'left' and self.angle % 180 == 0:
                return 'left'  # Вода движется влево
            elif direction == 'down' and self.angle % 180 == 90:
                return 'down'  # Вода движется вниз
            elif direction == 'up' and self.angle % 180 == 90:
                return 'up'  # Вода движется вверх

        elif self.pipe == 'bend':  # Фишка с коленом
            if direction == 'right' and self.angle == 0 or direction == 'left' and self.angle == 90:
                return 'down'  # Вода движется вниз
            elif direction == 'right' and self.angle == 270 or direction == 'left' and self.angle == 180:
                return 'up'  # Вода движется вверх
            elif direction == 'down' and self.angle == 180 or direction == 'up' and self.angle == 90:
                return 'right'  # Вода движется вправо
            elif direction == 'down' and self.angle == 270 or direction == 'up' and self.angle == 0:
                return 'left'  # Вода движется влево

        elif self.pipe == 'cross':  # Фишка с двумя противоположными коленами
            if direction == 'right' and self.angle % 180 == 0 or direction == 'left' and self.angle % 180 == 90:
                return 'down'  # Вода движется вниз
            elif direction == 'right' and self.angle % 180 == 90 or direction == 'left' and self.angle % 180 == 0:
                return 'up'  # Вода движется вверх
            elif direction == 'down' and self.angle % 180 == 0 or direction == 'up' and self.angle % 180 == 90:
                return 'right'  # Вода движется вправо
            elif direction == 'down' and self.angle % 180 == 90 or direction == 'up' and self.angle % 180 == 0:
                return 'left'  # Вода движется влево

        elif self.pipe == 'end' and (direction == 'right' and self.angle == 0 or  # Фишка с концом трубы
                                     direction == 'left' and self.angle == 180 or
                                     direction == 'down' and self.angle == 270 or
                                     direction == 'up' and self.angle == 90):
            return 'end'  # Вода достигла конечной фишки

        else:
            return None  # Трубы не соединены


class TextButton(Button):
    """
    Класс кнопки с текстовым полем
    """

    def __init__(self, text, hint):
        """
        Инициализация кнопки с текстовым полем
        """
        super().__init__(text)  # Вызов конструктора родительского класса Button
        self.hint = hint  # Текст подсказки
        self.font_italic = pygame.font.Font('assets/fonts/OpenSans-Italic.ttf', 32)  # Загрузка курсивного шрифта

    def draw(self, screen, x, y):
        """
        Отрисовка кнопки с текстовым полем
        """
        screen.blit(self.image, (x, y))  # Отрисовка изображения кнопки
        if not self.text:  # Текстовое поле пустое
            button_text = self.font_italic.render(self.hint, True, 'gray')
        else:
            button_text = self.font.render(self.text, True, 'black')
        button_text_x = x + ((320 - button_text.get_width()) // 2)
        button_text_y = y + 8
        screen.blit(button_text, (button_text_x, button_text_y))  # Отрисовка текстового поля

    def keyboard_input(self, event):
        """
        Обработка ввода с клавиатуры
        """
        if event.key == pygame.K_BACKSPACE:  # Нажатие клавиши Backspace
            self.text = self.text[:-1]  # Удаление последнего символа
        elif event.unicode.isalnum() or event.unicode in ' -_.':  # Ввод букв, цифр и некоторых символов
            width = self.font.render(self.text + event.unicode, True, 'black').get_width()
            if width <= 310:  # Ширина текста не превышает ширину текстового поля
                self.text += event.unicode  # Добавление символа


class Game:
    """
    Класс игры
    """

    def __init__(self, application):
        """
        Инициализация игры
        """
        self.app = application  # Экземпляр приложения

        self.pause = False  # Меню паузы
        self.win = False  # Меню победы
        self.new_record = False  # Меню нового рекорда

        self.scale = 16 * (min(576 // self.app.rows, 1152 // self.app.cols) // 16)  # Размер фишки
        self.grid_width, self.grid_height = self.app.cols * self.scale, self.app.rows * self.scale  # Размер поля
        self.width, self.height = max(self.grid_width, 512), max(self.grid_height, 512) + 64  # Размер окна
        self.grid_x = (self.width - self.grid_width) // 2  # Положение поля по оси X
        self.grid_y = (self.height - self.grid_height + 64) // 2  # Положение поля по оси Y

        if pygame.display.get_window_size() != (self.width, self.height):  # Размер окна не соответствует требуемому
            pygame.display.quit()  # Закрытие окна
            self.app.screen = pygame.display.set_mode((self.width, self.height))  # Создание окна
            pygame.display.set_caption('Игра "Трубопровод"')  # Название окна
            pygame.display.set_icon(pygame.image.load('assets/icon.png'))  # Иконка окна

        self.start_x, self.start_y = 0, 0  # Положение начальной фишки
        self.end_x, self.end_y = self.app.cols - 1, self.app.rows - 1  # Положение конечной фишки

        self.tiles = [[Tile(choice(['straight', 'bend', 'cross']), choice([0, 90, 180, 270]))  # Генерация фишек
                       for _ in range(self.app.cols)] for _ in range(self.app.rows)]
        self.tiles[self.start_y][self.start_x] = Tile('start', 0)  # Начальная фишка
        self.tiles[self.end_y][self.end_x] = Tile('end', 0)  # Конечная фишка

        self.water = []  # Создание списка координат труб с водой

        self.water_images = {  # Загрузка изображений воды в трубах
            'start': pygame.image.load('assets/pipes/start_water.png').convert_alpha(),
            'straight': pygame.image.load('assets/pipes/straight_water.png').convert_alpha(),
            'bend': pygame.image.load('assets/pipes/bend_water.png').convert_alpha(),
            'cross': pygame.image.load('assets/pipes/cross_water.png').convert_alpha(),
            'end': pygame.image.load('assets/pipes/end_water.png').convert_alpha()
        }

        self.font = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 45)  # Загрузка шрифта

        self.menu_tint = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Затемнение экрана
        self.menu_tint.fill((0, 0, 0, 128))
        self.menu_button_x = (self.width - 320) // 2  # Положение кнопок меню по оси X

        self.pause_button = pygame.image.load('assets/pause_button.png').convert_alpha()  # Загрузка кнопки паузы
        self.pause_menu_bg = pygame.image.load('assets/pause_menu_bg.png').convert_alpha()  # Загрузка фона меню паузы
        self.pause_menu_buttons = [  # Кнопки меню паузы
            Button('Продолжить'),
            Button('Выйти в меню')
        ]

        self.win_menu_bg = pygame.image.load('assets/win_menu_bg.png').convert_alpha()  # Загрузка фона меню победы
        self.win_menu_buttons = [  # Кнопки меню победы
            Button('Играть ещё раз'),
            Button('Выйти в меню')
        ]

        self.new_record_menu_buttons = [  # Кнопки меню нового рекорда
            TextButton(self.app.player_name, 'Введите имя'),
            Button('Сохранить')
        ]

        self.time = 0  # Счётчик времени
        self.turns = 0  # Счётчик ходов
        self.score = 0  # Счёт

        self.check_win()  # Проверка победной ситуации

    def event_handler(self, event):
        """
        Обработка событий
        """
        if event.type == pygame.MOUSEBUTTONDOWN:  # Нажатие клавиши мыши
            x, y = pygame.mouse.get_pos()  # Получение координат курсора

            if (self.grid_x <= x <= self.grid_x + self.grid_width and self.grid_y <= y <= self.grid_y + self.grid_height
                    and not self.pause and not self.win):  # Курсор находится в пределах поля
                tile_x, tile_y = (x - self.grid_x) // self.scale, (y - self.grid_y) // self.scale

                if event.button == 1:  # Левая клавиша мыши
                    _ = self.tiles[tile_y][tile_x] - 90  # Поворот фишки на 90 градусов по часовой стрелке
                    self.turns += 1  # Увеличение счётчика ходов
                    self.check_win()  # Проверка победной ситуации

                elif event.button == 3:  # Правая клавиша мыши
                    _ = self.tiles[tile_y][tile_x] + 90  # Поворот фишки на 90 градусов против часовой стрелки
                    self.turns += 1  # Увеличение счётчика ходов
                    self.check_win()  # Проверка победной ситуации

            elif 0 <= x <= 64 and 0 <= y <= 64 and event.button == 1 and not self.pause and not self.win:
                # Нажатие ЛКМ по кнопке паузы
                self.pause = True  # Переход в меню паузы

            elif self.menu_button_x <= x <= self.menu_button_x + 320 and event.button == 1:
                if self.pause:  # Меню паузы
                    if 160 <= y <= 224:  # Нажатие ЛКМ по кнопке "Продолжить"
                        self.pause = False  # Возврат к игре
                    elif 256 <= y <= 320:  # Нажатие ЛКМ по кнопке "Выйти в меню"
                        self.app.state = MainMenu(self.app)  # Переход в главное меню

                elif self.win and not self.new_record:  # Меню победы
                    if 224 <= y <= 288:  # Нажатие ЛКМ по кнопке "Играть ещё раз"
                        self.app.state = Game(self.app)  # Начало новой игры
                    elif 320 <= y <= 384:  # Нажатие ЛКМ по кнопке "Выйти в меню"
                        self.app.state = MainMenu(self.app)  # Переход в главное меню

                elif self.new_record:  # Меню нового рекорда
                    if 320 <= y <= 384:  # Нажатие ЛКМ по кнопке "Сохранить"
                        self.add_record()  # Добавление нового рекорда в таблицу рекордов
                        self.new_record = False  # Переход к меню победы

        elif event.type == pygame.KEYDOWN:  # Нажатие клавиши клавиатуры

            if not self.pause and not self.win:  # Обычное состояние игры
                if event.key == pygame.K_ESCAPE:  # Нажатие клавиши Escape
                    self.pause = True  # Переход в меню паузы

            elif self.pause:  # Меню паузы
                if event.key == pygame.K_RETURN:  # Нажатие клавиши Enter
                    self.pause = False  # Возврат к игре
                if event.key == pygame.K_ESCAPE:  # Нажатие клавиши Escape
                    self.app.state = MainMenu(self.app)  # Переход в главное меню

            elif self.win and not self.new_record:  # Меню победы
                if event.key == pygame.K_RETURN:  # Нажатие клавиши Enter
                    self.app.state = Game(self.app)  # Начало новой игры
                if event.key == pygame.K_ESCAPE:  # Нажатие клавиши Escape
                    self.app.state = MainMenu(self.app)  # Переход в главное меню

            elif self.new_record:  # Меню нового рекорда
                if event.key == pygame.K_RETURN:  # Нажатие клавиши Enter
                    self.add_record()  # Добавление нового рекорда в таблицу рекордов
                    self.new_record = False  # Переход к меню победы
                else:
                    self.new_record_menu_buttons[0].keyboard_input(event)  # Обработка ввода с клавиатуры

    def check_win(self):
        """
        Проверка победной ситуации
        """
        direction = None  # Направление движения воды
        x, y = self.start_x, self.start_y  # Начальные координаты воды
        self.water = [[x, y, 'start']]  # Очистка списка координат труб с водой

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

        while 0 <= x <= self.app.cols - 1 and 0 <= y <= self.app.rows - 1 and direction and direction != 'win':
            direction = self.tiles[y][x].water_direction(direction)  # Определение направления движения воды

            if direction:
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
                    self.win = True  # Переход в меню победы
                    time = self.time // 60 if self.time > 60 else 1
                    turns = self.turns if self.turns > 0 else 1
                    self.score = (self.app.rows ** 2 * self.app.cols ** 2 * 100) // (time * turns)  # Вычисление счёта
                    if not self.app.records or self.score > self.app.records[0]['score']:
                        self.new_record = True  # Переход в меню нового рекорда

    def add_record(self):
        """
        Добавление нового рекорда в таблицу рекордов
        """
        self.app.player_name = self.new_record_menu_buttons[0].text.strip()  # Получение имени игрока
        if not self.app.player_name:  # Текстовое поле пустое
            self.app.player_name = 'Anonymous'
        self.app.records = ([{'name': self.app.player_name, 'score': self.score,  # Добавление рекорда в список рекордов
                              'size': f'{self.app.rows}x{self.app.cols}',
                              'time': f'{self.time // 3600:02}:{self.time // 60 % 60:02}',
                              'turns': self.turns}] + self.app.records)

    def loop(self):
        """
        Цикл игры
        """
        self.app.clock.tick(60)  # Ограничение FPS до 60

        if not self.pause and not self.win:  # Обычное состояние игры
            self.time += 1  # Увеличение счётчика времени

    def render(self):
        """
        Отрисовка игры
        """
        self.app.screen.fill('white')  # Заливка экрана белым цветом, чтобы избавиться от прошлого кадра

        self.app.screen.blit(self.pause_button, (16, 16))  # Отрисовка кнопки паузы

        time_text = self.font.render(f'{self.time // 3600:02}:{self.time // 60 % 60:02}', True, 'black')
        time_x = (self.width - time_text.get_width()) // 2
        self.app.screen.blit(time_text, (time_x, -1))  # Отрисовка счётчика времени

        turns_text = self.font.render(f'{self.turns}', True, 'black')
        turns_x = self.width - turns_text.get_width() - 16
        self.app.screen.blit(turns_text, (turns_x, -1))  # Отрисовка счётчика ходов

        for tile_y, row in enumerate(self.tiles):
            for tile_x, tile in enumerate(row):
                x, y = self.grid_x + tile_x * self.scale, self.grid_y + tile_y * self.scale
                scaled_image = pygame.transform.scale(pygame.transform.rotate(tile.image, tile.angle),
                                                      (self.scale, self.scale))
                self.app.screen.blit(scaled_image, (x, y))  # Отрисовка фишек

        for tile_x, tile_y, pipe in self.water:
            x, y = self.grid_x + tile_x * self.scale, self.grid_y + tile_y * self.scale
            scaled_water = pygame.transform.scale(pygame.transform.rotate(
                self.water_images[pipe], self.tiles[tile_y][tile_x].angle), (self.scale, self.scale))
            self.app.screen.blit(scaled_water, (x, y))  # Отрисовка воды в трубах

        if self.pause:
            self.app.screen.blit(self.menu_tint, (0, 0))  # Отрисовка затемнения экрана
            self.app.screen.blit(self.pause_menu_bg, ((self.width - 384) // 2, 64))  # Отрисовка фона меню паузы

            pause_title_text = self.font.render('Пауза', True, 'black')
            pause_title_x = (self.width - pause_title_text.get_width()) // 2
            self.app.screen.blit(pause_title_text, (pause_title_x, 63))  # Отрисовка заголовка меню паузы

            for i, button in enumerate(self.pause_menu_buttons):
                button.draw(self.app.screen, self.menu_button_x, 160 + 96 * i)  # Отрисовка кнопок меню паузы

        if self.win:
            self.app.screen.blit(self.menu_tint, (0, 0))  # Отрисовка затемнения экрана
            self.app.screen.blit(self.win_menu_bg, ((self.width - 384) // 2, 64))  # Отрисовка фона меню победы

            win_title_text = self.font.render('Новый рекорд!' if self.new_record else 'Победа!', True, 'black')
            win_title_x = (self.width - win_title_text.get_width()) // 2
            self.app.screen.blit(win_title_text, (win_title_x, 63))  # Отрисовка заголовка меню победы

            score_text = self.font.render(f'Cчёт: {self.score}', True, 'black')
            score_x = (self.width - score_text.get_width()) // 2
            self.app.screen.blit(score_text, (score_x, 143))  # Отрисовка счёта

            for i, button in enumerate(self.new_record_menu_buttons if self.new_record else self.win_menu_buttons):
                button.draw(self.app.screen, self.menu_button_x, 224 + 96 * i)  # Отрисовка кнопок меню победы

        pygame.display.flip()  # Отображение изменений на экране


if __name__ == '__main__':
    app = App()  # Создание экземпляра приложения
    app.execute()  # Запуск приложения
