from random import choice

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


KEY_DIRECTIONS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}


class GameObject:
    def __init__(self, position=SCREEN_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self, occupied_positions):
        super().__init__(body_color=APPLE_COLOR)
        self.change_position(occupied_positions)

    def draw(self, screen):
        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
    
    def change_position(self, occupied_positions):
        """
        Принимает координаты всего туловища змейки.
        Меняет позицию яблока после поедания,
        Яблоко появляется там, где нет змейки.
        Если таких полей нет (змейка занимает все поле),
        Функция выбрасывает исключение, которое должно быть обработано
        в рантайме игры для ее рестарта.
        """
        occupied = set(occupied_positions)

        if len(occupied) >= GRID_WIDTH * GRID_HEIGHT:
            raise RuntimeError

        free_positions = []
        for column in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT):
                position = (column * GRID_SIZE, row * GRID_SIZE)
                if position not in occupied:
                    free_positions.append(position)
        
        self.position = choice(free_positions)


class Snake(GameObject):
    def __init__(self):
        super().__init__(
            position=SCREEN_CENTER,
            body_color=SNAKE_COLOR,
        )
        self.length = 1
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT

    def draw(self, screen):
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        head_x, head_y = self.positions[0]
        direction_x, direction_y = self.direction

        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def set_direction(self, direction):
        if (direction is not None
                and direction != OPPOSITE_DIRECTIONS[self.direction]):
            self.direction = direction
    
    def grow(self):
        self.length += 1

    def reset(self):
        self.position = SCREEN_CENTER
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            0,
            32,
        )
        pygame.display.set_caption('Змейка')

        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.apple = Apple(self.snake.positions)
        self.is_running = True

    def run(self):
        while self.is_running:
            self.clock.tick(SPEED)
            self.handle_events()

            if self.is_running:
                self.update()
                self.draw()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                direction = KEY_DIRECTIONS.get(event.key)
                if direction is not None:
                    self.snake.set_direction(direction)

    def update(self):
        self.snake.move()

        if self.snake.positions[0] == self.apple.position:
            self.snake.grow()
            self.place_apple()

        if self.snake.positions[0] in self.snake.positions[1:]:
            self.restart()

    def place_apple(self):
        try:
            self.apple.change_position(self.snake.positions)
        except RuntimeError:
            self.restart()

    def restart(self):
        self.snake.reset()
        self.apple.change_position(self.snake.positions)

    def draw(self):
        self.screen.fill(BOARD_BACKGROUND_COLOR)
        self.snake.draw(self.screen)
        self.apple.draw(self.screen)
        pygame.display.update()


def main():
    SnakeGame().run()


if __name__ == '__main__':
    main()
