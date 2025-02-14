# made by github.com/domslk ( <- if the game is bad this doesn't apply)
import random
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720), flags=pygame.SCALED, vsync=1)
clock = pygame.time.Clock()
running = True
dt = 0


scorefile = open("score.txt", "r")


class Flappy:
    def __init__(self):
        self.velocity = 0
        self.y = 330
        self.pipes = []
        self.freeze = True
        self.freeze_first = False
        self.flappybird = pygame.draw.rect(screen, "yellow", pygame.Rect(100, self.y, 20, 20))
        self.score = 0
        self.high_score = int(scorefile.readline())
    def flap(self):
        self.velocity = -300
        pygame.draw.rect(screen, "yellow", pygame.Rect(100, self.y, 20, 20))
        self.flappybird = pygame.draw.rect(screen, "yellow", pygame.Rect(100, self.y, 20, 20))
    def ok(self):
        self.velocity += 1100 * dt
        self.y += dt * self.velocity
        if self.y >= 600:
            self.reset()
            self.freeze_first = True
        pygame.draw.rect(screen, "yellow", pygame.Rect(100, self.y, 20, 20))
        self.flappybird = pygame.draw.rect(screen, "yellow", pygame.Rect(100, self.y, 20, 20))
    def reset(self):
        if self.high_score == None or self.score > self.high_score:
            self.high_score = self.score
            with open("score.txt", "w") as f:
                print(self.high_score, file=f)
        self.y = 330
        self.velocity = 0
        self.pipes = []
        self.freeze = True
        self.score = 0

class Pipe:
    def __init__(self):
        self.x = 1300
        self.speed = 0.5
        self.ynorm = 260
        self.distance = random.randint(a=-200, b=150)
        self.scored = False
    def update(self):
        self.x -= 800 * self.speed * dt
        self.gap = 150
        self.rect_upper = pygame.draw.rect(screen, "0x07ad32", pygame.Rect(self.x, 0, 50, 300 + self.distance))
        self.rect_lower = pygame.draw.rect(screen, "0x07ad32", pygame.Rect(self.x, 450 + self.distance, 50, 450))
        pygame.draw.rect(screen, "0x07ad32", pygame.Rect(self.x, 0, 50, 300 + self.distance))
        pygame.draw.rect(screen, "0x07ad32", pygame.Rect(self.x, 450 + self.distance, 50, 450))


bird = Flappy()
pipe = Pipe()
pipe_timer = 0

font = pygame.font.Font('./font.ttf', 40)
text_play = font.render("Press space to play", True, "white")
text_score = font.render(f"{bird.score}", True, "white")
textrect = text_play.get_rect()
textscore = text_score.get_rect()
textrect.center = (600, 340)
textscore.center = (640, 50)

while running:
    dt = clock.tick() / 1000
    text_score = font.render(f"{bird.score}", True, "white")
    text_dead = font.render(f"GAME OVER! HIGH SCORE: {bird.high_score}", True, "white")
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.freeze = False
            bird.flap()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("0x3ecbfa")

    # RENDER YOUR GAME HERE
    if not bird.freeze:
        pipe_timer += 1
        if pipe_timer > 80:
            pipe_timer = 0
            bird.pipes.append(Pipe())

    if bird.freeze and not bird.freeze_first:
        pygame.draw.rect(screen, "yellow", pygame.Rect(100, 330, 20, 20))
        screen.blit(text_play, textrect)
    elif bird.freeze and bird.freeze_first:
        screen.blit(text_dead, textrect)

    for p in bird.pipes:
        if p.x < - 650:
            bird.pipes.remove(p)
        p.update()
        if p.rect_upper.colliderect(bird.flappybird) or p.rect_lower.colliderect(bird.flappybird):
            bird.reset()
            bird.freeze_first = True
        if not (p.rect_upper.colliderect(bird.flappybird) or p.rect_lower.colliderect(bird.flappybird)) and not p.scored and p.x < 100:
            bird.score += 1
            p.scored = True
            text_score = font.render(f"{bird.score}", True, "white")

    if not bird.freeze:
        bird.ok()
    screen.blit(text_score, textscore)
    # flip() the display to put your work on screen
    pygame.draw.rect(screen, "0x41e86d", pygame.Rect(0, 630, 1920, 100))
    pygame.display.flip()
    pygame.display.set_caption(f"flappybird, {int(clock.get_fps())}")


pygame.quit()