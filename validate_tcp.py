# ||||

# converts an array with 2 IP addresses 
# into a single bytestring containing both.
def ipstobs(ips):
    bytestring = b''
    for addr in ips:
        addr = addr.split('.')
        for octet in addr:
            octet = int(octet).to_bytes(1, 'big')
            bytestring += octet
            # byte = octet.to_bytes(1, 'big')
            # bytestring += byte

    return bytestring   

# function that generates the IP pseudo header bytes 
# from the IP addresses from tcp_addrs_n.txt
# and the TCP length from the tcp_data_n.dat file.
def pseudoheader(source_ip, dest_ip, tcp_data):
    pseudo_header = b''
    tcp_length = len(tcp_data).to_bytes(1, 'big')
    # tcp_length = tcp_length.to_bytes(1, "big")

    pseudo_header = source_ip + dest_ip + b'\x00\x06' + tcp_length

    return pseudo_header
            

# for i in range(10):
with open(f"tcp_data/tcp_addrs_0.txt", "r") as fp:
    ips = fp.read().split()
    # print(ips)
bytestring = ipstobs(ips)
source_ip, dest_ip = bytestring[:4], bytestring[4:]

with open(f"tcp_data/tcp_data_0.dat", "rb") as fp:
    tcp_data = fp.read()

pseudo_header = pseudoheader(source_ip, dest_ip, tcp_data)
tcp_cksum = tcp_data[16:18]
tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]

if len(tcp_zero_cksum) % 2 == 1:
    tcp_zero_cksum += b'\x00'


# print(source_ip.hex())
# print(dest_ip)
# print(pseudo_header.hex())

# print(tcp_data.hex())
# print(tcp_cksum.hex())
# print(tcp_zero_cksum.hex())
