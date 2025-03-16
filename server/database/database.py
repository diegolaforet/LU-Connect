'''File to create the tables in the database'''
import sqlite3 #Source https://docs.python.org/3/library/sqlite3.html

DB_FILE  = "server/database/lu_connect.db" #Path to database

#Create a object to connect to database
def connect_db():
    return sqlite3.connect(DB_FILE)

#Create users table with user_id, username and hashed paswword for each user
def create_users_table():
    con = connect_db() #Create connection object
    cur = con.cursor() #Create a cursor to execute SQL statements 

    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)")

    con.commit() #Save changes
    con.close() #Close connection

#Create table to store conversations between two users preventing duplicate conversations between the two same users
def create_chats_table():
    con = connect_db() #Create connection object
    cur = con.cursor() #Create a cursor to execute SQL statements 

    cur.execute("CREATE TABLE IF NOT EXISTS chats(chat_id INTEGER PRIMARY KEY, user1_id INTEGER NOT NULL, user2_id INTEGER NOT NULL, FOREIGN KEY (user1_id) REFERENCES users(user_id), FOREIGN KEY (user2_id) REFERENCES users(user_id), UNIQUE (user1_id, user2_id))")

    con.commit()
    con.close()

#Create a table for messages linked to a specific conversation in chats table
def create_messages_table():
    con = connect_db() #Create connection object
    cur = con.cursor() #Create a cursor to execute SQL statements

    cur.execute("CREATE TABLE IF NOT EXISTS messages(message_id INTEGER PRIMARY KEY, chat_id INTEGER NOT NULL, sender_id INTEGER NOT NULL, message TEXT NOT NULL, timestamp TEXT NOT NULL, FOREIGN KEY (chat_id) REFERENCES chats(chat_id), FOREIGN KEY (sender_id) REFERENCES users(user_id))")

    con.commit()
    con.close()

#Create a different table for files linked to a specific conversation in chats table
def create_files_table():
    con = connect_db() #Create connection object
    cur = con.cursor() #Create a cursor to execute SQL statements

    cur.execute("CREATE TABLE IF NOT EXISTS files(file_id INTEGER PRIMARY KEY, chat_id INTEGER NOT NULL, sender_id INTEGER NOT NULL, file_name TEXT NOT NULL, file_type TEXT CHECK(file_type IN ('docx', 'pdf', 'jpeg')) NOT NULL, file_data BLOB NOT NULL, timestamp TEXT NOT NULL, FOREIGN KEY (chat_id) REFERENCES chats(chat_id), FOREIGN KEY (sender_id) REFERENCES users(user_id))")

    con.commit()
    con.close()

#Initialize database structure
if __name__ == "__main__":
    create_users_table()
    create_chats_table()
    create_messages_table()
    create_files_table()
    print("Database structure created successfully.")