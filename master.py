import socket
import os
import time
import csv

cluster_a_ips = ["172.16.0.3", "172.16.0.4", "172.16.0.5", "172.16.0.6", "172.16.0.7", "172.16.0.8", "172.16.0.9"]
cluster_b_ips = ["172.16.0.11", "172.16.0.12", "172.16.0.13", "172.16.0.14", "172.16.0.15", "172.16.0.16", "172.16.0.17"]

odd_a_ips = ["172.16.0.3", "172.16.0.5", "172.16.0.7", "172.16.0.9"]
odd_b_ips = ["172.16.0.11", "172.16.0.13", "172.16.0.15", "172.16.0.17"]

ip_address = socket.gethostbyname(socket.gethostname())

# ------------------------------------------------
# logging funcs
# ------------------------------------------------

# returns the cluster of the ip
def get_cluster(ip):
    if ip in cluster_a_ips or ip == "172.16.0.2":  # 172.16.0.2 = cluster_a_master
        return "Cluster A"
    
    elif ip in cluster_b_ips or ip == "172.16.0.10":  # 172.16.0.10 = cluster_b_master
        return "Cluster B"
    
    else:
        return "Unknown"

# returns the flags based on the message type
def get_message_flags(msg_type):
    if msg_type == "Broadcast":
        return "0x010"
    
    elif msg_type == "Multicast":
        return "0x012"
    
    else:
        return "0x000"  # unkwn

# logs the communication in a csv file
def log_communication(msg_type, src_ip, dst_ip, message_data):
    src_cluster = get_cluster(src_ip)
    dst_cluster = get_cluster(dst_ip)
    protocol = "UDP"
    length = len(message_data.encode())  # length of the message
    flags = get_message_flags(msg_type)

    # Intra vs Inter
    if src_cluster == dst_cluster:
        type_label = f"Intra-{msg_type}"

    else:
        type_label = f"Inter-{msg_type}"

    current_time = f"{time.time():.6f}"

    # write to the csv file
    with open("/app/logs/network_log.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            type_label,
            f"{time.time():.6f}",  # current time
            src_cluster,
            dst_cluster,
            src_ip,
            dst_ip,
            protocol,
            length,
            flags
        ])

# ------------------------------------------------
# server logic
# ------------------------------------------------


def start_server():
    # Wait 2 seconds to ensure container nodes initialize
    time.sleep(2)

    # Get name of container
    container_name = os.getenv("container_name", "unknown")

    print(f"{container_name} starting UDP server for receiving messages")

    if "cluster_a_master" in container_name:
        cluster_label = "Cluster A"

    else:
        cluster_label = "Cluster B"

    # Log the start of the server
    print(f"[{cluster_label} Master] Starting {cluster_label} with 8 containers...")

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
    broadcast_msg = f"Can you hear me my children. It is I, {container_name}"

    print(f"[{cluster_label} Master] Sending intra-cluster broadcast message: \"{broadcast_msg}\"")

    for ip in allowed_ips:  
        try:

            # Log the sending of a broadcast
            log_communication("Broadcast", ip_address, ip, broadcast_msg)

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

    multicast_msg = f"My odd children, how are you this fine evening. From {container_name}"

    print(f"[{cluster_label} Master] Sending intra-cluster multicast message: \"{multicast_msg}\"")

    for ip in odd_ips:
        try:

            # Log the sending of a multicast
            log_communication("Multicast", ip_address, ip, multicast_msg)

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