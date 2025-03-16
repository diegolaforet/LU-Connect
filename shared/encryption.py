from cryptography.fernet import Fernet #Encrypt messages and files 
import bcrypt #Bash passwords
import os #Needed to create file to store the key

KEY_FILE = "encryption.key" #Same key for all users, one unique key saved on local file

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

def encrypt_file():
    pass

def decrypt_file():
    pass

encr_message = encrypt_message("Hola, I want a car food")
message = decrypt_message(encr_message)
print(encr_message)
print(message)
