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
...
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





