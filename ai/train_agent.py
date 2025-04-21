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

# Training loop
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

    print(f"Episode {episode + 1}/{EPISODES}: Total Reward = {total_reward}")

# Save the Q-table after training
q_table_path = Path(__file__).resolve().parent / "q_table.pkl"
with open(q_table_path, "wb") as f:
    pickle.dump(agent.q_table, f)
print(f"Training complete. Q-table saved to {q_table_path}.")
