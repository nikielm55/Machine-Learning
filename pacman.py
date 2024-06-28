import pygame
import sys
import random
from pygame.locals import *

# Initialize the game
pygame.init()

# Set up display
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 40
SCORE_HEIGHT = 40
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pacman')

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Set up fonts
font = pygame.font.SysFont(None, 36)

# Set up game clock
clock = pygame.time.Clock()
FPS = 30

# Set up Pacman
pacman_size = 20
pacman_radius = pacman_size // 2
pacman_speed = TILE_SIZE

# Set up dots
dot_radius = 5

# Initialize score
score = 0

# Define the maze grid
ROWS = (HEIGHT - SCORE_HEIGHT) // TILE_SIZE
COLS = WIDTH // TILE_SIZE


class Ghost:
    def __init__(self, x, y):
        self.image = pygame.Surface((pacman_size, pacman_size))
        self.image.fill((255, 0, 0))  # Red color for ghosts
        self.rect = self.image.get_rect()
        self.set_position(x, y)
        self.target = None
        self.move_delay = 500  # Delay in milliseconds (adjust as needed)
        self.last_move_time = pygame.time.get_ticks()

    def set_position(self, x, y):
        self.rect.topleft = (x * TILE_SIZE + TILE_SIZE // 2 - pacman_radius,
                             y * TILE_SIZE + SCORE_HEIGHT + TILE_SIZE // 2 - pacman_radius)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move_towards_pacman(self, maze, pacman_x, pacman_y):
        current_time = pygame.time.get_ticks()

        # Check if enough time has passed since the last move
        if current_time - self.last_move_time < self.move_delay:
            return

        self.last_move_time = current_time

        # Calculate ghost's current position in terms of grid
        col = self.rect.centerx // TILE_SIZE
        row = (self.rect.centery - SCORE_HEIGHT) // TILE_SIZE

        # Calculate direction towards Pacman
        if pacman_x < self.rect.centerx:
            dx, dy = -1, 0
        elif pacman_x > self.rect.centerx:
            dx, dy = 1, 0
        elif pacman_y < self.rect.centery:
            dx, dy = 0, -1
        elif pacman_y > self.rect.centery:
            dx, dy = 0, 1
        else:
            return  # Already at Pacman's position

        # Check if moving in the chosen direction is possible (not blocked by a wall)
        if not self.is_wall_in_direction(maze, dx, dy):
            self.rect.move_ip(dx * TILE_SIZE, dy * TILE_SIZE)
    def is_wall_in_direction(self, maze, dx, dy):
        next_col = (self.rect.centerx // TILE_SIZE) + dx
        next_row = ((self.rect.centery - SCORE_HEIGHT) // TILE_SIZE) + dy
        if next_row < 0 or next_row >= ROWS or next_col < 0 or next_col >= COLS:
            return True  # Out of bounds
        return maze[next_row][next_col] == 1


def create_maze():
    maze = [[0] * COLS for _ in range(ROWS)]

    # Initialize maze with random walls
    for row in range(ROWS):
        for col in range(COLS):
            if random.random() < 0.2:
                maze[row][col] = 1

    # Ensure Pacman's starting position is clear
    maze[ROWS // 2][COLS // 2] = 0

    # Use BFS to check connectivity from Pacman's starting position
    def bfs(start_row, start_col):
        visited = [[False] * COLS for _ in range(ROWS)]
        queue = [(start_row, start_col)]
        visited[start_row][start_col] = True

        while queue:
            r, c = queue.pop(0)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and not visited[nr][nc] and maze[nr][nc] == 0:
                    visited[nr][nc] = True
                    queue.append((nr, nc))

        # Check if all dots are reachable
        for row in range(ROWS):
            for col in range(COLS):
                if maze[row][col] == 0 and not visited[row][col]:
                    return False
        return True

    # Try generating until all dots are reachable
    while not bfs(ROWS // 2, COLS // 2):
        maze = [[0] * COLS for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                if random.random() < 0.2:
                    maze[row][col] = 1
        maze[ROWS // 2][COLS // 2] = 0

    # Clear the maze where ghosts are at
    if maze[1][1]:
        maze[1][1] = 0

    return maze

def draw_maze(maze):
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                pygame.draw.rect(WINDOW, BLUE, (col * TILE_SIZE, row * TILE_SIZE + SCORE_HEIGHT, TILE_SIZE, TILE_SIZE))

def draw_pacman(x, y):
    pygame.draw.circle(WINDOW, YELLOW, (x, y), pacman_radius)

def draw_dots(dots):
    for dot in dots:
        pygame.draw.circle(WINDOW, WHITE, dot, dot_radius)

def draw_score(score):
    score_surface = font.render(f'Score: {score}', True, WHITE)
    WINDOW.blit(score_surface, (10, 10))

def check_collision(pacman_x, pacman_y, dot_x, dot_y):
    distance = ((pacman_x - dot_x) ** 2 + (pacman_y - dot_y) ** 2) ** 0.5
    return distance < pacman_radius + dot_radius

def check_wall_collision(maze, x, y):
    col = x // TILE_SIZE
    row = (y - SCORE_HEIGHT) // TILE_SIZE
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return True
    return maze[row][col] == 1

def check_ghost_collision(pacman_x, pacman_y, ghosts):
    for ghost in ghosts:
        if ghost.rect.collidepoint(pacman_x, pacman_y):
            return True
    return False


def reset_game():
    global pacman_x, pacman_y, score, dots, maze, ghosts, dot_number
    score = 0
    row = ROWS // 2
    col = COLS // 2

    maze = create_maze()

    pacman_x, pacman_y = col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + SCORE_HEIGHT + TILE_SIZE // 2

    dots = [(x, y) for x in range(TILE_SIZE // 2, WIDTH, TILE_SIZE) for y in
            range(SCORE_HEIGHT + TILE_SIZE // 2, HEIGHT, TILE_SIZE) if
            maze[(y - SCORE_HEIGHT) // TILE_SIZE][x // TILE_SIZE] == 0]

    # Initialize ghosts in the middle of the maze cells
    ghosts = [Ghost(1, 1)]

    dot_number = len(dots)



def main():
    global pacman_x, pacman_y, score, dots, maze, ghosts, dot_number

    reset_game()
    moving_direction = None


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                    moving_direction = event.key

        if moving_direction == K_LEFT:
            new_x = pacman_x - TILE_SIZE
            if not check_wall_collision(maze, new_x - pacman_radius, pacman_y):
                pacman_x = new_x
        elif moving_direction == K_RIGHT:
            new_x = pacman_x + TILE_SIZE
            if not check_wall_collision(maze, new_x + pacman_radius, pacman_y):
                pacman_x = new_x
        elif moving_direction == K_UP:
            new_y = pacman_y - TILE_SIZE
            if not check_wall_collision(maze, pacman_x, new_y - pacman_radius):
                pacman_y = new_y
        elif moving_direction == K_DOWN:
            new_y = pacman_y + TILE_SIZE
            if not check_wall_collision(maze, pacman_x, new_y + pacman_radius):
                pacman_y = new_y

        # Reset the direction after moving
        moving_direction = None

        # Check for collisions with dots
        remaining_dots = []
        for dot in dots:
            if check_collision(pacman_x, pacman_y, dot[0], dot[1]):
                score += 1
            else:
                remaining_dots.append(dot)
        dots = remaining_dots

        # Check for collisions with ghosts
        if check_ghost_collision(pacman_x, pacman_y, ghosts):
            reset_game()

        if score == dot_number:
            reset_game()

        # Clear the screen
        WINDOW.fill(BLACK)

        # Draw everything
        draw_maze(maze)
        draw_pacman(pacman_x, pacman_y)
        draw_dots(dots)
        draw_score(score - 1)

        # Draw ghosts
        for ghost in ghosts:
            ghost.draw(WINDOW)
            ghost.move_towards_pacman(maze, pacman_x, pacman_y)

        # Update display
        pygame.display.update()

        # Cap the frame rate
        clock.tick(FPS)


if __name__ == "__main__":
    main()
