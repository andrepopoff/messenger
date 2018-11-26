"""
Client functions:
- create a presence message
- send message to server
- receive answer from server
- read answer from server
- address - IP address from the server
- port - TCP-port on the server (by default, uses port 7777)

"""

import socket
import sys
import time
import json


def write_messages():
    pass


def read_messages():
    pass


def create_message():
    return {
        'action': 'presence',
        'time': time.time()
    }


def send_to_server(client_socket, message):
    if isinstance(message, dict):
        json_message = json.dumps(message)
        byte_message = json_message.encode('utf-8')
        client_socket.send(byte_message)
    else:
        raise TypeError


def get_message_from_server(client_socket):
    byte_answer = client_socket.recv(1024)
    if isinstance(byte_answer, bytes):
        json_answer = byte_answer.decode('utf-8')
        answer = json.loads(json_answer)
        if isinstance(answer, dict):
            return answer
        else:
            raise TypeError
    else:
        raise TypeError


def check_answer(answer):
    if not isinstance(answer, dict):
        raise TypeError
    if 'response' not in answer:
        raise KeyError
    return answer


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        address = sys.argv[1]
    except IndexError:
        address = 'localhost'

    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Port must be an integer!')
        sys.exit(0)

    try:
        mode = sys.argv[3]
    except IndexError:
        mode = 'r'

    sock.connect((address, port))
    message = create_message()
    send_to_server(sock, message)
    answer = get_message_from_server(sock)
    checked_answer = check_answer(answer)

    if answer['response'] == 200:
        # depending on the mode we will listen or send messages
        if mode == 'r':
            read_messages()
        elif mode == 'w':
            write_messages()
        else:
            raise Exception('Wrong mode!')
