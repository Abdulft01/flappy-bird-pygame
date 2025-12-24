import pygame
import sys

# init pygame
pygame.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird | Abdul")

clock = pygame.time.Clock()

# game loop
running = True
while running:
    clock.tick(60) # set to 60 frames per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((135, 206, 235)) # sky blue background of window

    pygame.display.update()

pygame.quit()
sys.exit()