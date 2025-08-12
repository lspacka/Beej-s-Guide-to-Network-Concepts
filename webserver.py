import socket
import sys
import os

def send_response(socket, status, content_type, data):
    content_length = len(data)
    response = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {content_length}\r\n"
        f"Connection: close\r\n\r\n" 
    ).encode('utf-8') + data
    socket.send(response)
    socket.close()

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
            # base_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.abspath('.')
            file_path = file_path.lstrip('/')
            file_path = os.path.join(base_dir, file_path)
            dir_listing = []

            # path resolution check
            # print(f"Base Dir: {base_dir}")
            # print(f"Requested file_path: {file_path}")
            # print(f"Real path: {os.path.realpath(file_path)}")
            # print(f"Base dir: {os.path.realpath(base_dir)}")

            file_path = os.path.abspath(file_path)
            if not file_path.startswith(base_dir):
                print(f"Security warning: Attempted access to {file_path} from {new_conn}[1][0]")
                send_response(new_socket, '403 Forbidden', 'text/plain', b'403 Forbidden: Access outside root directory\n')
                continue

            # file_path = full_path

            # strip file path
            file_name = os.path.split(file_path)[-1]
            # get extension
            file_ext = os.path.splitext(file_name)[-1]
            #set content type
            match file_ext:
                case '':
                    content_type = 'text/html'
                case '.html':
                    content_type = 'text/html'
                case '.txt':
                    content_type = 'text/plain'
                case '.pdf':
                    content_type = 'application/pdf'
                case '.jpeg':
                    content_type = 'image/jpeg'
                case '.jpg':
                    content_type = 'image/jpeg'
                case '.gif':
                    content_type = 'image/gif'
                case _:
                    content_type = 'application/octet-stream'

            content_length = 13         # default content length

            if (os.path.isdir(file_path)):
                print("its a folder")
                html_string = """
                    <!DOCTYPE html>
                    <html>
                        <head>
                            <title>Directory Listing</title>
                        </head>
                        <body>
                            <h1>Directory Listing:</h1>
                            <ul style="padding:0">
                """
                # fix here
                if (file_path == base_dir):
                    dir_listing = os.listdir(base_dir)
                    for item in dir_listing:
                        if (os.path.isdir(item) and os.path.basename(item) != ".git"):
                            html_string += f"<li><a href=\"/files\">{item}</a></li>"
                        else:
                            html_string += f"<li>{item}</li>"
                else:
                    dir_listing = os.listdir(file_path)
                    for item in dir_listing:
                        html_string += f"<p><a href=\"/files/{item}\">{item}</a></p>"

                # for item in dir_listing:
                #     # html_string += f"<li>{item}</li>"
                #     html_string += f"<p><a href=\"/files/{item}\">{item}</a></p>"
                
                html_string += """
                            </ul>
                        </body>
                    </html>
                """

                # dir_listing = str(dir_listing)
                # dir_listing = dir_listing.encode('utf-8')
                # data = dir_listing
                data = html_string.encode('utf-8')
                content_type = 'text/html'
                content_length = len(data)
                status = '200 OK'
            else:
                print("its a file")
                try:
                    with open(file_path, "rb") as fp:
                        data = fp.read()
                        status = '200 OK'
                        # content_length = len(data)
                except:
                    status = '404 Not Found'
                    data = b'404 Not Found\n'

            # payload = request_str.split('\r\n\r\n')[1]
            # response += f'\nPayload: {payload}'

            send_response(new_socket, status, content_type, data)

        else:
            s.close()
            break
        try:
            print(f"Received Request from {new_conn[1][0]}")
            print(f"Method: {request_method}")
            # print(f'Payload: {payload}')
            # print(f'Path: {file_path}')
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
