import socket
import json
from shared.encryption import encrypt_message
from datetime import datetime
from server.account_handler import user_exists, user_authentification, register_user

# Connect to the server
HOST = '127.0.0.1'  # Server IP
PORT = 65432        # Server Port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Function to create and send messages
def send_message(sender, receiver, message_text):
    # Create message structure
    message = {
        "from": sender,  #username
        "to": receiver,
        "message": message_text,  #message
        "timestamp": datetime.now().isoformat() #time of sending
    }

    # Convert the message to JSON and encode
    message_json = json.dumps(message)

    # Encrypt the message
    encrypted_msg = encrypt_message(message_json)

    # Send the encrypted message
    client_socket.send(encrypted_msg)

def send_credentials(username, password, client_socket):
    credentials = {
        "username": username,
        "password": password
    }
    encrypted_credentials = encrypt_message(json.dumps(credentials))
    client_socket.send(encrypted_credentials)    

# Main authentication flow
username = input("Introduce tu username: ")
password = input("Introduce tu contraseña: ")

if user_exists(username):
    if user_authentification(username, password):
        print("Inicio de sesión exitoso, conectando al servidor...")
    else:
        print("Contraseña incorrecta. Terminando.")
        client_socket.close()
        exit()
else:
    user_id = register_user(username, password)
    if user_id:
        print("Usuario nuevo registrado y conectado al servidor...")
    else:
        print("No se pudo registrar usuario. Terminando.")
        client_socket.close()
        exit()

# Send credentials to server after successful local check
send_credentials(username, password, client_socket)
