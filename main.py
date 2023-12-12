import pygame
import sys

# Tamaño del tablero de ajedrez
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = (WIDTH-200) // COLS

# Colores
RICH_BLACK = (13, 27, 42)
OXFORD_BLUE = (27, 38, 59)
YINMN_BLUE = (65, 90, 119)
SILVER_LAKE_BLUE = (119, 141, 169)
PLATINUM = (224, 225, 221)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recorrido del Caballo en Ajedrez")

horse_font = pygame.font.SysFont('Segoe UI Emoji', 36)
number_font = pygame.font.Font(None, 25)
font = pygame.font.Font(None, 30)
info_font = pygame.font.Font(None, 20)

# Lista para almacenar las coordenadas de las casillas visitadas (Para la linea que las conecta)
visited_coordinates = []

# Matriz para almacenar las casillas visitadas (Para el recorrido del caballo)
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

def draw_board(screen):
    for row in range(ROWS):
        for col in range(COLS):
            color = YINMN_BLUE if (row + col) % 2 == 0 else RICH_BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_number(screen, row, col, number):
    text = number_font.render(str(number), True, SILVER_LAKE_BLUE) 
    text_rect = text.get_rect()
    text_rect.topleft = (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 10)  # Ajusta la posición
    screen.blit(text, text_rect)

# Recorrido del caballo
def knight_tour(screen, start_position):
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)] # Movimientos relativos posibles del caballo
    row, col = start_position
    move_count = 1

    horse_char = "🐴" # Carácter (emoji) del caballo para mostrar en la animación

    # Lista para almacenar la posición y el número de cada casilla
    number_positions = []

    while move_count <= ROWS * COLS:
        draw_board(screen)
        visited[row][col] = True
        number_positions.append((row, col, move_count))  # Almacena la posición y el número en la lista
        
        for row_num, col_num, number in number_positions:
            draw_number(screen, row_num, col_num, number)  # Dibuja los números en sus posiciones

        # Dibuja las líneas que conectan las casillas visitadas
        for i in range(len(visited_coordinates) - 1):
            x1, y1 = visited_coordinates[i][1] * SQUARE_SIZE + SQUARE_SIZE // 2, visited_coordinates[i][0] * SQUARE_SIZE + SQUARE_SIZE // 2
            x2, y2 = visited_coordinates[i + 1][1] * SQUARE_SIZE + SQUARE_SIZE // 2, visited_coordinates[i + 1][0] * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, PLATINUM, (x1, y1), (x2, y2), 1)

        # Renderiza y dibuja el carácter del caballo
        text_surface = horse_font.render(horse_char, True, (255, 0, 0))
        emoji_rect = text_surface.get_rect()
        emoji_rect.center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
        screen.blit(text_surface, emoji_rect)

        pygame.display.update()

        possible_moves = []
        for dr, dc in moves:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS and not visited[r][c]:
                possible_moves.append((r, c))

        if not possible_moves:
            break
        
        # Ordena los movimientos posibles por el número de movimientos posibles que tienen
        possible_moves.sort(key=lambda x: sum(1 for dr, dc in moves if 0 <= x[0] + dr < ROWS and 0 <= x[1] + dc < COLS and not visited[x[0] + dr][x[1] + dc]))

        next_move = possible_moves[0]
        row, col = next_move
        move_count += 1

        visited_coordinates.append((row, col))

        pygame.time.delay(100)

# Botón para iniciar la animación
start_button = pygame.Rect(WIDTH - 142, 10, 85, 30)
start_button_color = OXFORD_BLUE
start_text = font.render("Iniciar", True, SILVER_LAKE_BLUE)
star_text_width = start_text.get_width()

# Selección de posición inicial
start_positions = [0, 0]
start_position_rect = pygame.Rect(WIDTH - 135, 55, 70, 40)
start_position_color = YINMN_BLUE

running_animation = False
animated = False

draw_board(screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos) and not running_animation:
                running_animation = True
            
        elif event.type == pygame.KEYDOWN and not running_animation:
            animated = False
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                start_positions[0] = (start_positions[0]+1) % ROWS
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                start_positions[1] = (start_positions[1]+1) % COLS
            elif pygame.key.get_pressed()[pygame.K_UP]:
                start_positions[0] = (start_positions[0]-1) % ROWS
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                start_positions[1] = (start_positions[1]-1) % COLS
            elif pygame.key.get_pressed()[pygame.K_RETURN]:
                running_animation = True

    # Dibujar la barra lateral
    pygame.draw.rect(screen, RICH_BLACK, pygame.Rect(WIDTH - 200, 0, 200, HEIGHT))

    pygame.draw.rect(screen, start_button_color, start_button)
    screen.blit(start_text, (int((WIDTH-200) + ((200-star_text_width)/2)), 15))

    pygame.draw.rect(screen, start_position_color, start_position_rect, 2)
    start_position_text = font.render(f"({start_positions[0]}, {start_positions[1]})", True, SILVER_LAKE_BLUE)
    start_position_text_width = start_position_text.get_width()
    screen.blit(start_position_text, (int((WIDTH-200) + ((200-start_position_text_width)/2)), 65))

    # Información
    text = info_font.render("Flechas para mover", True, SILVER_LAKE_BLUE)
    screen.blit(text, (WIDTH - 195, 120))
    text = info_font.render("el punto inicial", True, SILVER_LAKE_BLUE)
    screen.blit(text, (WIDTH - 195, 140))
    text = info_font.render("Enter para iniciar", True, SILVER_LAKE_BLUE)
    screen.blit(text, (WIDTH - 195, 180))

    if running_animation:
        if not all(all(visited[row][col] for col in range(COLS)) for row in range(ROWS)):
            visited_coordinates.append((start_positions[0], start_positions[1]))
            knight_tour(screen, start_positions)

            running_animation = False
        visited = [[False for _ in range(COLS)] for _ in range(ROWS)]
        visited_coordinates = []
        animated = True
    elif not animated:
        draw_board(screen)
        pygame.draw.circle(screen, (255, 0, 0), (start_positions[1] * SQUARE_SIZE + SQUARE_SIZE // 2, start_positions[0] * SQUARE_SIZE + SQUARE_SIZE // 2), 10)
        
    pygame.display.update()
