import socket
import os
import json
import time
import csv

# Cluster Configuration
cluster_a_ips = ["172.16.0.2", "172.16.0.3", "172.16.0.4", "172.16.0.5", "172.16.0.6", "172.16.0.7", "172.16.0.8", "172.16.0.9"]
cluster_b_ips = ["172.16.0.10", "172.16.0.11", "172.16.0.12", "172.16.0.13", "172.16.0.14", "172.16.0.15", "172.16.0.16", "172.16.0.17"]

# Get environment variables
ip_address = socket.gethostbyname(socket.gethostname())
cluster_master_ip = os.getenv("CLUSTER_MASTER_IP", "172.16.0.2")  # Default to Cluster A Master
cluster_port = int(os.getenv("CLUSTER_PORT", 5001))

# Logging Functions (Same as master.py)
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
    current_time = f"{time.time():.6f}"

    with open("/app/logs/network_log.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([type_label, current_time, src_cluster, dst_cluster, src_ip, dst_ip, protocol, length, flags])

# Send message function
def send_message(msg_type, dst_ip, message_data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dst_cluster = get_cluster(dst_ip)
    
    # Determine if message is intra or inter-cluster
    if dst_cluster == get_cluster(ip_address):  
        target_ip, target_port = dst_ip, cluster_port
    else:
        print(f"Inter-cluster message detected, routing via master {cluster_master_ip}")
        target_ip, target_port = cluster_master_ip, cluster_port

    message = json.dumps({
        "type": msg_type,
        "src_ip": ip_address,
        "dst_ip": dst_ip,
        "data": message_data
    })

    sock.sendto(message.encode(), (target_ip, target_port))
    log_communication(msg_type, ip_address, dst_ip, message_data)
    print(f"Sent {msg_type} message to {dst_ip} via {target_ip}:{target_port}")

# Example usage
if __name__ == "__main__":
    # Example: Define a list of nodes for broadcast/multicast
    multicast_group_ips = ["172.16.0.3", "172.16.0.5", "172.16.0.7", "172.16.0.9"]  # Example for odd nodes

    # Unicast: Pick a single target
    target_node = "172.16.0.4"  # Example target for unicast

    # If the target is in the same cluster, use Unicast
    if target_node in cluster_a_ips or target_node in cluster_b_ips:
        send_message("Unicast", target_node, "Hello from Node!")

    # Broadcast: Send to all nodes in the same cluster
    for node in (cluster_a_ips if ip_address in cluster_a_ips else cluster_b_ips):
        if node != ip_address:  # Don't send to itself
            send_message("Broadcast", node, "Broadcast Message from Node!")

    # Multicast: Send to specific group in the same cluster
    if ip_address in multicast_group_ips:
        for node in multicast_group_ips:
            if node != ip_address:
                send_message("Multicast", node, "Multicast Message from Node!")