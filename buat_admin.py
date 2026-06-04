import sqlite3

db = sqlite3.connect("database.db")

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
INSERT INTO admin(username,password)
VALUES(?,?)
""", ("admin","123456"))

db.commit()

print("Admin berjaya dicipta")