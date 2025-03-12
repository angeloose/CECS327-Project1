import socket
import os
import time

cluster_a_ips = ["172.16.0.3", "172.16.0.4", "172.16.0.5", "172.16.0.6", "172.16.0.7", "172.16.0.8", "172.16.0.9"]
cluster_b_ips = ["172.16.0.11", "172.16.0.12", "172.16.0.13", "172.16.0.14", "172.16.0.15", "172.16.0.16", "172.16.0.17"]

odd_a_ips = ["172.16.0.3", "172.16.0.5", "172.16.0.7", "172.16.0.9"]
odd_b_ips = ["172.16.0.11", "172.16.0.13", "172.16.0.15", "172.16.0.17"]

ip_address = socket.gethostbyname(socket.gethostname())

def start_server():
    # Wait 2 seconds to ensure container nodes initialize
    time.sleep(2)

    print(f"{container_name} starting UDP server for receiving messages")

    # Create UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout for socket operations
    server.settimeout(5)  # 5 seconds timeout for blocking operations

    try:
        # Bind to 0.0.0.0 which listens to all network interfaces
        server.bind(("0.0.0.0", 9999))  
        print(f"{container_name} Listening on port 9999...")
    except socket.error as e:
        print(f"Error binding socket: {e}")
        server.close()
        return

    # BROADCAST: send message to all nodes of same cluster
    for ip in allowed_ips:  
        try:
            # Send message to ip listening to port 9999
            server.sendto(f"Can you hear me my children. It is I, {container_name}".encode(), (ip, 9999))
            data, addr = server.recvfrom(1024)
            print("Received message:", data.decode())
        except socket.timeout:
            print(f"Timeout waiting for response from {ip}")
        except socket.error as e:
            print(f"Error during communication with {ip}: {e}")

    time.sleep(2)

    # MULTICAST: send message to only a certain group, in this case odd nodes only
    for ip in odd_ips:
        try:
            server.sendto(f"My odd children, how are you this fine evening. From {container_name}".encode(), (ip, 9999))
            data, addr = server.recvfrom(1024)
            print("Received message:", data.decode())
        except socket.timeout:
            print(f"Timeout waiting for response from odd node {ip}")
        except socket.error as e:
            print(f"Error during communication with odd node {ip}: {e}")

    # Close socket when done with
    server.close()

if __name__ == "__main__":
    # Get name of container
    container_name = os.getenv("container_name", "unknown") 

    # Get cluster type based on name (ex: 'cluster_a_master', container_name[8] = 'a')
    if container_name[8] == "a":
        allowed_ips = cluster_a_ips
        odd_ips = odd_a_ips
    else:
        allowed_ips = cluster_b_ips
        odd_ips = odd_b_ips

    start_server()