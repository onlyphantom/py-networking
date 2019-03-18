# =====================================================
#                        Purpose:
# Illustrate the Socket > Bind > Listen > Accept 
# > Receive > Send > Close paradigm illustrated in
# 2_tcpipmodel.md

# socket.socket(IPv4, TCP)
# socket.bind((Host, Port))
# socket.listen() # ready to accept connections
# socket.accept() # blocks port & return a new socket 
#                 # object representing the connection
# conn.recv
# conn.send()
# =====================================================

import socket

HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 44444     # Port to listen on. Non-privileged ports are > 1023

# Argument 1: the address family (AF_INET = IPv4)
# Argument 2: socket type (SOCK_STREAM = TCP, SOCK_DGRAM = UDP)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
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

