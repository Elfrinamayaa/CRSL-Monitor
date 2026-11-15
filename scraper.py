import requests
import re
from database.database import buat_tabel, simpan_produk
from bot import kirim_notifikasi

# API CRSL Store
API_URL = "https://api.plugo.world/v1/shop/5162/products"
BASE_URL = "https://www.crsl-store.id/products"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.crsl-store.id/"
}


# Mengubah nama produk menjadi slug URL
def buat_slug(nama):
    slug = nama.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


# Mengambil harga produk
def ambil_harga(item):
    produk = item.get("product", {})
    variasi = produk.get("productVariations", [])

    daftar_harga = []

    if variasi:
        for varian in variasi:
            harga = varian.get("price")

            if isinstance(harga, (int, float)):
                daftar_harga.append(harga)

    if daftar_harga:
        harga = min(daftar_harga)
    else:
        harga = produk.get("price")

    if harga is None:
        return None

    if isinstance(harga, (int, float)):
        return "Rp {:,.0f}".format(harga).replace(",", ".")

    return str(harga)


# Mengambil gambar produk
def ambil_gambar(produk):
    gambar = produk.get("images", [])

    if gambar:
        return gambar[0].get("url")

    return None


# Fungsi utama scraping
def ambil_produk():

    try:
        print("\n================================")
        print("MENGHUBUNGKAN KE API CRSL STORE")
        print("================================")

        session = requests.Session()
        session.headers.update(headers)

        daftar_produk = []

        limit = 12
        offset = 0
        total_produk = None

        while True:

            params = {
                "search": "",
                "available": "false",
                "sort": "sold_out,-id",
                "limit": limit,
                "offset": offset,
                "includeBundles": "true",
                "lang": "en"
            }

            print(f"\nMengambil produk dari offset {offset}...")

            response = session.get(
                API_URL,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            hasil = response.json()
            data_produk = hasil.get("data", [])

            if total_produk is None:
                total_produk = hasil.get("total", 0)
                print("Total produk tersedia:", total_produk)

            if not data_produk:
                break

            for item in data_produk:

                produk = item.get("product", {})
                nama = produk.get("name")

                if not nama:
                    continue

                id_produk = produk.get("id")

                # Mengambil harga
                harga = ambil_harga(item)

                # Mengambil gambar
                gambar = ambil_gambar(produk)

                # Membuat link produk
                slug = buat_slug(nama)

                link = (
                    f"{BASE_URL}/{id_produk}/{slug}"
                    if id_produk else None
                )

                data = {
                    "nama": nama,
                    "harga": harga,
                    "gambar": gambar,
                    "link": link
                }

                daftar_produk.append(data)

            print(
                "Berhasil mengambil:",
                len(data_produk),
                "produk"
            )

            offset += limit

            if offset >= total_produk:
                break

        session.close()

        # Menampilkan ringkasan hasil scraping
        jumlah_harga = sum(
            1 for produk in daftar_produk
            if produk["harga"] is not None
        )

        print("\n================================")
        print("HASIL SCRAPING CRSL STORE")
        print("================================")
        print("Total produk :", len(daftar_produk))
        print("Harga ditemukan :", jumlah_harga)
        print("Harga kosong :", len(daftar_produk) - jumlah_harga)

        print("\nContoh hasil produk:")

        for produk in daftar_produk[:5]:
            print("\nNama  :", produk["nama"])
            print("Harga :", produk["harga"])

        # Membuat tabel database
        buat_tabel()

        # Menyimpan produk dan mendeteksi perubahan
        daftar_perubahan = simpan_produk(daftar_produk)

        # Mengirim notifikasi Telegram
        print("\nMEMERIKSA PERUBAHAN PRODUK...")

        if daftar_perubahan:
            print("Ditemukan perubahan:", len(daftar_perubahan))
            kirim_notifikasi(daftar_perubahan)
        else:
            print("Tidak ada produk baru atau perubahan harga.")

        print("\nSCRAPING SELESAI!")

        return daftar_produk

    except requests.exceptions.RequestException as e:
        print("\nGagal mengakses API CRSL Store:", e)
        return []

    except (ValueError, KeyError, TypeError) as e:
        print("\nTerjadi kesalahan saat membaca data:", e)
        return []


# Program utama
if __name__ == "__main__":
    ambil_produk()