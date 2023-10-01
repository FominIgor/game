import pygame
import sys
import random
import sqlite3

# Инициализация Pygame
pygame.init()

# Размер экрана
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20

# Цвета
BACKGROUND_COLOR = (230, 230, 230)
TEXT_COLOR = (0, 0, 0)
HEAD_COLOR = (0, 255, 0)
BODY_COLOR = (0, 200, 0)

# Создаем экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Инициализация змейки
snake = [(100, 50), (90, 50), (80, 50)]
snake_direction = (CELL_SIZE, 0)
snake_color = HEAD_COLOR

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
fruit_color = generate_fruit_color()

# Инициализация счета
score = 0

# Начальный цвет змейки
snake_color = HEAD_COLOR

# Файлы для хранения лучших результатов
highscore_file_easy = "highscore_easy.txt"
highscore_file_medium = "highscore_medium.txt"
highscore_file_hard = "highscore_hard.txt"

# Загрузка лучших результатов
def load_highscore(file_name):
    try:
        with open(file_name, "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

highscore_easy = load_highscore(highscore_file_easy)
highscore_medium = load_highscore(highscore_file_medium)
highscore_hard = load_highscore(highscore_file_hard)

game_speed = 150  # Скорость игры (легкая сложность)

# База данных SQLite
conn = sqlite3.connect("snake_scores.db")
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    score INTEGER,
                    difficulty TEXT
                )''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

# Основная игровая логика
def start_game(speed, player_name):
    global snake, snake_direction, snake_color, fruit, fruit_color, score, game_speed
    game_speed = speed

    snake = [(100, 50), (90, 50), (80, 50)]
    snake_direction = (CELL_SIZE, 0)
    snake_color = HEAD_COLOR
    fruit = generate_fruit_position()
    fruit_color = generate_fruit_color()
    score = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP and snake_direction != (0, CELL_SIZE):
                    snake_direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -CELL_SIZE):
                    snake_direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and snake_direction != (CELL_SIZE, 0):
                    snake_direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-CELL_SIZE, 0):
                    snake_direction = (CELL_SIZE, 0)

        # Перемещение змейки
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        # Проверка на столкновение с фруктом
        if abs(snake[0][0] - fruit[0]) < CELL_SIZE and abs(snake[0][1] - fruit[1]) < CELL_SIZE:
            score += 1
            fruit = generate_fruit_position()
            snake_color = generate_fruit_color()  # Устанавливаем цвет змейке как цвет фрукта
        else:
            snake.pop()

        # Проверка на столкновение с границами экрана
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT):
            if game_speed == 150:
                if score > highscore_easy:
                    highscore_easy = score
                    save_highscore(player_name, score, "easy")  # Сохраняем рекорд в БД
            elif game_speed == 100:
                if score > highscore_medium:
                    highscore_medium = score
                    save_highscore(player_name, score, "medium")  # Сохраняем рекорд в БД
            elif game_speed == 50:
                if score > highscore_hard:
                    highscore_hard = score
                    save_highscore(player_name, score, "hard")  # Сохраняем рекорд в БД
            game_over_screen(player_name, score, speed)  # Передаем имя игрока и сложность
            return

        # Проверка на столкновение с самой собой
        for segment in snake[1:]:
            if snake[0] == segment:
                if game_speed == 150:
                    if score > highscore_easy:
                        highscore_easy = score
                        save_highscore(player_name, score, "easy")  # Сохраняем рекорд в БД
                elif game_speed == 100:
                    if score > highscore_medium:
                        highscore_medium = score
                        save_highscore(player_name, score, "medium")  # Сохраняем рекорд в БД
                elif game_speed == 50:
                    if score > highscore_hard:
                        highscore_hard = score
                        save_highscore(player_name, score, "hard")  # Сохраняем рекорд в БД
                game_over_screen(player_name, score, speed)  # Передаем имя игрока и сложность
                return

        # Заливка фона
        screen.fill(BACKGROUND_COLOR)

        # Отрисовка змейки
        for i, segment in enumerate(snake):
            if i == 0:
                pygame.draw.rect(screen, snake_color, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, BODY_COLOR, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Отрисовка фрукта
        pygame.draw.rect(screen, fruit_color, (fruit[0], fruit[1], CELL_SIZE, CELL_SIZE))

        # Отрисовка счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        clock.tick(speed)

# Экран после завершения игры
def game_over_screen(player_name, score, difficulty):
    conn = sqlite3.connect("snake_scores.db")
    cursor = conn.cursor()

    # Вставьте рекорд в таблицу
    cursor.execute("INSERT INTO players (name, score, difficulty) VALUES (?, ?, ?)", (player_name, score, difficulty))

    # Получите топ-5 рекордов для выбранной сложности
    cursor.execute("SELECT name, score FROM players WHERE difficulty = ? ORDER BY score DESC LIMIT 5", (difficulty,))
    top_scores = cursor.fetchall()

    # Получите место игрока в рейтинге
    cursor.execute("SELECT COUNT(*) FROM players WHERE difficulty = ? AND score > ?", (difficulty, score))
    player_rank = cursor.fetchone()[0] + 1

    conn.commit()
    conn.close()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    main_menu()

        screen.fill(BACKGROUND_COLOR)
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Игра окончена", True, TEXT_COLOR)
        retry_text = font.render("Нажмите Enter для повторной игры", True, TEXT_COLOR)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, 250))

        # Отрисовка топ-5 рекордов
        top_scores_text = font.render("Топ-5 рекордов:", True, TEXT_COLOR)
        screen.blit(top_scores_text, (WIDTH // 2 - top_scores_text.get_width() // 2, 300))
        y = 350
        for i, (player, player_score) in enumerate(top_scores, start=1):
            player_text = font.render(f"{i}. {player}: {player_score}", True, TEXT_COLOR)
            screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, y))
            y += 30

        # Отрисовка места игрока
        player_rank_text = font.render(f"Ваше место: {player_rank}", True, TEXT_COLOR)
        screen.blit(player_rank_text, (WIDTH // 2 - player_rank_text.get_width() // 2, y))

        pygame.display.flip()

# Сохранение лучшего результата
def save_highscore(player_name, score, difficulty):
    conn = sqlite3.connect("snake_scores.db")
    cursor = conn.cursor()

    # Получите текущий лучший рекорд для данной сложности
    cursor.execute("SELECT score FROM players WHERE difficulty = ? ORDER BY score DESC LIMIT 1", (difficulty,))
    current_highscore = cursor.fetchone()

    # Если текущий рекорд отсутствует или новый рекорд выше, обновите его
    if not current_highscore or score > current_highscore[0]:
        cursor.execute("INSERT INTO players (name, score, difficulty) VALUES (?, ?, ?)", (player_name, score, difficulty))

    conn.commit()
    conn.close()

# Главное меню
def main_menu():
    player_name = input("Введите имя игрока: ")

    selected_difficulty = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_1:
                    selected_difficulty = 10  # Легкая сложность
                elif event.key == pygame.K_2:
                    selected_difficulty = 20  # Средняя сложность
                elif event.key == pygame.K_3:
                    selected_difficulty = 30  # Высокая сложность

        if selected_difficulty is not None:
            start_game(selected_difficulty, player_name)

        screen.fill(BACKGROUND_COLOR)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Змейка", True, TEXT_COLOR)
        easy_text = font.render("1 - Легкая сложность", True, TEXT_COLOR)
        medium_text = font.render("2 - Средняя сложность", True, TEXT_COLOR)
        hard_text = font.render("3 - Высокая сложность", True, TEXT_COLOR)
        highscore_text = font.render(f"Лучший результат (легкая): {highscore_easy}", True, TEXT_COLOR)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, 200))
        screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, 250))
        screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, 300))
        screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, 350))
        pygame.display.flip()

# Запуск главного меню
main_menu()
