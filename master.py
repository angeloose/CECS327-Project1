import socket
import os
import time

cluster_a_ips = ["172.16.0.3", "172.16.0.4", "172.16.0.5", "172.16.0.6", "172.16.0.7", "172.16.0.8", "172.16.0.9"]
cluster_b_ips = ["172.16.0.11", "172.16.0.12", "172.16.0.13", "172.16.0.14", "172.16.0.15", "172.16.0.16", "172.16.0.17"]

odd_a_ips = ["172.16.0.3", "172.16.0.5", "172.16.0.7", "172.16.0.9"]
odd_b_ips = ["172.16.0.11", "172.16.0.13", "172.16.0.15", "172.16.0.17"]

ip_address = socket.gethostbyname(socket.gethostname())

def initialize_socket(ip, type, container_name):
    # Wait 2 seconds to ensure container nodes initiailize
    time.sleep(2)

    # Create server socket
    print(f"{container_name} starting UDP server for receiving messages")
    if type == "UDP":
        ssocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    elif type == "TCP":
        ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to 0.0.0.0 which listens to all network interfaces
    print(f"{container_name} Listening on port 9999...")
    ssocket.bind((ip_address, 9999))

    return ssocket

def start_server(server, container_name, allowed_ips, odd_ips):
    # BROADCAST: send message to all nodes of same cluster
    for ip in allowed_ips:  

        # Send message to ip listening to port 9999
        server.sendto(f"Can you hear me my children. It is I, {container_name}".encode(), (ip, 9999))
        data, addr = server.recvfrom(1024)

        print("Received message:", data.decode())

    time.sleep(2)
    # MULTICAST: send message to only a certain group, in this cade odd nodes conly
    for ip in odd_ips:
        
        server.sendto(f"My odd children, how are you this fine evening. From {container_name}".encode(), (ip, 9999))
        data, addr = server.recvfrom(1024)

        print("Received message:", data.decode())


    # Close socket when done with
    server.close()

def reroute_msg(server, allowed_ips, container_name):
    # Receive message from other cluster master and send to node destination

    # Wait and receive msg from node
    data, addr = server.recvfrom(1024)
    
    msg = data.decode()
    print("Redirecting message received:", msg)

    # Pass message to other master
    if container_name[8] == "a":
        other_master_ip = "172.16.0.10"
    else:
        other_master_ip = "172.16.0.2"
    
    server.sendto(f"{msg} {container_name}".encode(), (other_master_ip, 9999))

    # Receive message from master
    data, addr = server.recvfrom(1024)

    # Get destination node ip  (get first index of msg which tells what number container to send to)
    msg = data.decode()
    node_ip = allowed_ips[msg[1] - 1]

    # Send message to destination node
    server.sendto(f"{msg} {container_name}".encode(), (other_master_ip, 9999))
    



def main():
    # Get name of container
    container_name = os.getenv("container_name", "unknown") 

    # Get cluster type based of name  (ex: 'cluster_a_master', container_name[8] = 'a')
    if container_name[8] == "a":
        allowed_ips = cluster_a_ips
        odd_ips = odd_a_ips
    else:
        allowed_ips = cluster_b_ips
        odd_ips = odd_b_ips


    # Intra-Cluster Communication
    socket = initialize_socket(ip_address, "UDP", container_name)
    start_server(socket, container_name, allowed_ips, odd_ips)

    # Inter-Cluster Communication
    socket = initialize_socket(ip_address, "TCP", container_name)
    reroute_msg(socket, allowed_ips, container_name)



if __name__ == "__main__":
    main()