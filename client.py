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

from config import *


class User:
    def __init__(self, login, address, port):
        self.__login = login
        self.__address = address
        self.__port = port
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.__sock.connect((self.__address, self.__port))

    def create_message(self, action, to=None, text=None):
        if action == PRESENCE:
            return {
                ACTION: PRESENCE,
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: self.__login
                }

            }
        elif action == MSG:
            return {
                ACTION: MSG,
                TIME: time.time(),
                TO: to,
                FROM: self.__login,
                MESSAGE: text
            }

    def send_to_server(self, message):
        if isinstance(message, dict):
            json_message = json.dumps(message)
            byte_message = json_message.encode('utf-8')
            self.__sock.send(byte_message)
        else:
            raise TypeError

    def get_message_from_server(self):
        byte_answer = self.__sock.recv(1024)
        if isinstance(byte_answer, bytes):
            json_answer = byte_answer.decode('utf-8')
            answer = json.loads(json_answer)
            if isinstance(answer, dict):
                return answer
            else:
                raise TypeError
        else:
            raise TypeError

    @staticmethod
    def check_answer(answer):
        if not isinstance(answer, dict):
            raise TypeError
        if 'response' not in answer:
            raise KeyError
        return answer

    def read_messages(self):
        """
        Client reads incoming messages in an infinite loop
        """
        while True:
            message = self.get_message_from_server()
            print(message)

    def write_messages(self):
        """
        The client writes a message in an infinite loop.
        """
        while True:
            text = input('Enter text: ')
            message = self.create_message(MSG, text=text)
            self.send_to_server(message)


if __name__ == '__main__':
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

    user = User(input('Enter a login: '), address, port)
    user.connect()
    message = user.create_message(PRESENCE)
    user.send_to_server(message)
    answer = user.get_message_from_server()
    checked_answer = user.check_answer(answer)

    if answer[RESPONSE] == OK:
        # depending on the mode we will listen or send messages
        if mode == 'r':
            user.read_messages()
        elif mode == 'w':
            user.write_messages()
        else:
            raise Exception('Wrong mode!')
