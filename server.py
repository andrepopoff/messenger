"""
Server functions:
- accepts client's message
- forms the answer for the client
- sends a response to the client
- has command line options
- -p <port> - TCP-port for operation (by default, uses port 7777)
- -a <address> - IP address to listen (by default, listens to all available addresses)
"""

import socket
import sys
import json


def get_message(client_sock):
    """
    Receives a message from a client
    """
    byte_message = client_sock.recv(1024)

    if isinstance(byte_message, bytes):
        json_message = byte_message.decode('utf-8')
        message = json.loads(json_message)  # from json to dict
        if isinstance(message, dict):
            return message
        else:
            raise TypeError
    else:
        raise TypeError


def presence_response(presence):
    """
    Generates a response to the client
    """
    pass


def send_message(client, response):
    """
    Sends a response to the client
    """
    pass


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        address = sys.argv[1]
    except IndexError:
        address = ''

    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Port must be an integer!')
        sys.exit(0)

    sock.bind((address, port))
    sock.listen(5)

    while True:
        client, address = sock.accept()
        print('Получен запрос на соединение от', address)
        presence = get_message(client)
        response = presence_response(presence)
        send_message(client, response)
        client.close()