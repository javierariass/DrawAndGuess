import pygame
import sys
import math
import numpy as np

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

# Palabras objetivo
target_words = ["Cuadrado", "Casa", "Árbol", "Estrella", "Corazón"]
target_word = np.random.choice(target_words)

# Lista de puntos
points = []

# Botón revisar
button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 60, 120, 40)

def draw_button():
    pygame.draw.rect(screen, GREEN, button_rect)
    text = font.render("Revisar", True, WHITE)
    screen.blit(text, (button_rect.x + 20, button_rect.y + 5))

def interpolate_points(points):
    if len(points) < 2:
        return points
    
    # Crear una lista para los puntos interpolados
    interpolated = []
    
    # Interpolación cuadrática entre puntos
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        # Punto de control en el medio con un poco de curvatura
        cx = (x1 + x2) / 2 
        cy = (y1 + y2) / 2
        
        # Ajustar la curvatura basada en la posición relativa
        if i < len(points) - 2:
            x3, y3 = points[i + 2]
            cx += (y2 - y3) * 0.2
            cy += (x3 - x2) * 0.2
        
        # Generar puntos intermedios usando curva cuadrática de Bézier
        for t in np.linspace(0, 1, num=20):
            xt = (1-t)**2 * x1 + 2*(1-t)*t*cx + t**2*x2
            yt = (1-t)**2 * y1 + 2*(1-t)*t*cy + t**2*y2
            interpolated.append((xt, yt))
    
    return interpolated

def draw_points():
    if len(points) > 0:
        # Dibujar los puntos originales como círculos pequeños
        for point in points:
            pygame.draw.circle(screen, BLUE, (int(point[0]), int(point[1])), 5)
        
        # Dibujar líneas suavizadas si hay suficientes puntos
        if len(points) >= 2:
            interpolated = interpolate_points(points)
            if len(interpolated) > 1:
                pygame.draw.lines(screen, RED, False, [(int(x), int(y)) for x, y in interpolated], 3)

def check_shape():
    if len(points) < 3:
        return False
    
    # Aquí la logica de revision, se retorna true para testear 
    return True

def show_result(success):
    color = GREEN if success else RED
    message = "¡Correcto!" if success else "Intenta de nuevo"
    
    pygame.draw.rect(screen, color, (WIDTH//2 - 150, HEIGHT//2 - 50, 300, 100))
    text = font.render(message, True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    
    pygame.display.flip()
    pygame.time.wait(2000)

# Bucle principal del juego
running = True
while running:
    screen.fill(WHITE)
    
    # Mostrar palabra objetivo
    text = font.render(f"Dibuja: {target_word}", True, BLACK)
    screen.blit(text, (20, 20))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(pos):
                    success = check_shape()
                    show_result(success)
                    points = []  
                    target_word = np.random.choice(target_words)  
                else:
                    points.append(pos)
        
    draw_points()
    draw_button()
    
    pygame.display.flip()

pygame.quit()
sys.exit()
