import numpy as np

class Agent:
    def __init__(self, game, num_states, num_actions, alpha=0.5, gamma=0.9, epsilon=0.1):
        print("Agent file is running")
        self.game = game
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((num_states, num_actions))
    
    def get_state_hash(self, state):
    # Convert the state into a tuple of integers
        state_elements = []
        for key, value in state.items():
            if isinstance(value, tuple):
                state_elements.extend(value)
            elif isinstance(value, list):
                for item in value:
                    if not all(isinstance(i, int) for i in item):
                        raise ValueError(f"Non-integer values found in state element {item}")
                    state_elements.extend(item)
            else:
                if not isinstance(value, int):
                    raise ValueError(f"Non-integer value found: {value}")
                state_elements.append(value)
        
        # Hash the tuple
        state_tuple = tuple(state_elements)
        return hash(state_tuple) % self.q_table.shape[0]

    def choose_action(self, state):
        discretized_state = self.game.discretize_state(state)
        state_hash = self.get_state_hash(discretized_state)
        action = np.argmax(self.q_table[state_hash, :])

        return (
            np.random.choice(self.num_actions)
            if np.random.uniform(0, 1) < self.epsilon
            else action
        )
  
    def update_q_table(self, state, action, reward, next_state):
        discretized_state = self.game.discretize_state(state)
        discretized_next_state = self.game.discretize_state(next_state)

        state_hash = self.get_state_hash(discretized_state)
        next_state_hash = self.get_state_hash(discretized_next_state)

        old_value = self.q_table[state_hash, action]
        next_max = np.max(self.q_table[next_state_hash])
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)

        # Update the Q-table
        self.q_table[state_hash, action] = new_value

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