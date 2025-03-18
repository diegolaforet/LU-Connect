import socket
import time

HOST = '127.0.0.1'  # IP del servidor
PORT = 65432        # Puerto del servidor

# Crear socket de cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("[CONNECTED] Connected to server.")

# Esperar 10 segundos simulando una conexión activa
time.sleep(10)

# Desconectar el cliente
print("[DISCONNECTED] Closing connection.")
client_socket.close()
