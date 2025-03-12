import os
import socket
import time  #  Added to keep script alive

ip_address = socket.gethostbyname(socket.gethostname())

def listen_for_messages():
    
    # Create client UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client.bind((ip_address, 9999))

    # Wait for msg 
    data, addr = client.recvfrom(1024) 
    print(data.decode())

    client.sendto(f"Heya from {container_name}".encode(), addr)  

    data, addr = client.recvfrom(1024)  # Wait for msg
    print(data.decode())


if __name__ == "__main__":
    container_name = os.getenv("container_name", "unknown")
    print(f"Wasgood I am {container_name}, ip addy= {ip_address}")

    if str(container_name)[-2] == "a":
        cluster_master_ip = "172.16.0.2"
    else:
        cluster_master_ip = "172.16.0.10"

    listen_for_messages()
