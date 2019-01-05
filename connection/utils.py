""" Utils module """

import json
import numpy as np

DIM = 13                                                    # The size of our environment matrix

class Utils(object):
    """This class represents the methods wich are converting the JSON messages into"""

    def tiles_matrix_from_json(self, data):
        """ Returns the game state JSON response as a numpy matrix."""
        matrix = np.zeros((DIM, DIM)).astype("float32")
        j = json.loads(data)
        j = j['tiles']
        for line in j:
            if int(line) > 0:
                matrix[int(line)+5] = j[line]
            elif int(line) < 0:
                matrix[int(line)+6] = j[line]
            else:
                matrix[DIM-1] = j[line]
        return matrix

    def position_from_json(self, data):
        """ Returns the agents coordinates."""
        matrix = np.zeros((DIM, DIM)).astype("float32")
        j = json.loads(data)
        j = j['mario']
        return j['y'], j['x']   

    # Get the player's state
    # 0x00 - Leftmost of screen
    # 0x01 - Climbing vine
    # 0x02 - Entering reversed-L pipe
    # 0x03 - Going down a pipe
    # 0x04 - Autowalk
    # 0x05 - Autowalk
    # 0x06 - Player dies
    # 0x07 - Entering area
    # 0x08 - Normal
    # 0x09 - Cannot move
    # 0x0B - Dying
    # 0x0C - Palette cycling
    # @return True if stage was completed or the agent died, else False
    def player_state_from_json(self, data):
        """ Returns True if the game is finished or the player died, otherwise False. """
        j = json.loads(data)
        return j['state'] == 11 or j['state'] == 0 or j['state'] == 6 or j['state'] == 7 


    def find_first(self, array, value):
        """ Returns first apparence of value in array. """
        for k, val in enumerate(array):
            if val == value:
	            return k
        return -1

    def is_in_range(self, array, value):
        return np.isin(value, array)