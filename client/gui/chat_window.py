import tkinter as tk
from tkinter import messagebox

class ChatWindow:
    def __init__(self, root, username, client_socket):
        #Create new window
        self.root = root
        self.root.title(f"LU-Connect - Chat ({username})")
        self.root.geometry("300x150")

        self.username = username
        self.client_socket = client_socket

        #Buttons look
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        #Send message 
        self.send_button = tk.Button(self.button_frame, text="Send Message", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=10)

        #Send file 
        self.file_button = tk.Button(self.button_frame, text="Send File", command=self.send_file)
        self.file_button.pack(side=tk.LEFT, padx=10)

        #Exit button
        self.exit_button = tk.Button(root, text="Exit", command=self.exit_chat)
        self.exit_button.pack(pady=10)

    def send_message(self):
        pass

    def send_file(self):
        pass
    
    #Close window
    def exit_chat(self):
        try:
            self.client_socket.close()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    ChatWindow(root, "TestUser", None)
    root.mainloop()