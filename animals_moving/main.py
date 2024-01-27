import numpy as np
import pygame

pygame.init()

def clip(surface, x, y, x_size, y_size): #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pygame.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return

win = pygame.display.set_mode((500,480))
pygame.display.set_caption("First Game")
pygame.Surface((0, 0))
r = pygame.image.load('Hana Caraka Animals - Free/Chicken/Chicken right.png')
l = pygame.image.load('Hana Caraka Animals - Free/Chicken/Chicken left.png')
walkRight = [pygame.transform.scale_by(clip(r, 15*0, 0, 15, 11), 5), pygame.transform.scale_by(clip(r, 15*1, 0, 15, 11), 5), pygame.transform.scale_by(clip(r, 15*2, 0, 15, 11), 5), pygame.transform.scale_by(clip(r, 15*3, 0, 15, 11), 5) ,pygame.transform.scale_by(clip(r, 15*4, 0, 15, 11), 5) ,pygame.transform.scale_by(clip(r, 15*5, 0, 15, 11), 5)]
walkLeft = [pygame.transform.scale_by(clip(l, 15*0, 0, 15, 11), 5), pygame.transform.scale_by(clip(l, 15*1, 0, 15, 11), 5), pygame.transform.scale_by(clip(l, 15*2, 0, 15, 11), 5), pygame.transform.scale_by(clip(l, 15*3, 0, 15, 11), 5) ,pygame.transform.scale_by(clip(l, 15*4, 0, 15, 11), 5) ,pygame.transform.scale_by(clip(l, 15*5, 0, 15, 11), 5)]

bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

x = 50
y = 400
width = 40
height = 60
vel = 5

clock = pygame.time.Clock()

isJump = False
jumpCount = 10

left = False
right = False
walkCount = 0

def redrawGameWindow():
    global walkCount

    win.blit(bg, (0,0))
    if walkCount + 1 >= 27:
        walkCount = 0

    if left:
        win.blit(walkLeft[walkCount // 6], (x,y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount // 6], (x,y))
        walkCount += 1
    else:
        win.blit(char, (x, y))
        walkCount = 0

    pygame.display.update()



mov = [pygame.K_LEFT, pygame.K_LEFT, pygame.K_LEFT, 0, 0 ,0 , pygame.K_RIGHT, pygame.K_RIGHT, pygame.K_RIGHT]
s = 0

run = True



while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if s >= 9:
        s = 0

    if (mov[s % 9] == pygame.K_LEFT or keys[pygame.K_LEFT]) and x > vel:
        x -= vel
        left = True
        right = False

    elif (mov[s % 9] == pygame.K_RIGHT or keys[pygame.K_RIGHT]) and x < 500 - vel - width:
        x += vel
        left = False
        right = True

    else:
        left = False
        right = False
        walkCount = 0

    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
            left = False
            right = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else:
            jumpCount = 10
            isJump = False

    s += 1
    redrawGameWindow()


pygame.quit()
