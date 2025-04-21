import numpy as np
import random
import pickle


class QLearningAgent:
    def __init__(self, width, height, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.width = width
        self.height = height
        self.actions = actions  # List of possible actions: e.g., ["click", "flag"]
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def get_q_value(self, state, action):
        """Get the Q-value for a given state-action pair."""
        return self.q_table.get((tuple(state.flatten()), action), 0.0)

    def choose_action(self, state):
        """Choose an action using an epsilon-greedy policy."""
        if random.random() < self.epsilon:
            # Explore: choose a random action
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            action_type = random.choice(self.actions)
            return (x, y, action_type)
        else:
            # Exploit: choose the best action
            q_values = [
                (self.get_q_value(state, (x, y, action_type)), (x, y, action_type))
                for x in range(self.width)
                for y in range(self.height)
                for action_type in self.actions
            ]
            return max(q_values, key=lambda x: x[0])[1]

    def update_q_value(self, state, action, reward, next_state):
        """Update the Q-value for a given state-action pair."""
        current_q = self.get_q_value(state, action)
        max_next_q = max(
            self.get_q_value(next_state, (x, y, action_type))
            for x in range(self.width)
            for y in range(self.height)
            for action_type in self.actions
        )
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[(tuple(state.flatten()), action)] = new_q

    def load_q_table(self, filepath):
        """Load a Q-table from a file."""
        with open(filepath, "rb") as f:
            self.q_table = pickle.load(f)
