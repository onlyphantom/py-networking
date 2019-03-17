import socket

HOST = '127.0.0.1' # The server's hostname or IP address
PORT = 44444  # Port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # Send its message and then read the server's reply and prints it
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))