import socket
import os
import time

cluster_a_ips = ["172.16.0.3", "172.16.0.4", "172.16.0.5", "172.16.0.6", "172.16.0.7", "172.16.0.8", "172.16.0.9"]
cluster_b_ips = ["172.16.0.11", "172.16.0.12", "172.16.0.13", "172.16.0.14", "172.16.0.15", "172.16.0.16", "172.16.0.17"]

ip_address = socket.gethostbyname(socket.gethostname())

def start_server():
    # Wait 2 seconds to ensure container nodes initiailize
    time.sleep(2)

    print(f"{container_name} starting UDP server for receiving messages")

    # Create UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to 0.0.0.0 which listens to all network interfaces
    server.bind(("0.0.0.0", 9999))  

    print(f"{container_name} Listening on port 9999...")

    for ip in allowed_ips:  # Run until a message is sent to each of the 7 other containers

        # Send message to ip listening to port 9999
        server.sendto(f" Can you hear me my children. It is I, {container_name}".encode(), (ip, 9999))
        data, addr = server.recvfrom(1024)

        print(data.decode())
        server.sendto(f"Hello from {container_name}".encode(), addr)

    server.close()

if __name__ == "__main__":
    container_name = os.getenv("container_name", "unknown")  # Get name of container
    print(f"Hello I am {container_name}")

    print(container_name[8])
    if container_name[8] == "a":
        allowed_ips = cluster_a_ips
    else:
        allowed_ips = cluster_b_ips

    start_server()
