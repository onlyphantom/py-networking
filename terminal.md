# Terminal Commands for Networking

## IP Addresses
```bash
$ ifconfig
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	ether f0:18:98:55:ef:d8 
	inet6 fe80::1c6c:449d:1dc9:d60a%en0 prefixlen 64 secured scopeid 0xa 
	inet 192.168.88.162 netmask 0xffffff00 broadcast 192.168.88.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
```

From the resulting output, find `en0` - on later versions of macbooks `en0` is usually the AirPort (WiFi).

Typically a machine would have `en0`, `en1`, `lo0` and some other hardware interfaces:
- `en0`: Ethernet 0
- `en1`: Ethernet 1
- `lo0`: Loopback (localhost) 

To see all hardware ports:
```bash
$ networksetup -listallhardwareports
Hardware Port: Wi-Fi
Device: en0
Ethernet Address: f0:18:98:55:ef:d8

Hardware Port: Bluetooth PAN
Device: en6
Ethernet Address: f0:18:98:57:c9:71

Hardware Port: Thunderbolt 1
Device: en1
Ethernet Address: 86:00:9d:61:53:01
```

Our IP address is listed above (`192.168.88.162`). Alternatively, we can employ a more direct approach:
```bash
$ ipconfig getifaddr en0
192.168.88.162
```
## Nameservers Lookup
`nslookup` will display the actual IP address for the name queried (192.168.88.1) and also the name server used to make the request (in this case: 192.168.88.1).

```bash
$ nslookup algorit.ma 
Server:		192.168.88.1
Address:	192.168.88.1#53

Non-authoritative answer:
Name:	algorit.ma
Address: 103.9.100.186

$ nslookup google.com
Server:		192.168.88.1
Address:	192.168.88.1#53

Non-authoritative answer:
Name:	google.com
Address: 172.217.160.46
```

## Ping
```bash
$ ping algorit.ma
```

## Scan a network
```bash
$ nmap -sn 192.168.88.0/24
Starting Nmap 7.70 ( https://nmap.org ) at 2019-03-13 20:47 WIB
Nmap scan report for 192.168.88.1
Host is up (0.019s latency).
Nmap scan report for 192.168.88.160
Host is up (0.029s latency).
Nmap scan report for 192.168.88.162
Host is up (0.0016s latency).
Nmap scan report for 192.168.88.224
Host is up (0.071s latency).
Nmap scan report for 192.168.88.232
Host is up (0.041s latency).
Nmap scan report for 192.168.88.251
Host is up (0.032s latency).
Nmap done: 256 IP addresses (6 hosts up) scanned in 6.81 seconds
```

## Network / Sockets Status on Host Machine
1. Execute `helpers/echo-server.py` in one terminal; 
2. While (1) listens for connection open a second terminal; Execute `helpers/echo-client.py`
3. Go back to (1) and notice the the printed message: `Connected by ('127.0.0.1', 57007)`. 57007 is the port number for the client socket, not the server socket. 
4. Use `netstat -an` or `lsof -i -n` to view socket state

```bash
$ netstat -an
Active Internet connections (including servers)
Proto Recv-Q Send-Q  Local Address          Foreign Address        (state)   
tcp4       0      0  127.0.0.1.44444        *.*                    LISTEN 
```
If in `helpers/echo-server.py` we substituted `HOST='127.0.0.1'` for `HOST=''` we would expect the Local Address file printed in netstat to be `*.44444` instead of `127.0.0.1.44444`. When the `Local` address is `*.44444` which means all available host interfaces that support the address family will be used. The `tcp4` value in the `Proto` column tells us that `socket.AF_INET` was used (IPv4). 

Another way of seeing this is the `lsof` command, which stands for "list open files". When used with the `i` flag, it gives you the COMMAND, PID (process id) and USER (user id) of open Internet sockets.

```bash
$ lsof -i -n
COMMAND     PID   USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
python3.6 22459 samuel    3u  IPv4 0x1af15eb429051673      0t0  TCP 127.0.0.1:44444 (LISTEN)
```