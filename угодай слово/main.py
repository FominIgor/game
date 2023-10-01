import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размер экрана
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Создаем экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Инициализация змейки
snake = [(100, 50), (90, 50), (80, 50)]
snake_direction = (CELL_SIZE, 0)
snake_color = GREEN  # Исходный цвет змейки

# Инициализация фрукта
def generate_fruit_position():
    while True:
        fruit_position = (
            random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        )
        if fruit_position not in snake:
            return fruit_position

def generate_fruit_color():
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

fruit = generate_fruit_position()
fruit_color = generate_fruit_color()  # Исходный цвет фрукта

# Инициализация счета
score = 0

# Начальный цвет змейки
snake_color = GREEN

# Состояния игры
MAIN_MENU = 0
IN_GAME = 1
GAME_OVER = 2

# Изначально находимся в главном меню
game_state = MAIN_MENU

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == MAIN_MENU:
        # Главное меню
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # Переключаемся в состояние игры
            snake = [(100, 50), (90, 50), (80, 50)]
            snake_direction = (CELL_SIZE, 0)
            snake_color = GREEN
            fruit = generate_fruit_position()
            fruit_color = generate_fruit_color()
            score = 0
            game_state = IN_GAME

        # Отрисовка главного меню
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Змейка", True, (0, 0, 0))
        start_text = font.render("Нажмите Enter для начала игры", True, (0, 0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 200))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 250))
        pygame.display.flip()
        pygame.time.delay(150)

    elif game_state == IN_GAME:
        # Обработка клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, CELL_SIZE):
                    snake_direction = (0, -CELL_SIZE)  # Движение вверх
                elif event.key == pygame.K_DOWN and snake_direction != (0, -CELL_SIZE):
                    snake_direction = (0, CELL_SIZE)  # Движение вниз
                elif event.key == pygame.K_LEFT and snake_direction != (CELL_SIZE, 0):
                    snake_direction = (-CELL_SIZE, 0)  # Движение влево
                elif event.key == pygame.K_RIGHT and snake_direction != (-CELL_SIZE, 0):
                    snake_direction = (CELL_SIZE, 0)  # Движение вправо

        # Перемещение змейки
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        # Проверка на столкновение с фруктом
        if abs(snake[0][0] - fruit[0]) < CELL_SIZE and abs(snake[0][1] - fruit[1]) < CELL_SIZE:
            score += 1
            fruit = generate_fruit_position()
            snake_color = generate_fruit_color()

        else:
            snake.pop()

        # Проверка на столкновение с границами экрана
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT):
            game_state = GAME_OVER

        # Проверка на столкновение с самой собой
        for segment in snake[1:]:
            if snake[0] == segment:
                game_state = GAME_OVER

        # Заливка фона
        screen.fill(WHITE)

        # Отрисовка змейки
        for segment in snake:
            pygame.draw.rect(screen, snake_color, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Отрисовка фрукта
        pygame.draw.rect(screen, fruit_color, (fruit[0], fruit[1], CELL_SIZE, CELL_SIZE))

        # Отрисовка счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Обновление экрана
        pygame.display.flip()

        # Задержка
        pygame.time.delay(150)

    elif game_state == GAME_OVER:
        # Меню после проигрыша
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # Возвращаемся в главное меню
            game_state = MAIN_MENU

        # Отрисовка меню после проигрыша
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Игра окончена", True, (0, 0, 0))
        retry_text = font.render("Нажмите Enter для повторной игры", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, 250))
        pygame.display.flip()
        pygame.time.delay(150)
