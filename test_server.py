import socket
import json
from server import get_message, prepare_response, send_message


class ClientSocket:
    """
    Class for socket operations
    """
    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        pass

    def recv(self, l):
        message = {'response': 200}
        json_message = json.dumps(message)
        byte_message = json_message.encode('utf-8')
        return byte_message

    def send(self, message):
        pass


def test_get_message(monkeypatch):
    # replace the real socket with our class
    monkeypatch.setattr('socket.socket', ClientSocket)
    sock = socket.socket()
    assert get_message(sock) == {'response': 200}

