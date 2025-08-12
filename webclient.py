import socket
import sys

if len(sys.argv) != 3:
    print('usage: client.py <host> <port>')
    sys.exit(1)

host = sys.argv[1]
try:
    port = int(sys.argv[2])
    if not 1 <= port <= 65535: 
        print("error: port must be between 1 and 65535") 
        sys.exit(1)
except ValueError:
    print("error: port must be a number")
    sys.exit(1)

payload = 'name=etilber&message=Hi!'
req = f'GET /../../../../../../../../ HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n'
# req = f'GET /../secret/secret.txt HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Python-Client/1.0\r\nAccept: */*\r\nConnection: close\r\n\r\n'
# req += payload
req = req.encode('utf-8')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((host, port))
    s.sendall(req)
    response = b''

    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data

    print("Received:\n", response.decode('utf-8'))

except socket.error as e:
    print(f"Socket error: {e}")

finally:
    s.close()