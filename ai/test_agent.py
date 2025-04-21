import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from ai.minesweeper_env import MinesweeperEnv
from ai.q_learning_agent import QLearningAgent

# Parameters
WIDTH = 9
HEIGHT = 9
MINES = 10

# Initialize environment and agent
env = MinesweeperEnv(WIDTH, HEIGHT, MINES)
agent = QLearningAgent(
    WIDTH, HEIGHT, actions=["click", "flag"], epsilon=0
)  # Set epsilon to 0

# Load the trained Q-table
q_table_path = Path(__file__).resolve().parent / "q_table.pkl"
agent.load_q_table(q_table_path)

# Test the agent
state = env.reset()
done = False
total_reward = 0

while not done:
    action = agent.choose_action(state)
    state, reward, done = env.step(action)
    total_reward += reward

print(f"Game finished. Total Reward: {total_reward}")
