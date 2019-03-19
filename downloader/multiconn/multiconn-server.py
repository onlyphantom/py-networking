# =====================================================
#          Purpose [TODO: REPLACE THIS]:
# Illustrate the Socket > Bind > Listen > Accept 
# > Receive > Send > Close paradigm illustrated in
# 2_tcpipmodel.md


# select() allows server to MONITOR multiple client-connected
# connections to see which client has sent the data to process
# 
# socket.listen() # ready to accept connections
# conn.recv
# conn.send()
# =====================================================

import selectors
import socket
import sys

HOST, PORT = sys.argv[1], int(sys.argv[2])
if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit()

sel = selectors.DefaultSelector()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()
print('listening on', (HOST, PORT))

# set socket to non-blocking; The non-blocking socket
# can be used with sel.select() so we can wait for events on
# one or more sockets to perform read/write
lsock.setblocking(False) 
# register so it can be monitored with sel.select(). For the
# listening sockets we want read events: selectors.EVENT_READ
# data stores whatever arbitrary data along with the socket
# and returned when select() returns
sel.register(lsock, selectors.EVENT_READ, data=None)
while True:
    # blocks until there are sockets ready for I/O
    # when unblock, return a list of (key,event) tuples one for
    # each socket. key is a SelectorKey that contains the 
    # socket object (.fileobj). mask is an event mask of the
    # operations that are ready. 
    # 
    # When key.data is None, it's from the listening socket (server).
    # We accept() the connection by registering the new socket 
    # object with the selector.
    # When key.data is not None, it's a client socket that's already
    # accepted and we need to service it using the key and mask
    events = sel.select(timeout=None) 
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)

def accept_wrapper(sock):
    pass

def service_connection(key, mask):
    pass

