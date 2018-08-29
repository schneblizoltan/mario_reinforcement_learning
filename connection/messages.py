""" Messages module """

class Message(object):
    """This class represents all message types, that the LUA server recognizes."""

    def __init__(self):
        self.message = ""

    def clear(self):
        """ Clears the message for reusage."""
        self.message = ""

    def press_up(self):
        """ Creates or appends a press 'up' message to the 'message' """
        if not self.message:
            self.message += '"key": {"value":"Up"}'
        else:
            self.message += ', "key": {"value":"Up"}'

    def press_down(self):
        """ Creates or appends a press 'down' message to the 'message' """
        if not self.message:
            self.message += '"key": {"value":"Down"}'
        else:
            self.message += ', "key": {"value":"Down"}'

    def press_left(self):
        """ Creates or appends a press 'left' message to the 'message' """
        if not self.message:
            self.message += '"key": {"value":"Left"}'
        else:
            self.message += ', "key": {"value":"Left"}'

    def press_right(self):
        """ Creates or appends a press 'right' message to the 'message' """
        if not self.message:
            self.message += '"key": {"value":"Right"}'
        else:
            self.message += ', "key": {"value":"Right"}'

    def press_a(self):
        """ Creates or appends a press 'A' message to the 'message' """
        if not self.message:
            self.message += '"key": {"value":"A"}'
        else:
            self.message += ', "key": {"value":"A"}'

    def press_b(self):
        """ Creates or appends a press 'B' message to the 'message' """
        if not self.message:
            self.message += '"key": {"value":"B"}'
        else:
            self.message += ', "key": {"value":"B"}'

    def press_start(self):
        """ Creates or appends a press 'START' message to the 'message' """
        if not self.message:
            self.message += '"key": {"value":"Start"}'
        else:
            self.message += ', "key": {"value":"Start"}'

    def get_game_tiles(self):
        """ Creates or appends a get 'Tile' message. (surrounding informations: enemy, block, ..)"""
        if not self.message:
            self.message += '"game": {"value":"Tiles"}'
        else:
            self.message += ', "game": {"value":"Tiles"}'

    def get_game_image(self):
        """ Creates or appends a get 'Image' message to the 'message' (game state as a jpeg file)"""
        if not self.message:
            self.message += '"game": {"value":"Image"}'
        else:
            self.message += ', "game": {"value":"Image"}'

    def get_game_info(self):
        """ Creates or appends a get 'Info' message. (the game state in matrix format) """
        if not self.message:
            self.message += '"game": {"value":"Info"}'
        else:
            self.message += ', "game": {"value":"Info"}'

    def reset_game(self):
        """ Creates or appends a 'Reset' message to 'messages'. """
        if not self.message:
            self.message += '"game": {"value":"Reset"}'
        else:
            self.message += ', "game": {"value":"Reset"}'

    def skip_frames(self, frame_count):
        """
        * Creates or appends a skip 'Frame' message.
        * How many frames should be skipped before first action.
        """
        if not self.message:
            self.message += '"config": {"frame":' + str(frame_count) + '}'
        else:
            self.message += ', "config": {"frame":' + str(frame_count) + '}'

    def set_image_quality(self, image_quality):
        """
        * Creates or appends a skip 'ImageQuality' message to 'messages'.
        * Sets the resolution of the returned picture.
        """
        if not self.message:
            self.message += '"config": {"image":' + str(image_quality) + '}'
        else:
            self.message += ', "config": {"image":' + str(image_quality) + '}'

    def set_divisor(self, divisor_count):
        """ Creates or appends a 'Divisor' message to 'messages'. """
        if not self.message:
            self.message += '"config": {"divisor":' + str(divisor_count) + '}'
        else:
            self.message += ', "config": {"divisor":' + str(divisor_count) + '}'

    def set_game_speed(self, speed_type):
        """
        * Creates or appends a set 'GameSpeed' message.
        * Emulation speed can be normal, maximum or turbo
        """
        if not self.message:
            self.message += '"config": {"speed":' + '"' + speed_type + '"' + '}'
        else:
            self.message += ', "config": {"speed":' + '"' + speed_type + '"' + '}'

    def endpoint_message(self, host, port):
        """ Creates or appends an 'Endpoint' message to 'messages'. """
        if not self.message:
            self.message += '"endpoint": {"host":'+str(host)+ ' ,"port":'+str(port)+'}'
        else:
            self.message += ', "endpoint": {"host":'+str(host)+ ' ,"port":'+str(port)+'}'

    def get_endpoint(self):
        """ Creates or appends a get 'Endpoint' message to 'messages'. """
        if not self.message:
            self.message += 'get'
        else:
            self.message += ', get'

    def finalize_message(self):
        """ Finalizes the JSON message with {} brackets """
        if self.message:
            self.message = "{ " + self.message + " }\n"
