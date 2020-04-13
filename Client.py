#!/usr/bin/env python3
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("Hello, server".encode(), ('localhost', 9527))
message, address = client.recvfrom(1024)
print("recvData:", message.decode())
