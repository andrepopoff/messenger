import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8888))
time = sock.recv(1024)
sock.close()
print(time.decode('utf-8'))