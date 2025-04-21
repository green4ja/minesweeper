import sys
import numpy as np
from pathlib import Path

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from minesweeper import Minesweeper


class MinesweeperEnv:
    def __init__(self, width, height, number_of_mines):
        self.game = Minesweeper(width, height, number_of_mines)
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        """Reset the game environment."""
        self.game.reset_game()
        return self.get_state()

    def get_state(self):
        """Return the current state of the game as a 2D array."""
        state = np.zeros((self.width, self.height), dtype=int)
        for x in range(self.width):
            for y in range(self.height):
                tile = self.game.grid[x][y]
                if tile.revealed:
                    state[x, y] = -1 if tile.is_mine else tile.neighbor_mines
                elif tile.flagged:
                    state[x, y] = -2
        return state

    def step(self, action):
        x, y, action_type = action
        if action_type == "click":
            self.game.handle_click(x, y)
        elif action_type == "flag":
            self.game.toggle_flag(x, y)

        # Calculate reward
        if self.game.game_state == "lost":
            reward = -10  # Penalize losing
            done = True
        elif self.game.game_state == "won":
            reward = 10  # Reward winning
            done = True
        else:
            tile = self.game.grid[x][y]
            if tile.revealed:
                if tile.is_mine:
                    reward = -5  # Penalize revealing a mine
                else:
                    reward = (
                        5 if tile.neighbor_mines == 0 else 2
                    )  # Reward revealing safe tiles
            elif tile.flagged:
                reward = (
                    1 if tile.is_mine else -1
                )  # Reward correct flags, penalize incorrect flags
            else:
                reward = -1  # Penalize redundant actions
            done = False

        return self.get_state(), reward, done
