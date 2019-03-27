# Firewall
## Definition
Hardware or software that inspects the network packets flowing through it and filters what it lets through based on the packet's properties. Firewalls can sit at network boundaries or be run as applications on network clients and servers.

## Filtering Rules
Filters can be based on any property of the network traffic but common ones are:
- Transport layer protocol (TCP or UDP)
- Source and destination IP addresses
- Source and destination IP port numbers

One example of filtering strategy is to deny all inbound traffic with exceptions for traffic that matches very specific parameters. For example: block all incoming traffic except TCP traffic with the destination IP address of the web server and destination port number 80.

Firewalls can also block outbound traffic, for example to prevent network devices from sending data packets to outside its premise, or calling home. 

# Network Address Translation
Packets with sources or destination addresses in the private ranges are forbidden from being routed over the public Internet. NAT solves this by sitting at the gateway, and as it receives packets from the network destined for the Internet, rewrites the packets' headers to replace the private range source IP addresses with its own public range IP address. 

If the packet contain TCP or UDP packets and these contain a source port, NAT may also open up a new source port for listening on its external interface and rewrite the source port number in the packets to match this new number.

As it performs these rewrites, it records the mapping between the newly opened source port and the source device on the internal network. Any replies to the new source port will be translated and sent to the original device on the internal network. The originating network device shouldn't be aware that its traffic is undergoing NAT.

## Benefits
- Internal network devices are shielded from malicious traffic from the public Internet  
- Added layer of privacy since private addresses are hidden
- Network devices that need to be assigned precious IP addresses are reduced