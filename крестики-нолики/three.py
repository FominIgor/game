import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размер окна
screen_width = 600
screen_height = 700

# Цвета
black = (0, 0, 0)
neon_green = (57, 255, 20)
neon_yellow = (255, 255, 0)
neon_white = (255, 255, 255)

# Создание окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Крестики-нолики")

# Размеры сетки
rows = 3
cols = 3
cell_size = screen_width // cols

# Игровое поле
board = [[' ' for _ in range(cols)] for _ in range(rows)]

# Игроки
player_x = 'X'
player_o = 'O'

# Флаг для определения текущего игрока
current_player = player_x

# Счетчики побед
score_x = 0
score_o = 0

# Функция для отрисовки сетки
def draw_grid():
    for i in range(1, rows):
        pygame.draw.line(screen, neon_green if current_player == player_x else neon_yellow,
                         (0, i * cell_size), (screen_width, i * cell_size), 2)
        pygame.draw.line(screen, neon_green if current_player == player_x else neon_yellow,
                         (i * cell_size, 0), (i * cell_size, 600), 2)

# Функция для отрисовки крестика или нолика
def draw_symbol(row, col, symbol):
    x = col * cell_size + cell_size // 2
    y = row * cell_size + cell_size // 2

    if symbol == 'X':
        pygame.draw.line(screen, neon_green, (x - 50, y - 50), (x + 50, y + 50), 3)
        pygame.draw.line(screen, neon_green, (x + 50, y - 50), (x - 50, y + 50), 3)
    elif symbol == 'O':
        pygame.draw.circle(screen, neon_yellow, (x, y), 50, 3)

# Функция для проверки победителя
def check_winner(board, player):
    # Проверка по строкам и столбцам
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True

    # Проверка по диагоналям
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# Функция для проверки ничьей
def check_draw(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

# Функция для очистки игрового поля
def reset_board():
    return [[' ' for _ in range(cols)] for _ in range(rows)]

# Функция для отрисовки счетчика побед
def draw_score():
    font = pygame.font.Font(None, 36)
    font1 = pygame.font.Font(None, 33)
    text_x = font.render(f"Крестики: {score_x}", True, neon_white)
    text_o = font.render(f"Нолики: {score_o}", True, neon_white)
    text = font1.render(f"Для победы необходимо набрать 3 элемента в ряд", True, neon_white)
    screen.blit(text, (20, screen_height - 90))
    screen.blit(text_x, (120, screen_height - 50))
    screen.blit(text_o, (screen_width - 270, screen_height - 50))

# Основной игровой цикл
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            row = y // cell_size
            col = x // cell_size

            if board[row][col] == ' ':
                board[row][col] = current_player
                if current_player == player_x:
                    current_player = player_o
                else:
                    current_player = player_x

        # Проверка на победу или ничью
        if check_winner(board, player_x):
            score_x += 1
            print("Победили Крестики!")
            board = reset_board()
        elif check_winner(board, player_o):
            score_o += 1
            print("Победили Нолики!")
            board = reset_board()
        elif check_draw(board):
            print("Ничья!")
            board = reset_board()

    # Отрисовка игры
    screen.fill(black)
    draw_grid()

    for row in range(rows):
        for col in range(cols):
            if board[row][col] == player_x:
                draw_symbol(row, col, player_x)
            elif board[row][col] == player_o:
                draw_symbol(row, col, player_o)

    draw_score()
    pygame.display.flip()

# Код завершится при закрытии окна Pygame
