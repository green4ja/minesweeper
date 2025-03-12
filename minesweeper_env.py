import gym
from gym import spaces
import numpy as np
from minesweeper import Minesweeper

class MinesweeperEnv(gym.Env):
    def __init__(self, width, height, number_of_mines):
        super(MinesweeperEnv, self).__init__()
        self.minesweeper = Minesweeper(width, height, number_of_mines)
        self.action_space = spaces.Discrete(width * height)
        self.observation_space = spaces.Box(low=0, high=2, shape=(width, height), dtype=int)

    def reset(self):
        self.minesweeper = Minesweeper(self.minesweeper.width, self.minesweeper.height, self.minesweeper.number_of_mines)
        return self._get_observation()

    def step(self, action):
        x, y = divmod(action, self.minesweeper.width)
        self.minesweeper.handle_click(x, y)
        reward = self._get_reward()
        done = self.minesweeper.game_state != "active"
        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        grid = np.zeros((self.minesweeper.width, self.minesweeper.height), dtype=int)
        for x in range(self.minesweeper.width):
            for y in range(self.minesweeper.height):
                tile = self.minesweeper.grid[x][y]
                if tile.revealed:
                    grid[x, y] = 1 if tile.is_mine else 2
                elif tile.flagged:
                    grid[x, y] = -1
        return grid

    def _get_reward(self):
        if self.minesweeper.game_state == "won":
            return 1
        elif self.minesweeper.game_state == "lost":
            return -1
        else:
            return 0