# =====================================================
#          Purpose [TODO: REPLACE THIS]:
# This version of server uses .setblocking(False) to 
# prevent server from blocking. 
# Same loop: Socket > Bind > Listen > Accept 
# > Receive > Send > Close paradigm 
#
# ## Listening socket: 
# s.socket().bind().listen().setblocking(F) -> register with Sel
# ## Accept connections from listening socket:
# s.accept().setblocking(F) -> register with Sel
# ## Receiving data from connected sockets:
# s.recv() -> append to data; sel.unregister(); s.close()
# socket.listen() # ready to accept connections
# conn.recv
# conn.send()
# =====================================================

import selectors
import socket
import sys
import types

HOST, PORT = sys.argv[1], int(sys.argv[2])
if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit()

sel = selectors.DefaultSelector()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
lsock.bind((HOST, PORT)) # lsock = listening socket
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
    # blocks until there are sockets ready for I/O. When unblock,
    # return a list of (SelectorKey, event) tuples one for each 
    # socket. SelectorKey contains the socket object (.fileobj)
    # mask is an event mask of the operations that are ready
    events = sel.select(timeout=None) 
    for key, mask in events:
        # key.data can only be None if its the listening socket so we
        # accept the connection (get new socket object & register)
        if key.data is None:
            accept_wrapper(key.fileobj)
        # then we know its a client socket; Operate on the socket
        else:
            service_connection(key, mask)

def accept_wrapper(sock):
    # listening socket was registered for selectors.EVENT_READ so it is
    # ready to read. Call sock.accept() and put socket in non-blocking
    conn, addr = sock.accept()
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    # register again, but this socket READ / WRITE and return data
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    # key is tuple returned from select() containing socket object (fileobj)
    # and data object. mask contains events that are ready 
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            # it means client has closed their connection, so server should too
            print('closing connection to', data.addr)
            # so it's no longer monitored by selector
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)
            data.outb += data.outb[sent:]

