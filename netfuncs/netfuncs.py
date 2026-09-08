# 

import sys
import json

def ipv4_to_value(ipv4_addr):
    a, b, c, d = map(int, ipv4_addr.split('.'))

    return (a << 24) | (b << 16) | (c << 8) | d


def value_to_ipv4(addr):
    return '.'.join(str(addr>>shift & 0xff) for shift in (24, 16, 8, 0))


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
    for rd_ip, router_data in routers.items():
        mask = router_data.get("netmask")
        if ips_same_subnet(ip, rd_ip, mask):
            return rd_ip

    return None

# Uncomment this code to have it run instead of the real main.
# Be sure to comment it back out before you submit!
"""
def my_tests():
    print("-------------------------------------")
    print("This is the result of my custom tests")
    print("-------------------------------------")

    print(x)

    # Add custom test code here
"""

## -------------------------------------------
## Do not modify below this line
##
## But do read it so you know what it's doing!
## -------------------------------------------

def usage():
    print("usage: netfuncs.py infile.json", file=sys.stderr)

def read_routers(file_name):
    with open(file_name) as fp:
        json_data = fp.read()
        
    return json.loads(json_data)

def print_routers(routers):
    print("Routers:")

    routers_list = sorted(routers.keys())

    for router_ip in routers_list:

        # Get the netmask
        slash_mask = routers[router_ip]["netmask"]
        netmask_value = get_subnet_mask_value(slash_mask)
        netmask = value_to_ipv4(netmask_value)

        # Get the network number
        router_ip_value = ipv4_to_value(router_ip)
        network_value = get_network(router_ip_value, netmask_value)
        network_ip = value_to_ipv4(network_value)

        print(f" {router_ip:>15s}: netmask {netmask}: " \
            f"network {network_ip}")

def print_same_subnets(src_dest_pairs):
    print("IP Pairs:")

    src_dest_pairs_list = sorted(src_dest_pairs)

    for src_ip, dest_ip in src_dest_pairs_list:
        print(f" {src_ip:>15s} {dest_ip:>15s}: ", end="")

        if ips_same_subnet(src_ip, dest_ip, "/24"):
            print("same subnet")
        else:
            print("different subnets")

def print_ip_routers(routers, src_dest_pairs):
    print("Routers and corresponding IPs:")

    all_ips = sorted(set([i for pair in src_dest_pairs for i in pair]))

    router_host_map = {}

    for ip in all_ips:
        router = str(find_router_for_ip(routers, ip))
        
        if router not in router_host_map:
            router_host_map[router] = []

        router_host_map[router].append(ip)

    for router_ip in sorted(router_host_map.keys()):
        print(f" {router_ip:>15s}: {router_host_map[router_ip]}")

def main(argv):
    if "my_tests" in globals() and callable(my_tests):
        my_tests()
        return 0

    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    src_dest_pairs = json_data["src-dest"]

    print_routers(routers)
    print()
    print_same_subnets(src_dest_pairs)
    print()
    print_ip_routers(routers, src_dest_pairs)

if __name__ == "__main__":
    sys.exit(main(sys.argv))