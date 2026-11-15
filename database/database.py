import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "crsl.db")


# Membuat koneksi database
def koneksi_database():
    return sqlite3.connect(DB_PATH)


# Membuat tabel database
def buat_tabel():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            harga TEXT,
            gambar TEXT,
            link TEXT UNIQUE,
            terakhir_diperbarui DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS riwayat_harga (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT,
            harga TEXT,
            tanggal DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    print("Database berhasil dibuat!")


# Menyimpan produk sekaligus mendeteksi perubahan
def simpan_produk(daftar_produk):
    conn = koneksi_database()
    cursor = conn.cursor()

    jumlah_baru = 0
    jumlah_diperbarui = 0

    daftar_perubahan = []

    for produk in daftar_produk:

        link = produk["link"]
        harga = produk["harga"]

        cursor.execute(
            "SELECT nama, harga FROM produk WHERE link = ?",
            (link,)
        )

        data_lama = cursor.fetchone()

        # PRODUK BARU
        if data_lama is None:

            cursor.execute("""
                INSERT INTO produk
                (nama, harga, gambar, link)
                VALUES (?, ?, ?, ?)
            """, (
                produk["nama"],
                harga,
                produk["gambar"],
                link
            ))

            cursor.execute("""
                INSERT INTO riwayat_harga
                (link, harga)
                VALUES (?, ?)
            """, (link, harga))

            daftar_perubahan.append({
                "jenis": "produk_baru",
                "nama": produk["nama"],
                "harga": harga,
                "link": link
            })

            jumlah_baru += 1

        # PRODUK SUDAH ADA
        else:

            nama_lama, harga_lama = data_lama

            if harga_lama != harga:

                cursor.execute("""
                    INSERT INTO riwayat_harga
                    (link, harga)
                    VALUES (?, ?)
                """, (link, harga))

                daftar_perubahan.append({
                    "jenis": "harga_berubah",
                    "nama": produk["nama"],
                    "harga_lama": harga_lama,
                    "harga_baru": harga,
                    "link": link
                })

                jumlah_diperbarui += 1

            cursor.execute("""
                UPDATE produk
                SET nama = ?,
                    harga = ?,
                    gambar = ?,
                    terakhir_diperbarui = CURRENT_TIMESTAMP
                WHERE link = ?
            """, (
                produk["nama"],
                harga,
                produk["gambar"],
                link
            ))

    conn.commit()
    conn.close()

    print("\nDATA BERHASIL DISIMPAN")
    print("Produk baru:", jumlah_baru)
    print("Perubahan harga:", jumlah_diperbarui)

    return daftar_perubahan


# Melihat data produk
def lihat_produk():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produk")
    data = cursor.fetchall()

    print("\nDAFTAR PRODUK DALAM DATABASE\n")

    for produk in data:
        print("ID     :", produk[0])
        print("Nama   :", produk[1])
        print("Harga  :", produk[2])
        print("Gambar :", produk[3])
        print("Link   :", produk[4])
        print("-" * 40)

    print("Total produk dalam database:", len(data))

    conn.close()


# Mengecek produk tanpa harga
def cek_produk_tanpa_harga():
    conn = koneksi_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nama, harga
        FROM produk
        WHERE harga IS NULL OR harga = 'None'
    """)

    data = cursor.fetchall()

    print("\nPRODUK TANPA HARGA")

    for produk in data:
        print("Nama  :", produk[0])
        print("Harga :", produk[1])
        print("-" * 40)

    print("Total produk tanpa harga:", len(data))

    conn.close()


# Program utama
if __name__ == "__main__":
    buat_tabel()
    lihat_produk()
    cek_produk_tanpa_harga()