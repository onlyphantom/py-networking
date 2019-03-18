# The TCP/IP Five-Layer Network Model

There are several models that aim to explain how network devices communicate but in this guide we'll use the Five-Layer Network Model

|#  | Layer Name | Examle Protocols   | Protocol Data Unit  | Addressing   |
|---|------------|------------|---------------------|--------------|
|5  |Application |HTTP, SMTP, IMAP|Messages|n/a|
|4  |Transport   |TCP/UDP|Segment|Port #'s|
|3  |Network     |IP|Datagram|IP address|
|2  |Data Link   |Ethernet, WiFi|Frames|MAC Address|
|1  |Physical    |10 Base T, 802.11|Bits|n/a|

## Physical Layer
- Represents the physical devices that interconnect computers, such as a cable or a Wi-Fi radio
    - Specifications for the networking cable and the connectors that join devices together
    - Specifications describing how signals are sent over these connections
    - All about cabling, connectors and sending signals

## Data Link Layer
Responsible for defining a common way to interpret these signals so network devices can communicate. It provides the service of getting the data from one network device to another directly connected network device
    - Lots of protocols exist at this layer but the most common is the Ethernet, although wireless technologies are becoming more popular
    - Beyond specifying physical layer attributes, the Ethernet standards also define a protocol responsible for getting data to nodes on the same network or link

## Network Layer
- The "internet" layer that allows different networks to communicate with each other through devices known as routers
    - While the data link layer gets data across a single link, the network layer is responsible for getting data delivered across a collection of networks
    - The most common protocol at this layer is the Internet Protocol (IP)

## Transport Layer
- We may run an email application and web server on the same server at the same time, but our emails end up in our web browser while web pages arrive at our web browser: this is down to the transport layer.
    - While the network layer delivers data between two individual nodes, the transport layer sorts out which client and server programs are supposed to get the data. 
    - The most common protocol at this layer is the Transmission Control Protocol (TCP)
    - Other transfer protocols also use IP to get around, including the User Datagram Protocol (UDP). TCP and UDP ensure data gets to the right application running on those nodes  

### TCP and UDP
Recall that while IP facilitates the transport of data from one network device to another, it doesn't provide the destination device a way of knowing what to do with the data once it receives it. One solution would be to program every process running on the destination device to check all of the incoming data to see if any are interested in it, but this is infeasible from a performance and security standpoint. 

**Transmission Control Protocol (TCP)** and **User Datagram Protocol (UDP)** both provides end-to-end transportation of data between applications on different devices and they solve the question by introducing the concept of **ports**. A port is an endpoint, which is attached to one of the IP adderesses assigned to the network device. 
    - Ports are claimed by a process running on the device, and the process is said to be **listening** on that port
    - Ports are represented by a 16-bit number so each IP address on a device has 65,635 ports a process can claim (port number 0 is reserved)
    - Ports can be claimed by one process at a time (although a process can claim more than one port at a time)

1. When a message is sent over the network through TCP or UDP, the sending application sets the destination port number in the header of the TCP or UDP packet
    - Port numbers need to be known before the message was sent (hence "convention")
2. When the message arrives at the destination, the TCP or UDP protocol implementation on the receiving device reads the port number and delivers the message payload to the process listening on that port. Most OS contains a copy of this list of services, in `/etc/services`:

```bash
$ sed -n '70, 90 p' /etc/services
chargen          19/udp     # Character Generator
chargen          19/tcp     # Character Generator
ftp-data         20/udp     # File Transfer [Default Data]
ftp-data         20/tcp     # File Transfer [Default Data]
ftp              21/udp     # File Transfer [Control]
ftp              21/tcp     # File Transfer [Control]
#                          Jon Postel <postel@isi.edu>
ssh              22/udp     # SSH Remote Login Protocol
ssh              22/tcp     # SSH Remote Login Protocol
#                          Tatu Ylonen <ylo@cs.hut.fi>
telnet           23/udp     # Telnet
telnet           23/tcp     # Telnet
#                          Rick Adams <rick@UUNET.UU.NET>
smtp             25/udp     # Simple Mail Transfer
smtp             25/tcp     # Simple Mail Transfer
```

TCP and UDP packet headers may also include a **source port** number. This is optional for UDP but mandatory for TCP. The source port number tells the receiving application on the server where it should send replies to when sending data back to the client.

A quick overview on UDP: it is deliberately uncomplicated and provides no services other than those that we described in earlier sections. It just takes the data, packetizes it with the destination port number (and optional source port number) then hands it off to the local Internet Protocol for delivery. Applications on the receiving end see the data in the same discrete chunks in which it was packetized. Like IP, UDP is a connectionless protocol: both IP and UDP attempt to deliver their packets on a best effort basis but makes no guarantee that the packets will arrive their destinations. Often times it's up to a higher layer protocol or the sending application to determine if the packets have arrived. 
    - Tyoical applications of UDP: internet telephony, video streaming, DNS queries

An overview of the more dependable sibling, TCP: it is a connection based protocol (as opposed to connectionless like UDP). In such a protocol, no data is sent until the server and client **have performed an initial exchange of control packets** ("handshake"). This establishes a connection, and from then on data can be sent. Each data packet that is received is acknowledged by the receiving party, and it does so by sending a packet called an **ACK**. As such, TCP always requires that the packets include a source port number because it depends on the continual two-way exchange of messages.

From an application's point of view, the application sees data transmitted under the UDP protocol in discrete chunks whereas a TCP connections presents the data as a continuous, seamless stream of bytes. This also means that with TCP we must decide a mechanism for unambigiously determining where our messages start and end.

TCP provides the following services:
- In-order delivery
- Receipt acknowledgment 
- Error detection
- FLow and congestion control

Data sent through TCP is guaranteed to get delivered to the receiving application in the order that it was sent in. The receiving TCP implementation buffers the received packets on the receiving device and then waits until it can deliver them in the correct order before passing them to the application. If an ACK is not received for a sent packet, it will be resent within a time period - if there's still no response TCP will try resending the packet at increasing intervals until a second, longer timeout period expires at which point it gives up and notify the sending application that it has been unsuccessful. 

The TCP header includes a checksum of the header data and the payload, allowing the receiver to verify whether a packet's contents have been modified during the transmission. TCP also includes algorithms which ensure that traffic is not sent too quickly for the receiving device to process, which includes inference on network conditions and regulate the transmission rate to avoid network congestion. Many popular higher level protocols such as HTTP, SMTP, SSH and IMAP depend on TCP.

Why then would we need a connectionless protocol like UDP? For the most part it's because  the Internet is still pretty reliable and most packets do get delivered. The connectionless protocols are useful where the minimum transfer overhead is required and where occasional dropped packet isn't a big deal. TCP's reliability and congestion control necessitates additional packets and round-trips, and even introduces deliberate delays (to prevent congestion) leading to increased latency while providing little value for real-time services. Case in point: a football streaming media or Skype call may experience a small transient glitch or drop in signal quality, but as long as the packets keep coming, the steam can recover. The round-trips and added latency on the hand is less desirable.  

As we'll see later in the `helpers/echo-server.py` and `helpers/echo-client.py` example, the Python `socket` module provides a convenient and consistent API that maps directly to these system calls, their C counterparts. 
| ![](assets/tcp_flow.png)| 
|:--:| 
| *TCP Socket Flow diagram, OnionBulb* |

## Application Layer
- Lots of protocols exist at this layer, as this layer is deliberately left open as a catch-all for any protocol that is developed on top of TCP or UDP (or even IP, those these are rarer). Examples are HTTP, SMTP, IMAP, DNS and FTP.

## Summary
We can think of layers like different aspects of a package being delivered:
- Physical layer is the delivery truck and the roads
- The data link layer is how the deliver truck gets from one intersection to another over and over
- The network layer identifies which roads need to be taken to get from address A to B
- The transport layer ensures the delivery guy knows how to knock on your door when the package arrive
- The application layer is the contents of the package itself
- To see a demo of how the network modules act as a stack: [Demo: smtp](smtp.md)

