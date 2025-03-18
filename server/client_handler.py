from threading import Thread
from shared.encryption import decrypt_message
from server.database.database import connect_db
from server.queue_manager import QueueManager

queue_manager = QueueManager()

# Function to handle each client's connection individually
def client_handler(client_socket, addr, client_semaphore):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    try:
        while True:
            encrypted_message = client_socket.recv(1024) #Recieve data from client

            #If connection closed 
            if not encrypted_message:
                print(f"[DISCONNECTED] {addr} disconnected.")
                break

            print(f"[MESSAGE RECEIVED] Encrypted from {addr}: {encrypted_message}")

            # Here you will implement:
            # Decrypt message using decrypt_message from encryption
            # decrypted_message = decrypt_message(encrypted_message)

            # Store the encrypted message in the database
            # Retransmit the decrypted message to the intended receiver

    except ConnectionResetError:
        print(f"[ERROR] Connection reset by {addr}.")

    finally:
        client_socket.close()
        client_semaphore.release()
        print(f"[CONNECTION CLOSED] {addr} connection closed.")
