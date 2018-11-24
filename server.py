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
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8888))
sock.listen(5)

while True:
    client, address = sock.accept()
    print('Получен запрос на соединение от', address)
    time_for_client = time.ctime(time.time()) + '\n'
    client.send(time_for_client.encode('utf-8'))
    client.close()
