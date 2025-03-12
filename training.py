import gym
from minesweeper_env import MinesweeperEnv
from q_learning_agent import QLearningAgent

env = MinesweeperEnv(width=10, height=10, number_of_mines=10)
agent = QLearningAgent(env.action_space)

num_episodes = 1000
for episode in range(num_episodes):
    state = env.reset()
    done = False
    steps = 0
    while not done:
        action = agent.choose_action(state)
        next_state, reward, done, _ = env.step(action)
        agent.learn(state, action, reward, next_state)
        state = next_state
        steps += 1
        if steps > 1000:  # Prevent infinite loops
            print(f"Episode {episode + 1} exceeded 1000 steps, terminating early.")
            break
    print(f"Episode {episode + 1}/{num_episodes} finished with reward {reward}")

print("Training completed")