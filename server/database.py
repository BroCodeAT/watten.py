import sqlite3
import bcrypt

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("watten_py.db")
        self.c = self.conn.cursor()

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL)
        """)

    def register_user(self, email, username, password):
        self.c.execute("INSERT INTO accounts (email, username, password) VALUES (?, ?, ?)", (email, username, password))
        self.conn.commit()
    
    def verify_user(self, username:str, password:str):
        self.c.execute("SELECT password FROM accounts WHERE username = ?", (username,))
        db_entry = self.c.fetchone()
        if db_entry:
            db_password = db_entry[0]
            successful_login = bcrypt.checkpw(password.encode(), db_password)
            return successful_login
        else:
            return False


if __name__ == "__main__":
    db = Database()
    
    db.register_user("admin@admin", "admin", bcrypt.hashpw("admin".encode(), bcrypt.gensalt()))

    db.register_user("none", "Marcel", bcrypt.hashpw("toasttoast1".encode(), bcrypt.gensalt()))
    db.register_user("none", "Thomas", bcrypt.hashpw("toasttoast2".encode(), bcrypt.gensalt()))
    db.register_user("none", "Daniel", bcrypt.hashpw("toasttoast3".encode(), bcrypt.gensalt()))
    db.register_user("none", "Christoph", bcrypt.hashpw("toasttoast4".encode(), bcrypt.gensalt()))