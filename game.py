from minesweeper import Minesweeper
from pathlib import Path
import pygame
import sys
from ai.minesweeper_env import MinesweeperEnv
from ai.q_learning_agent import QLearningAgent

# Parameters
WIDTH = 9
HEIGHT = 9
MINES = 10
TILESIZE = 32

# Initialize pygame and set the application title
pygame.init()
pygame.display.set_caption("Minesweeper AI")

# Get script directory path
base_path = Path(__file__).resolve().parent

# Load flag tile as program icon
icon = pygame.image.load(base_path / "assets" / "tiles" / "flag.png")
pygame.display.set_icon(icon)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH * TILESIZE, HEIGHT * TILESIZE + 80))

# Start clock
clock = pygame.time.Clock()

# Create a Minesweeper game
game = Minesweeper(WIDTH, HEIGHT, MINES)

# Initialize the AI environment and agent
env = MinesweeperEnv(WIDTH, HEIGHT, MINES)
agent = QLearningAgent(WIDTH, HEIGHT, actions=["click", "flag"], epsilon=0)  # Set epsilon to 0 for testing

# Load the trained Q-table
q_table_path = base_path / "ai" / "q_table.pkl"
agent.load_q_table(q_table_path)

# Game loop
state = env.reset()
done = False

def draw_status(screen, status):
    font = pygame.font.SysFont(None, 36)
    text = font.render(status, True, (0, 0, 0))
    screen.blit(text, (10, 10))

while True:
    for event in pygame.event.get():
        # User clicks exit button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Reset the game when the user presses 'R'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            state = env.reset()
            done = False
            print("Game reset!")

    # If the game is not over, let the AI take an action
    if not done:
        action = agent.choose_action(state)
        q_value = agent.get_q_value(state, action)
        print(f"AI chose action: {action}, Q-value: {q_value}")
        state, reward, done = env.step(action)
        print(f"Reward: {reward}, Done: {done}")

        # Redraw the screen after each move
        game.draw(screen, TILESIZE)
        draw_status(screen, "Playing")
        pygame.display.flip()
        clock.tick(5)  # Limit to 5 FPS for better visualization

    # Draw the screen
    game.draw(screen, TILESIZE)
    status = "Playing" if not done else "Game Over!" if game.game_state == "lost" else "Game Won!"
    draw_status(screen, status)
    pygame.display.flip()
    clock.tick(5)