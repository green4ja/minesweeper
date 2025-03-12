import numpy as np
import random
from collections import defaultdict

class QLearningAgent:
    def __init__(self, action_space, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995):
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = defaultdict(lambda: np.zeros(action_space.n))

    def choose_action(self, state):
        state_key = tuple(map(tuple, state))  # Convert state to a hashable type
        if random.uniform(0, 1) < self.exploration_rate:
            return self.action_space.sample()
        else:
            return np.argmax(self.q_table[state_key])

    def learn(self, state, action, reward, next_state):
        state_key = tuple(map(tuple, state))  # Convert state to a hashable type
        next_state_key = tuple(map(tuple, next_state))  # Convert next_state to a hashable type
        best_next_action = np.argmax(self.q_table[next_state_key])
        td_target = reward + self.discount_factor * self.q_table[next_state_key][best_next_action]
        td_error = td_target - self.q_table[state_key][action]
        self.q_table[state_key][action] += self.learning_rate * td_error
        self.exploration_rate *= self.exploration_decay