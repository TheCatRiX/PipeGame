import pygame
import pickle
import os
from random import choice


class App:
    """
    Класс приложения
    """

    def __init__(self):
        self.running = True

        pygame.init()

        try:  # Загрузка списка рекордов из файла
            with open('data/scores.dat', 'rb') as f:
                self.scores = pickle.load(f)
        except FileNotFoundError:
            self.scores = {}

        self.player_name = ''

        self.screen = pygame.display.set_mode((576, 640))
        pygame.display.set_caption('Игра "Трубопровод"')
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))

        self.rows, self.cols = 9, 9  # Начальное количество строк и столбцов
        self.min_rows, self.max_rows = 9, 18
        self.min_cols, self.max_cols = 9, 36

        self.font_32 = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 32)
        self.font_45 = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 45)
        self.font_64 = pygame.font.Font('assets/fonts/OpenSans-Regular.ttf', 64)
        self.font_32_italic = pygame.font.Font('assets/fonts/OpenSans-Italic.ttf', 32)

        self.clock = pygame.time.Clock()

        self.state = MainMenu(self)  # Начальное состояние

    def execute(self):
        """
        Запуск приложения
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Игрок закрыл окно
                    self.running = False
                else:
                    self.state.event_handler(event)  # Обработка событий текущего состояния
            self.state.loop()  # Цикл текущего состояния
            self.state.render()  # Отрисовка текущего состояния

        # Сохранение списка рекордов в файл
        if not os.path.exists('data'):
            os.mkdir('data')
        with open('data/scores.dat', 'wb') as f:
            pickle.dump(self.scores, f)

        pygame.quit()


class Button:
    """
    Кнопка
    """

    def __init__(self, application, text, active=True):
        self.app = application
        self.text = text  # Текст кнопки
        self.active = active
        self.image = pygame.image.load(f'assets/button.png').convert_alpha()

    def draw(self, x, y):
        self.app.screen.blit(self.image, (x, y))  # Отрисовка изображения кнопки

        # Отрисовка текста кнопки
        button_text = self.app.font_32.render(self.text, True, 'black' if self.active else 'gray')
        button_text_x = x + ((320 - button_text.get_width()) // 2)
        button_text_y = y + 8
        self.app.screen.blit(button_text, (button_text_x, button_text_y))


class GridSizeButton(Button):
    """
    Кнопка изменения размера поля
    """

    def __init__(self, application, text):
        super().__init__(application, text)
        self.image = pygame.image.load(f'assets/size_button.png').convert_alpha()

    def draw(self, x, y):
        self.app.screen.blit(self.image, (x, y))  # Отрисовка изображения кнопки

        # Отрисовка текста кнопки
        button_text = self.app.font_32.render(self.text, True, 'black')
        button_text_x = x + ((210 - button_text.get_width()) // 2)
        button_text_y = y + 8
        self.app.screen.blit(button_text, (button_text_x, button_text_y))

        # Отрисовка количества строк
        rows_text = self.app.font_32.render(f'{self.app.rows}', True, 'black')
        rows_x = x + 230 - rows_text.get_width() // 2
        self.app.screen.blit(rows_text, (rows_x, 232))

        # Отрисовка количества столбцов
        cols_text = self.app.font_32.render(f'{self.app.cols}', True, 'black')
        cols_x = x + 298 - cols_text.get_width() // 2
        self.app.screen.blit(cols_text, (cols_x, 232))


class TextButton(Button):
    """
    Кнопка с текстовым полем
    """

    def __init__(self, application, text, hint):
        super().__init__(application, text)
        self.hint = hint  # Текст подсказки

    def draw(self, x, y):
        self.app.screen.blit(self.image, (x, y))  # Отрисовка изображения кнопки

        # Отрисовка текстового поля
        if not self.text:
            button_text = self.app.font_32_italic.render(self.hint, True, 'gray')
        else:
            button_text = self.app.font_32.render(self.text, True, 'black')
        button_text_x = x + ((320 - button_text.get_width()) // 2)
        button_text_y = y + 8
        self.app.screen.blit(button_text, (button_text_x, button_text_y))

    def keyboard_input(self, event):
        """
        Обработка ввода с клавиатуры
        """
        if event.key == pygame.K_BACKSPACE:  # Нажатие Backspace
            self.text = self.text[:-1]
        elif event.unicode.isalnum() or event.unicode in ' -_':  # Ввод букв, цифр и некоторых символов
            text_width = self.app.font_32.render(self.text + event.unicode, True, 'black').get_width()
            if text_width <= 310:
                self.text = (self.text + event.unicode).lstrip()


class Menu:
    """
    Меню
    """

    def __init__(self, application, title, buttons, bg_image):
        self.app = application
        self.title = title
        self.buttons = buttons
        self.bg_image = bg_image

        self.width, self.height = self.app.screen.get_size()

        self.tint = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.tint.fill((0, 0, 0, 128))

        self.button_x = (self.width - 320) // 2  # Положение кнопок меню по оси X

    def draw(self):
        self.app.screen.blit(self.tint, (0, 0))  # Затемнение экрана
        self.app.screen.blit(self.bg_image, ((self.width - 384) // 2, 64))  # Отрисовка фона меню

        # Отрисовка заголовка меню
        title_text = self.app.font_45.render(self.title, True, 'black')
        title_x = (self.width - title_text.get_width()) // 2
        self.app.screen.blit(title_text, (title_x, 63))

        # Отрисовка кнопок меню
        for i, button in enumerate(self.buttons):
            button.draw(self.button_x, 160 + 96 * i)


def change_size(value, min_value, max_value, button_x, x, y, mouse_button):
    """
    Изменение размера поля
    """
    if button_x <= x <= button_x + 43:
        if 224 <= y <= 240 and mouse_button == 1 or mouse_button == 4:  # Клик по "▲" или колесо мыши вверх
            return min(value + 1, max_value)
        elif 272 <= y <= 288 and mouse_button == 1 or mouse_button == 5:  # Клик по "▼" или колесо мыши вниз
            return max(value - 1, min_value)
        else:
            return value
    else:
        return value


class MainMenu:
    """
    Главное меню
    """

    def __init__(self, application):
        self.app = application

        self.new_game = False

        self.width, self.height = self.app.screen.get_size()  # Размер окна

        self.menu_tint = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.menu_tint.fill((0, 0, 0, 128))  # Затемнение экрана

        self.menu_button_x = (self.width - 320) // 2  # Положение кнопок меню по оси X

        self.main_menu_buttons = [
            Button(self.app, 'Новая игра'),
            GridSizeButton(self.app, 'Размер поля'),
            Button(self.app, 'Таблица рекордов'),
            Button(self.app, 'Выйти из игры')
        ]

        self.new_game_menu_buttons = [
            TextButton(self.app, self.app.player_name, 'Введите имя'),
            Button(self.app, 'Начать игру', bool(self.app.player_name)),
            Button(self.app, 'Вернуться в меню')
        ]
        self.new_game_menu_bg = pygame.image.load('assets/new_game_menu_bg.png').convert_alpha()
        self.new_game_menu = Menu(self.app, 'Новая игра', self.new_game_menu_buttons, self.new_game_menu_bg)

    def event_handler(self, event):
        """
        Обработка событий
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            # Обычное состояние главного меню
            if self.menu_button_x <= x <= self.menu_button_x + 320 and not self.new_game:

                if 128 <= y <= 192 and event.button == 1:  # Клик по "Новая игра"
                    self.new_game = True

                elif 224 <= y <= 288:  # "Размер поля"
                    self.app.rows = change_size(self.app.rows, self.app.min_rows, self.app.max_rows,
                                                self.menu_button_x + 209, x, y, event.button)
                    self.app.cols = change_size(self.app.cols, self.app.min_cols, self.app.max_cols,
                                                self.menu_button_x + 277, x, y, event.button)

                elif 320 <= y <= 384 and event.button == 1:  # Клик по "Таблица рекордов"
                    self.app.state = Leaderboard(self.app)

                elif 416 <= y <= 480 and event.button == 1:  # Клик по "Выйти из игры"
                    self.app.running = False

            # Меню новой игры
            elif self.menu_button_x <= x <= self.menu_button_x + 320 and self.new_game and event.button == 1:
                if 256 <= y <= 320 and self.new_game_menu_buttons[1].active:  # Клик по "Начать игру"
                    app.player_name = self.new_game_menu_buttons[0].text.strip()
                    self.app.state = Game(self.app)
                elif 352 <= y <= 416:  # Клик по "Вернуться в меню"
                    self.new_game = False
                    self.new_game_menu_buttons[0].text = self.app.player_name
                    self.new_game_menu_buttons[1].active = bool(self.app.player_name)

        elif event.type == pygame.KEYDOWN:

            # Обычное состояние главного меню
            if not self.new_game:

                if event.key == pygame.K_RETURN:  # Нажатие Enter
                    self.new_game = True

                elif event.key == pygame.K_UP:  # Нажатие стрелки вверх
                    self.app.rows = min(self.app.rows + 1, self.app.max_rows)
                elif event.key == pygame.K_DOWN:  # Нажатие стрелки вниз
                    self.app.rows = max(self.app.rows - 1, self.app.min_rows)

                elif event.key == pygame.K_RIGHT:  # Нажатие стрелки вправо
                    self.app.cols = min(self.app.cols + 1, self.app.max_cols)
                elif event.key == pygame.K_LEFT:  # Нажатие стрелки влево
                    self.app.cols = max(self.app.cols - 1, self.app.min_cols)

                elif event.key == pygame.K_TAB:  # Нажатие Tab
                    self.app.state = Leaderboard(self.app)

                elif event.key == pygame.K_ESCAPE:  # Нажатие Escape
                    self.app.running = False

            # Меню новой игры
            elif self.new_game:

                if event.key == pygame.K_RETURN and self.new_game_menu_buttons[1].active:  # Нажатие Enter
                    app.player_name = self.new_game_menu_buttons[0].text.strip()
                    self.app.state = Game(self.app)

                elif event.key == pygame.K_ESCAPE:  # Нажатие Escape
                    self.new_game = False
                    self.new_game_menu_buttons[0].text = self.app.player_name
                    self.new_game_menu_buttons[1].active = bool(self.app.player_name)

                else:  # Обработка ввода с клавиатуры
                    self.new_game_menu_buttons[0].keyboard_input(event)
                    if not self.new_game_menu_buttons[0].text.strip() and self.new_game_menu_buttons[1].active:
                        self.new_game_menu_buttons[1].active = False
                    elif self.new_game_menu_buttons[0].text.strip() and not self.new_game_menu_buttons[1].active:
                        self.new_game_menu_buttons[1].active = True

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

        # Отрисовка названия игры
        title_text = self.app.font_64.render('Трубопровод', True, 'black')
        self.app.screen.blit(title_text, ((self.width - title_text.get_width()) // 2, 8))

        # Отрисовка кнопок главного меню
        for i, button in enumerate(self.main_menu_buttons):
            button.draw(self.menu_button_x, 128 + 96 * i)

        # Отрисовка меню новой игры
        if self.new_game:
            self.new_game_menu.draw()

        pygame.display.flip()  # Отображение изменений на экране


class Leaderboard:
    """
    Таблица рекордов
    """

    def __init__(self, application):
        self.app = application

        self.width, self.height = 1088, 640

        if pygame.display.get_window_size() != (self.width, self.height):  # Размер окна не соответствует требуемому
            pygame.display.quit()
            self.app.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Игра "Трубопровод"')
            pygame.display.set_icon(pygame.image.load('assets/icon.png'))

        self.leaderboard_bg = pygame.image.load('assets/leaderboard_bg.png').convert_alpha()
        self.first_page_button = pygame.image.load('assets/first_page_button.png').convert_alpha()
        self.previous_page_button = pygame.image.load('assets/previous_page_button.png').convert_alpha()
        self.next_page_button = pygame.image.load('assets/next_page_button.png').convert_alpha()
        self.last_page_button = pygame.image.load('assets/last_page_button.png').convert_alpha()
        self.back_button = pygame.image.load('assets/back_button.png').convert_alpha()

        self.sorted_scores = sorted(self.app.scores.items(), key=lambda item: item[1]['score'], reverse=True)

        self.last_page = (len(self.sorted_scores) - 1) // 7 + 1 if len(self.sorted_scores) > 0 else 1
        self.page = 1

    def event_handler(self, event):
        """
        Обработка событий
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if 0 <= x <= 64 and 0 <= y <= 64 and event.button == 1:  # Клик по кнопке возврата в меню
                self.app.state = MainMenu(self.app)

            elif 64 <= x <= 1024 and 128 <= y <= 576 and event.button == 4:  # Прокрутка колеса мыши вверх
                self.page = max(self.page - 1, 1)
            elif 64 <= x <= 1024 and 128 <= y <= 576 and event.button == 5:  # Прокрутка колеса мыши вниз
                self.page = min(self.page + 1, self.last_page)

            elif 64 <= x <= 128 and 576 <= y <= 640 and event.button == 1:  # Клик по кнопке первой страницы
                self.page = 1
            elif 128 <= x <= 192 and 576 <= y <= 640 and event.button == 1:  # Клик по кнопке предыдущей страницы
                self.page = max(self.page - 1, 1)
            elif 896 <= x <= 960 and 576 <= y <= 640 and event.button == 1:  # Клик по кнопке следующей страницы
                self.page = min(self.page + 1, self.last_page)
            elif 960 <= x <= 1024 and 576 <= y <= 640 and event.button == 1:  # Клик по кнопке последней страницы
                self.page = self.last_page

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:  # Нажатие Escape
                self.app.state = MainMenu(self.app)

            elif event.key == pygame.K_HOME:  # Нажатие Home
                self.page = 1
            elif event.key == pygame.K_LEFT:  # Нажатие стрелки влево
                self.page = max(self.page - 1, 1)
            elif event.key == pygame.K_RIGHT:  # Нажатие стрелки вправо
                self.page = min(self.page + 1, self.last_page)
            elif event.key == pygame.K_END:  # Нажатие End
                self.page = self.last_page

    def loop(self):
        """
        Цикл таблицы рекордов
        """
        self.app.clock.tick(60)  # Ограничение FPS до 60

    def render(self):
        """
        Отрисовка таблицы рекордов
        """
        self.app.screen.fill('white')  # Заливка экрана белым цветом, чтобы избавиться от прошлого кадра

        self.app.screen.blit(self.leaderboard_bg, (64, 0))  # Отрисовка фона таблицы рекордов

        title_text = self.app.font_45.render('Таблица рекордов', True, 'black')
        self.app.screen.blit(title_text, ((self.width - title_text.get_width()) // 2, -1))  # Отрисовка названия таблицы

        # Отрисовка названий столбцов
        number_title = self.app.font_32.render('№', True, 'black')
        self.app.screen.blit(number_title, ((64 - number_title.get_width()) // 2 + 64, 72))
        name_title = self.app.font_32.render('Имя', True, 'black')
        self.app.screen.blit(name_title, ((320 - name_title.get_width()) // 2 + 128, 72))
        score_title = self.app.font_32.render('Счёт', True, 'black')
        self.app.screen.blit(score_title, ((192 - score_title.get_width()) // 2 + 448, 72))
        size_title = self.app.font_32.render('Поле', True, 'black')
        self.app.screen.blit(size_title, ((128 - size_title.get_width()) // 2 + 640, 72))
        time_title = self.app.font_32.render('Время', True, 'black')
        self.app.screen.blit(time_title, ((128 - time_title.get_width()) // 2 + 768, 72))
        turns_title = self.app.font_32.render('Ходы', True, 'black')
        self.app.screen.blit(turns_title, ((128 - turns_title.get_width()) // 2 + 896, 72))

        for i in range(7 * self.page - 7, min(7 * self.page, len(self.sorted_scores))):
            name = self.sorted_scores[i][0]
            score = self.sorted_scores[i][1]['score']
            size = self.sorted_scores[i][1]['size']
            time = self.sorted_scores[i][1]['time']
            turns = self.sorted_scores[i][1]['turns']

            # Отрисовка данных о рекордах
            number_text = self.app.font_32.render(f'{i + 1}', True, 'black')
            self.app.screen.blit(number_text, ((64 - number_text.get_width()) // 2 + 64, 136 + 64 * (i % 7)))
            name_text = self.app.font_32.render(f'{name}', True, 'black')
            self.app.screen.blit(name_text, ((320 - name_text.get_width()) // 2 + 128, 136 + 64 * (i % 7)))
            score_text = self.app.font_32.render(f'{score}', True, 'black')
            self.app.screen.blit(score_text, ((192 - score_text.get_width()) // 2 + 448, 136 + 64 * (i % 7)))
            size_text = self.app.font_32.render(f'{size}', True, 'black')
            self.app.screen.blit(size_text, ((128 - size_text.get_width()) // 2 + 640, 136 + 64 * (i % 7)))
            time_text = self.app.font_32.render(f'{time}', True, 'black')
            self.app.screen.blit(time_text, ((128 - time_text.get_width()) // 2 + 768, 136 + 64 * (i % 7)))
            turns_text = self.app.font_32.render(f'{turns}', True, 'black')
            self.app.screen.blit(turns_text, ((128 - turns_text.get_width()) // 2 + 896, 136 + 64 * (i % 7)))

        self.app.screen.blit(self.first_page_button, (72, 584))  # Отрисовка кнопки первой страницы
        self.app.screen.blit(self.previous_page_button, (136, 584))  # Отрисовка кнопки предыдущей страницы

        page_text = self.app.font_32.render(f'Страница {self.page} из {self.last_page}', True, 'black')
        self.app.screen.blit(page_text, ((self.width - page_text.get_width()) // 2, 584))  # Отрисовка номера страницы

        self.app.screen.blit(self.next_page_button, (904, 584))  # Отрисовка кнопки следующей страницы
        self.app.screen.blit(self.last_page_button, (968, 584))  # Отрисовка кнопки последней страницы

        self.app.screen.blit(self.back_button, (8, 8))  # Отрисовка кнопки возврата в меню

        pygame.display.flip()  # Отображение изменений на экране


class Tile:
    """
    Фишка
    """

    def __init__(self, pipe, angle):
        self.pipe = pipe  # Тип трубы
        self.angle = angle  # Угол поворота фишки
        self.image = pygame.image.load(f'assets/pipes/{pipe}.png').convert_alpha()

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
    Игровой процесс
    """

    def __init__(self, application):
        self.app = application

        self.pause = False
        self.win = False
        self.high_score = False

        self.scale = 16 * (min(576 // self.app.rows, 1152 // self.app.cols) // 16)  # Размер фишки
        self.grid_width, self.grid_height = self.app.cols * self.scale, self.app.rows * self.scale  # Размер поля
        self.width, self.height = max(self.grid_width, 512), max(self.grid_height, 512) + 64  # Размер окна
        self.grid_x = (self.width - self.grid_width) // 2  # Положение поля по оси X
        self.grid_y = (self.height - self.grid_height + 64) // 2  # Положение поля по оси Y

        if pygame.display.get_window_size() != (self.width, self.height):  # Размер окна не соответствует требуемому
            pygame.display.quit()
            self.app.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Игра "Трубопровод"')
            pygame.display.set_icon(pygame.image.load('assets/icon.png'))

        self.start_x, self.start_y = 0, 0  # Положение начальной фишки
        self.end_x, self.end_y = self.app.cols - 1, self.app.rows - 1  # Положение конечной фишки

        self.tiles = [[Tile(choice(['straight', 'bend', 'cross']), choice([0, 90, 180, 270]))  # Генерация фишек
                       for _ in range(self.app.cols)] for _ in range(self.app.rows)]
        self.tiles[self.start_y][self.start_x] = Tile('start', 0)  # Начальная фишка
        self.tiles[self.end_y][self.end_x] = Tile('end', 0)  # Конечная фишка

        self.water = []

        self.water_images = {
            'start': pygame.image.load('assets/pipes/start_water.png').convert_alpha(),
            'straight': pygame.image.load('assets/pipes/straight_water.png').convert_alpha(),
            'bend': pygame.image.load('assets/pipes/bend_water.png').convert_alpha(),
            'cross': pygame.image.load('assets/pipes/cross_water.png').convert_alpha(),
            'end': pygame.image.load('assets/pipes/end_water.png').convert_alpha()
        }

        self.menu_tint = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.menu_tint.fill((0, 0, 0, 128))  # Затемнение экрана

        self.menu_button_x = (self.width - 320) // 2  # Положение кнопок меню по оси X

        self.pause_button = pygame.image.load('assets/pause_button.png').convert_alpha()
        self.pause_menu_buttons = [
            Button(self.app, 'Продолжить'),
            Button(self.app, 'Выйти в меню')
        ]
        self.pause_menu_bg = pygame.image.load('assets/pause_menu_bg.png').convert_alpha()
        self.pause_menu = Menu(self.app, 'Пауза', self.pause_menu_buttons, self.pause_menu_bg)

        self.win_menu_buttons = [
            Button(self.app, 'Играть ещё раз'),
            Button(self.app, 'Выйти в меню')
        ]
        self.win_menu_bg = pygame.image.load('assets/win_menu_bg.png').convert_alpha()

        self.time = 0
        self.turns = 0
        self.score = 0

        self.check_win()

    def check_win(self):
        """
        Проверка победной ситуации
        """
        direction = None
        x, y = self.start_x, self.start_y
        self.water = [[x, y, 'start']]  # Список координат труб с водой

        if self.tiles[y][x].angle == 0:
            direction = 'right'
            x += 1
        elif self.tiles[y][x].angle == 90:
            direction = 'up'
            y -= 1
        elif self.tiles[y][x].angle == 180:
            direction = 'left'
            x -= 1
        elif self.tiles[y][x].angle == 270:
            direction = 'down'
            y += 1

        while 0 <= x <= self.app.cols - 1 and 0 <= y <= self.app.rows - 1 and direction:
            direction = self.tiles[y][x].water_direction(direction)  # Определение направления движения воды

            if direction:
                pipe = self.tiles[y][x].pipe  # Тип трубы
                if pipe == 'cross' and (self.tiles[y][x].angle == 0 and (direction in ['down', 'left']) or
                                        self.tiles[y][x].angle == 90 and (direction in ['down', 'right']) or
                                        self.tiles[y][x].angle == 180 and (direction in ['up', 'right']) or
                                        self.tiles[y][x].angle == 270 and (direction in ['up', 'left'])):
                    pipe = 'bend'  # Вода движется по нижнему колену (в остальных случаях - по верхнему)

                self.water.append([x, y, pipe])  # Добавление координат трубы с водой в список

                if direction == 'right':
                    x += 1
                elif direction == 'left':
                    x -= 1
                elif direction == 'up':
                    y -= 1
                elif direction == 'down':
                    y += 1
                elif direction == 'end':  # Вода достигла конечной фишки
                    self.win = True
                    time = self.time // 60 if self.time > 60 else 1
                    turns = self.turns if self.turns > 0 else 1
                    self.score = (self.app.rows ** 2 * self.app.cols ** 2 * 100) // (time * turns)
                    if (self.app.player_name not in self.app.scores
                            or self.score > self.app.scores[self.app.player_name]['score']):
                        self.high_score = True
                        self.app.scores[self.app.player_name] = {'score': self.score,
                                                                 'size': f'{self.app.rows}x{self.app.cols}',
                                                                 'time': f'{self.time // 3600:02}:'
                                                                         f'{self.time // 60 % 60:02}',
                                                                 'turns': self.turns}
                    break

    def event_handler(self, event):
        """
        Обработка событий
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            # Обычное состояние игрового процесса
            if (self.grid_x <= x <= self.grid_x + self.grid_width and self.grid_y <= y <= self.grid_y + self.grid_height
                    and not self.pause and not self.win):  # Курсор находится в пределах поля
                tile_x, tile_y = (x - self.grid_x) // self.scale, (y - self.grid_y) // self.scale

                if event.button == 1:  # Левая клавиша мыши
                    _ = self.tiles[tile_y][tile_x] - 90  # Поворот фишки на 90 градусов по часовой стрелке
                    self.turns += 1
                    self.check_win()

                elif event.button == 3:  # Правая клавиша мыши
                    _ = self.tiles[tile_y][tile_x] + 90  # Поворот фишки на 90 градусов против часовой стрелки
                    self.turns += 1
                    self.check_win()

            elif 0 <= x <= 64 and 0 <= y <= 64 and event.button == 1 and not self.pause and not self.win:
                # Клик по кнопке паузы
                self.pause = True

            elif self.menu_button_x <= x <= self.menu_button_x + 320 and event.button == 1:

                # Меню паузы
                if self.pause:
                    if 160 <= y <= 224:  # Клик по "Продолжить"
                        self.pause = False
                    elif 256 <= y <= 320:  # Клик по "Выйти в меню"
                        self.app.state = MainMenu(self.app)

                # Меню победы
                elif self.win:
                    if 224 <= y <= 288:  # Клик по "Играть ещё раз"
                        self.app.state = Game(self.app)
                    elif 320 <= y <= 384:  # Клик по "Выйти в меню"
                        self.app.state = MainMenu(self.app)

        elif event.type == pygame.KEYDOWN:

            # Обычное состояние игрового процесса
            if not self.pause and not self.win:
                if event.key == pygame.K_ESCAPE:  # Нажатие Escape
                    self.pause = True

            # Меню паузы
            elif self.pause:
                if event.key == pygame.K_RETURN:  # Нажатие Enter
                    self.pause = False
                if event.key == pygame.K_ESCAPE:  # Нажатие Escape
                    self.app.state = MainMenu(self.app)

            # Меню победы
            elif self.win:
                if event.key == pygame.K_RETURN:  # Нажатие Enter
                    self.app.state = Game(self.app)
                if event.key == pygame.K_ESCAPE:  # Нажатие Escape
                    self.app.state = MainMenu(self.app)

    def loop(self):
        """
        Цикл игрового процесса
        """
        self.app.clock.tick(60)  # Ограничение FPS до 60

        if not self.pause and not self.win:
            self.time += 1  # Увеличение счётчика времени

    def render(self):
        """
        Отрисовка игрового процесса
        """
        self.app.screen.fill('white')  # Заливка экрана белым цветом, чтобы избавиться от прошлого кадра

        self.app.screen.blit(self.pause_button, (8, 8))  # Отрисовка кнопки паузы

        # Отрисовка счётчика времени
        time_text = self.app.font_45.render(f'{self.time // 3600:02}:{self.time // 60 % 60:02}', True, 'black')
        time_x = (self.width - time_text.get_width()) // 2
        self.app.screen.blit(time_text, (time_x, -1))

        # Отрисовка счётчика ходов
        turns_text = self.app.font_45.render(f'{self.turns}', True, 'black')
        turns_x = self.width - turns_text.get_width() - 16
        self.app.screen.blit(turns_text, (turns_x, -1))

        # Отрисовка фишек
        for tile_y, row in enumerate(self.tiles):
            for tile_x, tile in enumerate(row):
                x, y = self.grid_x + tile_x * self.scale, self.grid_y + tile_y * self.scale
                scaled_image = pygame.transform.scale(pygame.transform.rotate(tile.image, tile.angle),
                                                      (self.scale, self.scale))
                self.app.screen.blit(scaled_image, (x, y))

        # Отрисовка воды в трубах
        for tile_x, tile_y, pipe in self.water:
            x, y = self.grid_x + tile_x * self.scale, self.grid_y + tile_y * self.scale
            scaled_water = pygame.transform.scale(pygame.transform.rotate(
                self.water_images[pipe], self.tiles[tile_y][tile_x].angle), (self.scale, self.scale))
            self.app.screen.blit(scaled_water, (x, y))

        # Отрисовка меню паузы
        if self.pause:
            self.pause_menu.draw()

        # Отрисовка меню победы
        if self.win:
            self.app.screen.blit(self.menu_tint, (0, 0))  # Отрисовка затемнения экрана
            self.app.screen.blit(self.win_menu_bg, ((self.width - 384) // 2, 64))  # Отрисовка фона меню победы

            # Отрисовка заголовка меню победы
            win_title_text = self.app.font_45.render('Новый рекорд!' if self.high_score else 'Победа!', True, 'black')
            win_title_x = (self.width - win_title_text.get_width()) // 2
            self.app.screen.blit(win_title_text, (win_title_x, 63))

            # Отрисовка счёта
            score_text = self.app.font_45.render(f'Cчёт: {self.score}', True, 'black')
            score_x = (self.width - score_text.get_width()) // 2
            self.app.screen.blit(score_text, (score_x, 143))

            # Отрисовка кнопок меню победы
            for i, button in enumerate(self.win_menu_buttons):
                button.draw(self.menu_button_x, 224 + 96 * i)

        pygame.display.flip()  # Отображение изменений на экране


if __name__ == '__main__':
    app = App()
    app.execute()
