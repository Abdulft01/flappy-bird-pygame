import pygame
import sys

# init pygame
pygame.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird | Abdul")

clock = pygame.time.Clock()

# bird
bird_x = 80
bird_y = 300
bird_radius = 15

gravity = 0.5
bird_velocity = 0
jump_force = -8

# game loop
running = True
while running:
    clock.tick(60) # set to 60 frames per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_force

    # gravity effect
    bird_velocity += gravity
    bird_y += bird_velocity

    screen.fill((135, 206, 235)) # sky blue background of window

    # bird design
    pygame.draw.circle(screen, (255, 255, 0), (bird_x, int(bird_y)), bird_radius)


    pygame.display.update()

pygame.quit()
sys.exit()