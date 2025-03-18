import sqlite3 #Needed for user registration and credentials validation when log in
from server.database.database import connect_db #Import function to create connection with the database
from shared.encryption import hash_password #Import function to hash passwords from encryption.py
import bcrypt #Needed to validate hashed password

def register_user(username, password):

    con = connect_db() #Create connection object
    cur = con.cursor() #Create a cursor to execute SQL statements 

    password_hash = hash_password(password)

    #Insert new user into database, if user with same username existed raise error
    try:
        cur.execute(f"INSERT INTO users(username, password_hash) VALUES ('{username}', '{password_hash}')")
        user_id = cur.lastrowid()
        con.commit()
        print("User registered successfully!")
        return user_id #Return user id 
    except sqlite3.IntegrityError:
        print("Error: Username already exists!")
        return None
    finally:
        con.close()

#Validate user credentials in login and returns true if succesful
def user_authentification(username, password):

    con = connect_db() #Create connection object
    cur = con.cursor() #Create a cursor to execute SQL statements 
        
    cur.execute(f"SELECT password_hash FROM users WHERE username = '{username}'") #Take the stored hashed password of the given username account
    result = cur.fetchone() #Save in result for comparasion
    
    con.close()
    
    #if result is not None and the entered password hashed with the same salt from the stored password are the same, return True else false
    if result and bcrypt.checkpw(password.encode(), result[0].encode()):
        return True
    else:
        return False

#Function to get a user_id from the username
def get_user_id(username):

    con = connect_db() #Create connection object
    cur = con.cursor() #Create a cursor to execute SQL statements

    cur.execute(f"SELECT user_id FROM users WHERE username = '{username}'")
    result = cur.fetchone()
    
    con.close()
    
    return result[0] if result else None #If the user exists return the user_id else return None      
