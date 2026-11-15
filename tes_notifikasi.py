from bot import kirim_notifikasi

# Simulasi produk baru
daftar_perubahan = [
    {
        "jenis": "produk_baru",
        "nama": "TEST NOTIFIKASI CRSL",
        "harga": "Rp 150.000",
        "link": "https://www.crsl-store.id"
    }
]

# Mengirim notifikasi ke Telegram
kirim_notifikasi(daftar_perubahan)
print("Pengujian notifikasi selesai!")