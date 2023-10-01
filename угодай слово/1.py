import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы для экрана
WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)
FPS = 10

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FOOD_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Инициализация экрана
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Змейка")

# Функция рисования змейки
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, segment[2], (segment[0], segment[1], 20, 20))

# Функция создания еды
def create_food():
    x = random.randrange(0, WIDTH, 20)
    y = random.randrange(0, HEIGHT, 20)
    color = random.choice(FOOD_COLORS)
    return [x, y, color]

# Инициализация змейки
snake = [[100, 50, WHITE]]
snake_dir = [20, 0]

# Инициализация еды
food = create_food()

# Главный игровой цикл
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление змейкой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake_dir = [-20, 0]
    elif keys[pygame.K_RIGHT]:
        snake_dir = [20, 0]
    elif keys[pygame.K_UP]:
        snake_dir = [0, -20]
    elif keys[pygame.K_DOWN]:
        snake_dir = [0, 20]

    # Движение змейки
    new_head = [snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1], snake[0][2]]
    snake.insert(0, new_head)

    # Проверка на столкновение с едой
    if new_head[0] == food[0] and new_head[1] == food[1]:
        food = create_food()
    else:
        snake.pop()

    # Проверка на столкновение с преградой
    if new_head in snake[1:]:
        running = False

    # Очистка экрана
    screen.fill(BLACK)

    # Рисование змейки и еды
    draw_snake(snake)
    pygame.draw.rect(screen, food[2], (food[0], food[1], 20, 20))

    # Обновление экрана
    pygame.display.flip()

    # Ограничение кадров в секунду
    clock.tick(FPS)

# Завершение игры
pygame.quit()
