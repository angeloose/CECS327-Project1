import os
import socket

ip_address = socket.gethostbyname(socket.gethostname())
multicast_group_ips = ["172.16.0.3", "172.16.0.5", "172.16.0.7", "172.16.0.9", "172.16.0.11", "172.16.0.13", "172.16.0.15", "172.16.0.17"]

def listen_for_messages():
    
    # Create client UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client.bind((ip_address, 9999))

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


if __name__ == "__main__":
    container_name = os.getenv("container_name", "unknown")
    #print(f"Wasgood I am {container_name}, ip addy= {ip_address}")

    # if str(container_name)[-2] == "a":
    #     cluster_master_ip = "172.16.0.2"
    # else:
    #     cluster_master_ip = "172.16.0.10"

    listen_for_messages()
