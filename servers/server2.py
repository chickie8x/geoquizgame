import socket
import threading
import time
import random

clients_list = []
uid_list = []


def handle_client(c_socket, addr):
    print(f"Accepted connection from {addr}")
    uid = None
    while uid not in uid_list:
        uid = random.randint(1,1000)
        uid_list.append(uid)
    client = {
        'uid': uid,
        'address': addr,
        'socket': c_socket
    } 

    clients_list.append(client)

    c_socket.send((f'you UID is: {uid}').encode())

    while True:
        data = c_socket.recv(1024)
        if not data:
            print(f"Connection from {addr} closed.")
            break

        message = data.decode()
        print(f"Received from {addr}: {message}")

        # Your server-side processing goes here

        # Echo the message back to the client
        c_socket.send(message.encode())

    c_socket.close()


def send_broadcast(addr):
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    b_address = ('127.0.0.1', 12347)
    broadcast_socket.bind(b_address)
    while True:
        message = bytes(addr, 'utf-8')
        broadcast_socket.sendto(message, ('255.255.255.255', 12349))
        time.sleep(4)

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_IP = '127.0.0.1'
server_port = 12344
server_socket.bind((server_IP, server_port))
server_socket.listen()
print(type(server_socket))

broadcast_server_addr = f"{server_IP} {server_port}" #server address is sent to clients via broadcast


print("Server is listening for connections...")
broadcast_thread = threading.Thread(target=send_broadcast, args=(broadcast_server_addr,))
broadcast_thread.start()

while True:
    client, addr = server_socket.accept()

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client, addr))
    client_thread.start()
