from cryptography.fernet import Fernet #Encrypt messages and files 
import bcrypt #Bash passwords
import os #Needed to create file to store the key
import base64 #Needed to encrypt files

KEY_FILE = "shared/encryption.key" #Same key for all users, one unique key saved on local file

#Funciton to generate new key and store it
def generate_key(): 
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file: #write key in the key file
        key_file.write(key)

#Generate key if doesnt exist or load existing key
def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file: #Open key file in read mode
        return key_file.read()   

#Encrypt message(string) into encrypted bytes
def encrypt_message(message):
    key = load_key() #Load key to encrypt
    cipher = Fernet(key) #Create object to encrypt using key
    return cipher.encrypt(message.encode())

#Decrypt form encrypted bytes to string message
def decrypt_message(encrypted_message):
    key = load_key()
    cipher  = Fernet(key) #Create objet to decrypt using key
    return cipher.decrypt(encrypted_message).decode() 

def encrypt_file(file_path):
    
    key = load_key()
    cipher = Fernet(key)

    with open(file_path, 'rb') as file:
        file_data = file.read()
        encrypted_data = cipher.encrypt(file_data)
    
    return base64.b64encode(encrypted_data).decode()

def decrypt_file(encrypted_data_b64, output_path):
    
    key = load_key()
    cipher = Fernet(key)

    encrypted_data = base64.b64decode(encrypted_data_b64)
    decrypted_data = cipher.decrypt(encrypted_data)
    
    with open(output_path, "wb") as file:
        file.write(decrypted_data)
    
    print(f"File saved on {output_path}")    

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode() 


