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
import select

from serverhandlers import MessageHandler


class Server:
    def __init__(self, message_handler):
        self.message_handler = message_handler
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def bind(self, address, port):
        self.sock.bind((address, port))

    def listen_forever(self):
        self.sock.listen(10)
        self.sock.settimeout(0.2)

        while True:
            try:
                client, address = self.sock.accept()
                message = self.message_handler.get_message(client)
                response = self.message_handler.prepare_response(message)
                self.message_handler.send_message(client, response)
            except OSError:
                pass  # timeout
            else:
                print('Сonnection request from', address)
                self.clients.append(client)
            finally:
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], 0)
                except:
                    pass  # Do nothing if a client disconnects

                requests = self.message_handler.read_requests(r, self.clients)
                self.message_handler.write_responses(requests, w, self.clients)


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

    message_handler = MessageHandler()
    server = Server(message_handler)
    server.bind(address, port)
    server.listen_forever()
