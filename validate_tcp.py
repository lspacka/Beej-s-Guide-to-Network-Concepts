# converts an array with 2 IP addresses 
# into a single bytestring containing both.
def ipstobs(ips):
    bytestring = b''
    for addr in ips:
        addr = addr.split('.')
        for octet in addr:
            octet = int(octet).to_bytes(1, 'big')
            bytestring += octet

    return bytestring   

# function that generates the IP pseudo header bytes 
# from the IP addresses from tcp_addrs_n.txt
# and the TCP length from the tcp_data_n.dat file.
def pseudoheader(source_ip, dest_ip, tcp_data):
    pseudo_header = b''
    tcp_length = len(tcp_data).to_bytes(2, 'big')
    pseudo_header = source_ip + dest_ip + b'\x00\x06' + tcp_length

    return pseudo_header

# calculates checksum to be compared against the one on the tcp header
def checksum(pseudo_header, tcp_data):
    data = pseudo_header + tcp_data
    total = 0
    offset = 0

    while offset < len(data):
        word = int.from_bytes(data[offset:offset+2], 'big')
        offset += 2
        total += word
        total = (total & 0xffff) + (total >> 16)

    return (~total) & 0xffff
            

for i in range(10):
    with open(f"tcp_data/tcp_addrs_{i}.txt", "r") as fp:
        ips = fp.read().split()
    
    bytestring = ipstobs(ips)
    source_ip, dest_ip = bytestring[:4], bytestring[4:]

    with open(f"tcp_data/tcp_data_{i}.dat", "rb") as fp:
        tcp_data = fp.read()

    pseudo_header = pseudoheader(source_ip, dest_ip, tcp_data)
    tcp_cksum = int.from_bytes(tcp_data[16:18], 'big')
    tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]

    if len(tcp_zero_cksum) % 2 == 1:
        tcp_zero_cksum += b'\x00'

    calc_cksum = checksum(pseudo_header, tcp_zero_cksum)

    if tcp_cksum == calc_cksum:
        print("PASS")
    else:
        print("FAIL")