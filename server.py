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
import select


def read_requests():
    pass


def write_responses():
    pass


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


def prepare_response(client_message):
    """
    Generates a response to the client
    """
    if 'action' in client_message and client_message['action'] == 'presence' \
            and 'time' in client_message and isinstance(client_message['time'], float):
        return {'response': 200}
    return {'response': 400, 'error': 'Invalid request'}


def send_message(client_sock, response):
    """
    Sends a response to the client
    """
    if isinstance(response, dict):
        json_message = json.dumps(response)
        byte_message = json_message.encode('utf-8')
        client_sock.send(byte_message)
    else:
        raise TypeError


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
    sock.settimeout(0.2)
    clients = []

    while True:
        try:
            client, address = sock.accept()
            print('Получен запрос на соединение от', address)
            message = get_message(client)
            response = prepare_response(message)
            send_message(client, response)
        except OSError:
            pass  # timeout
        else:
            print('Получен запрос на соединение от', address)
            clients.append(client)
        finally:
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], 0)
            except:
                pass  # Do nothing if a client disconnects

            read_requests()
            write_responses()
