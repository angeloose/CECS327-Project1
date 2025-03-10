import socket
import threading

# Cluster master details
CLUSTER_A_MASTER = "172.16.0.2"
CLUSTER_B_MASTER = "172.16" \
"\\\\.0.10"

def handle_message(data, addr):
    """Process received messages"""
    message = data.decode()
    print(f"Received: {message} from {addr}")

    if message.startswith("FORWARD_TO:"):
        parts = message.split(",")
        destination_ip = parts[1]
        forwarded_message = parts[2]
        send_message(destination_ip, forwarded_message)

def send_message(ip, message):
    """Send a message to a specific IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(message.encode(), (ip, 5000))
    s.close()

def start_server():
    """Start UDP server for receiving messages"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 5000))

    print("Cluster Master Listening on port 5000...")

    while True:
        data, addr = s.recvfrom(1024)
        threading.Thread(target=handle_message, args=(data, addr)).start()

if __name__ == "__main__":
    start_server()
