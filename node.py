import os
import socket
import time
import csv

# determining clusters
cluster_a_ips = ["172.16.0.2", "172.16.0.3", "172.16.0.4", "172.16.0.5", "172.16.0.6", "172.16.0.7", "172.16.0.8", "172.16.0.9"]
cluster_b_ips = ["172.16.0.10", "172.16.0.11", "172.16.0.12", "172.16.0.13", "172.16.0.14", "172.16.0.15", "172.16.0.16", "172.16.0.17"]

ip_address = socket.gethostbyname(socket.gethostname())
multicast_group_ips = ["172.16.0.3", "172.16.0.5", "172.16.0.7", "172.16.0.9"]  # Example for odd nodes

# ------------------------------------------------
# logging funcs
# ------------------------------------------------

# returns the cluster of the ip
def get_cluster(ip):
    if ip in cluster_a_ips:
        return "Cluster A"
    
    elif ip in cluster_b_ips:
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
        return "0x000"

# logs the communication in a csv file
def log_communication(msg_type, src_ip, dst_ip, message_data):

    src_cluster = get_cluster(src_ip)
    dst_cluster = get_cluster(dst_ip)
    protocol = "UDP"
    length = len(message_data.encode())
    flags = get_message_flags(msg_type)

    # Intra vs Inter
    if src_cluster == dst_cluster:
        type_label = f"Intra-{msg_type}"

    else:
        type_label = f"Inter-{msg_type}"

    current_time = f"{time.time():.6f}"

    with open("/app/logs/network_log.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            type_label,
            f"{time.time():.6f}",
            src_cluster,
            dst_cluster,
            src_ip,
            dst_ip,
            protocol,
            length,
            flags
        ])
    

# ------------------------------------------------
# node logic
# ------------------------------------------------


def start_client():
    # Wait for the server to start (adjust as necessary)
    time.sleep(2)

    container_name = os.getenv("container_name", "unknown")

    print(f"{container_name} starting UDP client")

    # Set the container label
    if "a" in container_name:
        container_label = "Container A" + container_name[-1]

    elif "b" in container_name:
        container_label = "Container B" + container_name[-1]

    else:
        container_label = container_name

    print(f"[{container_label}] Connecting to master...")

    # Create UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout for socket operations
    client.settimeout(5)  # 5 seconds timeout for blocking operations

    # Listen on port 9999 (for broadcast messages)
    try:
        client.bind(("0.0.0.0", 9999))
    except socket.error as e:
        print(f"Error binding client socket: {e}")
        client.close()
        return

    # Listen for incoming messages from the master server
    message_count = 0
    max_messages = 5 # Set a maximum number of messages before exiting 

    while message_count <= max_messages:
        try:
            # Receive the incoming message (this will assign 'addr' to the sender's address)
            data, addr = client.recvfrom(1024)

            decoded_msg = data.decode()

            print(f"Received message: {data.decode()} from {addr}")

            # Determine the message type
            if "my children" in decoded_msg:
                msg_type = "Broadcast"

            elif "odd children" in decoded_msg:
                msg_type = "Multicast"

            else:
                msg_type = "Unknown"

            # Log the received message
            if "Hello, Cluster" in decoded_msg:
                print(f"[{container_label}] Received broadcast message: \"{decoded_msg}\"")

            elif "Hello, Group" in decoded_msg:
                print(f"[{container_label}] Received multicast message: \"{decoded_msg}\"")

            else:
                print(f"[{container_label}] Received message: \"{decoded_msg}\"")

            # Log the receiving csv
            log_communication(msg_type, addr[0], ip_address, decoded_msg)

            # Send a response to the sender
            response = f"Heya from {container_name}"
            
            # Send a response to the sender
            client.sendto(f"Heya from {container_name}".encode(), addr)  # Send to the received 'addr'

            # Log the sending of the response csv
            log_communication("Response", ip_address, addr[0], response)

            # Optionally send another message

            second_msg = f"I'm odd and I'm proudly {container_name}"

            client.sendto(f"I'm odd and I'm proudly {container_name}".encode(), addr)  # Send another message to addr

            # Log the sending of the second message
            log_communication("Response", ip_address, addr[0], second_msg)

            message_count += 1  # Increment the message count

        except socket.timeout:
            print("Timeout waiting for incoming message.")
        except socket.error as e:
            print(f"Error receiving message: {e}")

    print("Reached message limit, closing client.")
    client.close()

if __name__ == "__main__":
    # Get the name of the container
    container_name = os.getenv("container_name", "unknown")

    start_client()
