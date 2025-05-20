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