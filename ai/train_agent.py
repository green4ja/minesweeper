import sys
import pickle
from pathlib import Path

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from ai.minesweeper_env import MinesweeperEnv
from ai.q_learning_agent import QLearningAgent

# Parameters
WIDTH = 9
HEIGHT = 9
MINES = 10
EPISODES = 1000

# Initialize environment and agent
env = MinesweeperEnv(WIDTH, HEIGHT, MINES)
agent = QLearningAgent(WIDTH, HEIGHT, actions=["click", "flag"])

win_count = 0

for episode in range(EPISODES):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        agent.update_q_value(state, action, reward, next_state)
        state = next_state
        total_reward += reward

    if env.game.game_state == "won":
        win_count += 1

    if (episode + 1) % 100 == 0:  # Log every 100 episodes
        print(
            f"Episode {episode + 1}/{EPISODES}: Total Reward = {total_reward}, Win Rate = {win_count / 100:.2%}"
        )
        win_count = 0
