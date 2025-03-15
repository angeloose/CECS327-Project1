import socket
import os
import json
import time
import csv
import threading

# Define clusters
cluster_a_ips = ["172.16.0.2", "172.16.0.3", "172.16.0.4", "172.16.0.5", "172.16.0.6", "172.16.0.7", "172.16.0.8", "172.16.0.9"]
cluster_b_ips = ["172.16.0.10", "172.16.0.11", "172.16.0.12", "172.16.0.13", "172.16.0.14", "172.16.0.15", "172.16.0.16", "172.16.0.17"]

# Get environment variables
ip_address = socket.gethostbyname(socket.gethostname())
cluster_port = int(os.getenv("CLUSTER_PORT", 5001))

# Inter-cluster routing table
routing_table = {
    "Cluster A": {"master_ip": "172.16.0.2", "port": 5001},
    "Cluster B": {"master_ip": "172.16.0.10", "port": 5002},
}

# ------------------------------------------------
# Logging functions (Keeping your previous implementation)
# ------------------------------------------------

def get_cluster(ip):
    if ip in cluster_a_ips:
        return "Cluster A"
    elif ip in cluster_b_ips:
        return "Cluster B"
    else:
        return "Unknown"

def get_message_flags(msg_type):
    return {
        "Broadcast": "0x010",
        "Multicast": "0x012"
    }.get(msg_type, "0x000")

def log_communication(msg_type, src_ip, dst_ip, message_data):
    src_cluster = get_cluster(src_ip)
    dst_cluster = get_cluster(dst_ip)
    protocol = "UDP"
    length = len(message_data.encode())
    flags = get_message_flags(msg_type)

    type_label = f"{'Intra' if src_cluster == dst_cluster else 'Inter'}-{msg_type}"

    print(f"[DEBUG] Logging: {type_label} {src_ip} -> {dst_ip}")  # Debugging print

    current_time = f"{time.time():.6f}"

    with open("/app/logs/network_log.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([type_label, current_time, src_cluster, dst_cluster, src_ip, dst_ip, protocol, length, flags])


# ------------------------------------------------
# UDP Server Logic (Handles Intra & Inter Cluster Messages)
# ------------------------------------------------

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip_address, cluster_port))
    print(f"Cluster Master [{ip_address}] listening on port {cluster_port}...")

    while True:
        data, addr = sock.recvfrom(1024)
        message = json.loads(data.decode())
        
        src_ip = message["src_ip"]
        dst_ip = message["dst_ip"]
        msg_type = message["type"]
        message_data = message["data"]

        print(f"[DEBUG] Received {msg_type} message from {src_ip} to {dst_ip}")

        # If the destination is in another cluster, forward it
        if get_cluster(src_ip) != get_cluster(dst_ip):
            target_master = routing_table[get_cluster(dst_ip)]
            master_ip, master_port = target_master["master_ip"], target_master["port"]

            print(f"[DEBUG] Routing to {master_ip}:{master_port}")
            sock.sendto(data, (master_ip, master_port))
        
        log_communication(msg_type, src_ip, dst_ip, message_data)


if __name__ == "__main__":
    start_server()
