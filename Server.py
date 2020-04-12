import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('localhost', 9527))
while True:
    message, address = server.recvfrom(1024)
    server.sendto("Hello, client".encode(), address)
    print("recvData:", message.decode())
