import pygame
import sys

# init pygame
pygame.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird | Abdul")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
restart_font = pygame.font.SysFont(None, 30)

# bird
bird_x = 80
bird_y = 300
bird_radius = 15

gravity = 0.5
bird_velocity = 0
jump_force = -8

# game state
game_active = True

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

            if event.key == pygame.K_r and not game_active:
                bird_y = 300
                bird_velocity = 0
                game_active = True

    # game logic
    if game_active:
        bird_velocity += gravity
        bird_y += bird_velocity

        # ceiling collision
        if bird_y - bird_radius <=0:
            bird_y = bird_radius
            bird_velocity = 0

        # ground collision
        if bird_y + bird_radius >= HEIGHT:
            game_active = False

    screen.fill((135, 206, 235)) # sky blue background of window

    # bird design
    pygame.draw.circle(screen, (255, 255, 0), (bird_x, int(bird_y)), bird_radius)

    if not game_active:
        game_over_text = font.render("Game Over :)", True, (255, 0, 0))
        game_restart_text = restart_font.render("Press R to Restart the Game", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 30))
        screen.blit(game_restart_text, (WIDTH // 2 - 130, HEIGHT // 2 + 10))


    pygame.display.update()

pygame.quit()
sys.exit()