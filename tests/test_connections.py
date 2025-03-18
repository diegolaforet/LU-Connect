import socket
import time
import threading

HOST = '127.0.0.1'  # IP del servidor
PORT = 65432        # Puerto donde escucha el servidor

def simulate_client(client_id, wait_time=5):
    """Simula un cliente que se conecta, espera un tiempo y se desconecta."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        print(f"[CLIENT {client_id}] Connected to server.")

        # Mantener la conexión abierta por un tiempo antes de desconectar
        time.sleep(wait_time)
        
        print(f"[CLIENT {client_id}] Disconnecting.")
        client_socket.close()
    except ConnectionRefusedError:
        print(f"[CLIENT {client_id}] Connection refused. Server might be down.")

# Crear 5 clientes en paralelo
for i in range(5):
    threading.Thread(target=simulate_client, args=(i, 8)).start()

