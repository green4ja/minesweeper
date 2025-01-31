from minesweeper import minesweeper
from pathlib import Path
import pygame

"""
Beginner - > 9x9 + 10 mines
Intermediate -> 16x16 + 40 mines
Expert -> 30x16 + 99 mines
Grandmaster -> 40x22 + 182 mines
"""

# Parameters
WIDTH = 16
HEIGHT = 16
MINES = 40
TILESIZE = 32

# Initalize pygame and set the application title
pygame.init()
pygame.display.set_caption("Minesweeper")

# Get script directory path
basePath = Path(__file__).resolve().parent

# Load flag tile as program icon
icon = pygame.image.load(basePath / "assets" / "tiles" / "flag.png")
pygame.display.set_icon(icon)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH*TILESIZE, HEIGHT*TILESIZE))

# Start clock
clock = pygame.time.Clock()

# Create a Minesweeper game
game = minesweeper(WIDTH, HEIGHT, MINES)

# Game loop
while True:
    for event in pygame.event.get():
        # User clicks exit button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # User releases a mouse click
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            grid_x, grid_y = x // TILESIZE, y // TILESIZE  # Convert to grid coordinates
            if 0 <= grid_x < game.width and 0 <= grid_y < game.height:
                if event.button == 1:  # Left click (action)
                    game.handleClick(grid_x, grid_y)
                elif event.button == 3: # Right click (flag)
                    game.toggleFlag(grid_x, grid_y)

        # User presses the spacebar
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Spacebar to flag
            x, y = pygame.mouse.get_pos()
            grid_x, grid_y = x // TILESIZE, y // TILESIZE
            if 0 <= grid_x < game.width and 0 <= grid_y < game.height:
                game.toggleFlag(grid_x, grid_y)

    # Draw the screen
    game.draw(screen, TILESIZE)
    pygame.display.flip()
    clock.tick(30) # 30 FPS

