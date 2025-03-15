import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # internet, TCP protocol
server.bind(('0.0.0.0', 9999))         # IP address, port

server.listen(5)

while True:
    client, addr = server.accept()
    print(client.recv(1024).decode())   # receive and decode message from client
    client.send("Hello From Server".encode())   # send message to client