# The TCP/IP Five-Layer Network Model

There are several models that aim to explain how network devices communicate but in this guide we'll use the Five-Layer Network Model

|#  | Layer Name | Protocol   | Protocol Data Unit  | Addressing   |
|---|------------|------------|---------------------|--------------|
|5  |Application |HTTP, SMTP etc|Messages|n/a|
|4  |Transport   |TCP/UDP|Segment|Port #'s|
|3  |Network     |IP|Datagram|IP address|
|2  |Data Link   |Ethernet, WiFi|Frames|MAC Address|
|1  |Physical    |10 Base T, 802.11|Bits|n/a|

## Physical Layer
- Represents the physical devices that interconnect computers
    - Specifications for the networking cable and the connectors that join devices together
    - Specifications describing how signals are sent over these connections
    - All about cabling, connectors and sending signals

## Data Link Layer
Responsible for defining a common way to interpret these signals so network devices can communicate 
    - Lots of protocols exist at this layer but the most common is the Ethernet, although wireless technologies are becoming more popular
    - Beyond specifying physical layer attributes, the Ethernet standards also define a protocol responsible for getting data to nodes on the same network or link

## Network Layer
- The "internet" layer that allows different networks to communicate with each other through devices known as routers.
    - While the data link layer gets data across a single link, the network layer is responsible for getting data delivered across a collection of networks
    - The most common protocol at this layer is the Internet Protocol (IP)

## Transport Layer
- We may run an email application and web server on the same server at the same time, but our emails end up in our web browser while web pages arrive at our web browser: this is down to the transport layer.
    - While the network layer delivers data between two individual nodes, the transport layer sorts out which client and server programs are supposed to get the data. 
    - The most common protocol at this layer is the Transmission Control Protocol (TCP)
    - Other transfer protocols also use IP to get around, including the User Datagram Protocol (UDP). TCP and UDP ensis how data gets to the right application running on those nodes  

## Application Layer
- Lots of protocols exist at this layer, and they're application-specific. 

## Summary
We can think of layers like different aspects of a package being delivered:
- Physical layer is the delivery truck and the roads
- The data link layer is how the deliver truck gets from one intersection to another over and over
- The network layer identifies which roads need to be taken to get from address A to B
- The transport layer ensures the delivery guy knows how to knock on your door when the package arrive
- The application layer is the contents of the package itself