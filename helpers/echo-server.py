import socket

HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 44444     # Non-privileged ports are > 1024

# SOCK_STREAM is the socket type for TCP
# SOCK_DGRAM is for UDP
# AF_INET is the internet address family for IPv4

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    # enables server to accept() connections by becoming a listening socket
    s.listen() 
    # accept() blocks and waits for an incoming connection
    # when a client connects, it returns a new socket object representing the connection
    # and a tuple holding the address of the client. (host, port) for IPv4 connections
    # this new socket is what we use to communicate with the client; it's different from
    # the listening socket that the server is using to accept new connections
    conn, addr = s.accept() 
    # loop over blocking calls
    with conn:
        print('Connected by', addr)
        print('Server listening on port', PORT)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # reads whatever data the client sends and echoes back using .sendall()
            conn.sendall(data)

