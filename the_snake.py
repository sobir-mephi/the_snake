from random import randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

KEY_DIRECTIONS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
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
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Инициализировать яблоко."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Установить случайную позицию яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовать яблоко на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        """Инициализировать змейку."""
        super().__init__(
            position=SCREEN_CENTER,
            body_color=SNAKE_COLOR,
        )
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

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
        """Отрисовать змейку и стереть её предыдущий хвост."""
        for position in self.positions:
            self.draw_cell(position)

        if self.last:
            last_rect = pygame.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE),
            )
            pygame.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                last_rect,
            )

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбросить змейку в начальное состояние."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработать действия пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            new_direction = KEY_DIRECTIONS.get(event.key)

            if (
                new_direction is not None
                and new_direction
                != OPPOSITE_DIRECTIONS[game_object.direction]
            ):
                game_object.next_direction = new_direction


def main():
    """Запустить основной игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    # Яблоко не должно появляться внутри змейки.
    while apple.position in snake.positions:
        apple.randomize_position()

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
            apple.randomize_position()

            while apple.position in set(snake.positions):
                apple.randomize_position()

        # Змейка столкнулась сама с собой.
        if head_position in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

            while apple.position in set(snake.positions):
                apple.randomize_position()

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
