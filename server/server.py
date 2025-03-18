import socket
from threading import Semaphore, Thread
from server.queue_manager import QueueManager
from server.client_handler import client_handler

HOST = '127.0.0.1'
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

#Derive client connections to client_handler
def handle_client(client_socket, addr):
    print(f"Handling client {addr}")

    client_handler(client_socket, addr, client_semaphore)

    next_client_socket, next_addr = queue_manager.remove_client() #Remove client from queue

    if next_client_socket:
        print(f"[QUEUE] Accepting next client: {next_addr}")

        #If there is a client waiting create a new thread and all again handle_client
        Thread(target=handle_client, args=(next_client_socket, next_addr)).start()

#Run start_server only when server.py is executed directly not imported
if __name__ == "__main__":
    print("[STARTING] Server is starting...")  
    start_server()
