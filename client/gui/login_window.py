import tkinter as tk
import socket
from tkinter import messagebox
from client.gui.chat_window import ChatWindow
from client.client import check_user_exists, user_authentification, register_new_user

class LoginWindow:
    def __init__(self, root):

        #Initialize login window 
        self.root = root
        self.root.title("LU-Connect - Login")
        self.root.geometry("300x200")

        # Username input field
        tk.Label(root, text="Username:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()
        
        #Button to check if the username exists
        self.next_button = tk.Button(root, text="Next", command=self.check_username)
        self.next_button.pack()

        #Label for password prompt
        self.password_label = tk.Label(root, text="")  
        self.password_label.pack()

        #Password input field
        self.password_entry = tk.Entry(root, show="*", state=tk.DISABLED)  
        self.password_entry.pack()

        #Login/Register button
        self.login_button = tk.Button(root, text="Login/Register", command=self.process_login, state=tk.DISABLED)
        self.login_button.pack()
    
    #Check if the entered username exists in database before asking for a password
    def check_username(self):
        self.username = self.username_entry.get().strip()

        #If username left empty
        if not self.username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return
        
        self.user_exists = check_user_exists(self.username)  

        #Update UI based on whether the username exists or not
        if self.user_exists:
            self.password_label.config(text="Password to log in:")
        else:
            self.password_label.config(text="Password to register:")
        
        self.password_entry.config(state=tk.NORMAL)
        self.login_button.config(state=tk.NORMAL)

    #Authentication for existing users and registration for new users
    def process_login(self):
        password = self.password_entry.get().strip()

        #If password empty
        if not password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return

        #Authentication for existing users
        if self.user_exists:
            if user_authentification(self.username, password):
                messagebox.showinfo("Success", "Login successful!")
                self.open_chat_window()
            else:
                messagebox.showerror("Error", "Incorrect password. Try again.")

        #Registration for new users
        else:
            if register_new_user(self.username, password):
                messagebox.showinfo("Success", "Registration successful! You can now log in.")
                self.open_chat_window()
            else:
                messagebox.showerror("Error", "Registration failed. Try again.")

    #Opens the chat window after successful login/registration
    def open_chat_window(self): 
        self.root.destroy() #Close the login window

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("127.0.0.1", 65432))  # Connect to the server

            chat_root = tk.Tk()
            ChatWindow(chat_root, self.username, client_socket)
            chat_root.mainloop()
        except Exception as e:
            print(f"Error opening chat window: {e}")

#Run window
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
