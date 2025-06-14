import textwrap
import socket
import sys
import os

if len(sys.argv) != 2:
    print("usage: server.py <port>")
    sys.exit(1)

try:
    port = int(sys.argv[1])
except ValueError:
    print("error: port must be a number\n")
    sys.exit(1)

if not 1 <= port <= 65535:
    print("error: port must be between 1 and 65535")
    sys.exit(1)

resp_msg = 'Hello client!'
# response = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(resp_msg)}\r\nConnection: close\r\n\r\n'
# response += resp_msg
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind(('', port))
    s.listen()
    
    while True:
        new_conn = s.accept()
        new_socket = new_conn[0]
        request_data = new_socket.recv(4096)

        try:
            request_str = request_data.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Error decoding request: {e}")
            new_socket.close()
            continue

        if request_data:
            # get first line & file path
            first_line = request_str.split('\r\n')[0]
            request_method = first_line.split(' ')[0]
            file_path = first_line.split(' ')[1]

            # strip file path
            file_name = os.path.split(file_path)[-1]

            # get extension
            file_ext = os.path.splitext(file_name)[-1]

            #set content type
            content_type = 'text/html' if (file_ext=='.html') else 'text/plain'

            # Reading the File, Content-Length, and Handling Not Found
            try:
                with open(file_name, "rb") as fp:
                    data = fp.read()
                    status = '200 OK'
                    content_length = len(data)
                    # return data
            except:
                status = '404 Not Found'
                data = b'404 Not Found\n'
                content_type = 'text/plain'
                content_length = 13
                
            # payload = request_str.split('\r\n\r\n')[1]
            # response += f'\nPayload: {payload}'

            # form & send response
            response = (
                f"HTTP/1.1 {status}\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Length: {content_length}\r\n"
                f"Connection: close\r\n\r\n"
            )
            response = response.encode('utf-8')
            response += data 
            new_socket.send(response)
            new_socket.close()
            # continue
        else:
            s.close()
            break
        try:
            # first_line = request_str.split('\r\n')[0]
            
            # payload = request_str.split('\r\n\r\n')[1]

            print(f"Received Request from {new_conn[1][0]}")
            print(f"Method: {request_method}")
            # print(f'Payload: {payload}')
            # print(f'File: {file_name}')
            # print(f'Extension: {file_extension}')
            print(f"\nFull Request:\n{request_str.rstrip('\r\n')}\n")
        except IndexError:
            print(f"received malformed request from new_conn[1][0]")
            new_socket.close()
            continue

except socket.error as err:
    print(f"socket error: {err}")

finally:
    s.close()