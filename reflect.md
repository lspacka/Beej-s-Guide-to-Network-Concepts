### What role does the OS play when you’re writing networked programs?
It takes the data and encapsulates it in consecutive operations or layers. each layer is independent and ignores the functions of the others, it just does its job.

### What is a protocol?
it's a set of rules for establishing communication.

### What are the reasons for having a protocol stack and data encapsulation?
since each layer is just responsible for its own encapsulation, it doesnt need to know what the other layers are doing. each layer is associated with its own set of protocols.

### What are the practical differences between a WiFi network and a wired network?
one consists of computers connected to the same access point, and the other of computers wired together. at a low level they use the ethernet protocol.

### When a router sees an IP address, how does it know where to forward it?
it uses a routing table

### Speculate on why the IP header wraps up the TCP header in the layered model, and not the other way around.
if the TCP header wraps the IP header there's no way to know where to send the data, as the TCP header only has a port number. 

### What is the benefit to having a static IP? How does it relate to DNS?
the benefit is that the website will be easily reachable because the DNS entry stays the same, there is no need to update it.

### Speculate on why accept() returns a new socket as opposed to just reusing the one we called listen() with.
to support concurrency ig

### What would happen if the server didn’t loop to another accept() call? What would happen when a second client tried to connect?
since the server is listening for connections but not accepting, the client's request is not received, so there's no connection established.

### Speculate about why ports exist. What functionality do they make possible that plain IP addresses do not?
IP addresses only purpose is to route data to a specific host. a port numbers is associated with a specific service or program. just the IP address alone wouldnt deliver the data to the receiving service.