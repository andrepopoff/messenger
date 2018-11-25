import socket
import sys
import time


def create_message():
    return {
        'action': 'presence',
        'time': time.time()
    }


def send_to_server(message):
    pass


def get_message_from_server():
    pass


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
    send_to_server(message)
    answer = get_message_from_server()
    print(answer)