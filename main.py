# *****************Hunter game developed by Rohit Bhetal*********************************************************


import pygame
import random
from pygame import mixer

# Initialize pygame
pygame.init()

# create the gme screen
screen = pygame.display.set_mode((800, 600))
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Background
bg = pygame.image.load("93Z_2109.w023.n001.1077B.p1.1077.jpg")
# icon and title
pygame.display.set_caption("Hunter X Hunter")

# Bg Music
mixer.music.load('bg_music.mp3')
mixer.music.play(-1)

# Player
playerimg = pygame.image.load('hunting.png')
playerx = 370
playery = 480
player_change = 0

# enemy
enemyx = []
enemyy = []
enemy_changeX = []
enemy_changeY = []
enemyimg = []
no_enemy = 6
for i in range(no_enemy):
    enemyimg.append(pygame.image.load('demon.png'))
    enemyx.append(random.randint(0, 734))
    enemyy.append(random.randint(10, 150))
    enemy_changeX.append(0.6)
    enemy_changeY.append(40)

# Bullet-Ready state(Bullet not visible)
# Bullet-Fire state(Bullet moving)

bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bullet_changeX = 0
bullet_changeY = 4
bullet_state = "ready"

# score displaying
score_value = 0
font = pygame.font.Font('Exo2-Regular.ttf', 32)

textX = 10
TextY = 10

#Game over text
over_text = pygame.font.Font('Exo2-Regular.ttf',64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 250, 240))
    screen.blit(score, (x, y))

def game_over_text():
    over = over_text.render("Game Over", True, (255, 250, 240))
    screen.blit(over, (230, 250))

def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = ((bullety - enemyy) ** 2 + (bulletx - enemyx) ** 2) ** 0.5
    if distance <= 27:
        return True
    else:
        return False


# player screen
def player(x, y):
    screen.blit(playerimg, (x, y))


# enemy screen
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


# bullet
def Fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 10, y))


# events in loop
running = True
while running:

    screen.fill((200, 255, 255))
    # Background
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If a keystroke has been pressed right key and left key
        if event.type == pygame.KEYDOWN:
            print("Keystroke has been pressed")
            if event.key == pygame.K_LEFT:
                player_change = -1.3
            if event.key == pygame.K_RIGHT:
                player_change = 1.3

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('gunshot.mp3')
                    bullet_sound.play()
                    bulletx = playerx
                    Fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0

    playerx += player_change

    if playerx <= 0:
        player_change = 0
    elif playerx >= 736:
        player_change = 0

    for i in range(no_enemy):
        #Game over
        if enemyy[i]>=480:
            for j in range(no_enemy):
                enemyy[j]=2000
                game_over_text()
        enemyx[i] += enemy_changeX[i]
        if enemyx[i] <= 0:
            enemy_changeX[i] = 0.6
            enemyy[i] += enemy_changeY[i]
        elif enemyx[i] >= 736:
            enemy_changeX[i] = -0.6
            enemyy[i] += enemy_changeY[i]

        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = 480
            bullet_state = 'ready'
            score_value += 1
            enemyx[i] = random.randint(0, 734)
            enemyy[i] = random.randint(10, 150)

        enemy(enemyx[i], enemyy[i], i)

    # Bullet change
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        Fire_bullet(bulletx, bullety)
        bullety -= bullet_changeY

    player(playerx, playery)

    show_score(textX, textX)

    pygame.display.update()
