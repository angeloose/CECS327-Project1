import socket
import threading
import os


ip_address = socket.gethostbyname(socket.gethostname())

def start_server():
    print(f"{container_name} starting UDP server for receiving messages")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("0.0.0.0", 9999))  # Bind to 0.0.0.0 which listens to all network interfaces

    print(f"{container_name} Listening on port 9999...")

    while True:
        data, addr = server.recvfrom(1024)
        print(data.decode())
        server.sendto(f"Hello from {container_name}".encode(), addr)

if __name__ == "__main__":
    container_name = os.getenv("container_name", "unknown")  # Get name of container
    print(f"Hello I am {container_name}")
    start_server()
