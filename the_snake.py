import sys
from random import choice
import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона — чёрный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Центр игрового поля:
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

KEY_DIRECTIONS = {
    pg.K_UP: UP,
    pg.K_DOWN: DOWN,
    pg.K_LEFT: LEFT,
    pg.K_RIGHT: RIGHT,
}


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        """Инициализировать позицию и цвет игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовать игровой объект."""

    def draw_cell(self, position):
        """Нарисовать одну игровую ячейку с границей."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(
        self,
        body_color=APPLE_COLOR,
        occupied_positions=None,
    ):
        """Инициализировать яблоко."""
        super().__init__(body_color=body_color)

        if occupied_positions is None:
            occupied_positions = []

        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Установить яблоко на свободную случайную позицию."""
        occupied_positions = set(occupied_positions)

        free_positions = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in occupied_positions
        ]

        if free_positions:
            self.position = choice(free_positions)

    def draw(self):
        """Отрисовать яблоко на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(
        self,
        position=SCREEN_CENTER,
        body_color=SNAKE_COLOR,
    ):
        """Инициализировать змейку."""
        super().__init__(
            position=position,
            body_color=body_color,
        )
        self.reset()

    def update_direction(self):
        """Обновить направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Переместить змейку на одну ячейку."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_x = (
            head_x + direction_x * GRID_SIZE
        ) % SCREEN_WIDTH
        new_y = (
            head_y + direction_y * GRID_SIZE
        ) % SCREEN_HEIGHT

        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовать голову змейки и стереть старый хвост."""
        self.draw_cell(self.get_head_position())

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбросить змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработать действия пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            new_direction = KEY_DIRECTIONS.get(event.key)

            if (
                new_direction is not None
                and new_direction
                != OPPOSITE_DIRECTIONS[game_object.direction]
            ):
                game_object.next_direction = new_direction


def main():
    """Запустить основной игровой цикл."""
    pg.init()

    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head_position = snake.get_head_position()

        # Змейка съела яблоко.
        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Змейка столкнулась сама с собой.
        elif head_position in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
