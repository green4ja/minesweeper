from ai.minesweeper_env import MinesweeperEnv
from ai.q_learning_agent import QLearningAgent

# Parameters
WIDTH = 9
HEIGHT = 9
MINES = 10

# Initialize environment and agent
env = MinesweeperEnv(WIDTH, HEIGHT, MINES)
agent = QLearningAgent(WIDTH, HEIGHT, actions=["click", "flag"])

# Load the trained Q-table
agent.load_q_table("q_table.pkl")

# Test the agent
state = env.reset()
done = False
total_reward = 0

while not done:
    action = agent.choose_action(state)
    state, reward, done = env.step(action)
    total_reward += reward

print(f"Game finished. Total Reward: {total_reward}")
