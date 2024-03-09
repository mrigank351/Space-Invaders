import numpy as np
import random

MOVES = ['r', 'l', 's']

class Agent:
    def __init__(self, game = "", num_states=0, num_actions=0, alpha=0.5, gamma=0.9, epsilon=0.1):
        print("Agent file is running")
        self.game = game
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((num_states, num_actions))
    
    def get_state_hash(self, state):
        pass

    def choose_action(self, state=''):
        return random.choice(MOVES)
    
    def update_q_table(self, state, action, reward, next_state):
        pass

    def save_q_table(self, file_name):
        np.save(file_name, self.q_table)

    def load_q_table(self, file_name):
        self.q_table = np.load(file_name)
        
    def is_terminal_state(self, state):
        if 'player_alive' in state and not state['player_alive']:
            return True  # Player is dead, terminal state

        if 'game_over' in state and state['game_over']:
            return True  # Game over, terminal state

        return False  # Not a terminal state