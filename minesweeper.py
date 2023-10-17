import pygame
import sys
import random

pygame.init()

# Constants for the game
GRID_SIZE = 16  # Grid size (16x16 for easy)
CELL_SIZE = 40  # Cell size (adjust as needed)
BOMB_COUNT = 40  # Total bomb count for easy difficulty

# Calculate screen dimensions based on grid and cell size
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to initialize the grid with bombs and numbers
def initialize_grid():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    bomb_positions = random.sample(range(GRID_SIZE * GRID_SIZE), BOMB_COUNT)
    for pos in bomb_positions:
        row = pos // GRID_SIZE
        col = pos % GRID_SIZE
        grid[row][col] = -1  # Marking bomb positions as -1

    return grid

# Function to draw the grid
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (192, 192, 192), cell_rect, 1)  # Draw grid lines

# Initialize the Minesweeper grid
grid = initialize_grid()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw the grid
    draw_grid()

    # Update the display
    pygame.display.update()

pygame.quit()






