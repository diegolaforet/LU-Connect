from threading import Thread
from shared.encryption import decrypt_message
import json #To handle messages

#Store encryipted messages temporarly 
encrypt_messages = {} 

#Dictionary to map sockets and users (only active)
active_clients = {}

#Obtain the user to send the message to
def get_receiver_username(decrypted_message):
    try:
        message_data = json.loads(decrypted_message)
        return message_data.get("to")
    except json.JSONDecodeError:
        return None
        
def retransmit_message(receiver_username, encrypted_message):
    receiver = active_clients.get(receiver_username)
    
    if receiver:
        receiver_socket, _ = receiver
        receiver_socket.send(encrypted_message)
        print(f"[SENT] Message sent to {receiver_username}")
    else:
        print(f"[ERROR] {receiver_username} not connected.")

def retransmit_file(receiver_username, encrypted_message):
    receiver = active_clients.get(receiver_username)
    
    if receiver:
        receiver_socket, _ = receiver
        receiver_socket.send(encrypted_message)
        print(f"[SENT] File sent to {receiver_username}")
    else:
        print(f"[ERROR] {receiver_username} not connected.")

# Diccionario para almacenar usuarios activos
def client_handler(client_socket, addr, client_semaphore):
    print(f"[NEW CONNECTION] {addr} connected.")
      
    username = None  #Initialize username 

    try:
        #Recieve credentials from client (username, password)
        encrypted_credentials = client_socket.recv(1024)
        credentials = json.loads(decrypt_message(encrypted_credentials))

        username = credentials.get("username")

        #Save client on active client diccionary
        active_clients[username] = (client_socket, addr)
        print(f"[USER CONNECTED] {username} connected successfully.")

        #Start while to always listen to upcoming messages
        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print(f"[DISCONNECTED] {username} {addr} disconnected.")
                break

            print(f"[MESSAGE RECEIVED] Encrypted from {username}: {encrypted_message}")

            decrypted_message = decrypt_message(encrypted_message)
            message_data = json.loads(decrypted_message)
            
            receiver_username = message_data.get("to")
            message_type = message_data.get("type", "message")

            if receiver_username:
                if message_type == "file":
                    retransmit_file(receiver_username, encrypted_message)
                else:
                    retransmit_message(receiver_username, encrypted_message)
            else:
                print("[ERROR] Receiver username not found in message.")

    except ConnectionResetError:
        print(f"[ERROR] Connection reset by {addr}.")
    finally:
        #Remove user from active clients when connection is closed
        if username in active_clients:
            del active_clients[username]
            print(f"[ACTIVE USERS] {username} removed from active clients.")

        client_socket.close()
        client_semaphore.release()
        print(f"[CONNECTION CLOSED] {addr} connection closed.")