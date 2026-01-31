import pygame
import random
import sys

# Configuración inicial
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colores Neón
BLACK = (5, 5, 15)
NEON_BLUE = (0, 180, 255)
NEON_PINK = (255, 0, 120)
NEON_CYAN = (0, 255, 255)
GRID_COLOR = (20, 20, 40)

# Variables del juego
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_dir = "RIGHT"
food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
score = 0
clock = pygame.time.Clock()

# Variables para el Swipe (Deslizamiento)
start_pos = None

def show_score():
    font = pygame.font.SysFont('consolas', 40, bold=True)
    surface = font.render(f'SCORE: {score}', True, NEON_CYAN)
    screen.blit(surface, (20, 20))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # DETECCIÓN DE SWIPE
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos # Guarda donde empezaste a tocar
            
        if event.type == pygame.MOUSEBUTTONUP and start_pos:
            end_pos = event.pos # Guarda donde soltaste
            dx = end_pos[0] - start_pos[0] # Diferencia en X
            dy = end_pos[1] - start_pos[1] # Diferencia en Y

            # Determinamos si el movimiento fue más horizontal o vertical
            if abs(dx) > abs(dy):
                if dx > 30 and snake_dir != "LEFT": snake_dir = "RIGHT"
                elif dx < -30 and snake_dir != "RIGHT": snake_dir = "LEFT"
            else:
                if dy > 30 and snake_dir != "UP": snake_dir = "DOWN"
                elif dy < -30 and snake_dir != "DOWN": snake_dir = "UP"
            
            start_pos = None

    # Lógica de movimiento (La misma que en PC)
    if snake_dir == "UP": snake_pos[0][1] -= 10
    if snake_dir == "DOWN": snake_pos[0][1] += 10
    if snake_dir == "LEFT": snake_pos[0][0] -= 10
    if snake_dir == "RIGHT": snake_pos[0][0] += 10

    # Teletransporte
    if snake_pos[0][0] >= WIDTH: snake_pos[0][0] = 0
    if snake_pos[0][0] < 0: snake_pos[0][0] = WIDTH - 10
    if snake_pos[0][1] >= HEIGHT: snake_pos[0][1] = 0
    if snake_pos[0][1] < 0: snake_pos[0][1] = HEIGHT - 10

    # Crecimiento
    snake_pos.insert(0, list(snake_pos[0]))
    if snake_pos[0] == food_pos:
        score += 10
        food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
    else:
        snake_pos.pop()

    # Dibujo
    screen.fill(BLACK)
    for x in range(0, WIDTH, 20): pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 20): pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))
    
    pygame.draw.circle(screen, NEON_PINK, (food_pos[0]+5, food_pos[1]+5), 7)
    for pos in snake_pos:
        pygame.draw.rect(screen, NEON_BLUE, (pos[0], pos[1], 10, 10), border_radius=3)
    
    # Colisión
    for block in snake_pos[1:]:
        if snake_pos[0] == block:
            # En móvil, reiniciamos directo para no cerrar la App
            snake_pos = [[100, 50], [90, 50], [80, 50]]
            snake_dir = "RIGHT"
            score = 0

    show_score()
    pygame.display.flip()
    clock.tick(15 + (score // 50))