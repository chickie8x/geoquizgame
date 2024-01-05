import time
import socket

IP = '127.0.0.1'

def send_broadcast(bind_addr, mes, broadcast_send_port):
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.bind(bind_addr)
    while True:
        message = bytes(mes, 'utf-8')
        broadcast_socket.sendto(message, ('255.255.255.255', broadcast_send_port))
        time.sleep(4)