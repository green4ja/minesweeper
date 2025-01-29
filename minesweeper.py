from pathlib import Path
import pygame
import random
from tile import tile

"""
Beginner - > 9x9 + 10 mines
Intermediate -> 16x16 + 40 mines
Expert -> 30x16 + 99 mines
"""

class minesweeper:
    def __init__(self, width, height, numMines):
        self.width = width
        self.height = height
        self.numMines = numMines
        self.grid = [[tile(x,y) for y in range(self.height)] for x in range(self.width)]
        self.generateMines()
        self.calculateNeighborMines()
        self.basePath = Path(__file__).resolve().parent

        # Load blank tile
        self.blankTile = pygame.image.load(self.basePath / "assets" / "tiles" / "blank.png")
        self.blankTile = pygame.transform.scale(self.blankTile, (32, 32))  # Scale to 32x32

    def generateMines(self):
        minesPlaced = 0

        while minesPlaced < self.numMines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if self.grid[x][y].isMine == False:
                self.grid[x][y].isMine = True
                minesPlaced += 1

    def calculateNeighborMines(self):
        for x in range(self.width):
            for y in range(self.height):
                currentTile = self.grid[x][y]

                if currentTile.isMine == True:
                    continue

                neighborMines = 0

                for dx in [-1,0,1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[nx][ny].isMine:
                            neighborMines += 1
                currentTile.neighborMines = neighborMines
    
    def draw(self, screen, tileSize):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.grid[x][y]
                tileRect = pygame.Rect(x * tileSize, y * tileSize, tileSize, tileSize)
                
                if tile.revealed:
                    if tile.isMine:
                        pygame.draw.rect(screen, (255, 0, 0), tileRect)
                    else:
                        pygame.draw.rect(screen, (200, 200, 200), tileRect)
                        if tile.neighborMines > 0:
                            font = pygame.font.SysFont("Arial", 16)
                            text = font.render(str(tile.neighborMines), True, (0, 0, 0))
                            screen.blit(text, tileRect.move(10, 10))
                else:
                    screen.blit(self.blankTile, (x * tileSize, y * tileSize))
                
                pygame.draw.rect(screen, (123, 123, 123), tileRect, 2)

    def handleClick(self, x, y):
        tile = self.grid[x][y]
        if tile.revealed or tile.flagged:
            return
        
        tile.revealed = True
        if tile.isMine:
            print("Game Over!")
        elif tile.neighborMines == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and not self.grid[nx][ny].revealed:
                        self.handleClick(nx, ny)