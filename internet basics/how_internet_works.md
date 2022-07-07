### Who creates all the rules/protocols?
- The Internet Society.


### TCP: Transmission Control Protocol
- Non corruptible.


### What is IP address?
-  Unique address of an entity in the world of internet.


### How modem manages internal IPs?
- The ISP generally provide a single public IP to the user through the modem. All the devices which are then
    connected are provided private IP addresses/local IP addresses. This is managed through a protocol called 
    as NAT(Network address translation)
- Within a modem network which device sends/receives request is managed through NAT.


### How does internet reach to different applications within a device?
- Internet reaches devices through IP addresses and reaches different applications through different ports.
- Ports are 16-bit numbers. Total around 2^16.
- Ports 0-1023 are reserved ports. We can't create our own application to dedicate these ports.
- HTTP: Port 80
- HTTPS: Port 443
- Postgres: Port 5432


### LAN, WAN, MAN:
- LAN: local area, connected through ethernet cables.
- MAN: connect across cities
- WAN: connect across countries
- The internet is a collection of such above connections/networks.


### What is use of a modem?
- Modem transfers digital data to electrical(analogue) signals and vice-versa.


### What is use of a router?
- Router is a device which routes the packets based on their IP address.


### What is an ISP?
- It is the internet service provider. Further more there are different tiers of ISPs.
- Tier 1 ISPs actually handle the inter-country internet setup. From them, other smaller players pay to use.


### OSI Model:
- Open system interconnection model. This was designed to have a standard way of communication between 2 or more 
    computers.
- Layers: 
  - Application layer: Implemented at software level, actual application. Eg: Protocols like: HTTP, FTP
        Users interact with this layer. Eg: Whatsapp, Browsers. 
        Client-server architecture is one architecture where there will be a central server which caters to requests
        sent by multiple clients.
        P2P(Peer to Peer): Connection only b/w 2 systems to share data. Eg: ShareIt, Torrent

  - Presentation layer: Encoding, encryption, compression of the actual ASCII code to binary happens here. 
        Eg: Protocol like: SSL
  
  - Session layer: Authentication and authorization happen at this stage. Adds the session ID from the cookies.
  
  - Transport layer: Protocols of how actually data to be transmitted. First data is segmented. Every segmented data 
        will have a port num and a sequence number. Chunking happens in this layer. Protocols like: TCP, UDP
  
  - Network layer: Transmission of data across networks. Router lives in this layer. Assigns the sender's and receiver's
        IP address to each segment, and it forms an IP packet. Also routes the packet to the required destination.
  
  - Data link layer: The physical addressing/Mac addressing is done at this layer. A packet is created after adding a 
        MAC address and sent to the actual physical address. Computer's bluetooth may have one Mac address, Wi-Fi may 
        have a different MAC address.
  
  - Physical layer: Hardware layer which converts the binary to electrical signals and sends it over wires. Modem lives
        in this layer.


### TCP/IP Model:
- Another model different from OSI Model.
- Has the following layers:
  - Application layer
  - Transport layer
  - Network layer
  - Datalink layer
  - Physical layer
- This is actually a more practical model which is in usage and OSI is a theoretical model.


### Protocols:
- TCP/IP: HTTP, SMTP (to send emails), FTP, POP3 AND IMAP (to receive emails), SSH
- UDP: Doesn't contain session and data might get lost in between.


### What are sockets?
- Any time a program needs to connect to the internet, an OS process helps in doing so. In that process, the program 
    binds the IP and a certain port. This binding/combination is called a socket. So as many number of connections, 
    same are the number of sockets created. 
- A host creates a socket and keeps on listening to the same for any exchange of information. Once the information
    transfer cycle is completed, the socket is closed.
- Its more of a software thing created by the process and doesn't have any hardware significance.
- A connection/session has 2 sockets opened on client/server side.


### Ports:
- On the server side usually the port numbers are fixed. 
- On the client side the port numbers are more dynamic and short-lived and are called ephemeral port numbers. 


### How email transfer works?
- Application layer protocol for sending email - SMTP, receiving - POP3
- Transport layer protocol used: TCP.
- User's email client, will send the email to the sender's SMTP server. Then it would make a connection with the
    receiver's SMTP server. After connection established, data is transferred. The receiver then keeps polling until it
    downloads the actual email from its SMTP server.
- For same domain email client for sender and receiver, the intermediary servers aren't involved.


### What is DNS resolution?
- DNS resolution is converting the domain name to some valid IP address where the client can send data.
- It is something which runs parallel at the application layer.
- DNS mostly works as a phone book or one giant large database.
- First the system will check in its own cache for the ip address of the domain that we've just used. If not found
    in the local cache, it will then ask the ISP to check if that has the IP address of the searched domain.
- If not resolved by the ISP, it will reach out to root server. Root server contains the IP address of all the top level
    domains. For eg: in google.com here the top level domain is .com. The root server won't have the direct address of 
    google.com but, it will have for the top level .com domain server. The TLD server would then send the address of the 
    authoritative name server. The authoritative name server definitely contains the details of ip add of google.com.

  
### Transport layer:
- The actual transportation of messages from one system to another is being done by the network layer.
- Transport layer transports the messages from the network layer to the application layer. It happens within the same 
    computer.
- The transport layer is located on every device.
- If we're sending a message, mail and video call to somebody else, then transport layer multiplexes them.
    In the receiver's system the de-multiplexing will happen.
- The transport layer since maintains the application level data sending/receiving, it does so by using sockets
    which contains the port details.
- Transport layer also handles congestion control using various algorithms. The congestion control also happens at the
    network layer.


## TCP(Transmission control protocol)
- TCP segments data sent from application layer. Adds segment number, port num, checksum, other headers.
- It is connection oriented.
- Provides congestion control.
- One connection only between 2 computers.


#### How connection is actualy established?
- Through 3 way handshake.
- Client sends a request to establish connection using the SYN flag. The server responds it back with an ACK flag.
    The client then will again send an ACK flag.


#### How TCP maintains order of data?
- After chunking the data sent from application layer, it maintains something called sequence number.


#### How is data integrity maintained in TCP?
  - Using something called checksum.
  - A number is generated depending on the actual data. Along with the actual data we send, we send the checksum we 
    calculated. The receiver again calculates the checksum at their end. If both of them mismatch, then
    the data packet is rejected by the receiver, and it sends a negative acknowledgment. The sender will then resend the 
    same.
  

#### How to verify data actually got received in TCP?
  - This is achieved through timers. For most operations we've associated timers. If the activity doesn't complete
    within specified time or acknowledgment isn't received within the timer expiration then we'll assume that the packet
    got lost.

    
### UDP (User datagram protocol)
- It is a  transport layer protocol (Transfers data from application layer to network layer and vice-versa).
- It is a connection less protocol. (Unlike TCP)
- Data may/mayn't delivered.
- Data may get corrupt.
- Data mayn't be in order.
- UDP uses checksum to check if data has got corrupted or not but won't take any action on it. The receiver would
    silently drop the packet without asking for the same again from the source.
- UDP packet consists of source port no, destination port no, checksum, length of datagram, actual data.
- UDP is faster



### Network Layer:
- In the transport layer, data travels in segments. In the network layer after addition of ip addresses they're converted
    into packets.
- In n/w layer, we work with routers.
- A router maintains a routing table. By using a routing table, a router knows which direction to send the ip packets
    for it to reach its destination. This process is called forwarding. This hopping generally happens at the ISP level
    and not at individual router level.
- Router also performs something called filtering which is by using the Address resolution protocol (ARP) to figure out
    the MAC address to which a packet is to be forwarded.


### Internet Protocol (IP):
- IPV4 32 bit, 4 words. 192.168.2.30 the first 3 words: 192.168.2 is the network address and 30 is the device address.
- The network address is otherwise known as subnet.


### Datalink layer:
- Takes the ip packets and breaks them down into frames. It then adds the target MAC address.
- The address resolution of IP to mac is done by the router using the ARP(Address resolution protocol).
- Every device's interface card has a unique MAC address. The wifi card and bluetooth card of a laptop would have
    different MAC addresses.


### Physical Layer:
- Process of sending bits through electrical signals. This is done by the Modem.


- Data always get past through our network, although not meant for us. Its job of the network card to keep/discard the
    data.