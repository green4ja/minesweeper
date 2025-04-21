import numpy as np
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
        """
        Perform an action in the environment.

        Args:
            action (tuple): (x, y, action_type), where action_type is "click" or "flag".

        Returns:
            state (np.array): The new state of the game.
            reward (float): The reward for the action.
            done (bool): Whether the game is over.
        """
        x, y, action_type = action
        if action_type == "click":
            self.game.handle_click(x, y)
        elif action_type == "flag":
            self.game.toggle_flag(x, y)

        # Calculate reward
        if self.game.game_state == "lost":
            reward = -10
            done = True
        elif self.game.game_state == "won":
            reward = 10
            done = True
        else:
            reward = 1 if self.game.grid[x][y].revealed else 0
            done = False

        return self.get_state(), reward, done
