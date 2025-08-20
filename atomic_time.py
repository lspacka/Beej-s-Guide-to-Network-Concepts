# atomic time p.52

import socket
import time

# The time server returns the number of seconds since 1900, but Unix
# systems return the number of seconds since 1970. This function
# computes the number of seconds since 1900 on the system.

def system_secs(): 
    # number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800
    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
response = b''

try:
    s.connect(('time.nist.gov', 37))
    data = s.recv(4)
    s.close()
    response += data
    response = int.from_bytes(response, "big")
    system_time = system_secs()

    print(f"NIST time: {response}")
    print(f"System time: {system_time}")

except socket.error as e:
    print(f"Socket error: {e}")
