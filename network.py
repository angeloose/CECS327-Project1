import socket

def send_message(ip, message):
    """Send a UDP message to a specific IP"""
    print(f"Sending message to {ip}: {message}")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message.encode(), (ip, 5000))
    s.close()

def broadcast_message(message, cluster_nodes):
    """Send message to all nodes in the same cluster"""
    print("Broadcasting message to all nodes...")

    for node in cluster_nodes:
        send_message(node, message)

def anycast_message(message, cluster_nodes):
    """Send message to the first available node in the cluster"""
    print("Sending anycast message to the first available node...")

    for node in cluster_nodes:
        if is_node_alive(node):
            send_message(node, message)
            break

def multicast_message(message, group_nodes):
    """Send message to a subset of nodes"""
    print("Sending multicast message to the group...")

    for node in group_nodes:
        send_message(node, message)

def is_node_alive(ip):
    """Check if a node is alive by sending a ping"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, 5000))
        s.close()

        return True
    
    except socket.error:
        return False

def define_group(cluster_nodes, group_criteria):
    """Define a group of nodes based on criteria"""
    group_nodes = []

    for node in cluster_nodes:
        if group_criteria(node):
            group_nodes.append(node)
            
    return group_nodes

# Example usage
if __name__ == "__main__":
    cluster_nodes = ["172.16.0.3", "172.16.0.4", "172.16.0.5"]
    
    # Broadcast message to all nodes
    broadcast_message("Hello, Cluster!", cluster_nodes)
    
    # Anycast message to the first available node
    anycast_message("Hello, Anycast!", cluster_nodes)
    
    # Define a group based on some criteria (e.g., IP ends with '4' or '5')
    group_criteria = lambda ip: ip.endswith('4') or ip.endswith('5')
    group_nodes = define_group(cluster_nodes, group_criteria)
    
    # Multicast message to the defined group
    multicast_message("Hello, Group!", group_nodes)
