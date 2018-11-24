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
