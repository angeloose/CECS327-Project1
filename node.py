import socket
import threading
import time
from network import send_message

CLUSTER_MASTER = "192.168.1.2"  # Update based on setup

def listen_for_messages():
    """Node listens for incoming messages"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    try:
        s.bind(("", 5000))
        print("Listening on port 5000...")
    except OSError as e:
        print(f"Error binding to port 5000: {e}")
        return

    while True:
        data, addr = s.recvfrom(1024)
        print(f"Message received from {addr}: {data.decode()}")

def send_to_cluster_master(message):
    """Send a message to the cluster master"""
    send_message(CLUSTER_MASTER, message)

if __name__ == "__main__":
    threading.Thread(target=listen_for_messages, daemon=True).start()

    # Keep the script running
    while True:
        time.sleep(1)  # Prevents container from exiting
