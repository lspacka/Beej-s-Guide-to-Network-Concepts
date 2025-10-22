### ipv4_to_value

Convert a dots-and-numbers IP address to a single 32-bit numeric
value of integer type. Returns an integer type.

### value_to_ipv4

Convert a single 32-bit numeric value of integer type to a
dots-and-numbers IP address. Returns a string type.

### get_subnet_mask_value

Given a subnet mask in slash notation, return the value of the mask
as a single number of integer type. The input can contain an IP
address optionally, but that part should be discarded.
Returns an integer type.

### ips_same_subnet

Given two dots-and-numbers IP addresses and a subnet mask in slash
notation, return true if the two IP addresses are on the same subnet.
Returns a boolean.
FOR FULL CREDIT: this must use your get_subnet_mask_value() and
    ipv4_to_value() functions. Don't do it with pure string
    manipulation.

    This needs to work with any subnet from /1 to /31

    Example:

    ip1:    "10.23.121.17"
    ip2:    "10.23.121.225"
    slash:  "/23"
    return: True
    
    ip1:    "10.23.230.22"
    ip2:    "10.24.121.225"
    slash:  "/16"
    return: False

### get_network

Return the network portion of an address value as integer type.
    
    Example:

    ip_value: 0x01020304
    netmask:  0xffffff00
    return:   0x01020300

### find_router_for_ip

Search a dictionary of routers (keyed by router IP) to find which
    router belongs to the same subnet as the given IP.

    Return None if no routers is on the same subnet as the given IP.

    FOR FULL CREDIT: you must do this by calling your ips_same_subnet()
    function.

    Example:

    [Note there will be more data in the routers dictionary than is
    shown here--it can be ignored for this function.]

    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.3.5"
    return: "1.2.3.1"


    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.5.6"
    return: None