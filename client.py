import socket
import sys
import time
import json


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

    sock.connect((address, port))
    message = create_message()
    send_to_server(sock, message)
    answer = get_message_from_server(sock)
    print(answer)