from pathlib import Path
import pygame
import random
from tile import tile
import time

class minesweeper:
    def __init__(self, width, height, numMines):
        # Dimensions and mine count
        self.width = width
        self.height = height
        self.numMines = numMines

        # Game grid
        self.grid = [[tile(x,y) for y in range(self.height)] for x in range(self.width)]
        self.minesGenerated = False
        self.basePath = Path(__file__).resolve().parent

        # Load blank tile
        self.blankTile = pygame.image.load(self.basePath / "assets" / "tiles" / "blank.png")
        self.blankTile = pygame.transform.scale(self.blankTile, (32, 32))  # Scale to 32x32

        # Load flag tile
        self.flagTile = pygame.image.load(self.basePath / "assets" / "tiles" / "flag.png")
        self.flagTile = pygame.transform.scale(self.flagTile, (32, 32))  # Scale to 32x32

        # Load mine tile
        self.mineTile = pygame.image.load(self.basePath / "assets" / "tiles" / "mine.png")
        self.mineTile = pygame.transform.scale(self.mineTile, (32, 32))  # Scale to 32x32

        # Load number tiles
        self.numberTiles = {}
        for i in range(1,9):
            imgPath = self.basePath / "assets" / "tiles" / f"{i}.png"
            self.numberTiles[i] = pygame.image.load(imgPath)
            self.numberTiles[i] = pygame.transform.scale(self.numberTiles[i], (32,32))

        # Load reset tiles
        self.startTile = pygame.image.load(self.basePath / "assets" / "tiles" / "start.png")
        self.startTile = pygame.transform.scale(self.startTile, (32, 32))
        self.gameOverTile = pygame.image.load(self.basePath / "assets" / "tiles" / "game-over-reset.png")
        self.gameOverTile = pygame.transform.scale(self.gameOverTile, (32, 32))
        self.resetTile = self.startTile

        # Timer and bombs left
        self.startTime = None
        self.flagsPlaced = 0

    def generateMines(self, safeX, safeY, safeRadius=2):
        minesPlaced = 0

        safeZone = set()
        for dx in range(-safeRadius, safeRadius + 1):
            for dy in range(-safeRadius, safeRadius + 1):
                nx, ny = safeX + dx, safeY + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    safeZone.add((nx,ny))

        while minesPlaced < self.numMines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) in safeZone:
                continue

            if not self.grid[x][y].isMine:
                self.grid[x][y].isMine = True
                minesPlaced += 1

        # After mines are placed, calculate neighbor counts
        self.calculateNeighborMines()

    def calculateNeighborMines(self):
        for x in range(self.width):
            for y in range(self.height):
                currentTile = self.grid[x][y]

                if currentTile.isMine:
                    continue

                neighborMines = 0

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[nx][ny].isMine:
                            neighborMines += 1
                currentTile.neighborMines = neighborMines

    def drawResetButton(self, screen, buttonRect):
        screen.blit(self.resetTile, buttonRect.topleft)
    
    def draw(self, screen, tileSize):
        # Fill background area above grid
        screen.fill((189, 189, 189), pygame.Rect(0, 0, screen.get_width(), 50))
        
        # Draw reset button
        buttonRect = pygame.Rect((screen.get_width() - 32) // 2, 10, 32, 32)
        self.drawResetButton(screen, buttonRect)

        # Draw the timer
        if self.startTime:
            elapsedTime = int(time.time() - self.startTime)
            font = pygame.font.SysFont(None, 36)
            timerText = font.render(f"Time: {elapsedTime}", True, (0, 0, 0))
            screen.blit(timerText, (screen.get_width() - 150, 10))
        else:
            font = pygame.font.SysFont(None, 36)
            timerText = font.render(f"Time: 0", True, (0, 0, 0))
            screen.blit(timerText, (screen.get_width() - 150, 10))

        # Draw the bombs left indicator
        bombsLeft = self.numMines - self.flagsPlaced
        font = pygame.font.SysFont(None, 36)
        bombsLeftText = font.render(f"Bombs: {bombsLeft}", True, (0, 0, 0))
        screen.blit(bombsLeftText, (10, 10))


        for x in range(self.width):
            for y in range(self.height):
                tile = self.grid[x][y]
                tileRect = pygame.Rect(x * tileSize, y * tileSize + 50, tileSize, tileSize)
                
                if tile.revealed:
                    if tile.isMine:
                        screen.blit(self.mineTile, tileRect.topleft)
                    else:
                        pygame.draw.rect(screen, (189, 189, 189), tileRect)
                        if tile.neighborMines > 0:
                            screen.blit(self.numberTiles[tile.neighborMines], tileRect.topleft)
                        else:
                            pygame.draw.rect(screen, (123, 123, 123), tileRect, 1)
                else:
                    if tile.flagged:
                        screen.blit(self.flagTile, tileRect.topleft)
                    else:
                        screen.blit(self.blankTile, tileRect.topleft)

    def handleClick(self, x, y):
        # Handle first click on new board
        if not self.minesGenerated:
            self.generateMines(x, y, safeRadius=2)
            self.minesGenerated = True
            self.startTime = time.time()
        
        tile = self.grid[x][y]
        if tile.revealed or tile.flagged:
            return
        
        tile.revealed = True
        if tile.isMine:
            print("Game Over!")
            self.resetTile = self.gameOverTile
            self.startTime = None
        elif tile.neighborMines == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and not self.grid[nx][ny].revealed:
                        self.handleClick(nx, ny)

    def handleResetButtonClick(self, mousePos):
        buttonRect = pygame.Rect((self.width * 32 - 32) // 2, 10, 32, 32)
        if buttonRect.collidepoint(mousePos):
            self.resetGame()

    def toggleFlag(self, x, y):
        tile = self.grid[x][y]
        if not tile.revealed:
            tile.flagged = not tile.flagged
            self.flagsPlaced += 1 if tile.flagged else -1

    def resetGame(self):
        self.minesGenerated = False
        self.resetTile = self.startTile
        self.grid = [[tile(x, y) for y in range(self.height)] for x in range(self.width)]
        self.startTime = None
        self.flagsPlaced = 0