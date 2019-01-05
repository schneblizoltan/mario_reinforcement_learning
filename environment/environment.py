""" Environment module """

from connection import client, messages, utils

import numpy as np

class Environment(object):
    """
    Creates connection between the game and the agent.
    """

    SOCKET = "localhost"
    PORT = 4561
    ACTION_NR = 5                                           # Number of action wich the agent knows about
    STATE_NR = 13                                           # Number of states defined

    def __init__(self):
        self.action_n = Environment.ACTION_NR
        self.state_n = Environment.STATE_NR
        self.reward_matrix = np.zeros((self.state_n, self.action_n)).astype("float32")
        self.reward_matrix = self.get_reward_matrix()
        self.request = messages.Message()
        self.client = client.Client()
        self.utils = utils.Utils()
        self.client.connect(Environment.SOCKET, Environment.PORT)

    def set_game_mode(self, mode="maximum"):
        self.request.set_game_speed(mode) 
        self.request.finalize_message()
        self.client.send(self.request.message)
        self.request.clear()

    def set_frame_divisor(self, number=30):
        self.request.set_divisor(number) 
        self.request.finalize_message()
        self.client.send(self.request.message)
        self.request.clear()

    def get_game_tiles(self):
        self.request.get_game_tiles()
        self.request.finalize_message()
        self.client.send(self.request.message)
        self.request.clear()
        return self.utils.tiles_matrix_from_json(self.client.receive())

    def get_distance(self):
        self.request.get_game_info()
        self.request.finalize_message()
        self.client.send(self.request.message)
        self.request.clear()
        return self.utils.position_from_json(self.client.receive())

    def reset(self):
        self.request.reset_game() 
        self.request.finalize_message()
        self.client.send(self.request.message)
        self.request.clear()
        return self.get_game_tiles()

    def step(self, action, obs):
        state = self.get_state(obs)
        reward = self.reward_matrix[state, action]
        # if action == 0:                                    # Down
        #     self.request.press_down()
        # elif action == 1:                                  # Up
        #     self.request.press_up()
        if action == 0:                                      # Left
            self.request.press_left()
        elif action == 1:                                    # Right
            self.request.press_right()
        elif action == 2:                                    # A
            self.request.press_a()
        # elif action == 5:                                  # B
        #     self.request.press_b()
        elif action == 3:                                    # A-Left
            self.step(0, obs)
            self.step(2, obs)
        elif action == 4:                                    # A-Right
            self.step(1, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(2, obs)
            self.step(1, obs)
            self.step(1, obs)
            self.step(1, obs)
        self.request.get_game_info()
        self.request.finalize_message()
        self.client.send(self.request.message)
        self.request.clear()
 
        response = self.client.receive()
        tiles = self.utils.tiles_matrix_from_json(response)
        state = self.utils.player_state_from_json(response)
        coordinates = self.utils.position_from_json(response)

        return tiles, reward, state, coordinates

    def get_reward_matrix(self):
        # Action order (OLD): Down, Up, Left, Right, A, B, A-Left, A-Right
        # Action order (CURRENT): Left, Right, A, A-Left, A-Right
        # A = Jump

        # State 0 - No enemy in front, no block above, no block in front
        self.reward_matrix[0,:] = [-1, 1, 0, -1, 0]

        # State 1 - Block above, no enemy in front, no enemy in back
        self.reward_matrix[1,:] = [-1, 0.9, 1, -1, 1]

        # State 2 - Enemy in front in 1? tile range, no tiles above / tiles above
        self.reward_matrix[2,:] = [-1, -1, +1, -1, 0.9]

        # State 3 - Small obstacle
        self.reward_matrix[3,:] = [-1, -1, -1, -1, 1]

        # State 4 - Large obstacle in front
        self.reward_matrix[4,:] = [0.9, -1, 0, -0.5, 1]

        # State 5 - Block above, enemy in front: range >= 2 tiles
        self.reward_matrix[5,:] = [-1, 0.9, 1, -1, 0.9]

        # State 6 - In air
        self.reward_matrix[6,:] = [0.1, 1, 0, -1, 0]

        # State 7 - No floor in front
        self.reward_matrix[7,:] = [-1, -1, -1, -1, 1]

        # State 8 - Stuck in front of pipe
        self.reward_matrix[8,:] = [1, -1, -1, -0.5, 1]

        # State 9 - Enemy behind 1 tile
        self.reward_matrix[9,:] = [-1, -1, 1, -1, -1]

        # State 10 - Stuck in front of pipe while in air
        self.reward_matrix[10,:] = [1, -1, -1, -0.8, -1]

        # State 11 - Stuck in front of mini pipe
        self.reward_matrix[11,:] = [-1, -1, -1, -1, 1]

        # State 12 - Enemy in front while in air
        self.reward_matrix[12,:] = [1, -1, -1, -1, -1]

        return self.reward_matrix

    def get_state(self, game_state):
        # 1 - block, coin, mushroom
        # 2 - enemy
        # 3 - mario
        
        mario_row = game_state[6,:]
        mario_pos = self.utils.find_first(mario_row, 3)

        if game_state[6, mario_pos+1] == 1 and game_state[7,mario_pos] == 0:
                return 10                                # Stuck in front of pipe; in air - State 9

        if game_state[6, mario_pos+1] == 1:
            if game_state[5, mario_pos+1] == 1:
                return 8                                 # Stuck in front of pipe - State 8
            return 11                                    # Stuck in front of mini pipe - State 11

        column = game_state[:,mario_pos+1]
        if game_state[7,mario_pos+1] == 0 and not(self.utils.is_in_range(column[mario_pos+1:], 1)):
        #if game_state[7, mario_pos+1] == 0 and game_state[7, mario_pos] == 1:
            return 7                                     # No floor in front - State 7

        if game_state[7,mario_pos] == 0:                 # In air - State 6
            if game_state[7,mario_pos+1] == 2:           # In air and enemy in front - State 12
                return 12
            return 6

        if game_state[4, mario_pos] == 1:
            if self.utils.is_in_range(game_state[6,mario_pos+5:], 2):
                return 5                                 # Tile above, enemy not in range - State 5
        
        if (game_state[6, mario_pos+2] == 1) and (game_state[6, mario_pos+3] == 1):
            if (game_state[5, mario_pos+2] == 1) and (game_state[5, mario_pos+3] == 1):
                return 4                                 # Large object in front - State 4
            return 3                                     # Small object in front - State 3

        if game_state[6, mario_pos+2] == 2:
            return 2                                     # Enemy in front - State 2

        if game_state[6, mario_pos-2] == 2:
            return 9                                     # Enemy behind - State 9

        if not self.utils.is_in_range(game_state[6,0:mario_pos], 2):       # No enemy before
            if not self.utils.is_in_range(game_state[6,mario_pos+1:], 2):  # No enemy after
                if game_state[4, mario_pos] == 1:                          # Tile above
                    return 1                             # Block above, no enmies - State 1 
       
        return 0                                         # Nothin in front, above, in back - State 0