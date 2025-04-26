# file_server.py
import socket
import os

# Create a directory to save uploaded files if it doesn't exist
if not os.path.exists('server_files'):
    os.makedirs('server_files')

# Server settings
host = '0.0.0.0'
port = 5001

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(5)
print(f"Server listening on port {port}...")

while True:
    client_socket, address = server_socket.accept()
    print(f"Client connected: {address}")

    command = client_socket.recv(1024).decode()

    if command == "upload":
        filename = client_socket.recv(1024).decode()
        filesize = int(client_socket.recv(1024).decode())

        filepath = os.path.join('server_files', filename)
        with open(filepath, "wb") as f:
            bytes_read = 0
            while bytes_read < filesize:
                data = client_socket.recv(4096)
                if not data:
                    break
                f.write(data)
                bytes_read += len(data)

        print(f"File uploaded: {filename}")

    elif command == "download":
        filename = client_socket.recv(1024).decode()
        filepath = os.path.join('server_files', filename)

        if os.path.exists(filepath):
            client_socket.send(b"OK")
            filesize = os.path.getsize(filepath)
            client_socket.send(str(filesize).encode())

            with open(filepath, "rb") as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    client_socket.sendall(data)

            print(f"File sent: {filename}")
        else:
            client_socket.send(b"ERROR")

    client_socket.close()
    print("Client disconnected.\n")
