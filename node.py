import os
import socket
import random

ip_address = socket.gethostbyname(socket.gethostname())
multicast_group_ips = ["172.16.0.3", "172.16.0.5", "172.16.0.7", "172.16.0.9", "172.16.0.11", "172.16.0.13", "172.16.0.15", "172.16.0.17"]
cluster_a_ips = ["172.16.0.3", "172.16.0.4", "172.16.0.5", "172.16.0.6", "172.16.0.7", "172.16.0.8", "172.16.0.9"]
cluster_b_ips = ["172.16.0.11", "172.16.0.12", "172.16.0.13", "172.16.0.14", "172.16.0.15", "172.16.0.16", "172.16.0.17"]


def initialize_socket(ip, type):
    # Create client socket
    if type == "UDP":
        csocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    elif type == "TCP":
        csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to 0.0.0.0 which listens to all network interfaces
    csocket.bind((ip_address, 9999))

    return csocket


def listen_for_messages(client, container_name):
    # Wait for msg 
    data, addr = client.recvfrom(1024) 
    print("Received message:", data.decode())

    # Send msg back to sender
    client.sendto(f"Heya from {container_name}".encode(), addr)  


    # If in multicast group, wait for second message
    if ip_address in multicast_group_ips:
        # Wait for seecond message
        data, addr = client.recvfrom(1024)  
        print("Received message:", data.decode())
        client.sendto(f"I'm odd and I'm proudly {container_name}".encode(), addr) 


def send_message(client, master_ip):
    # Send message to node by first sending message to master, which then passed to other cluster master and then to node destination


    # Message sent to container number
    destination_node = "7"

    # Send msg to master
    client.sendto(f"{destination_node} Hello container 7, it's me, 1, from the other side!".encode(), (master_ip, 9999)) 

    # Wait for confirmation


def listen_for_messages(client, container_name):
    # Wait for msg 
    data, addr = client.recvfrom(1024) 
    print("Received message:", data.decode())

    # Send msg back to sender
    client.sendto(f"Heya from {container_name}".encode(), addr)  


    # If in multicast group, wait for second message
    if ip_address in multicast_group_ips:
        # Wait for seecond message
        data, addr = client.recvfrom(1024)  
        print("Received message:", data.decode())
        client.sendto(f"I'm odd and I'm proudly {container_name}".encode(), addr) 
    
def receive_msg():
    
def main():
    container_name = os.getenv("container_name", "unknown")
    #print(f"Wasgood I am {container_name}, ip addy= {ip_address}")

    if str(container_name)[-2] == "a":
        cluster_master_ip = "172.16.0.2"
        cluster_ips = cluster_a_ips
    else:
        cluster_master_ip = "172.16.0.10"
        cluster_ips = cluster_b_ips
    

    # Intra-Cluster Communication
    socket = initialize_socket(ip_address, "UDP")
    listen_for_messages(socket, container_name)

    # Inter-Cluster Communication (Only container 2 will send a msg to container 7
    if ip_address == cluster_ips[1]:
        socket = initialize_socket(ip_address, "UDP")
        send_message(socket, cluster_master_ip)
    if ip_address == cluster_ips[6]:
        socket = initialize_socket(ip_address, "UDP")
        receive_message(socket, cluster_master_ip)
        

if __name__ == "__main__":
    main()

