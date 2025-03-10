import socket

def send_message(ip, message):
    """Send a UDP message to a specific IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message.encode(), (ip, 5000))
    s.close()

def broadcast_message(message, cluster_nodes):
    """Send message to all nodes in the same cluster"""
    for node in cluster_nodes:
        send_message(node, message)

def anycast_message(message, cluster_nodes):
    """Send message to the first available node in the cluster"""
    closest_node = cluster_nodes[0]
    send_message(closest_node, message)

def multicast_message(message, group_nodes):
    """Send message to a subset of nodes"""
    for node in group_nodes:
        send_message(node, message)

if __name__ == "__main__":
    print("Hi i am network")