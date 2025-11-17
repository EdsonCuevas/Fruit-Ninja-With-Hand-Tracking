import pygame, sys
import os
import random
import cv2
import mediapipe as mp
import threading
import time

# -------------------------
# CONFIGURACIÓN DEL JUEGO
# -------------------------
player_lives = 3
score = 0
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']

WIDTH, HEIGHT = 800, 500
FPS = 15
GAME_TIME = 30  # 30 segundos de juego

pygame.init()
pygame.display.set_caption('Fruit-Ninja con manos')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
background = pygame.image.load('back.jpg')
font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
small_font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 20)
score_text = font.render('Score : ' + str(score), True, WHITE)
lives_icon = pygame.image.load('images/white_lives.png')

# Variables de tiempo
start_time = 0
time_remaining = GAME_TIME
paused = False

# -------------------------
# CAPTURA DE MANO CON MEDIAPIPE
# -------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Variable global para guardar la posición del dedo
finger_pos = (WIDTH//2, HEIGHT//2)
PREVIEW_W, PREVIEW_H = 240, 180
preview_frame = None

def hand_tracking():
    global finger_pos
    global preview_frame
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)  # espejo
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Landmark 8 = punta del índice
                h, w, c = frame.shape
                x = int(hand_landmarks.landmark[8].x * WIDTH)
                y = int(hand_landmarks.landmark[8].y * HEIGHT)
                finger_pos = (x, y)
                mp_draw.draw_landmarks(rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        preview = cv2.resize(rgb, (PREVIEW_W, PREVIEW_H))
        preview_frame = preview

    cap.release()
    cv2.destroyAllWindows()

# Hilo aparte para captura de cámara
threading.Thread(target=hand_tracking, daemon=True).start()

# -------------------------
# FUNCIONES DEL JUEGO
# -------------------------
def generate_random_fruits(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,500),
        'y' : 800,
        'speed_x': random.randint(-5,5),
        'speed_y': random.randint(-80, -60),
        'throw': random.random() >= 0.90,
        't': 0,
        'hit': False,
    }

data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))

def draw_text(display, text, size, x, y, color=WHITE):
    font_draw = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), size)
    text_surface = font_draw.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

def draw_lives(display, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)

def draw_controls():
    """Dibuja las instrucciones de control en pantalla"""
    controls_text = small_font.render('ESC: Pausa | R: Reiniciar', True, YELLOW)
    gameDisplay.blit(controls_text, (WIDTH//2 - 150, HEIGHT - 30))

def show_pause_screen():
    """Muestra la pantalla de pausa"""
    # Semi-transparente overlay
    s = pygame.Surface((WIDTH, HEIGHT))
    s.set_alpha(180)
    s.fill(BLACK)
    gameDisplay.blit(s, (0,0))
    
    draw_text(gameDisplay, "PAUSA", 90, WIDTH / 2, HEIGHT / 3, YELLOW)
    draw_text(gameDisplay, "Presiona ESC para continuar", 40, WIDTH / 2, HEIGHT / 2, WHITE)
    draw_text(gameDisplay, "Presiona R para reiniciar", 40, WIDTH / 2, HEIGHT / 2 + 60, WHITE)
    pygame.display.flip()

def show_gameover_screen():
    gameDisplay.blit(background, (0,0))
    draw_text(gameDisplay, "GAME OVER!", 90, WIDTH / 2, HEIGHT / 4)
    draw_text(gameDisplay,"Score Final: " + str(score), 50, WIDTH / 2, HEIGHT / 2)
    
    if time_remaining <= 0:
        draw_text(gameDisplay, "¡Tiempo agotado!", 40, WIDTH / 2, HEIGHT / 2 + 60, YELLOW)
    
    draw_text(gameDisplay, "Presiona R para jugar de nuevo", 40, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    waiting = False

def show_start_screen():
    gameDisplay.blit(background, (0,0))
    draw_text(gameDisplay, "FRUIT NINJA!", 90, WIDTH / 2, HEIGHT / 4)
    draw_text(gameDisplay, "Tienes 30 segundos", 35, WIDTH / 2, HEIGHT / 2, WHITE)
    draw_text(gameDisplay, "¡Evita las bombas!", 35, WIDTH / 2, HEIGHT / 2 + 50, WHITE)
    draw_text(gameDisplay, "Presiona ESPACIO para comenzar", 40, WIDTH / 2, HEIGHT * 3 / 4)
    draw_controls()
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False

# -------------------------
# LOOP PRINCIPAL DEL JUEGO
# -------------------------
first_round = True
game_over = True
game_running = True

while game_running:
    if game_over:
        if first_round:
            show_start_screen()
            first_round = False
        else:
            show_gameover_screen()
        
        # Reiniciar variables
        game_over = False
        player_lives = 3
        score = 0
        start_time = time.time()
        time_remaining = GAME_TIME
        paused = False
        
        # Regenerar frutas
        for fruit in fruits:
            generate_random_fruits(fruit)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
                if paused:
                    pause_start = time.time()
            
            if event.key == pygame.K_r:
                game_over = True
                continue

    # Si está pausado, mostrar pantalla de pausa
    if paused:
        show_pause_screen()
        waiting_unpause = True
        while waiting_unpause and not game_over:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    waiting_unpause = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                        waiting_unpause = False
                        # Ajustar el tiempo para compensar la pausa
                        pause_duration = time.time() - pause_start
                        start_time += pause_duration
                    if event.key == pygame.K_r:
                        game_over = True
                        waiting_unpause = False
        continue

    # Calcular tiempo restante
    elapsed_time = time.time() - start_time
    time_remaining = max(0, GAME_TIME - int(elapsed_time))
    
    # Verificar si se acabó el tiempo
    if time_remaining <= 0:
        game_over = True
        continue

    gameDisplay.blit(background, (0, 0))
    
    # Dibujar Score
    score_text = font.render('Score: ' + str(score), True, WHITE)
    gameDisplay.blit(score_text, (10, 10))
    
    # Dibujar Timer
    timer_color = YELLOW if time_remaining > 10 else (255, 0, 0)
    timer_text = font.render('Time: ' + str(time_remaining), True, timer_color)
    gameDisplay.blit(timer_text, (WIDTH//2 - 80, 10))
    
    # Dibujar vidas
    draw_lives(gameDisplay, 690, 15, player_lives, 'images/red_lives.png')
    
    # Dibujar controles
    draw_controls()

    # Posición del dedo
    current_position = finger_pos
    pygame.draw.circle(gameDisplay, (0,255,0), current_position, 10)

    if preview_frame is not None:
        px = WIDTH - PREVIEW_W - 10
        py = HEIGHT - PREVIEW_H - 10
        pygame.draw.rect(gameDisplay, YELLOW, (px-2, py-2, PREVIEW_W+4, PREVIEW_H+4), 2)
        w = PREVIEW_W
        h = PREVIEW_H
        surf = pygame.image.frombuffer(preview_frame.tobytes(), (w, h), "RGB")
        gameDisplay.blit(surf, (px, py))

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                generate_random_fruits(key)

            if not value['hit'] and value['x'] < current_position[0] < value['x']+60 \
                                and value['y'] < current_position[1] < value['y']+60:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 2:
                        hide_cross_lives(690, 15)
                    elif player_lives == 1:
                        hide_cross_lives(725, 15)
                    elif player_lives == 0:
                        hide_cross_lives(760, 15)
                    
                    if player_lives <= 0:
                        game_over = True
                    half_fruit_path = "images/explosion.png"
                else:
                    half_fruit_path = "images/" + "half_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 5
                if key != 'bomb':
                    score += 1
                value['hit'] = True
        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()