import os
import socket
import time
import datetime

ip_address = socket.gethostbyname(socket.gethostname())
multicast_group_ips = ["172.16.0.3", "172.16.0.5", "172.16.0.7", "172.16.0.9"]  # Example for odd nodes

def log_info(msg_type, elasped, sourceip, destip, sourceport, destport, protocol, length, flags):
    timestamp = datetime.datetime.fromtimestamp(float(elasped)).strftime('%Y-%m-%d %H:%M:%S')
    with open("logs.txt", "a") as f:
        f.write(f"Type: {timestamp}, Time: {msg_type}, Source IP: {sourceip}, Destination IP: {destip}, Source Port: {sourceport}, Destination Port: {destport}, Protocol: {protocol}, Length: {length}, Flags: {flags}\n")

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
    message_count = 0
    max_messages = 5 # Set a maximum number of messages before exiting 

    while message_count <= max_messages:
        try:
            # Receive the incoming message (this will assign 'addr' to the sender's address)
            data, addr = client.recvfrom(1024)
            print(f"Received message: {data.decode()} from {addr}")
            
            # Send a response to the sender
            client.sendto(f"Heya from {container_name}".encode(), addr)  # Send to the received 'addr'

            # Optionally send another message
            client.sendto(f"I'm odd and I'm proudly {container_name}".encode(), addr)  # Send another message to addr

            message_count += 1  # Increment the message count

        except socket.timeout:
            print("Timeout waiting for incoming message.")
        except socket.error as e:
            print(f"Error receiving message: {e}")

    print("Reached message limit, closing client.")
    client.close()

if __name__ == "__main__":
    # Get the name of the container
    container_name = os.getenv("container_name", "unknown")

    start_client()
