import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((120, 20))
        self.surf.fill((128, 128, 0))
        self.rect = self.surf.get_rect()
        self.rect.bottom = SCREEN_HEIGHT
        self.rect.centerx = SCREEN_WIDTH/2
        self.velocity = 0
        self.score = 0

    def move(self, pressed_keys):
        if not pressed_keys[K_LEFT] or not pressed_keys[K_RIGHT]:
            self.velocity = 0
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-15, 0)
            self.velocity = -1
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(15, 0)
            self.velocity = 1
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((128, 128, 0))
        self.rect = self.surf.get_rect()
        self.rect.top = 0
        self.rect.centerx = SCREEN_WIDTH/2
        self.velocity = [max(2, random.random() * 10), max(5, random.random() * 10)]

    def move(self, player, score):
        if ball.rect.centery in range(player.rect.top, player.rect.bottom) and ball.rect.centerx in range(player.rect.left, player.rect.right):
            if player.velocity != 0:
                self.velocity[0] += player.velocity
            self.velocity[0] *= 1.5
            self.velocity[1] *= 1.5
            self.velocity[1] *= -1
            score += 1
        self.velocity[0] = max(-25, min(25, self.velocity[0]))
        self.velocity[1] = max(-25, min(25, self.velocity[1]))
        if ball.rect.centery >= SCREEN_HEIGHT:
            self.rect.center = (SCREEN_WIDTH/2, 0)
            self.velocity = [max(2, random.random() * 10) * (self.velocity[0] / abs(self.velocity[0])), max(5, random.random() * 10)]
            score -= 1
        if ball.rect.centery < 0:
            self.velocity[1] *= -1
        if ball.rect.centerx not in range(0, SCREEN_WIDTH):
            self.velocity[0] *= -1
        self.rect.move_ip(self.velocity)
        return score


class Score:
    def __init__(self, score):
        self.text = pygame.font.Font('freesansbold.ttf', 32)
        self.rendered = self.text.render('Score: ' + str(score), True, (128, 128, 0))
        self.rect = self.rendered.get_rect()
        self.rect.top = 0
        self.rect.left = 0

    def update(self, score):
        self.rendered = self.text.render('Score: ' + str(score), True, (128, 128, 0))
        self.rect = self.rendered.get_rect()
        self.rect.top = 0
        self.rect.left = 0


pygame.init()
random.seed()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player()
ball = Ball()
score = 0
score_text = Score(score)
clock = pygame.time.Clock()
running = True
paused = False
while running:
    clock.tick(60)
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                paused = True
                while paused:
                    for event in pygame.event.get():
                        # Did the user hit a key?
                        if event.type == KEYDOWN:
                            # Was it the Escape key? If so, stop the loop.
                            if event.key == K_ESCAPE:
                                paused = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

        # Fill the screen with green
    screen.fill((0, 128, 0))
    pressed_keys = pygame.key.get_pressed()
    player.move(pressed_keys)
    score = ball.move(player, score)
    score_text.update(score)
    screen.blit(score_text.rendered, score_text.rect)
    screen.blit(ball.surf, ball.rect)
    screen.blit(player.surf, player.rect)
    pygame.display.flip()
