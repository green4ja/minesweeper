from minesweeper import minesweeper
import pygame

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

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            grid_x, grid_y = x // TILESIZE, y // TILESIZE  # Convert to grid coordinates
            if 0 <= grid_x < game.width and 0 <= grid_y < game.height:
                game.handleClick(grid_x, grid_y)  # Call handleClick on release

    game.draw(screen, TILESIZE)
    pygame.display.flip()
    clock.tick(30)

