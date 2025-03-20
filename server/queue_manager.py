from queue import Queue 
import time #Needed to calculate waiting times
import json
from shared.encryption import encrypt_message

#Class to manage the client queue
class QueueManager:
    def __init__(self):
        self.queue = Queue() #Create empty queue
        self.total_clients_served = 0 #Clients attended needed to calculate average waiting time 
        self.total_waiting_time = 0  # Needed to average waiting time

    # Add a new client to the queue
    def add_client(self, client_socket, addr):
        position = self.queue.qsize() + 1
        entry_time = time.time() 

        self.queue.put((client_socket, addr, entry_time)) #Save on queue the client socket, the IP address and entry time 

        estimated_wait = self.estimate_wait_time(position - 1) #Save waiting time

        message = {
            "status": "queue",
            "position": position,
            "estimated_wait": estimated_wait
        }

        encrypted_msg = encrypt_message(json.dumps(message))
        client_socket.send(encrypted_msg)  #Send client that he is in the queue and estimated waiting time

        print(f"Client {addr} added to queue. Position: {position}. Estimated wait time: {estimated_wait:.2f} seconds.")       


    # Remove client from queue 
    def remove_client(self):
        if not self.queue.empty(): #Check if there are clients in the queue
            client_socket, addr, entry_time = self.queue.get() #Take first client in queue

            #Take wait time and update wait time vaiables to calculate avergae wait time
            wait_time = time.time() - entry_time
            self.total_clients_served += 1
            self.total_waiting_time += wait_time

            print(f"Client {addr} removed from queue after waiting {wait_time:.2f} seconds.")
            return client_socket, addr
        
        #No clients waiting in queue
        else:
            print("Queue is empty.")
            return None, None

    # Calculate estimated wait time based on queue position
    def estimate_wait_time(self, client_position):
        if self.queue.empty():
            return 0  #If queue empty no calculation

        current_time = time.time()

        #Take entry time of client
        first_entry_time = self.queue.queue[0][2]

        #Put first client base waiting time 60 sec
        estimated_base_time = (self.total_waiting_time / self.total_clients_served) if self.total_clients_served > 0 else 60

        estimated_wait = estimated_base_time * client_position

        #Calculate waiting time 
        real_wait_time = max(estimated_wait - (current_time - first_entry_time), 0)

        return round(real_wait_time, 2)
