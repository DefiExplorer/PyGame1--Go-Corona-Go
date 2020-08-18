import pygame
import random as ran
import math
from pygame import mixer  # Library for sound effects.
from sys import exit

# Initialization
pygame.init()
# creating a screen/window
screen = pygame.display.set_mode((800, 600))  # Width X, Height Y

# Background Sound
mixer.music.load('bckgnd1.wav')
mixer.music.play(-1)  # Set On loop
# Title and Icon
pygame.display.set_caption("Go Corona Go")
icon = pygame.image.load('jet.png')
pygame.display.set_icon(icon)
# Player details
playerImage = pygame.image.load('bullet.png')
playerX = 400  # position on screen X coordinate
playerY = 450  # position on screen Y coordinate
# Below variable will be used for coordinate changes when keys are pressed

# Bullet to fire: -
# Ready (No firing or bullet not visible on screen)
# Fire (Bullet is moving and is visible)
BulletImage = pygame.image.load('inject.png')
bulletX = 0
bulletY = playerY
by_change = 10  # No need of changing the x direction of bullet.
bullet_state = "Ready"

# Enemy details
foeImage = []
foeX = []
foeY = []
# fx_change = []
# fy_change = []
num_of_enemies = 4
# List help create multiple Enemies
for i in range(0, num_of_enemies):
    foeImage.append(pygame.image.load('virus.png'))
    foeX.append(ran.randint(0, 780))  # random X coordinate, with starting value and end value.
    foeY.append(ran.randint(10, 350))  # random Y coordinate, with starting value and end value.
fx_change = 0.5
fy_change = 0.2
# Required variables
px_change = 0
py_change = 0
cng = 1
# Background
background = pygame.image.load('symbol.png').convert()
# Displaying_Score in terms of hit and miss.
hit = 0
font = pygame.font.Font('font#1.ttf', 30)
textX = 20
textY = 8


# Defining a Function
def player(x, y):
    screen.blit(playerImage, (x, y))  # this is like to draw player on the play screen using method blit()


def enemy(x, y, i):
    screen.blit(foeImage[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(BulletImage, (x + 16, y - 30))  # Just make sure bullet is at the center of the weapon.
    print(bullet_state)


def isCollision(foeX, bulletX, foeY, bulletY):  # Collision Detection using distance formula
    distance = math.sqrt(math.pow(foeX - bulletX, 2) + math.pow(foeY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score -> " + str(hit), True, (90, 40, 20))
    screen.blit(score, (x, y))


# Game loop
running = True
'''while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False
'''
# Since above wasn't working well, therefore
while running:
    screen.fill((200, 80, 24))  # RGB

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Keboard keystrokes for controlling the player
        # Keyup means button is released and Keydown means button is pressed.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                px_change -= cng
            elif event.key == pygame.K_RIGHT:
                px_change += cng
            elif event.key == pygame.K_UP:
                py_change -= cng
            elif event.key == pygame.K_DOWN:
                py_change += cng
            print(playerX, playerY)
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    bullet_sound = mixer.Sound('lazer.wav')
                    bullet_sound.play() # No need of (-1) as it is for loop only
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                px_change += cng
            elif event.key == pygame.K_RIGHT:
                px_change -= cng
            elif event.key == pygame.K_UP:
                py_change = 0
            elif event.key == pygame.K_DOWN:
                py_change = 0
    # pygame.display.update()  # Necessary to update any changes to display_screen
    # Need to update player in every frame, so...
    # Keep screen first always, then the other elements of the game which goes on top of it.
    playerX += px_change
    playerY += py_change
    # Boundary Condition/Screen Limit
    if playerX <= 0:
        playerX = 780
    elif playerX >= 780:
        playerX = 0
    elif playerY <= 10:
        playerY = 10
    elif playerY >= 540:
        playerY = 540
    player(playerX, playerY)

    # Enemy Boundary & movements.
    # Note fx_change and fy_change both are set to 2.5.
    for i in range(0, num_of_enemies):
        # foeX[i] += fx_change
        foeY[i] += fy_change
        if foeX[i] <= 10:
            foeX[i] = 10
            foeY[i] += fy_change
        elif foeX[i] >= 740:
            foeX[i] = 740
            foeY[i] += fy_change
        elif foeY[i] <= 10:
            foeY[i] = 10
        elif foeY[i] >= 560:
            foeY[i] = 10

        # Collision check
        collision = isCollision(foeX[i], bulletX, foeY[i], bulletY)
        if collision:
            explosion_sound = mixer.Sound('destroy.wav')
            explosion_sound.play()
            foeX[i] = ran.randint(0, 780)
            foeY[i] = ran.randint(10, 350)
            bulletY = playerY
            bullet_state = "Ready"
            hit += 10

        enemy(foeX[i], foeY[i], i)
    # Bullet Movement
    disp = math.sqrt(math.pow(playerX - bulletX, 2) + math.pow(playerY - bulletY, 2))
    # Above helps in someway to fix the shooting problem.
    if bulletY <= disp:# Required to F.I.X this Problem of Shooting.
        bulletY = playerY
        bullet_state = "Ready"
        # The above statement helps fire multiple bullet w.r.t the enemy.
    if bullet_state == "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= by_change

    '''
     # Collision check
    collision = isCollision(foeX, bulletX, foeY, bulletY)
    if collision:
        foeX = ran.randint(0, 1740)
        foeY = ran.randint(10, 660)
        bulletY = playerY
        bullet_state = "Ready"
        score += 10
        print(score)
    '''
    show_score(textX, textY)
    pygame.display.update()
pygame.quit()
quit()