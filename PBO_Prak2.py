import pygame
import sys

pygame.init()

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game PBO")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)

def changebackground(keys, color):
    if keys[pygame.K_r]:
        color = RED
    if keys[pygame.K_g]:
        color = GREEN
    if keys[pygame.K_b]:
        color = BLUE
    if keys[pygame.K_w]:
        color = WHITE
    if keys[pygame.K_c]:
        color = CYAN
    if keys[pygame.K_x]:
        color = BLACK
    return color


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 50
        self.height = 50

        self.speed = 2

        self.color = CYAN

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

    def batasan(self, keys):
        if self.x > 0:
            self.x -= self.speed
        if self.x < WIDTH - self.width:
            self.x += self.speed
        if self.y > 0:
            self.y -= self.speed
        if self.y < HEIGHT - self.height:
            self.y += self.speed

    def changecolor(self, keys):
        if keys[pygame.K_1]:
            self.color = RED
        if keys[pygame.K_2]:
            self.color = BLUE
        if keys[pygame.K_3]:
            self.color = GREEN
        if keys[pygame.K_4]:
            self.color = CYAN
        if keys[pygame.K_5]:
            self.color = WHITE
        if keys[pygame.K_6]:
            self.color = BLACK

    def increaseSize(self, keys):
        if keys[pygame.K_p]:
            self.width += 0.01
            self.height += 0.01

    def decreaseSize(self, keys):
        if keys[pygame.K_o]:
            self.width -= 0.01
            self.height -= 0.01

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                         [self.x, self.y, self.width, self.height])

player = Player(375, 275)
background = BLACK

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    player.move(keys)
    player.batasan(keys)
    player.changecolor(keys)
    player.increaseSize(keys)
    player.decreaseSize(keys)
    background = changebackground(keys, background)

    screen.fill(background)
    player.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()