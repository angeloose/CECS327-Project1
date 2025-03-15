import socket
import os
import time
import csv

cluster_a_ips = ["172.16.0.3", "172.16.0.4", "172.16.0.5", "172.16.0.6", "172.16.0.7", "172.16.0.8", "172.16.0.9"]
cluster_b_ips = ["172.16.0.11", "172.16.0.12", "172.16.0.13", "172.16.0.14", "172.16.0.15", "172.16.0.16", "172.16.0.17"]

cluster_a_master_ip = "172.16.0.2"
cluster_b_master_ip = "172.16.0.10"

ip_address = socket.gethostbyname(socket.gethostname())

# ------------------------------------------------
# logging funcs
# ------------------------------------------------

def get_cluster(ip):
    if ip in cluster_a_ips or ip == cluster_a_master_ip:
        return "Cluster A"
    elif ip in cluster_b_ips or ip == cluster_b_master_ip:
        return "Cluster B"
    else:
        return "Unknown"

def get_message_flags(msg_type):
    if msg_type == "Broadcast":
        return "0x010"
    elif msg_type == "Multicast":
        return "0x012"
    else:
        return "0x000"  # unknown

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

    with open("/app/logs/network_log.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([type_label, current_time, src_cluster, dst_cluster, src_ip, dst_ip, protocol, length, flags])

# ------------------------------------------------
# server logic
# ------------------------------------------------

def forward_to_cluster_b(src_ip, dst_ip, message_data):
    # Forward message from Cluster A to Cluster B via Cluster B Master
    print(f"Forwarding message from {src_ip} to {dst_ip} via Cluster B Master")
    log_communication("Inter-Unicast", src_ip, dst_ip, message_data)

def start_server():
    # Wait 2 seconds to ensure container nodes initialize
    time.sleep(2)
    container_name = os.getenv("container_name", "unknown")

    print(f"{container_name} starting UDP server")

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip_address, 5001))  # Cluster A port

    print(f"Listening on {ip_address}:5001")

    while True:
        message_data, addr = sock.recvfrom(1024)
        print(f"Received message: {message_data.decode()} from {addr}")

        if addr[0] == cluster_a_master_ip:  # This is a forwarding from Cluster A Master
            print(f"Forwarding message to {cluster_b_master_ip}")
            forward_to_cluster_b(addr[0], addr[1], message_data.decode())
            sock.sendto(message_data, (cluster_b_master_ip, 5002))  # Send to Cluster B Master
        else:
            log_communication("Unicast", addr[0], addr[1], message_data.decode())

start_server()
