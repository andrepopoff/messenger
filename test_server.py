"""
Use PyTest for testing
"""

import socket
import json
import time

from pytest import raises

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
    monkeypatch.setattr('socket.socket', ClientSocket)  # replace the real socket with our class
    sock = socket.socket()
    assert get_message(sock) == {'response': 200}


def test_prepare_response():
    # There is no action key
    assert prepare_response({'any_key': 'any_answer', 'time': time.time()}) == {'response': 400,
                                                                                'error': 'Invalid request'}
    # There is no time key
    assert prepare_response({'action': 'presence'}) == {'response': 400, 'error': 'Invalid request'}
    # Key - not 'presence'
    assert prepare_response({'action': 'any_action', 'time': time.time()}) == {'response': 400,
                                                                               'error': 'Invalid request'}
    # Wrong time key format
    assert prepare_response({'action': 'presence', 'time': 'string_time'}) == {'response': 400,
                                                                               'error': 'Invalid request'}
    # All is good
    assert prepare_response({'action': 'presence', 'time': time.time()}) == {'response': 200}


def test_send_message(monkeypatch):
    monkeypatch.setattr('socket.socket', ClientSocket)
    sock = socket.socket()

    assert send_message(sock, {'any_key': 'any_value'}) is None

    with raises(TypeError):
        send_message(sock, 'not_dict')
        