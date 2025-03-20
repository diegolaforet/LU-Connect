import sqlite3

DB_FILE = "server/database/lu_connect.db"  

def reset_database():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    
    #Delete all exisiting rows
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS chats")
    cur.execute("DROP TABLE IF EXISTS messages")
    cur.execute("DROP TABLE IF EXISTS files")
    
    con.commit()
    con.close()
    
    print("Database reset successfully.")

if __name__ == "__main__":
    reset_database()
