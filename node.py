import os
import socket
import time  #  Added to keep script alive

ip_address = socket.gethostbyname(socket.gethostname())

def listen_for_messages():
    """Node listens for incoming messages"""
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client.sendto(f"Heya from {container_name}".encode(), ((cluster_master), 9999))  

    data, addr = client.recvfrom(1024)
    print(data.decode())


if __name__ == "__main__":
    container_name = os.getenv("container_name", "unknown")
    print(f"Wasgood I am {container_name}, ip addy= {ip_address}")

    if str(ip_address)[-2] == "a":
        cluster_master = "172.16.0.2"
    else:
        cluster_master = "172.16.0.10"


    listen_for_messages()
    # threading.Thread(target=listen_for_messages, daemon=True).start()

    # # Keep the script running
    # while True:
    #     time.sleep(1)  # Prevents container from exiting