import socket
import sys

if len(sys.argv) != 2:
    print("usage: server.py <port>")
    sys.exit(1)

try:
    port = int(sys.argv[1])
except ValueError:
    print("error: port must be a number\n")
    sys.exit(1)

resp_msg = 'Hello client!'
response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(resp_msg)}\r\nConnection: close\r\n\r\n{resp_msg}'
response = response.encode('utf-8')
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind(('', port))
    s.listen()
    
    while True:
        new_conn = s.accept()
        new_socket = new_conn[0]
        request_data = new_socket.recv(4096)
        request_data = request_data.decode('utf-8')
        print("Received Request:\n" + request_data.rstrip('\r\n') + '\n')

        if request_data:
            new_socket.send(response)
            new_socket.close()
        else:
            s.close()
            break

except socket.error as err:
    print(f"socket error: {err}")

finally:
    s.close()