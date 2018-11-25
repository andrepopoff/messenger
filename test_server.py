import socket
from server import get_message, prepare_response, send_message


class ClientSocket():
    """
    Class for socket operations
    """
    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        pass

    def recv(self, l):
        pass

    def send(self, message):
        pass
    