#!/usr/bin/env python3
import socket
import _thread
import random
import sys


def create(content, secret, step, client_digit):
    pad = int((len(content) + 3) / 4) * 4 - len(content)
    return len(content).to_bytes(4, 'big') + secret.to_bytes(4, 'big') + step.to_bytes(2, 'big') + (client_digit).to_bytes(2, 'big') + content + bytes(pad)


def header_is_verified(content, payload_len, psecret, client_digit):
    len = int.from_bytes(content[0:4], 'big')
    pre = int.from_bytes(content[4:8], 'big')
    step = int.from_bytes(content[8:10], 'big')
    digit = int.from_bytes(content[10:12], 'big')
    if len != payload_len or pre != psecret or step != step_num_client or digit != client_digit:
        return False
    return True


def new_client(message, client_address):
    # part a
    message_a = "hello world\0"
    psecret_a = 0
    num_a = random.randint(0, 50)
    len_a = random.randint(4, 64)
    udp_port_a = random.randint(49152, 65535)
    secret_a = random.randint(1, 1000)

    # check header
    payload_len = int.from_bytes(message[0:4], 'big')
    pre = int.from_bytes(message[4:8], 'big')
    step = int.from_bytes(message[8:10], 'big')
    client_digit = int.from_bytes(message[10:12], 'big')
    if payload_len != len(message_a) or pre != psecret_a or step != step_num_client:
        print("illegal header at stage a")
        return

    if len(message) == (len(message_a) + 3) // 4 * 4:
        return

    # check client send "hello world"
    if message_a.encode('utf-8') != message[header_len:header_len+len(message_a)]:
        print("illegal message from client")
        return

    new_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload_a = num_a.to_bytes(4, 'big') + len_a.to_bytes(4, 'big') + udp_port_a.to_bytes(4, 'big') + secret_a.to_bytes(4, 'big')
    new_client_socket.sendto(create(payload_a, 0, 2, client_digit),client_address)

    # part b
    new_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    new_client_socket.bind((ip, udp_port_a))
    new_client_socket.settimeout(server_timeout)
    packet_received = 0
    while packet_received < num_a:
        message_b, address_b = new_client_socket.recvfrom(buffer_len)
        ack_bool = random.randint(0, 1)
        if ack_bool:
            continue

        if not header_is_verified(message_b, len_a + 4, secret_a, client_digit):
            print("incorrect header from client")
            return

        if not len(message_b) == (len_a + 4 + header_len + 3) // 4 * 4:
            print("packet length should be len + 4")
            return

        packet_id = int.from_bytes(message_b[header_len:header_len+4], 'big')

        if packet_id != packet_received:
            print("packet_id != packet_received")
            continue

        acked_packet_id = packet_id.to_bytes(4, 'big')
        for i in range(header_len + 4, len(message_b)):
            if not message_b[i] == 0:
                print("the rest of the packet from client is not 0 in step b1")
                return
        new_client_socket.sendto(create(acked_packet_id, secret_a, 1, client_digit), client_address)
        packet_received += 1
    tcp_port = random.randint(49152, 65535)
    secret_b = random.randint(1000, 2000)
    payload_b = tcp_port.to_bytes(4, 'big') + secret_b.to_bytes(4, 'big')
    new_client_socket.sendto(create(payload_b, secret_a, 2, client_digit), client_address)

    # part c
    new_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_client_socket.bind((ip, tcp_port))
    new_client_socket.listen(5)
    connection, address_c = new_client_socket.accept()
    num2 = random.randint(1, 20)
    len2 = random.randint(1, 20)
    secret_c = random.randint(2000, 3000)
    c = chr(random.randint(1, 128))
    payload_c = num2.to_bytes(4, 'big') + len2.to_bytes(4, 'big') + secret_c.to_bytes(4, 'big') + c.encode('utf-8')
    connection.sendto(create(payload_c, secret_b, 2, client_digit), address_c)

    # part d
    length_received = 0
    new_client_socket.settimeout(server_timeout)
    packet_length = (len2 + header_len + 3) // 4 * 4
    while length_received < packet_length * num2:
        message_d = connection.recv(1024)
        length_received += len(message_d)
        while len(message_d) > 0:
            if not header_is_verified(message_d, len2, secret_c, client_digit):
                print("incorrect header in stage d")
                return
            for i in range(header_len, header_len + len2):
                if c != chr(message_d[i]):
                    print("sent incorrect special character")
                    return
            message_d = message_d[(header_len + len2 + 3) // 4 * 4:]

    secret_d = random.randint(3000, 4000)
    connection.send(create(secret_d.to_bytes(4, 'big'), secret_c, 2, client_digit))


if len(sys.argv) != 4:
    print('Wrong number of argument')
step_num_client = 1
header_len = 12
if sys.argv[1] == 0:
    ip = socket.gethostbyname(sys.argv[2])
else:
    ip = sys.argv[2]
port = int(sys.argv[3])
buffer_len = 1024
server_timeout = 3
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((ip, port))
while True:
    message, address = server.recvfrom(buffer_len)
    _thread.start_new_thread(new_client, (message, address))

