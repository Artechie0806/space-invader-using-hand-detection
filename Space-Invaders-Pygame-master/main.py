import math
import random
import pygame
import cv2
import mediapipe as mp
from pygame import mixer
from pygame_gesture_kit import GestureRecognizer, Camera
import pygame_gesture_kit.hand_visualizer




mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

clock = pygame.time.Clock()
# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1200, 720))

# Background
background = pygame.image.load('Space-Invaders-Pygame-master/background.png')

# Sound
mixer.music.load("Space-Invaders-Pygame-master/background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('Space-Invaders-Pygame-master/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Space-Invaders-Pygame-master/player.png')
playerX = 550
playerY = 600
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
x=1
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Space-Invaders-Pygame-master/enemy.png'))
    enemyX.append(random.randint(0, 1136))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(20)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('Space-Invaders-Pygame-master/bullet.png')
bulletX = 0
bulletY = 600
bulletX_change = 0
bulletY_change = 60
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 70)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (400, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False


# Game Loop
cap = cv2.VideoCapture(0)
running = True
while running:
    
    
    
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -15
            if event.key == pygame.K_RIGHT:
                playerX_change = 15
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("Space-Invaders-Pygame-master\laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                
                
                
    success, image = cap.read()
    if success:
        # Convert image to RGB
        image = cv2.flip(image, 1)
        results = hands.process(image)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                    x = hand_landmarks.landmark[0].x
                    playerX = x*1200
                    if playerX <= 0:
                        playerX = 0
                    elif playerX >= 1136:
                        playerX = 1136
                    y1=hand_landmarks.landmark[12].y
                    y =hand_landmarks.landmark[9].y
                    if y1>y:
                        if bullet_state is "ready":
                            bulletSound = mixer.Sound("Space-Invaders-Pygame-master\laser.wav")
                            bulletSound.play()
                            # Get the current x cordinate of the spaceship
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                        else:
                            continue
    
    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 550:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = random.randint(10, 20)
            enemyY[i] += 30
        elif enemyX[i] >= 1136:
            enemyX_change[i] = -random.randint(10, 20)
            enemyY[i] += 30

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("Space-Invaders-Pygame-master/explosion.wav")
            explosionSound.play()
            bulletY = 600
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 1136)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 700
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
    clock.tick(60)
