import pygame
import sys
import random

# init pygame
pygame.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird | Abdul")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 30)

# bird
bird_x = 80
bird_y = 300
bird_radius = 15

gravity = 0.5
bird_velocity = 0
jump_force = -8

# pipes
pipe_width = 60
pipe_gap = 150
pipe_speed = 3
pipes = []

SPWANPIPE = pygame.USEREVENT
pygame.time.set_timer(SPWANPIPE, 1500) # pipe spawn every 1.5 seconds that helps bird to adjust to pass the next pipe

# game state
game_active = True
# score
score = 0

# fun to create pipes
def create_pipe():
    height = random.randint(150, 450)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height - pipe_gap // 2)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap // 2, pipe_width, HEIGHT - (height + pipe_gap // 2))

    return {"top": top_pipe, "bottom": bottom_pipe, "passed": False}

# fun to reset the game
def reset_game():
    global bird_y, bird_velocity, pipes, score, pipe_speed, game_active
    bird_y = 300
    bird_velocity = 0
    pipes = []
    score = 0
    pipe_speed = 3
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
                reset_game()

        if event.type == SPWANPIPE and game_active:
            pipes.append(create_pipe())

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

        # moving the pipes
        for pipe in pipes:
            pipe["top"].x -= pipe_speed
            pipe["bottom"].x -= pipe_speed

        pipes = [pipe for pipe in pipes if pipe["top"].right > 0]


        bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius *2)

        for pipe in pipes:
            # collision
            if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
                game_active = False

            # scoring
            if pipe["top"].right < bird_x and not pipe["passed"]:
                pipe["passed"]= True
                score += 1

                if score % 5 == 0:
                    pipe_speed += 0.5

    screen.fill((135, 206, 235)) # sky blue background color 

    # drawing pipe
    for pipe in pipes:
        pygame.draw.rect(screen, (0, 200, 0), pipe["top"])
        pygame.draw.rect(screen, (0, 200, 0), pipe["bottom"])

    # drawing bird
    pygame.draw.circle(screen, (255, 255, 0), (bird_x, int(bird_y)), bird_radius)

    # score display
    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))


    if not game_active:
        game_over_text = font.render("Game Over :)", True, (255, 0, 0))
        restart_text = score_font.render("Press R to Restart the Game", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 2 - 130, HEIGHT // 2 + 10))


    pygame.display.update()

pygame.quit()
sys.exit()