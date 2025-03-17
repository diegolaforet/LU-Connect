import socket
from threading import Semaphore, Thread

HOST = '127.0.01'
PORT = 65432

MAX_CLIENTS = 3 #Create constant with the number of maximum connections permitted
client_semaphore = Semaphore(MAX_CLIENTS)


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
            '''Send client to queue manager'''
            print(f"No space for client {addr}. Adding to queue.")
            client_socket.close()  

def handle_client():
    print(f"Handling client {addr}")

    '''Call client handler in future'''

    client_socket.close()
    client_semaphore.release()  
