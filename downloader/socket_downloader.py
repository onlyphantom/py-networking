import sys, socket

try:
    rfc_number = int(sys.argv[1])
except (IndexError, ValueError):
    print('Must supply an RFC number as first argument')
    sys.exit(2)

host = 'www.ietf.org'
port = 80 # http uses port 80 and https uses 443 by default
sock = socket.create_connection((host, port)) # creates a TCP connection

req = (
    'GET /rfc/rfc{rfcnum}.txt HTTP/1.1\r\n'
    'Host: {host}:{port}\r\n'
    'Connection: close\r\n'
    '\r\n'
)

req = req.format(
    rfcnum=rfc_number,
    host=host,
    port=port
)

sock.sendall(req.encode('ascii'))
rfc_raw = bytearray()
while True:
    buf = sock.recv(4096) # receive up to 4096 bytes from the socket
    if not len(buf):
        break
    rfc_raw += buf
rfc = rfc_raw.decode('utf-8')
print(rfc)