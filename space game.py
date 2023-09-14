import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((1000, 600))
background = pygame.image.load('big-back.png')
mixer.music.load('Mario-theme-song.mp3')
mixer.music.play(-1)
play_game = True
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)
pygame.display.set_caption('Space War')
player_1 = pygame.image.load('spaceship.png')
playerX = 450
playerY = 500
move_side = 0
move_vertical = 0
bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bullet_side = 0
bullet_up = 0.5
bullet_state = "ready"
score = 0
image = pygame.font.Font('freesansbold.ttf', 32)
game_over_text = pygame.font.Font('freesansbold.ttf', 64)
scoreX = 10
scoreY = 10
enemy_1 = []
enemyX = []
enemyY = []
enemy_move1 = []
enemy_down = []
num_of_enemies = 5
for i in range(num_of_enemies):
    enemy_1.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 928))
    enemyY.append(random.randint(0, 100))
    enemy_move1.append(0.25)
    enemy_down.append(30)


def game_over():
    over_text = game_over_text.render('GAME OVER!!', True, (255, 255, 255))
    screen.blit(over_text, (350, 300))


def display_score(x, y):
    score_value = image.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))


def display_player(x, y):
    screen.blit(player_1, (x, y))


def display_enemy(x, y, i):
    screen.blit(enemy_1[i], (x, y))


def collided(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 36:
        return True
    else:
        return False


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 25))


while play_game:
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            play_game = False
        if action.type == pygame.KEYDOWN:
            if action.key == pygame.K_LEFT:
                move_side -= 0.4
            if action.key == pygame.K_RIGHT:
                move_side += 0.4
            if action.key == pygame.K_UP:
                move_vertical -= 0.4
            if action.key == pygame.K_DOWN:
                move_vertical += 0.4
            if action.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    bullet_sound = mixer.Sound('bullet-sound.wav')
                    bullet_sound.play()
                    fire_bullet(bulletX, bulletY)

        if action.type == pygame.KEYUP:
            if action.key == pygame.K_LEFT:
                move_side = 0
            if action.key == pygame.K_RIGHT:
                move_side = 0
            if action.key == pygame.K_UP:
                move_vertical = 0
            if action.key == pygame.K_DOWN:
                move_vertical = 0

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    playerX += move_side
    playerY += move_vertical

    if playerX <= 0:
        playerX = 0
    elif playerX >= 934:
        playerX = 934
    if playerY <= 300:
        playerY = 300
    elif playerY >= 528:
        playerY = 528

    for i in range(num_of_enemies):

        if enemyY[i] > 250:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                game_over()
                break

        enemyX[i] += enemy_move1[i]
        if enemyX[i] <= 0:
            enemy_move1[i] = 0.25
            enemyY[i] += enemy_down[i]
        elif enemyX[i] >= 934:
            enemy_move1[i] = -0.25
            enemyY[i] += enemy_down[i]
        collision = collided(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collide_sound = mixer.Sound('bomb-blast.wav')
            collide_sound.play()
            bulletY = 500
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 928)
            enemyY[i] = random.randint(0, 100)

        display_enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"
    if bullet_state in "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_up

    display_player(playerX, playerY)
    display_score(scoreX, scoreY)

    pygame.display.update()
