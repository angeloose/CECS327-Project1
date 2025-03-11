import socket
import os
import time

cluster_a_ips = ["172.16.0.2", "172.16.0.3", "172.16.0.4", "172.16.0.5", "172.16.0.6", "172.16.0.7", "172.16.0.8", "172.16.0.9"]
cluster_b_ips = ["172.16.0.10", "172.16.0.11", "172.16.0.12", "172.16.0.13", "172.16.0.14", "172.16.0.15", "172.16.0.16", "172.16.0.17"]

ip_address = socket.gethostbyname(socket.gethostname())

def start_server():
    print(f"{container_name} starting UDP server for receiving messages")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("0.0.0.0", 9999))  # Bind to 0.0.0.0 which listens to all network interfaces

    print(f"{container_name} Listening on port 9999...")

    for _ in range(7):  # Run until a message is sent to each of the 7 other containers
        while True:
            data, addr = server.recvfrom(1024)
            server_ip = addr[0]
            if server_ip in allowed_ips:  # Ensure master only finds ips within its cluster
                print(data.decode())
                server.sendto(f"Hello from {container_name}".encode(), addr)
                break
            time.sleep(1)

if __name__ == "__main__":
    container_name = os.getenv("container_name", "unknown")  # Get name of container
    print(f"Hello I am {container_name}")

    if container_name[8] == "a":
        allowed_ips = cluster_a_ips
    else:
        allowed_ips = cluster_b_ips


    start_server()
