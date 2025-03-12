import os
import socket
import time

ip_address = socket.gethostbyname(socket.gethostname())
multicast_group_ips = ["172.16.0.3", "172.16.0.5", "172.16.0.7", "172.16.0.9"]  # Example for odd nodes

def start_client():
    # Wait for the server to start (adjust as necessary)
    time.sleep(2)

    print(f"{container_name} starting UDP client")

    # Create UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout for socket operations
    client.settimeout(5)  # 5 seconds timeout for blocking operations

    # Listen on port 9999 (for broadcast messages)
    try:
        client.bind(("0.0.0.0", 9999))
    except socket.error as e:
        print(f"Error binding client socket: {e}")
        client.close()
        return

    # Listen for incoming messages from the master server
    while True:
        try:

            data, addr = client.recvfrom(1024)

            # Send msg back to sender
            client.sendto(f"Heya from {container_name}".encode(), addr)  

            print(f"Received message: {data.decode()} from {addr}")
            # Optionally send a response
            #client.sendto(f"Message received from {container_name}".encode(), addr)

            client.sendto(f"I'm odd and I'm proudly {container_name}".encode(), addr) 

        except socket.timeout:
            print("Timeout waiting for incoming message.")
        except socket.error as e:
            print(f"Error receiving message: {e}")

    client.close()

if __name__ == "__main__":
    # Get the name of the container
    container_name = os.getenv("container_name", "unknown")

    start_client()
