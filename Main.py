import pygame
import sys
from functions.aux_functions import interpolate_points
import numpy as np


# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DrawAndGuess")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 200,  0)
RED = (200, 0, 0)

# Fuente
font = pygame.font.SysFont(None, 36)

# Lista de puntos
points = []

# Botón Continuar
button_rect_continuar = pygame.Rect(WIDTH - 460, HEIGHT - 80, 150, 40)

def draw_button_continuar():
    pygame.draw.rect(screen, GREEN, button_rect_continuar)
    text = font.render("Continuar", True, WHITE)
    screen.blit(text, (button_rect_continuar.x + 20, button_rect_continuar.y + 5))

# Botón Revisar
button_rect_revisar = pygame.Rect(WIDTH - 460, HEIGHT - 80, 130, 40)

def draw_button_revisar():
    pygame.draw.rect(screen, GREEN, button_rect_revisar)
    text = font.render("Revisar", True, WHITE)
    screen.blit(text, (button_rect_revisar.x + 20, button_rect_revisar.y + 5))

# Botón Jugar
button_rect_jugar = pygame.Rect(WIDTH - 480, HEIGHT - 350, 160, 60)

def draw_button_jugar():
    pygame.draw.rect(screen, GREEN, button_rect_jugar)
    text = font.render("Iniciar", True, WHITE)
    screen.blit(text, (button_rect_jugar.x + 50, button_rect_jugar.y + 16))

# Botón Bezier
button_rect_Bezier = pygame.Rect(WIDTH - 480, HEIGHT - 350, 160, 60)

def draw_button_Bezier():
    pygame.draw.rect(screen, GREEN, button_rect_Bezier)
    text = font.render("Bezier", True, WHITE)
    screen.blit(text, (button_rect_Bezier.x + 50, button_rect_Bezier.y + 16))

# Botón Polinomio
button_rect_Polinomio = pygame.Rect(WIDTH - 480, HEIGHT - 250, 160, 60)

def draw_button_Polinomio():
    pygame.draw.rect(screen, GREEN, button_rect_Polinomio)
    text = font.render("Polinomio", True, WHITE)
    screen.blit(text, (button_rect_Polinomio.x + 30, button_rect_Polinomio.y + 16))

def draw_points(metodo):
    if len(points) > 0:
        # Dibujar los puntos originales como círculos pequeños
        if(fase == "Dibujo"):
            for point in points:
                 pygame.draw.circle(screen, BLUE, (int(point[0]), int(point[1])), 5)
        
        # Dibujar líneas suavizadas si hay suficientes puntos
        if len(points) >= 2:
            interpolated = interpolate_points(points,metodo)
            if len(interpolated) > 1:
                pygame.draw.lines(screen, RED, False, [(int(x), int(y)) for x, y in interpolated], 3)

def check(target_word,player_word):   
    if(target_word.upper() == player_word.upper()):
        return True
    else:
        return False
                        

def show_result(success,life):
    color = GREEN if success else RED
    message = "¡Correcto!" if success else "Intenta de nuevo. Quedan " + str(life) + " intentos"
    
    if life == 0:
        message = "Perdiste. Vuelvan a empezar."
        
    pygame.draw.rect(screen, color, (WIDTH - 850, HEIGHT//2 - 50, 880, 100))
    text = font.render(message, True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    
    pygame.display.flip()
    pygame.time.wait(3000)

# Variables del juego
Initial_points = 5
Rest_points = 5
time = 60
clock = pygame.time.Clock()
life = 3
fase = "Menu"
target_words = ["Cuadrado", "Casa", "Arbol", "Estrella", "Corazon"]
target_word = np.random.choice(target_words)
player_word = ""
metodo = "Polinomio"
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT,1000)

# Bucle principal del juego
running = True
while running:
    screen.fill(WHITE)
    if(fase != "Menu" and fase != "Interpolar"):
        text = font.render(f"{time}", True, BLACK)
        screen.blit(text, (390, 25))
        draw_points(metodo)
    
    if(fase == "Menu"):
        draw_button_jugar()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    pos = pygame.mouse.get_pos()
                    if button_rect_jugar.collidepoint(pos):
                        fase = "Interpolar"
                        
    elif(fase == "Interpolar"):
        draw_button_Bezier()
        draw_button_Polinomio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    pos = pygame.mouse.get_pos()
                    if button_rect_Bezier.collidepoint(pos):
                        fase = "Dibujo"
                        time = 60
                        Rest_points = 5
                        life = 3
                        target_word = np.random.choice(target_words)
                        player_word = ""
                        points = []
                        metodo = "Bezier"
                    if button_rect_Polinomio.collidepoint(pos):
                        fase = "Dibujo"
                        time = 60
                        Rest_points = 5
                        life = 3
                        target_word = np.random.choice(target_words)
                        player_word = ""
                        points = []
                        metodo = "Polinomio"
    elif(fase == "Dibujo"):
        # Mostrar palabra objetivo
        text = font.render(f"Dibuja: {target_word}", True, BLACK)
        screen.blit(text, (20, 20))
        text = font.render(f"Puntos restantes: {Rest_points}", True, BLACK)
        screen.blit(text, (540, 20))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == TIMER_EVENT:
                time-= 1
                if(time == 0):
                    time = 120
                    fase = "Adivinar"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    pos = pygame.mouse.get_pos()
                    if button_rect_continuar.collidepoint(pos):
                        fase = "Adivinar"
                        time = 120
                    elif Rest_points > 0:
                        points.append(pos)
                        Rest_points -= 1
                elif event.button == 3:
                    if len(points) > 0:
                         points.pop()
                         Rest_points += 1
                
        draw_button_continuar()
    
    elif fase == "Adivinar":
        texto = player_word
        while len(texto) < len(target_word):
            texto += "_"
        
        text = font.render(f"Letras Restantes: {len(target_word)-len(player_word)}", True, BLACK)
        screen.blit(text, (20, 20))
        
        text = font.render(f"Palabra: {texto}", True, BLACK)
        screen.blit(text, (20, 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == TIMER_EVENT:
                time-= 1
                if(time == 0):
                    time = 60
                    fase = "Dibujo"
                    life = 3
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    pos = pygame.mouse.get_pos()
                    if button_rect_revisar.collidepoint(pos):
                        result = check(target_word,player_word)
                        if not result:
                            life -=1
                            player_word = ""
                        show_result(result,life)
                        if result:
                            target_word = np.random.choice(target_words)  
                            time = 60
                            Initial_points = int(time / 20 + life) # Ajustar esto de los puntos
                            Rest_points += Initial_points
                            if Rest_points < 5:
                                Rest_points = 5
                            fase = "Dibujo"
        
                        if life == 0:
                            fase = "Dibujo"
                            Initial_points = 5
                            Rest_points = 5
                            time = 60
            elif event.type == pygame.KEYDOWN:
                if len(target_word) - len(player_word) > 0:
                     letra = event.unicode.upper()
                     player_word += letra
                if(event.key == pygame.K_BACKSPACE):
                    player_word = player_word[:-2]
        
        text = ""
      
        draw_button_revisar()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
