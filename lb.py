import socket
import threading
import time
from helpers import send_broadcast

nodes_list = []

#receive broadcast from servers 
def discover_hosts():
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Enable broadcasting mode
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind to a specific address and port
    client_socket.bind(('127.0.0.1', 12349))

    try:
        print("Listening for broadcasts...")
        while True:
            # Receive data
            data, addr = client_socket.recvfrom(1024)
            # print(f"receive {data}")
            if(data.decode() not in nodes_list):
                nodes_list.append(data.decode())
                print(nodes_list)
            # return data.decode()

    except:
        pass

    finally:
        pass

if __name__ == '__main__':
    discover_hosts()

