import pygame
import sys

pygame.init()

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Praktikum PBO - Pygame")

WHITE = (255, 255, 255)
MERAH = (255, 0, 0)
BIRU = (0, 0, 255)
HIJAU = (0, 255, 0)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BIRU)
    pygame.display.flip()

pygame.quit()
sys.exit()