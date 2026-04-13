import time

import pygame
import sys

pygame.init()

WIDTH = 600
HEIGHT = 400


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Kejar Maling")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Character:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 0.2
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                            [self.x, self.y, self.width, self.height])

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def batasan(self, keys):
        if self.x > 0:
            self.x -= self.speed
        if self.x < WIDTH - self.width:
            self.x += self.speed
        if self.y > 0:
            self.y -= self.speed
        if self.y < HEIGHT - self.height:
            self.y += self.speed

class Polisi(Character):
    def move (self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

class Maling(Character):
    def move (self, keys):
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

polisi = Polisi(100, 200, BLUE)
maling = Maling(400, 200, RED)

running = True
game_over = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        polisi.move(keys)
        maling.move(keys)
        polisi.batasan(keys)
        maling.batasan(keys)

    if polisi.get_rect().colliderect(maling.get_rect()):
        print("Polisi Menang!")
        game_over = True

    screen.fill(WHITE)

    if game_over:
        font = pygame.font.SysFont(None, 48)
        text = font.render("POLISI MENANG",
                               True, (0, 0, 0))
        screen.blit(text, (150, 100))

    polisi.draw(screen)
    maling.draw(screen)

    pygame.display.update()

pygame.quit()
sys.exit()