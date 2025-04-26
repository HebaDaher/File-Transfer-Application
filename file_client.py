# file_client.py
import socket
import os

# Create a directory to save downloaded files if it doesn't exist
if not os.path.exists('client_files'):
    os.makedirs('client_files')

host = input("Enter server IP (e.g., 127.0.0.1 for local): ")
port = 5001

client_socket = socket.socket()
client_socket.connect((host, port))
print("Connected to server.")

command = input("Enter 'upload' to upload a file OR 'download' to download a file: ").lower()
client_socket.send(command.encode())

if command == "upload":
    filepath = input("Enter path of file to upload: ")
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    client_socket.send(filename.encode())
    client_socket.send(str(filesize).encode())

    with open(filepath, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            client_socket.sendall(data)

    print(f"File uploaded successfully: {filename}")

elif command == "download":
    filename = input("Enter the file name to download: ")
    client_socket.send(filename.encode())

    response = client_socket.recv(1024)
    if response == b"OK":
        filesize = int(client_socket.recv(1024).decode())
        filepath = os.path.join('client_files', filename)

        with open(filepath, "wb") as f:
            bytes_read = 0
            while bytes_read < filesize:
                data = client_socket.recv(4096)
                if not data:
                    break
                f.write(data)
                bytes_read += len(data)

        print(f"File downloaded successfully: {filename}")
    else:
        print("ERROR: File not found on server!")

client_socket.close()
print("Connection closed.")
