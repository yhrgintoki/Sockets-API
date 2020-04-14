#!/usr/bin/env python3
import socket


def create(content, secret):
    pad = int((len(content) + 3) / 4) * 4 - len(content)
    return len(content).to_bytes(4, 'big') + secret.to_bytes(4, 'big') + (1).to_bytes(2, 'big') + (40).to_bytes(2, 'big') + content + bytes(pad)


def check_header(content, secret, st):
    # not checking the payload length since 461 server has error
    pre = int.from_bytes(content[4:8], 'big')
    step = int.from_bytes(content[8:10], 'big')
    digit = int.from_bytes(content[10:12], 'big')
    if pre != secret or step != st or digit != 40:
        print('Illegal header')


def check_ack(content, id):
    if id != int.from_bytes(content[12:16], 'big'):
        print('Ack package not match')


buffer = 1024
ip = socket.gethostbyname("attu2.cs.washington.edu")
port = 12235
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(create("hello world\0".encode(), 0), (ip, port))
message, addr = client.recvfrom(buffer)
check_header(message, 0, 2)
num = int.from_bytes(message[12:16], 'big')
length = int.from_bytes(message[16:20], 'big')
port = int.from_bytes(message[20:24], 'big')
secretA = int.from_bytes(message[24:28], 'big')
sendNum = 0
client.settimeout(0.5)
while sendNum < num:
    send = create(sendNum.to_bytes(4, 'big') + bytes(length), secretA)
    client.sendto(send, (ip, port))
    try:
        message, addr = client.recvfrom(buffer)
        check_header(message, secretA, 1)
        check_ack(message, sendNum)
        sendNum += 1
    except socket.timeout as e:
        continue
message, addr = client.recvfrom(buffer)
check_header(message, secretA, 2)
port = int.from_bytes(message[12:16], 'big')
secretB = int.from_bytes(message[16:20], 'big')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))
message = client.recv(buffer)
check_header(message, secretB, 2)
num = int.from_bytes(message[12:16], 'big')
length = int.from_bytes(message[16:20], 'big')
secretC = int.from_bytes(message[20:24], 'big')
c = message[24:25]
for i in range(num):
    s = b''
    for j in range(length):
        s += c
    client.send(create(s, secretC))
message = client.recv(buffer)
check_header(message, secretC, 2)
secretD = int.from_bytes(message[12:16], 'big')
client.close()
print('A', secretA, 'B', secretB, 'C', secretC, 'D', secretD)
