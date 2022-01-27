import pygame
import random
import math
from pygame import mixer

pygame.init()

width = 800
height = 600
background_color = (255, 255, 255)

white = (255, 255, 255)
dead = False

running = True
enemyimage = None

screen = pygame.display.set_mode((width, height))

background = pygame.image.load('assets/images/background.PNG')

mixer.music.load('assets/sounds/background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Viktors's game")
icon = pygame.image.load('assets/images/Icon.png')
pygame.display.set_icon(icon)

playerIMG = pygame.image.load('assets/images/Player.png')

playerX = width / 2 - 32
playerY = height / 2 + 175
movement_change = 0
randomNum = random.randint(0, 3)

enemyIMG = []
number_of_enemies = 6
enemy_X = []
enemy_Y = []
enemy_movement_change = []
y_change_of_enemy = []

for i in range(number_of_enemies):
    enemy_X.append(random.randint(0, width - 64))
    enemy_Y.append(random.randint(0, 250))
    enemy_movement_change.append(2)
    y_change_of_enemy.append(30)
    enemyIMG.append(pygame.image.load('assets/images/alien.png'))
    enemyIMG.append(pygame.image.load('assets/images/alien0.png'))
    enemyIMG.append(pygame.image.load('assets/images/alien1.png'))
    enemyIMG.append(pygame.image.load('assets/images/alien2.png'))

bulletIMG = pygame.image.load('assets/images/bullet.png')
bullet_X = 0
bullet_Y = height / 2 + 175
bullet_Y_change = 8.5
bullet_X_change = 0
bullet_state = 'ready'


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score():
    score = font.render("Score: " + str(score_value), True, white)
    screen.blit(score, (textX, textY))


def game_over_text():
    game_over_text = game_over_font.render("GAME OVER!", True, white)
    play_again = game_over_font.render(f"Your score was: {score_value}", True, white)
    screen.blit(game_over_text, (200, 250))
    screen.blit(play_again, (125, 300))


def player():
    screen.blit(playerIMG, (playerX, playerY))


def enemy(i):
    if 0 <= randomNum < 1:
        image = enemyIMG[0]
    elif 1 <= randomNum < 2:
        image = enemyIMG[1]
    elif 2 <= randomNum < 3:
        image = enemyIMG[2]
    elif 3 <= randomNum < 4:
        image = enemyIMG[3]
    screen.blit(image, (enemy_X[i], enemy_Y[i]))


def fire_bullet():
    global bullet_state
    bullet_state = 'Fire'
    screen.blit(bulletIMG, (bullet_X + 16, bullet_Y + 10))


def isCollision(i):
    distance = math.sqrt((math.pow(enemy_X[i] - bullet_X, 2)) + (math.pow(enemy_Y[i] - bullet_Y, 2)))
    if distance < 32:
        return True
    else:
        return False


clock = pygame.time.Clock()

while running:
    clock.tick(100)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                movement_change = -3

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('assets/sounds/laser.wav')
                    bullet_sound.play()
                    bullet_X = playerX
                    fire_bullet()

            if event.key == pygame.K_LEFT:
                movement_change = -3

            if event.key == pygame.K_d:
                movement_change = 3

            if event.key == pygame.K_RIGHT:
                movement_change = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                movement_change = 0

    screen.fill(background_color)
    screen.blit(background, (0, 0))

    playerX += movement_change

    if playerX < 0:
        playerX = 0
    elif playerX > 735:
        playerX = 735

    for i in range(number_of_enemies):

        if enemy_Y[i] > 430:
            for j in range(number_of_enemies):
                enemy_Y[j] = 2000
            game_over_text()
            dead = True
            break

        enemy_X[i] += enemy_movement_change[i]
        if enemy_X[i] < 0:
            enemy_movement_change[i] = 2
            enemy_Y[i] += y_change_of_enemy[i]
        elif enemy_X[i] > 735:
            enemy_movement_change[i] = -2
            enemy_Y[i] += y_change_of_enemy[i]

        collision = isCollision(i)
        if collision:
            explosion = mixer.Sound('assets/sounds/explosion.wav')
            explosion.play()
            bullet_Y = 480
            bullet_state = 'ready'
            score_value += 1
            enemy_X[i] = random.randint(0, width - 64)
            enemy_Y[i] = 0

        enemy(i)

    if bullet_Y < -32:
        bullet_Y = 480
        bullet_state = 'ready'

    if bullet_state == 'Fire':
        fire_bullet()
        bullet_Y -= bullet_Y_change

    player()
    show_score()
    pygame.display.update()
