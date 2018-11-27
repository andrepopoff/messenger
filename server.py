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


def read_requests(clients_for_reading, all_clients):
    """
    Reading messages that clients send
    """
    messages = []
    for sock in clients_for_reading:
        try:
            message = get_message(sock)
            print(message)
            messages.append(message)
        except:
            print('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)

    return messages


def write_responses(messages, clients_for_writing, all_clients):
    """
    Sending messages to clients who are waiting for them
    """
    for sock in clients_for_writing:
        # We will send every message to everyone
        for message in messages:
            try:
                send_message(sock, message)
            except:
                print('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)


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


class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def bind(self, address, port):
        self.sock.bind((address, port))

    def listen_forever(self):
        self.sock.listen(10)
        self.sock.settimeout(0.2)


if __name__ == '__main__':
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

    server = Server()
    server.bind(address, port)
    server.listen_forever()

    #
    # while True:
    #     try:
    #         client, address = sock.accept()
    #         message = get_message(client)
    #         response = prepare_response(message)
    #         send_message(client, response)
    #     except OSError:
    #         pass  # timeout
    #     else:
    #         print('Сonnection request from', address)
    #         clients.append(client)
    #     finally:
    #         r = []
    #         w = []
    #         try:
    #             r, w, e = select.select(clients, clients, [], 0)
    #         except:
    #             pass  # Do nothing if a client disconnects
    #
    #         requests = read_requests(r, clients)
    #         write_responses(requests, w, clients)
