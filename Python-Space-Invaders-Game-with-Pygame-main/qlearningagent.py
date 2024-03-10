import pickle
import numpy as np

class QLearningAgent:
    def __init__(self, actions):
        self.actions = actions
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_table = {}

    def get_state(self, game):
        # Define state representation for firing control
        spaceship_pos = game.spaceship_group.sprite.rect.center
        spaceship_laser_ready = game.spaceship_group.sprite.laser_ready
        closest_alien_distance = None
        closest_alien_type = None

        for alien in game.aliens_group.sprites():
            alien_distance = np.linalg.norm(np.array(spaceship_pos) - np.array(alien.rect.center))
            if closest_alien_distance is None or alien_distance < closest_alien_distance:
                closest_alien_distance = alien_distance
                closest_alien_type = alien.type

        state = (spaceship_pos, spaceship_laser_ready, closest_alien_distance, closest_alien_type)
        return str(state)


    def get_action(self, state):
        if state not in self.q_table:
            # Initialize Q-values for the new state
            self.q_table[state] = [0 for _ in range(len(self.actions))]
        
        if np.random.rand() < self.epsilon:
            # Exploration: select a random action
            action = np.random.choice(len(self.actions))
        else:
            # Exploitation: select the action with max Q-value
            state_action = self.q_table[state]
            action = self.arg_max(state_action)
        return action

    def learn(self, state, action, reward, next_state):
        if next_state not in self.q_table:
        # Initialize Q-values for the new state
            self.q_table[next_state] = [0 for _ in range(len(self.actions))]

        current_q = self.q_table[state][action]
        new_q = reward + self.discount_factor * max(self.q_table[next_state])
        self.q_table[state][action] += self.learning_rate * (new_q - current_q)
    

    @staticmethod
    def arg_max(state_action):
        max_index_list = []
        max_value = state_action[0]
        for index, value in enumerate(state_action):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return np.random.choice(max_index_list)

    def save_q_table(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, file_name):
        with open(file_name, 'rb') as f:
            self.q_table = pickle.load(f)
