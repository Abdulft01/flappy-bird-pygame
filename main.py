import pygame
import os
import sys
import random

HIGHSCORE_FILE = "highscore.txt"

def load_high_score():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, "r") as file:
        return int(file.read().strip() or 0)
    
def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as file:
        file.write(str(score))

high_score = load_high_score()

# added resource path as i want to convert in to .exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# init pygame
pygame.init()

pygame.mixer.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird | Abdul")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 30)

# loading the bird image from the assets folder
bird_img = pygame.image.load(resource_path("assets/bird.png")).convert_alpha()
bird_img = pygame.transform.scale(bird_img, (40, 30))

# loading the pipe image from the assets folder
pipe_img = pygame.image.load(resource_path("assets/pipe.png")).convert_alpha()

# loading the sound effects like jump, hit and background music of mp3 formats
jump_sound = pygame.mixer.Sound(resource_path("assets/jump.mp3"))
hit_sound = pygame.mixer.Sound(resource_path("assets/hit.mp3"))

pygame.mixer.music.load(resource_path("assets/bg_music.mp3"))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)


# game state
game_active = True
hit_played = False

# score
score = 0



# class bird
class Bird:
    def __init__(self, image):
        self.image = image
        self.x = 80
        self.y = 300
        self.velocity = 0
        self.gravity = 0.5
        self.jump_force = -8

    def jump(self):
        self.velocity = self.jump_force


    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        # ceiling collision
        if self.y <= 0:
            self.y = 0
            self.velocity = 0

    def get_rect(self):
        return self.image.get_rect(center = (self.x, self.y))
    
    def draw(self, screen):
        screen.blit(self.image, self.get_rect())

# class pipe

class Pipe:
    def __init__(self, image, x, gap):
        self.image = image
        self.width = 60
        self.gap = gap
        self.x = x
        self.passed = False

        height = random.randint(150, 450)

        self.top_rect = pygame.Rect(
            self.x,
            0,
            self.width,
            height - self.gap // 2
        )

        self.bottom_rect = pygame.Rect(
            self.x,
            height + self.gap // 2,
            self.width,
            HEIGHT - ( height + self.gap // 2)
        )

    def update(self, speed):
        self.top_rect.x -= speed
        self.bottom_rect.x -= speed

    def draw(self, screen):
        top_img = pygame.transform.scale(self.image, (self.top_rect.width, self.top_rect.height))
        top_img = pygame.transform.flip(top_img, False, True)
        screen.blit(top_img, self.top_rect)

        bottom_img = pygame.transform.scale(self.image, (self.bottom_rect.width, self.bottom_rect.height))
        screen.blit(bottom_img, self.bottom_rect)

    def collides_with(self, bird_rect):
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)
        
    def is_off_screen(self):
        return self.top_rect.right < 0


bird = Bird(bird_img) 
pipes = []

pipe_gap = 150
pipe_speed = 3

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)


# fun to reset the game
def reset_game():
    global pipes, score, pipe_speed, game_active, hit_played
    bird.y = 300
    bird.velocity = 0
    pipes = []
    score = 0
    pipe_speed = 3
    game_active = True
    hit_played = False
    pygame.mixer.music.play(-1)

# game loop
running = True
while running:
    clock.tick(60) # set to 60 frames per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird.jump()
                jump_sound.play()

            if event.key == pygame.K_r and not game_active:
                reset_game()

        if event.type == SPAWNPIPE and game_active:
            pipes.append(Pipe(pipe_img, WIDTH, pipe_gap))

    # game logic
    if game_active:
        bird.update()

        # ground collision
        if bird.y + bird.image.get_height() >= HEIGHT:
            game_active = False

        # moving the pipes
        for pipe in pipes:
            pipe.update(pipe_speed)

        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]


        bird_rect = bird.get_rect()

        for pipe in pipes:
            # collision
            if pipe.collides_with(bird_rect):
                game_active = False

            # scoring
            if pipe.top_rect.right < bird.x and not pipe.passed:
                pipe.passed= True
                score += 1

                if score % 5 == 0:
                    pipe_speed += 0.3

    # gamer over sound
    if not game_active and not hit_played:
        hit_sound.play()
        pygame.mixer.music.stop()

        # update high score
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        hit_played = True
    
    screen.fill((135, 206, 235)) # sky blue background color 

    # pipe image
    for pipe in pipes:
        pipe.draw(screen)

    # bird image
    bird.draw(screen)

    # score display
    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # highscore display
    high_score_text = score_font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(high_score_text, (10, 40))


    if not game_active:
        game_over_text = font.render("Game Over :)", True, (255, 0, 0))
        restart_text = score_font.render("Press R to Restart the Game", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 2 - 130, HEIGHT // 2 + 10))


    pygame.display.update()

pygame.quit()
sys.exit()