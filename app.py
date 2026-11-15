from flask import Flask, render_template, request
import sqlite3
import os

from kategori import KATEGORI, kategorikan_produk

app = Flask(__name__)

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "database",
    "crsl.db"
)


def ambil_produk():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM produk
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return data


def jumlah_produk():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM produk")

    jumlah = cursor.fetchone()[0]
    conn.close()

    return jumlah


@app.route("/")
def dashboard():
    produk = ambil_produk()
    total_produk = jumlah_produk()

    # Mengambil kategori dari URL
    kategori_aktif = request.args.get("kategori", "semua")

    # Filter produk berdasarkan kategori
    if kategori_aktif != "semua":
        produk = [
            item for item in produk
            if kategorikan_produk(item["nama"]) == kategori_aktif
        ]

    return render_template(
        "index.html",
        produk=produk,
        total_produk=total_produk,
        kategori=KATEGORI,
        kategori_aktif=kategori_aktif
    )


if __name__ == "__main__":
    app.run(debug=True)