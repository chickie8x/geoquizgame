import socket
import threading
import time

clientUID = None

def discover_hosts():
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Enable broadcasting mode
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind to a specific address and port
    client_socket.bind(('0.0.0.0', 12341))

    try:
        print("Listening for broadcasts...")
        while True:
            # Receive data
            data, addr = client_socket.recvfrom(1024)
            print(f"connected to {data}")
            return data.decode()

    except:
        pass

    finally:
        client_socket.close()

[server_IP, server_port] = discover_hosts().split(' ')
server_address = (server_IP, int(server_port))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

def send_message():
    while True:
        message = input("Enter a message to send to the server (type 'exit' to close): ")
    
        if message.lower() == 'exit':
            break
        try:
            client_socket.send(message.encode())
        except:
            print('can not send mesage to server')
        time.sleep(0.2)
    client_socket.close()

send_mes_thread = threading.Thread(target=send_message)
send_mes_thread.start()

while True:
    # Receive the response from the server
    response = client_socket.recv(1024)
    print(f"Received from server: {response.decode()}")

# client_socket.close()
