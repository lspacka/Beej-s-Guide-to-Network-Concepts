# |||||
import json

# routers = json.loads("example1.json")

hex_ip = 0xc0a88225
ip = ''

def value_to_ipv4(addr):
    return '.'.join(str(addr>>shift & 0xff) for shift in (24, 16, 8, 0))

def ipv4_to_value(ipv4_addr):
    a, b, c, d = map(int, ipv4_addr.split('.'))

    return (a << 24) | (b << 16) | (c << 8) | d

def get_subnet_mask_value(slash):
    bitrun = (1 << 32) - 1
    subnet = int(slash.split('/')[-1])
    
    return (bitrun << (32-subnet)) & 0xFFFFFFFF

def ips_same_subnet(ip1, ip2, slash):
    subnet_mask = get_subnet_mask_value(slash)
    ip_1 = ipv4_to_value(ip1)
    ip_2 = ipv4_to_value(ip2)

    subnet1 = subnet_mask & ip_1
    subnet2 = subnet_mask & ip_2
   
    return subnet1 == subnet2

def get_network(ip_value, netmask):
    return netmask & ip_value

def find_router_for_ip(routers, ip):
    with open(routers, 'r') as f:
        rd = json.load(f)

    return rd
# print(value_to_ipv4(16909060))
# print(ipv4_to_value("1.2.3.4"))
# print(get_subnet_mask_value("10.20.30.40/23"))
# print(ips_same_subnet("10.23.121.17", "10.23.121.225", "/23"))
# print(hex(get_network(0x01020304, 0xffffff00)))
print(find_router_for_ip('netfuncs/example1.json', '1.2.3.4'))