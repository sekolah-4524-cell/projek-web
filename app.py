from flask import Flask, request, render_template, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "rahsia123"

conn = sqlite3.connect(
    "database.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pengguna(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    email TEXT
)
""")

conn.commit()
def sambung_db():
    return sqlite3.connect("database.db")
    

@app.route('/')
def home():
    return render_template(
        'index.html'
    )

@app.route('/simpan', methods=['POST'])
def simpan():

    nama = request.form['nama']
    email = request.form['email']

    db = sambung_db()

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO pengguna (nama,email) VALUES (?,?)",
        (nama,email)
    )

    db.commit()
    db.close()
    
    return """
    <h3>Data berjaya disimpan!</h3>

    <a href="/">Tambah Lagi</a>

    <br><br>

    <a href="/senarai">Lihat Senarai Pengguna</a>
    """
    

@app.route('/senarai')
def senarai():

    db = sambung_db()

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM pengguna"
    )

    data = cursor.fetchall()

    return render_template(
        'senarai.html',
        data=data
    )
    db.commit()
    db.close()
    
@app.route('/delete/<int:id>')
def delete(id):

    db = sambung_db()

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM pengguna WHERE id=?",
        (id,)
    )

    db.commit()
    db.close()
    
    return """
    Data berjaya dipadam.

    <br><br>

    <a href="/senarai">
    Kembali ke Senarai
    </a>
    """
@app.route('/edit/<int:id>')
def edit(id):

    db = sambung_db()

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM pengguna WHERE id=?",
        (id,)
    )

    row = cursor.fetchone()

    return render_template(
        'edit.html',
        row=row
    )
    db.commit()
    db.close()
    
@app.route('/update/<int:id>',
           methods=['POST'])
       
def update(id):

    nama = request.form['nama']
    email = request.form['email']

    db = sambung_db()

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE pengguna
        SET nama=?,
            email=?
        WHERE id=?
        """,
        (nama,email,id)
    )

    db.commit()
    db.close()
    
    return """
    Data berjaya dikemaskini.

    <br><br>

    <a href="/senarai">
    Kembali ke Senarai
    </a>
    """
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        db = sambung_db()
        cursor = db.cursor()

        cursor.execute(
            """
            SELECT * FROM admin
            WHERE username=?
            AND password=?
            """,
            (username, password)
        )

        user = cursor.fetchone()

        if user:
            session['login'] = True
            return redirect('/dashboard')

        return "Login gagal"

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():

    if not session.get('login'):
        return redirect('/login')

    db = sambung_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM pengguna"
    )

    jumlah = cursor.fetchone()[0]

    return f"""
    <h1>Dashboard Admin</h1>

    <h3>Jumlah Pengguna: {jumlah}</h3>

    <br>

    <a href='/senarai'>
    Senarai Pengguna
    </a>

    <br><br>

    <a href='/logout'>
    Logout
    </a>
    """
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')
if __name__ == '__main__':
    app.run(debug=True)