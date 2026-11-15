import re

# KATEGORI PRODUK CRSL

KATEGORI = {
    "baju": {
        "nama": "👕 Baju",
        "kata_kunci": [
            "tees",
            "tee",
            "t-shirt",
            "shirt",
            "kaos",
            "kemeja",
            "jacket",
            "jaket",
            "cardigan",
            "sweatshirt",
            "hoodie",
            "sweater",
            "vest",
            "rompi",
            "blouse",
            "crop top",
            "jersey",
            "polo",
            "top",
            "atasan",
            "long sleeve",
            "short sleeve",
            "skirt",
            "skort"
        ]
    },

    "tas": {
        "nama": "🎒 Tas",
        "kata_kunci": [
            "backpack",
            "back pack",
            "rucksack",
            "slingbag",
            "sling bag",
            "sling baggu",
            "totebag",
            "tote bag",
            "waistbag",
            "waist bag",
            "hip pack",
            "pouch",
            "shoulder bag",
            "crossbody",
            "hand bag",
            "mini bag",
            "baggu",
            "bag"
        ]
    },

    "celana": {
        "nama": "👖 Celana",
        "kata_kunci": [
            "short pants",
            "long pants",
            "pants",
            "jorts",
            "trousers",
            "jeans",
            "shorts",
            "celana"
        ]
    },

    "sepatu": {
        "nama": "👟 Sepatu & Sandal",
        "kata_kunci": [
            "sneakers",
            "shoes",
            "sandals",
            "sandal",
            "loafers",
            "boots",
            "derby",
            "clogs",
            "mary jane",
            "flat shoes"
        ]
    },

    "aksesori": {
        "nama": "🧢 Aksesori",
        "kata_kunci": [
            "tumbler",
            "tumblr",
            "bottle",
            "botol",
            "straw",
            "lid",
            "cap",
            "hat",
            "topi",
            "wallet",
            "dompet",
            "card holder",
            "keychain",
            "key chain",
            "gantungan kunci",
            "bandana",
            "watch",
            "jam tangan",
            "pin",
            "charm",
            "accessories",
            "aksesoris",
            "shoes charm",
            "bag charm"
        ]
    }
}


# KATEGORISASI PRODUK

def cocok_kata(nama, kata):
    pola = r"(?<![a-z0-9])" + re.escape(kata.lower()) + r"(?![a-z0-9])"
    return re.search(pola, nama.lower()) is not None


def kategorikan_produk(nama):
    nama = nama.lower()

    # Prioritas aksesori
    # Agar produk tumbler tidak dianggap sepatu
    for kata in KATEGORI["aksesori"]["kata_kunci"]:
        if cocok_kata(nama, kata):
            return "aksesori"

    # Tas
    for kata in KATEGORI["tas"]["kata_kunci"]:
        if cocok_kata(nama, kata):
            return "tas"

    # Sepatu dan sandal
    for kata in KATEGORI["sepatu"]["kata_kunci"]:
        if cocok_kata(nama, kata):
            return "sepatu"

    # Celana
    for kata in KATEGORI["celana"]["kata_kunci"]:
        if cocok_kata(nama, kata):
            return "celana"

    # Baju
    for kata in KATEGORI["baju"]["kata_kunci"]:
        if cocok_kata(nama, kata):
            return "baju"

    return "lainnya"


# TEST KATEGORI

if __name__ == "__main__":

    import sqlite3

    conn = sqlite3.connect("database/crsl.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nama
        FROM produk
        ORDER BY nama
    """)

    produk = cursor.fetchall()
    conn.close()

    jumlah_kategori = {
        kode: 0 for kode in KATEGORI
    }

    jumlah_kategori["lainnya"] = 0

    print("\n========== HASIL KATEGORISASI CRSL ==========\n")

    for item in produk:
        nama = item[0]
        kategori = kategorikan_produk(nama)

        jumlah_kategori[kategori] += 1

        print(f"{nama} --> {kategori.upper()}")

    print("\n========== TOTAL PER KATEGORI ==========\n")

    for kode, jumlah in jumlah_kategori.items():
        nama = KATEGORI[kode]["nama"] if kode in KATEGORI else "📦 Lainnya"
        print(f"{nama}: {jumlah} produk")

    print(f"\nTOTAL PRODUK: {len(produk)}")