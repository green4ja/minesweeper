from pathlib import Path
import pygame
import random
from tile import Tile
import time

class minesweeper:
    def __init__(self, width, height, numMines):
        # Dimensions and mine count
        self.width = width
        self.height = height
        self.numMines = numMines

        # Game grid
        self.grid = [[Tile(x,y) for y in range(self.height)] for x in range(self.width)]
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
        self.startTile = pygame.transform.scale(self.startTile, (64, 64))
        self.gameOverTile = pygame.image.load(self.basePath / "assets" / "tiles" / "game-over-reset.png")
        self.gameOverTile = pygame.transform.scale(self.gameOverTile, (64, 64))
        self.resetTile = self.startTile

        # Timer and bombs left
        self.startTime = None
        self.gameOverTime = None
        self.flagsPlaced = 0

        # Load number tiles for timer and bomb counter
        self.timerTiles = {}
        for i in range(10):
            imgPath = self.basePath / "assets" / "tiles" / f"n{i}.png"
            self.timerTiles[str(i)] = pygame.image.load(imgPath)
            self.timerTiles[str(i)] = pygame.transform.scale(self.timerTiles[str(i)], (32, 64))

        # Load negative sign tile
        self.timerTiles["-"] = pygame.image.load(self.basePath / "assets" / "tiles" / "nneg.png")
        self.timerTiles["-"] = pygame.transform.scale(self.timerTiles["-"], (32, 64))


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

            if not self.grid[x][y].is_mine:
                self.grid[x][y].is_mine = True
                minesPlaced += 1

        # After mines are placed, calculate neighbor counts
        self.calculateNeighborMines()

    def calculateNeighborMines(self):
        for x in range(self.width):
            for y in range(self.height):
                currentTile = self.grid[x][y]

                if currentTile.is_mine:
                    continue

                neighbor_mines = 0

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[nx][ny].is_mine:
                            neighbor_mines += 1
                currentTile.neighbor_mines = neighbor_mines

    def drawResetButton(self, screen, buttonRect):
        screen.blit(self.resetTile, buttonRect.topleft)

    def drawNumber(self, screen, number, x, y):
        numStr = str(max(-99, min(999, number)))  # Clamp number between -99 and 999
        
        # Ensure it's always 3 characters long
        if number < 0:
            numStr = "-" + numStr[1:].zfill(2)  # Example: -5 -> "-05"
        else:
            numStr = numStr.zfill(3)  # Example: 5 -> "005"

        # Draw each digit
        for i, char in enumerate(numStr):
            digitImage = self.timerTiles[char]  # Get the image for the digit/negative sign
            screen.blit(digitImage, (x + i * 32, y))  # Offset for each digit

    
    def draw(self, screen, tileSize):
        # Fill background area above grid
        screen.fill((189, 189, 189), pygame.Rect(0, 0, screen.get_width(), 80))
        
        # Draw reset button
        buttonRect = pygame.Rect((screen.get_width() - 64) // 2, (80 - 64) // 2, 64, 64)
        self.drawResetButton(screen, buttonRect)

        # Determine elapsed time
        elapsedTime = self.gameOverTime if self.gameOverTime is not None else int(time.time() - self.startTime) if self.startTime else 0
        elapsedTime = min(elapsedTime, 999)  # Limit to 999 max

        # Draw timer using images
        self.drawNumber(screen, elapsedTime, screen.get_width() - 120, 10)

        # Calculate bombs left
        bombsLeft = self.numMines - self.flagsPlaced

        # Draw bombs left using images
        self.drawNumber(screen, bombsLeft, 10, 10)

        # Draw the game grid
        for x in range(self.width):
            for y in range(self.height):
                tile = self.grid[x][y]
                tileRect = pygame.Rect(x * tileSize, y * tileSize + 80, tileSize, tileSize)
                
                if tile.revealed:
                    if tile.is_mine:
                        screen.blit(self.mineTile, tileRect.topleft)
                    else:
                        pygame.draw.rect(screen, (189, 189, 189), tileRect)
                        if tile.neighbor_mines > 0:
                            screen.blit(self.numberTiles[tile.neighbor_mines], tileRect.topleft)
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
        if tile.is_mine:
            print("Game Over!")
            self.resetTile = self.gameOverTile
            if self.startTime is not None:
                self.gameOverTime = int(time.time() - self.startTime)
            self.startTime = None
        else:
            if self.checkWin():
                print("You win!")
                self.resetTile = self.startTile
                if self.startTime is not None:
                    self.gameOverTime = int(time.time() - self.startTime)
                self.startTime = None
            elif tile.neighbor_mines == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and not self.grid[nx][ny].revealed:
                            self.handleClick(nx, ny)

    def handleResetButtonClick(self, mousePos):
        buttonRect = pygame.Rect((self.width * 32 - 64) // 2, (80 - 64) // 2, 64, 64)
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
        self.grid = [[Tile(x, y) for y in range(self.height)] for x in range(self.width)]
        self.startTime = None
        self.gameOverTime = None
        self.flagsPlaced = 0

    def checkWin(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = self.grid[x][y]
                if not tile.is_mine and not tile.revealed:
                    return False
        return True