import pygame
import sys
import math

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Interpolación")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Fuente
font = pygame.font.SysFont(None, 36)

# Palabra objetivo
target_word = "Cuadrado"

# Lista de puntos
points = []

# Botón revisar
button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 60, 120, 40)

def draw_button():
    pygame.draw.rect(screen, GREEN, button_rect)
    text = font.render("Revisar", True, WHITE)
    screen.blit(text, (button_rect.x + 20, button_rect.y + 5))

def draw_points():
    for point in points:
        pygame.draw.circle(screen, BLACK, point, 5)
    if len(points) > 1:
        pygame.draw.lines(screen, BLUE, False, points, 2)


def show_result(success):
    msg = "¡Correcto!" if success else "Intenta otra vez"
    color = GREEN if success else RED
    text = font.render(msg, True, color)
    screen.blit(text, (20, HEIGHT - 50))

# Bucle principal
running = True
result = None

while running:
    screen.fill(WHITE)

    # Mostrar palabra objetivo
    word_text = font.render(f"Dibuja: {target_word}", True, BLACK)
    screen.blit(word_text, (20, 20))

    draw_points()
    draw_button()

    if result is not None:
        show_result(result)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Clic del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if button_rect.collidepoint(x, y):
                result = False # Aqui debo crear funcion para revisar que este correcta la figura
            else:
                points.append((x, y))

        # Tecla R para reiniciar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                points = []
                result = None

    pygame.display.flip()

pygame.quit()
sys.exit()