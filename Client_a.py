#!/usr/bin/env python3
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
header = (4).to_bytes(4, 'big') + bytes(4) + (1).to_bytes(2, 'big') + (40).to_bytes(2, 'big');
client.sendto(header + "hello world\0".encode(), (socket.gethostbyname("attu2.cs.washington.edu"), 12235))

message, address = client.recvfrom(1024)
print(message)
