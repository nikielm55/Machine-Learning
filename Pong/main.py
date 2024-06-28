import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Ball dimensions
BALL_SIZE = 20

# Paddle movement speed
PADDLE_SPEED = 5

# Ball movement speed
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Clock object to control the frame rate
clock = pygame.time.Clock()

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, y):
        self.rect.y += y

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

# Create paddle and ball objects
player1_paddle = Paddle(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
player2_paddle = Paddle(SCREEN_WIDTH - PADDLE_WIDTH - 10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Move player 1 paddle (W and S keys)
    if keys[pygame.K_w] and player1_paddle.rect.top > 0:
        player1_paddle.move(-PADDLE_SPEED)
    if keys[pygame.K_s] and player1_paddle.rect.bottom < SCREEN_HEIGHT:
        player1_paddle.move(PADDLE_SPEED)

    # Move player 2 paddle (UP and DOWN arrow keys)
    if keys[pygame.K_UP] and player2_paddle.rect.top > 0:
        player2_paddle.move(-PADDLE_SPEED)
    if keys[pygame.K_DOWN] and player2_paddle.rect.bottom < SCREEN_HEIGHT:
        player2_paddle.move(PADDLE_SPEED)

    # Move the ball
    ball.move()

    # Ball collision with top and bottom
    if ball.rect.top <= 0 or ball.rect.bottom >= SCREEN_HEIGHT:
        ball.speed_y *= -1

    # Ball collision with paddles
    if ball.rect.colliderect(player1_paddle.rect) or ball.rect.colliderect(player2_paddle.rect):
        ball.speed_x *= -1

    # Ball goes out of bounds (reset ball position)
    if ball.rect.left <= 0 or ball.rect.right >= SCREEN_WIDTH:
        ball.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        ball.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        ball.speed_x *= -1

    # Clear the screen
    screen.fill(BLACK)

    # Draw the paddles and ball
    player1_paddle.draw()
    player2_paddle.draw()
    ball.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
