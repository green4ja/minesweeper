from minesweeper import minesweeper
import pygame

# TEST PARAMETERS
WIDTH = 9
HEIGHT = 9
MINES = 10
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x //= TILESIZE
            y //= TILESIZE
            game.handleClick(x, y)

    game.draw(screen, TILESIZE)
    pygame.display.flip()
    clock.tick(30)

