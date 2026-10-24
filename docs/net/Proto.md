### Chapter 2: Network Fundamentals

#### 2.1 Network Models and Protocols

The foundation of network programming is understanding network models and protocols. A network model provides an abstract framework for network communication, while protocols define the concrete rules of communication.

##### 2.1.1 The OSI Seven-Layer Model

The OSI (Open Systems Interconnection) model is a network communication model proposed by the International Organization for Standardization (ISO). It divides network communication into seven layers, each with its own responsibilities:

1. **Physical layer**: handles establishing, maintaining and tearing down physical connections, including the transmission medium and signal encoding.
2. **Data link layer**: handles physical addressing, frame transmission and error detection.
3. **Network layer**: handles logical addressing (such as IP addresses) and routing.
4. **Transport layer**: handles end-to-end communication and provides reliable data transmission.
5. **Session layer**: handles establishing, managing and terminating sessions.
6. **Presentation layer**: handles data format conversion, encryption and decryption.
7. **Application layer**: provides the communication interface between applications, such as HTTP and FTP.

##### 2.1.2 The TCP/IP Model

The TCP/IP model is the model actually used on the internet. It divides network communication into four layers:

1. **Network interface layer**: corresponds to the physical and data link layers of the OSI model, and is responsible for frame transmission.
2. **Internet layer**: corresponds to the network layer of the OSI model, and is responsible for IP addressing and routing.
3. **Transport layer**: corresponds to the transport layer of the OSI model, providing reliable TCP and unreliable UDP transport services.
4. **Application layer**: corresponds to the application, presentation and session layers of the OSI model, and provides the communication interface between applications.

#### 2.2 IP Addresses and Ports

Network communication relies on IP addresses and ports to identify the hosts and services taking part in communication.

##### 2.2.1 IPv4 and IPv6

- **IPv4** (Internet Protocol Version 4): uses 32-bit addresses, roughly 4.3 billion of them. An IPv4 address is usually written as four dot-separated decimal numbers, such as 192.168.1.1.
- **IPv6** (Internet Protocol Version 6): uses 128-bit addresses, which gives you an almost unlimited address space. An IPv6 address is usually written as eight colon-separated hexadecimal groups, such as 2001:0db8:85a3:0000:0000:8a2e:0370:7334.

##### 2.2.2 Subnet Masks and Subnets

- **Subnet mask**: used to split an IP address into its network part and its host part. A common subnet mask is 255.255.255.0.
- **Subnet**: divides one large network into several smaller ones, achieved by adjusting the subnet mask.

##### 2.2.3 Ports

- **Port**: identifies a specific service on a host. A port number is a 16-bit integer, ranging from 0 to 65535. Common ports include port 80 for HTTP and port 443 for HTTPS.

#### 2.3 Packets and Segmentation

Data moves over a network as packets. Understanding packet structure and segmentation matters a lot for network programming.

##### 2.3.1 Packet Structure

- **Packet**: consists of a header and the data. The header holds information such as the source address, destination address and protocol; the data part is the data actually being transmitted.

##### 2.3.2 Fragmentation and Reassembly

- **Fragmentation**: when a packet is too large, it has to be split into several smaller packets for transmission.
- **Reassembly**: the receiver puts the smaller fragmented packets back together into the complete packet.

A few numbers come up all the time: IPv4 is 32 bits (about 4.3 billion addresses), IPv6 is 128 bits, and a port is a 16-bit integer ranging from 0 to 65535. The mapping between the OSI seven layers and the TCP/IP four layers is in the lists above; you will keep hitting these concepts while writing network code.

## References

- [net standard library](https://pkg.go.dev/net)
- [net/http standard library](https://pkg.go.dev/net/http)


## Sibling pages

- [Advanced](/net/Advanced.md)
- [Concurrence](/net/Concurrence.md)
- [Intro](/net/Intro.md)
- [Netpoll](/net/Netpoll.md)
- [SlidingWindow](/net/SlidingWindow.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [SlidingWindow](/net/SlidingWindow.md)
