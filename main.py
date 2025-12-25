import pygame
import os
import sys
import random

# constants
WIDTH = 400
HEIGHT = 600
PIPE_GAP = 150
PIPE_SPEED_START = 3
HIGHSCORE_FILE = "highscore.txt"

# added resource path as i want to convert in to .exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# loading high score from a file

def load_high_score():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, "r") as file:
        return int(file.read().strip() or 0)
    
# saving high score to a file
    
def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as file:
        file.write(str(score))


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
    def __init__(self, image, x):
        self.image = image
        self.width = 60
        self.x = x
        self.passed = False

        height = random.randint(150, 450)

        self.top_rect = pygame.Rect(
            self.x,
            0,
            self.width,
            height - PIPE_GAP // 2
        )

        self.bottom_rect = pygame.Rect(
            self.x,
            height + PIPE_GAP // 2,
            self.width,
            HEIGHT - ( height + PIPE_GAP // 2)
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

# class game

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird | Abdul")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.score_font = pygame.font.SysFont(None, 30)

        # loading the bird image from the assets folder
        self.bird_img = pygame.transform.scale(
            pygame.image.load(resource_path("assets/bird.png")).convert_alpha(),
            (40, 30)
        )

        # loading the pipe image from the assets folder
        self.pipe_img = pygame.image.load(resource_path("assets/pipe.png")).convert_alpha()

        # loading the sound effects like jump, hit and background music of mp3 formats
        self.jump_sound = pygame.mixer.Sound(resource_path("assets/jump.mp3"))
        self.hit_sound = pygame.mixer.Sound(resource_path("assets/hit.mp3"))

        pygame.mixer.music.load(resource_path("assets/bg_music.mp3"))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        # states
        self.bird = Bird(self.bird_img)
        self.pipes = []
        self.pipe_speed = PIPE_SPEED_START
        self.score = 0
        self.high_score = load_high_score()
        self.game_active = True
        self.hit_played = False

        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1500)
        
    # fun to reset the game
    def reset_game(self):
        self.bird.y = 300
        self.bird.velocity = 0
        self.pipes.clear()
        self.pipe_speed = PIPE_SPEED_START
        self.score = 0
        self.game_active = True
        self.hit_played = False
        pygame.mixer.music.play(-1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird.jump()
                    self.jump_sound.play()

                if event.key == pygame.K_r and not self.game_active:
                    self.reset_game()

            if event.type == self.SPAWNPIPE and self.game_active:
                self.pipes.append(Pipe(self.pipe_img, WIDTH))


    def update(self):
        if not self.game_active:
            return
        
        self.bird.update()

        # ground collision
        if self.bird.y + self.bird.image.get_height() >= HEIGHT:
            self.game_active = False 

        # moving the pipes
        for pipe in self.pipes:
            pipe.update(self.pipe_speed)

        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]


        bird_rect = self.bird.get_rect()

        for pipe in self.pipes:
            # collision
            if pipe.collides_with(bird_rect):
                self.game_active = False

            # scoring
            if pipe.top_rect.right < self.bird.x and not pipe.passed:
                pipe.passed= True
                self.score += 1

                if self.score % 5 == 0:
                    self.pipe_speed += 0.3

    def draw(self):
        self.screen.fill((135, 206, 235)) # sky blue background color

        # pipe image
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # bird image
        self.bird.draw(self.screen)

        # score display
        self.score_text = self.score_font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(self.score_text, (10, 10))        

        # highscore display
        high_score_text = self.score_font.render(f"High Score: {self.high_score}", True, (0, 0, 0))
        self.screen.blit(high_score_text, (10, 40))

        # game over display
        if not self.game_active:
            game_over_text = self.font.render("Game Over :)", True, (255, 0, 0))
            restart_text = self.score_font.render("Press R to Restart the Game", True, (0, 0, 0))
            self.screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2 - 30))
            self.screen.blit(restart_text, (WIDTH // 2 - 130, HEIGHT // 2 + 10))

        pygame.display.update()

    def handle_game_over(self):
        # gamer over sound
        if not self.game_active and not self.hit_played:
            self.hit_sound.play()
            pygame.mixer.music.stop()

            # update high score
            if self.score > self.high_score:
                self.high_score = self.score
                save_high_score(self.high_score)

            self.hit_played = True

    def run(self):
        while True:
            self.clock.tick(60) # set to 60 frames per second
            self.handle_events()
            self.update()
            self.handle_game_over()
            self.draw()

if __name__ == "__main__":
    Game().run()