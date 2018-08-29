""" Client module """
import socket

class Client(object):
    """ This class allows us to connect to a given socket, to send and receive messages from it."""

    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print ("Socket creation failed with error: %s" %(err))

    def connect(self, host, port):
        """ Connects to the host on a given port. """
        self.socket.connect((host, port))

    def receive(self):
        """ Receives a 1024 kbyte message from the socket. """
        return self.socket.recv(1048576).decode("utf-8")

    def send(self, message):
        """ Sents the whole 'message' to the socket. """
        self.socket.sendall(message.encode())
