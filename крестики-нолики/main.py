import pygame
import sys
import os 


# Размер окна меню
menu_width = 600
menu_height = 600

# Цвета
black = (0, 0, 0)
neon_green = (57, 255, 20)
neon_yellow = (255, 255, 0)
neon_white = (255, 255, 255)

# Создание окна меню
pygame.init()
menu_screen = pygame.display.set_mode((menu_width, menu_height))
pygame.display.set_caption("Главное меню")

# Шрифт для кнопок
font = pygame.font.Font(None, 38)

# Функция для выполнения выбранного скрипта и закрытия меню
def run_selected_script(script_to_run):
    if script_to_run:
        os.system(f"python {script_to_run}")
        pygame.quit()
        sys.exit()

# Функция для отрисовки кнопки
def draw_button(text, x, y, width, height, button_color, text_color, script_to_run=None):
    pygame.draw.rect(menu_screen, button_color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x + width // 2, y + height // 2)
    menu_screen.blit(text_surface, text_rect)

    if script_to_run:
        if x <= pygame.mouse.get_pos()[0] <= x + width and y <= pygame.mouse.get_pos()[1] <= y + height:
            run_selected_script(script_to_run)

# Основной игровой цикл меню
menu_running = True
selected_level = None

while menu_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 200 <= x <= 400:
                if 150 <= y <= 200:
                    selected_level = "three.py"  # Уровень сложности 3x3
                elif 250 <= y <= 300:
                    selected_level = "six.py" # Уровень сложности 6x6
                elif 350 <= y <= 400:
                    selected_level = "twelve.py"  # Уровень сложности 12x12

    # Отрисовка фона
    menu_screen.fill(black)

    # Отрисовка кнопок
    draw_button("Выбрать 3x3", 200, 150, 200, 50, neon_yellow if selected_level == "three.py" else neon_green, neon_white, "three.py")
    draw_button("Выбрать 6x6", 200, 250, 200, 50, neon_yellow if selected_level == "six.py" else neon_green, neon_white, "six.py")
    draw_button("Выбрать 12x12", 200, 350, 200, 50, neon_yellow if selected_level == "twelve.py" else neon_green, neon_white, "twelve.py")

    # Надпись "Выбор сложности"
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Выбор сложности", True, neon_yellow)
    title_rect = title_text.get_rect()
    title_rect.center = (menu_width // 2, 50)
    menu_screen.blit(title_text, title_rect)

    pygame.display.flip()

    if selected_level:
        menu_running = False
