from minesweeper import minesweeper
import pygame

"""
Beginner - > 9x9 + 10 mines
Intermediate -> 16x16 + 40 mines
Expert -> 30x16 + 99 mines
"""

# TEST PARAMETERS
WIDTH = 30
HEIGHT = 16
MINES = 99
TILESIZE = 32

pygame.init()
screen = pygame.display.set_mode((WIDTH*TILESIZE, HEIGHT*TILESIZE))
clock = pygame.time.Clock()

# Create a Minesweeper game
game = minesweeper(WIDTH, HEIGHT, MINES)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            grid_x, grid_y = x // TILESIZE, y // TILESIZE  # Convert to grid coordinates
            if 0 <= grid_x < game.width and 0 <= grid_y < game.height:
                if event.button == 1: # left click
                    game.handleClick(grid_x, grid_y)  # Call handleClick on release
                elif event.button == 3: # right click to flag
                    game.toggleFlag(grid_x, grid_y)
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE: # spacebar to flag
            x, y = pygame.mouse.get_pos()
            grid_x, grid_y = x // TILESIZE, y // TILESIZE
            if 0 <= grid_x < game.width and 0 <= grid_y < game.height:
                game.toggleFlag(grid_x, grid_y)

    game.draw(screen, TILESIZE)
    pygame.display.flip()
    clock.tick(30)

