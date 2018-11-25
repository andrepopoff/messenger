import socket
import json

from pytest import raises
from client import create_message, send_to_server, get_message_from_server, check_answer


def test_create_message():
    message = create_message()
    assert message['action'] == 'presence'


class ClientSocket:
    """
    Class for socket operations
    """
    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        pass

    def recv(self, n):
        message = {'response': 200}
        json_message = json.dumps(message)
        byte_message = json_message.encode('utf-8')
        return byte_message

    def send(self, byte_message):
        pass


def test_send_to_server(monkeypatch):
    monkeypatch.setattr('socket.socket', ClientSocket)
    sock = socket.socket()

    assert send_to_server(sock, {'any_key': 'any_value'}) is None

    with raises(TypeError):
        send_to_server('not_a_dict')


def test_get_message_from_server(monkeypatch):
    monkeypatch.setattr('socket.socket', ClientSocket)  # replace the real socket with our class
    sock = socket.socket()
    assert get_message_from_server(sock) == {'response': 200}

