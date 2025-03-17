import socket
from threading import Semaphore, Thread
from server.queue_manager import QueueManager

HOST = '127.0.01'
PORT = 65432

MAX_CLIENTS = 3 #Create constant with the number of maximum connections permitted
client_semaphore = Semaphore(MAX_CLIENTS)
queue_manager = QueueManager()


def start_server():
    #Create listening socket in server using IPv4 and TCP conneection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    #Always listening for upcoming connections (clients)
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        #Check if free spaces in semaphore
        if client_semaphore.acquire(blocking=False):
            # Client accepted if there is space in the semaphore and call handle_client
            Thread(target=handle_client, args=(client_socket, addr)).start()
        else:
            queue_manager.add_client(client_socket, addr)

def handle_client(client_socket, addr):
    print(f"Handling client {addr}")

    '''Call client handler in future'''

    client_socket.close()
    client_semaphore.release()  
