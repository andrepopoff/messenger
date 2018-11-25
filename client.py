import socket


def create_message():
    pass


def send_to_server(message):
    pass


def get_message_from_server():
    pass


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8888))
    message = create_message()
    send_to_server(message)
    answer = get_message_from_server()
    sock.close()
    print(answer.decode('utf-8'))