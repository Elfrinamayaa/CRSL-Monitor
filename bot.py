import os
import sqlite3
import requests

from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from kategori import KATEGORI, kategorikan_produk


# MEMUAT KONFIGURASI
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "database",
    "crsl.db"
)


# MENGAMBIL DATA PRODUK
def ambil_data_produk():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nama, harga, link
        FROM produk
        ORDER BY nama
    """)

    data = cursor.fetchall()
    conn.close()

    return data


# MEMBUAT TOMBOL KATEGORI
def buat_tombol_kategori(mode):
    keyboard = []

    daftar_kategori = list(KATEGORI.items())
    daftar_kategori.append(
        ("lainnya", {"nama": "📦 Lainnya"})
    )

    for kode, kategori in daftar_kategori:
        keyboard.append([
            InlineKeyboardButton(
                kategori["nama"],
                callback_data=f"{mode}|{kode}"
            )
        ])

    return InlineKeyboardMarkup(keyboard)


# PERINTAH START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = (
        "🛍️ SELAMAT DATANG DI CRSL MONITOR!\n\n"
        "Bot pemantau produk CRSL Store.\n\n"
        "Gunakan perintah berikut:\n"
        "/produk - Melihat produk berdasarkan kategori\n"
        "/harga - Melihat harga berdasarkan kategori\n"
        "/id - Melihat ID Telegram kamu\n\n"
        "🔔 Bot juga dapat mengirim notifikasi "
        "produk baru dan perubahan harga."
    )

    await update.message.reply_text(pesan)


# MELIHAT ID TELEGRAM
async def id_telegram(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id

    await update.message.reply_text(
        f"🆔 ID Telegram kamu:\n\n"
        f"`{chat_id}`\n\n"
        f"Salin ID tersebut ke file .env.",
        parse_mode="Markdown"
    )


# PERINTAH PRODUK
async def produk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = buat_tombol_kategori("produk")

    await update.message.reply_text(
        "🛍️ DAFTAR PRODUK CRSL STORE\n\n"
        "Silakan pilih kategori produk:",
        reply_markup=keyboard
    )


# PERINTAH HARGA
async def harga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = buat_tombol_kategori("harga")

    await update.message.reply_text(
        "💰 DAFTAR HARGA PRODUK CRSL STORE\n\n"
        "Silakan pilih kategori produk:",
        reply_markup=keyboard
    )


# MEMILIH KATEGORI
async def pilih_kategori(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    mode, kode_kategori = query.data.split("|")

    data = ambil_data_produk()

    produk_terpilih = [
        item for item in data
        if kategorikan_produk(item[0]) == kode_kategori
    ]

    nama_kategori = (
        KATEGORI[kode_kategori]["nama"]
        if kode_kategori in KATEGORI
        else "📦 Lainnya"
    )

    if not produk_terpilih:
        await query.message.reply_text(
            f"Belum ada produk dalam kategori {nama_kategori}."
        )
        return

    if mode == "produk":
        pesan = f"🛍️ PRODUK KATEGORI {nama_kategori.upper()}\n\n"
    else:
        pesan = f"💰 HARGA KATEGORI {nama_kategori.upper()}\n\n"

    for nomor, item in enumerate(produk_terpilih, start=1):
        nama, harga_produk, link = item

        if mode == "produk":
            pesan += (
                f"{nomor}. {nama}\n"
                f"💰 Harga: {harga_produk}\n"
                f"🔗 {link}\n\n"
            )
        else:
            pesan += (
                f"{nomor}. {nama}\n"
                f"💰 Harga: {harga_produk}\n\n"
            )

    batas = 3500

    for i in range(0, len(pesan), batas):
        await query.message.reply_text(
            pesan[i:i + batas]
        )


# FORMAT NOTIFIKASI PRODUK BARU DAN PERUBAHAN HARGA
def buat_pesan_notifikasi(perubahan):
    jenis = perubahan["jenis"]

    if jenis == "produk_baru":

        nama = perubahan["nama"]
        harga_produk = perubahan["harga"]
        link = perubahan["link"]

        kategori = kategorikan_produk(nama)

        nama_kategori = (
            KATEGORI[kategori]["nama"]
            if kategori in KATEGORI
            else "📦 Lainnya"
        )

        pesan = (
            "🆕 PRODUK BARU CRSL!\n\n"
            f"📦 Nama: {nama}\n"
            f"💰 Harga: {harga_produk}\n"
            f"🏷️ Kategori: {nama_kategori}\n\n"
            f"🔗 {link}"
        )

    elif jenis == "harga_berubah":

        nama = perubahan["nama"]
        harga_lama = perubahan["harga_lama"]
        harga_baru = perubahan["harga_baru"]
        link = perubahan["link"]

        # Mengambil angka dari format harga
        angka_lama = int(
            harga_lama.replace("Rp", "").replace(".", "").replace(",", "").strip()
        )

        angka_baru = int(
            harga_baru.replace("Rp", "").replace(".", "").replace(",", "").strip()
        )

        selisih = abs(angka_baru - angka_lama)
        selisih_format = "Rp {:,.0f}".format(selisih).replace(",", ".")

        if angka_baru < angka_lama:
            judul = "🔻 HARGA PRODUK TURUN!"
        else:
            judul = "🔺 HARGA PRODUK NAIK!"

        pesan = (
            f"{judul}\n\n"
            f"📦 Produk: {nama}\n"
            f"💰 Harga sebelumnya: {harga_lama}\n"
            f"💰 Harga terbaru: {harga_baru}\n"
            f"📊 Selisih: {selisih_format}\n\n"
            f"🔗 {link}"
        )

    else:
        return None

    return pesan


# MENGIRIM NOTIFIKASI KE TELEGRAM
def kirim_notifikasi(daftar_perubahan):
    if not daftar_perubahan:
        print("Tidak ada perubahan. Notifikasi tidak dikirim.")
        return

    if not TOKEN or not CHAT_ID:
        print("Token atau Chat ID Telegram belum diatur.")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    for perubahan in daftar_perubahan:

        pesan = buat_pesan_notifikasi(perubahan)

        if not pesan:
            continue

        try:
            response = requests.post(
                url,
                data={
                    "chat_id": CHAT_ID,
                    "text": pesan
                },
                timeout=20
            )

            response.raise_for_status()

            hasil = response.json()

            if hasil.get("ok"):
                print(
                    "Notifikasi berhasil dikirim:",
                    perubahan["nama"]
                )
            else:
                print("Telegram gagal mengirim notifikasi:", hasil)

        except requests.exceptions.RequestException as e:
            print("Gagal mengirim notifikasi Telegram:", e)


# MENJALANKAN BOT
def main():
    if not TOKEN:
        raise ValueError(
            "Token Telegram tidak ditemukan. Periksa file .env"
        )

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", id_telegram))
    app.add_handler(CommandHandler("produk", produk))
    app.add_handler(CommandHandler("harga", harga))

    app.add_handler(
        CallbackQueryHandler(pilih_kategori)
    )

    print("CRSL MONITOR TELEGRAM BOT BERHASIL DIJALANKAN!")

    app.run_polling()


if __name__ == "__main__":
    main()