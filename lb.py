import socket
import threading
import time
from helpers import send_broadcast, IP

nodes_list = []
leader_node = None
node_sock = None
client_list ={}
user_index =1


def lb_connect_to_leader_node():
    [node_IP, node_port] = leader_node.split(' ')
    node_addr = (node_IP, int(node_port))
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_socket.connect(node_addr)
    global node_sock
    node_sock = node_socket
    print('connecting to node....')

    while True:
        response = node_socket.recv(1024)
        print(f'replay from node :{response.decode()}')
        # if(client):
        #     client.send(bytes(response))
        


def lb_handle_client(c_socket, addr):
    print(f'accepted connection from {addr}')
    global user_index
    client_username = f'user{user_index}'
    client_list[client_username] = c_socket
    user_index += 1
    c_socket.send(bytes(f'username_set:{client_username}'.encode()))
    while True:
        mes_from_client = c_socket.recv(1024)
        if not mes_from_client:
            print(f'client connection from {addr} closed')
        print(f'mes from client: {mes_from_client.decode()}')
        forward_to_node = mes_from_client
        if node_sock:
            node_sock.send(bytes(forward_to_node))


#receive broadcast from servers 
def discover_hosts():
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Enable broadcasting mode
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind to a specific address and port
    client_socket.bind((IP, 12349))

    global leader_node

    try:
        print("Listening for broadcasts...")
        while True:
            # Receive data
            data, addr = client_socket.recvfrom(1024)
            if(data.decode() not in nodes_list):
                nodes_list.append(data.decode())
                print(f"receive {data}")
                if not leader_node:
                    leader_node = nodes_list[0]
                    lb_connect_to_leader_node_thread = threading.Thread(target=lb_connect_to_leader_node)
                    lb_connect_to_leader_node_thread.start()
                    print(nodes_list)
    except:
        pass

    finally:
        pass


if __name__ == '__main__':

    lb_IP = IP
    lb_port = 12340
    send_broadcast_port = 12341
    broadcast_mes = f'{lb_IP} {lb_port}'

    # Set up the server socket
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.bind((lb_IP, lb_port))
    lb_socket.listen()
    print('load balancer start listening....')


    #start discover hosts thread
    discover_nodes_thread = threading.Thread(target=discover_hosts)
    discover_nodes_thread.start()

    #start broadcast send thread
    send_broadcast_thread = threading.Thread(target=send_broadcast, args=(broadcast_mes, send_broadcast_port))
    send_broadcast_thread.start()

    while True:
         client, addr = lb_socket.accept()
        # Start a new thread to handle the client
         client_thread = threading.Thread(target=lb_handle_client, args=(client, addr))
         client_thread.start()
    
