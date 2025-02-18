from pathlib import Path
import pygame
import random
from tile import Tile
import time

class Minesweeper:
    def __init__(self, width, height, number_of_mines):
        """
        Initialize the Minesweeper game.

        Args:
            width (int): The width of the game grid.
            height (int): The height of the game grid.
            number_of_mines (int): The number of mines to place on the grid.
        
        Returns:
            None
        """
        # Dimensions and mine count
        self.width = width
        self.height = height
        self.number_of_mines = number_of_mines

        # Game grid
        self.grid = [[Tile(x,y) for y in range(self.height)] for x in range(self.width)]
        self.mines_generated = False
        self.base_path = Path(__file__).resolve().parent

        # Load blank tile
        self.blank_tile = pygame.image.load(self.base_path / "assets" / "tiles" / "blank.png")
        self.blank_tile = pygame.transform.scale(self.blank_tile, (32, 32))  # Scale to 32x32

        # Load flag tile
        self.flag_tile = pygame.image.load(self.base_path / "assets" / "tiles" / "flag.png")
        self.flag_tile = pygame.transform.scale(self.flag_tile, (32, 32))  # Scale to 32x32

        # Load mine tile
        self.mine_tile = pygame.image.load(self.base_path / "assets" / "tiles" / "mine.png")
        self.mine_tile = pygame.transform.scale(self.mine_tile, (32, 32))  # Scale to 32x32

        # Load number tiles
        self.number_tiles = {}
        for i in range(1,9):
            image_path = self.base_path / "assets" / "tiles" / f"{i}.png"
            self.number_tiles[i] = pygame.image.load(image_path)
            self.number_tiles[i] = pygame.transform.scale(self.number_tiles[i], (32,32))

        # Load reset tiles
        self.start_tile = pygame.image.load(self.base_path / "assets" / "tiles" / "start.png")
        self.start_tile = pygame.transform.scale(self.start_tile, (64, 64))
        self.game_over_tile = pygame.image.load(self.base_path / "assets" / "tiles" / "game-over-reset.png")
        self.game_over_tile = pygame.transform.scale(self.game_over_tile, (64, 64))
        self.reset_tile = self.start_tile

        # Timer and bombs left
        self.start_time = None
        self.game_over_time = None
        self.flags_placed = 0

        # Load number tiles for timer and bomb counter
        self.timer_tiles = {}
        for i in range(10):
            image_path = self.base_path / "assets" / "tiles" / f"n{i}.png"
            self.timer_tiles[str(i)] = pygame.image.load(image_path)
            self.timer_tiles[str(i)] = pygame.transform.scale(self.timer_tiles[str(i)], (32, 64))

        # Load negative sign tile
        self.timer_tiles["-"] = pygame.image.load(self.base_path / "assets" / "tiles" / "nneg.png")
        self.timer_tiles["-"] = pygame.transform.scale(self.timer_tiles["-"], (32, 64))


    def generate_mines(self, safe_x, safe_y, safe_radius=2):
        """
        Generate mines on the game grid.

        Args:
            safe_x (int): The x-coordinate of the safe tile.
            safe_y (int): The y-coordinate of the safe tile.
            safe_radius (int): The radius around the safe tile where no mines will be placed.
        
        Returns:
            None
        """
        mines_placed = 0

        safe_zone = set()
        for dx in range(-safe_radius, safe_radius + 1):
            for dy in range(-safe_radius, safe_radius + 1):
                nx, ny = safe_x + dx, safe_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    safe_zone.add((nx,ny))

        while mines_placed < self.number_of_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) in safe_zone:
                continue

            if not self.grid[x][y].is_mine:
                self.grid[x][y].is_mine = True
                mines_placed += 1

        # After mines are placed, calculate neighbor counts
        self.calculate_neighbor_mines()

    def calculate_neighbor_mines(self):
        """
        Calculate the number of mines in neighboring tiles for each tile on the grid.

        Args:
            None

        Returns:
            None
        """
        for x in range(self.width):
            for y in range(self.height):
                current_tile = self.grid[x][y]

                if current_tile.is_mine:
                    continue

                neighbor_mines = 0

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[nx][ny].is_mine:
                            neighbor_mines += 1
                current_tile.neighbor_mines = neighbor_mines

    def draw_reset_button(self, screen, button_rect):
        """
        Draw the reset button on the screen.
        
        Args:
            screen (pygame.Surface): The screen to draw on.
            button_rect (pygame.Rect): The rectangle to draw the button inside.
            
        Returns:
            None
        """
        screen.blit(self.reset_tile, button_rect.topleft)

    def draw_number(self, screen, number, x, y):
        """
        Draw a number on the screen using images.
        
        Args:
            screen (pygame.Surface): The screen to draw on.
            number (int): The number to draw.
            x (int): The x-coordinate to draw the number.
            y (int): The y-coordinate to draw the number.
        
        Returns:
            None
        """
        formatted_number = str(max(-99, min(999, number)))  # Clamp number between -99 and 999
        
        # Ensure it's always 3 characters long
        if number < 0:
            formatted_number = "-" + formatted_number[1:].zfill(2)  # Example: -5 -> "-05"
        else:
            formatted_number = formatted_number.zfill(3)  # Example: 5 -> "005"

        # Draw each digit
        for i, char in enumerate(formatted_number):
            digit_image = self.timer_tiles[char]  # Get the image for the digit/negative sign
            screen.blit(digit_image, (x + i * 32, y))  # Offset for each digit

    
    def draw(self, screen, tile_size):
        """
        Draw the Minesweeper game on the screen.
        
        Args:
            screen (pygame.Surface): The screen to draw on.
            tile_size (int): The size of each tile.
            
        Returns:
            None
        """
        # Fill background area above grid
        screen.fill((189, 189, 189), pygame.Rect(0, 0, screen.get_width(), 80))
        
        # Draw reset button
        button_rect = pygame.Rect((screen.get_width() - 64) // 2, (80 - 64) // 2, 64, 64)
        self.draw_reset_button(screen, button_rect)

        # Determine elapsed time
        elapsed_time = self.game_over_time if self.game_over_time is not None else int(time.time() - self.start_time) if self.start_time else 0
        elapsed_time = min(elapsed_time, 999)  # Limit to 999 max

        # Draw timer using images
        self.draw_number(screen, elapsed_time, screen.get_width() - 120, 10)

        # Calculate bombs left
        bombs_left = self.number_of_mines - self.flags_placed

        # Draw bombs left using images
        self.draw_number(screen, bombs_left, 10, 10)

        # Draw the game grid
        for x in range(self.width):
            for y in range(self.height):
                tile = self.grid[x][y]
                tile_rect = pygame.Rect(x * tile_size, y * tile_size + 80, tile_size, tile_size)
                
                if tile.revealed:
                    if tile.is_mine:
                        screen.blit(self.mine_tile, tile_rect.topleft)
                    else:
                        pygame.draw.rect(screen, (189, 189, 189), tile_rect)
                        if tile.neighbor_mines > 0:
                            screen.blit(self.number_tiles[tile.neighbor_mines], tile_rect.topleft)
                        else:
                            pygame.draw.rect(screen, (123, 123, 123), tile_rect, 1)
                else:
                    if tile.flagged:
                        screen.blit(self.flag_tile, tile_rect.topleft)
                    else:
                        screen.blit(self.blank_tile, tile_rect.topleft)

    def handle_click(self, x, y):
        """
        Handle a click on the game grid.

        Args:
            x (int): The x-coordinate of the clicked tile.
            y (int): The y-coordinate of the clicked tile.
        
        Returns:
            None
        """
        # Handle first click on new board
        if not self.mines_generated:
            self.generate_mines(x, y, safe_radius=2)
            self.mines_generated = True
            self.start_time = time.time()
        
        tile = self.grid[x][y]
        if tile.revealed or tile.flagged:
            return
        
        tile.revealed = True
        if tile.is_mine:
            print("Game Over!")
            self.reset_tile = self.game_over_tile
            if self.start_time is not None:
                self.game_over_time = int(time.time() - self.start_time)
            self.start_time = None
        else:
            if self.check_win():
                print("You win!")
                self.reset_tile = self.start_tile
                if self.start_time is not None:
                    self.game_over_time = int(time.time() - self.start_time)
                self.start_time = None
            elif tile.neighbor_mines == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and not self.grid[nx][ny].revealed:
                            self.handle_click(nx, ny)

    def handle_reset_button_click(self, mouse_position):
        """
        Handle a click on the reset button.
        
        Args:
            mouse_position (tuple): The x, y coordinates of the mouse click.
        
        Returns:
            None
        """
        button_rect = pygame.Rect((self.width * 32 - 64) // 2, (80 - 64) // 2, 64, 64)
        if button_rect.collidepoint(mouse_position):
            self.reset_game()

    def toggle_flag(self, x, y):
        """
        Toggle the flag on a tile.

        Args:
            x (int): The x-coordinate of the tile.
            y (int): The y-coordinate of the tile.

        Returns:
            None
        """
        tile = self.grid[x][y]
        if not tile.revealed:
            tile.flagged = not tile.flagged
            self.flags_placed += 1 if tile.flagged else -1

    def reset_game(self):
        """
        Reset the game to its initial state.

        Args:
            None
        
        Returns:
            None
        """
        self.mines_generated = False
        self.reset_tile = self.start_tile
        self.grid = [[Tile(x, y) for y in range(self.height)] for x in range(self.width)]
        self.start_time = None
        self.game_over_time = None
        self.flags_placed = 0

    def check_win(self):
        """
        Check if the player has won the game.

        Args:
            None
        
        Returns:
            bool: True if the player has won, False otherwise.
        """
        for x in range(self.width):
            for y in range(self.height):
                tile = self.grid[x][y]
                if not tile.is_mine and not tile.revealed:
                    return False
        return True