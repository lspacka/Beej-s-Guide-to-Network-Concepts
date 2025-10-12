# 

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


# print(value_to_ipv4(16909060))
# print(ipv4_to_value("1.2.3.4"))
print(get_subnet_mask_value("10.20.30.40/23"))