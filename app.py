from flask import Flask, request
import pymysql

app = Flask(__name__)

def sambung_db():
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="latihan_web"
    )

@app.route('/')
def home():

    return """
    <h2>Borang Pendaftaran</h2>

    <form method="POST" action="/simpan">

        Nama:<br>
        <input type="text" name="nama" required>

        <br><br>

        Email:<br>
        <input type="email" name="email" required>

        <br><br>

        <button type="submit">
            Simpan
        </button>

    </form>

    <br>

    <a href="/senarai">Lihat Senarai Pengguna</a>
    """

@app.route('/simpan', methods=['POST'])
def simpan():

    nama = request.form['nama']
    email = request.form['email']

    db = sambung_db()

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO pengguna (nama,email) VALUES (%s,%s)",
        (nama,email)
    )

    db.commit()

    return """
    <h3>Data berjaya disimpan!</h3>

    <a href="/">Tambah Lagi</a>

    <br><br>

    <a href="/senarai">Lihat Senarai Pengguna</a>
    """

@app.route('/senarai')
@app.route('/senarai')
def senarai():

    db = sambung_db()

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM pengguna"
    )

    data = cursor.fetchall()

    html = """
    <h2>Senarai Pengguna</h2>

    <table border='1' cellpadding='8'>

    <tr>
        <th>ID</th>
        <th>Nama</th>
        <th>Email</th>
        <th>Tindakan</th>
    </tr>
    """

    for row in data:

        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>

            <td>
                <a href="/edit/{row[0]}">
                Edit
                </a>

                |

                <a href="/delete/{row[0]}"
                onclick="return confirm('Padam data ini?')">
                Delete
                </a>
            </td>
        </tr>
        """

    html += """
    </table>

    <br>

    <a href="/">Kembali</a>
    """

    return html
@app.route('/delete/<int:id>')
def delete(id):

    db = sambung_db()

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM pengguna WHERE id=%s",
        (id,)
    )

    db.commit()

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
        "SELECT * FROM pengguna WHERE id=%s",
        (id,)
    )

    row = cursor.fetchone()

    return f"""
    <h2>Edit Pengguna</h2>

    <form method="POST"
          action="/update/{id}">

        Nama:<br>

        <input
            name="nama"
            value="{row[1]}"
        >

        <br><br>

        Email:<br>

        <input
            name="email"
            value="{row[2]}"
        >

        <br><br>

        <button>
            Update
        </button>

    </form>
    """
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
        SET nama=%s,
            email=%s
        WHERE id=%s
        """,
        (nama,email,id)
    )

    db.commit()

    return """
    Data berjaya dikemaskini.

    <br><br>

    <a href="/senarai">
    Kembali ke Senarai
    </a>
    """
if __name__ == '__main__':
    app.run(debug=True)