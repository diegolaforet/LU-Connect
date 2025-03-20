import socket
import json
import os
from threading import Thread
from shared.encryption import encrypt_message, decrypt_message, encrypt_file, decrypt_file
from datetime import datetime
from server.account_handler import user_exists, user_authentification, register_user

# Connect to the server
HOST = '127.0.0.1'  # Server IP
PORT = 65432        # Server Port

ALLOWED_FILE_TYPES = {"docx", "pdf", "jpeg"}
OUTPUT_FOLDER = "received_files/"
os.makedirs(OUTPUT_FOLDER, exist_ok=True) #Create folder if it doesnt exist

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

def send_file(sender, receiver, file_path):
    if not os.path.exists(file_path):
        print("[ERROR] Archivo no encontrado.")
        return
    
    file_extension = file_path.split(".")[-1].lower()
    if file_extension not in ALLOWED_FILE_TYPES:
        print(f"[ERROR] Tipo de archivo {file_extension} no permitido.")
        return
    
    encrypted_file_data = encrypt_file(file_path)
    filename = os.path.basename(file_path)
    
    file_message = {
        "from": sender,
        "to": receiver,
        "type": "file",
        "filename": filename,
        "filedata": encrypted_file_data
    }
    
    encrypted_msg = encrypt_message(json.dumps(file_message))
    client_socket.send(encrypted_msg)
    print(f"[INFO] Archivo {filename} enviado a {receiver}.")

def listen_for_messages(client_socket):

    #Listen for upcoming messages 
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print("[INFO] Conexion closed by server")
                break

            decrypted_message = decrypt_message(encrypted_message)
            try:
                message_data = json.loads(decrypted_message)

                if "type" in message_data and message_data["type"] == "file":
                    filename = message_data['filename']
                    filedata = message_data['filedata']
                    output_path = os.path.join(OUTPUT_FOLDER, filename)
                    decrypt_file(filedata, output_path)
                    print(f"\n[INFO] Archivo recibido de {message_data['from']}: {filename}, guardado en {output_path}")
                else:
                    sender = message_data.get("from")
                    message_text = message_data.get("message")
                    timestamp = message_data.get("timestamp")
                    if sender and message_text:
                        print(f"\n[{timestamp}] Nuevo mensaje de {sender}: {message_text}")

            #Ignore not JSON messages
            except json.SDONDecodeError:
                pass

        except Exception as e:
            print(f"[ERROR] Error al recibir mensaje: {e}")
            break               

# Main authentication flow
while True:
    username = input("Write your username: ").strip()
    if not username:
        print("username needs at least one character")
        continue  #Asks for username again
    else:
        break #Only break loop if credentials not empty

if user_exists(username):
    while True:
        password = input("Write your password: ").strip()
        if not password:
            print("Password needs at least one character")
            continue  #Only break loop if password not empty
        
        if user_authentification(username, password):
            print("Inicio de sesión exitoso, conectando al servidor...")
            break  #Break loop if authentification is succesfull
        else:
            print("Incorrect passwords")

#If user does not exist in database
else:
    while True:
        password = input("Create a password to registrate: ").strip()
        if not password:
            print("Password needs at least one character")
            continue
        else:
            break

    user_id = register_user(username, password)
    if user_id:
        print("New user registered, connecting to server...")
    else:
        print("Error creating account, finish program")
        client_socket.close()
        exit()

# Send credentials to server after successful local check
send_credentials(username, password, client_socket)

response_encrypted = client_socket.recv(1024)
response = json.loads(decrypt_message(response_encrypted))

if response["status"] == "queue":
    print(f"You are in the queue. Your position: {response['position']}, estimated waiting time: {response['estimated_wait']} seconds.")

    #Wait for server confirmation of free semaphore
    response = json.loads(decrypt_message(client_socket.recv(1024)))

if response.get("status") == "accepted":
    print("¡Ahora puede comenzar a enviar mensajes!")

#Thread to listen to upcoming messages
listen_thread = Thread(target=listen_for_messages, args=(client_socket,))
listen_thread.start()

while True:
    action = input("\nSelecta action to do (message/file/exit): ").strip().lower()
    if action == "message":
        receiver = input("Send message to (username): ")
        message_text = input("Message: ")
        send_message(username, receiver, message_text)
    elif action == "file":
        receiver = input("Send file to (username): ")
        file_path = input("Path of file: ")
        send_file(username, receiver, file_path)
    elif action == "exit":
        print("Closing ocnnection...")
        client_socket.close()
        break
    else:
        print("Not valid option")
