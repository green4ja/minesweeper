from minesweeper import Minesweeper
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
base_path = Path(__file__).resolve().parent

# Load flag tile as program icon
icon = pygame.image.load(base_path / "assets" / "tiles" / "flag.png")
pygame.display.set_icon(icon)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH * TILESIZE, HEIGHT * TILESIZE + 80))

# Start clock
clock = pygame.time.Clock()

# Create a Minesweeper game
game = Minesweeper(WIDTH, HEIGHT, MINES)

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
            if y <= 80 and event.button == 1:
                game.handle_reset_button_click(event.pos)
            else:
                grid_x, grid_y = x // TILESIZE, (y - 80) // TILESIZE  # Convert to grid coordinates
                if 0 <= grid_x < game.width and 0 <= grid_y < game.height:
                    if event.button == 1:  # Left click (action)
                        game.handle_click(grid_x, grid_y)
                    elif event.button == 3: # Right click (flag)
                        game.toggle_flag(grid_x, grid_y)

        # User presses the spacebar
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Spacebar to flag
            x, y = pygame.mouse.get_pos()
            if y > 80:
                grid_x, grid_y = x // TILESIZE, (y - 80) // TILESIZE
                if 0 <= grid_x < game.width and 0 <= grid_y < game.height:
                    game.toggle_flag(grid_x, grid_y)

    # Draw the screen
    game.draw(screen, TILESIZE)
    pygame.display.flip()
    clock.tick(30) # 30 FPS

