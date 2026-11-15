# CRSL Monitor
Aplikasi web pemantauan produk CRSL Store berbasis Python yang digunakan untuk mengambil, menyimpan, dan memantau informasi produk serta perubahan harga secara otomatis. Sistem ini dilengkapi dengan Dashboard Flask dan Telegram Bot untuk memudahkan pengguna dalam melihat informasi produk dan menerima notifikasi.

## Fitur Utama
- **Web Scraping:** Mengambil data produk dari API CRSL Store, meliputi nama produk, harga, gambar, dan link produk.
- **Database SQLite:** Menyimpan data produk serta riwayat perubahan harga.
- **Kategori Produk:** Mengelompokkan produk secara otomatis ke dalam kategori baju, tas, celana, sepatu, aksesori, dan lainnya.
- **Dashboard Flask:** Menampilkan daftar produk, informasi harga, pencarian, dan filter berdasarkan kategori.
- **Telegram Bot:** Memudahkan pengguna melihat daftar produk dan informasi harga melalui perintah Telegram.
- **Notifikasi Otomatis:** Mengirim pemberitahuan melalui Telegram ketika ditemukan produk baru atau perubahan harga.
- **Scheduler:** Menjalankan proses scraping secara otomatis setiap hari pukul 09.00 serta melakukan scraping langsung ketika scheduler pertama kali diaktifkan.

## Struktur Folder
```text
CRSL-Monitor/
│
├── database/
│   └── database.py
│
├── templates/
│   └── index.html
│
├── app.py
├── bot.py
├── scraper.py
├── scheduler.py
├── kategori.py
├── requirements.txt
├── .env
├── .gitignore
└── jalankan_crsl.bat
```

## ⚙️ Cara Instalasi dan Menjalankan
### 1. Clone Repository

```bash
git clone https://github.com/USERNAME/CRSL-Monitor.git
```

Masuk ke folder proyek:

```bash
cd CRSL-Monitor
```

### 2. Membuat Virtual Environment
```bash
python -m venv venv
```

Aktifkan virtual environment di Windows:

```powershell
venv\Scripts\activate
```

### 3. Instalasi Dependencies
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment
Buat file `.env` di folder utama proyek, kemudian isi dengan konfigurasi berikut:

```env
TELEGRAM_TOKEN=TOKEN_BOT_KAMU
TELEGRAM_CHAT_ID=ID_TELEGRAM_KAMU
```

Ganti nilai tersebut dengan token bot dan ID Telegram milik masing-masing pengguna.

**Catatan:** Jangan membagikan token Telegram atau mengunggah file `.env` ke repository publik.

### 5. Menjalankan Aplikasi
CRSL Monitor memiliki tiga komponen utama yang dapat dijalankan melalui terminal terpisah.

**Menjalankan Telegram Bot:**

```bash
python bot.py
```

**Menjalankan Dashboard Flask:**

```bash
python app.py
```

Dashboard dapat diakses melalui browser:

```text
http://127.0.0.1:5000
```

**Menjalankan Scheduler dan Scraper:**

```bash
python scheduler.py
```

Scheduler akan melakukan scraping langsung ketika pertama kali dijalankan, kemudian menjalankan scraping otomatis setiap hari pukul 09.00.

## Perintah Telegram Bot
| Perintah | Fungsi |
|---|---|
| `/start` | Memulai Telegram Bot |
| `/id` | Menampilkan ID Telegram |
| `/produk` | Menampilkan daftar produk berdasarkan kategori |
| `/harga` | Menampilkan informasi harga produk berdasarkan kategori |

## Sistem Notifikasi
CRSL Monitor memiliki dua jenis notifikasi otomatis:

1. **Notifikasi Produk Baru:** Dikirim ketika sistem menemukan produk yang belum tersimpan di database.
2. **Notifikasi Perubahan Harga:** Dikirim ketika sistem mendeteksi perubahan harga produk, baik kenaikan maupun penurunan harga.

Setiap notifikasi berisi informasi nama produk, harga, dan link produk agar pengguna dapat mengetahui perubahan yang terjadi.

## Alur Kerja Sistem
1. Scraper mengambil data produk dari API CRSL Store.
2. Data produk diproses dan dikelompokkan berdasarkan kategori.
3. Sistem membandingkan data terbaru dengan data yang tersimpan di database SQLite.
4. Jika ditemukan produk baru atau perubahan harga, sistem mencatat perubahan tersebut.
5. Telegram Bot mengirimkan notifikasi kepada pengguna.
6. Dashboard Flask menampilkan informasi produk yang telah tersimpan.
7. Scheduler mengatur proses scraping agar berjalan secara otomatis setiap hari pukul 09.00.

## Pengujian Sistem
Pengujian dilakukan untuk memastikan setiap fitur berjalan sesuai fungsinya, meliputi:

- Pengambilan data produk dari API CRSL Store.
- Penyimpanan data produk ke database SQLite.
- Pengelompokan produk berdasarkan kategori.
- Penampilan data pada Dashboard Flask.
- Penggunaan perintah Telegram Bot.
- Deteksi produk baru.
- Deteksi kenaikan dan penurunan harga.
- Pengiriman notifikasi Telegram.
- Penjadwalan scraping otomatis.

Hasil pengujian menunjukkan bahwa fitur-fitur utama CRSL Monitor berhasil dijalankan.

## Catatan Penggunaan
- Scheduler harus tetap berjalan agar scraping otomatis dapat dilakukan sesuai jadwal.
- Laptop atau komputer harus menyala dan terhubung ke internet.
- Telegram Bot harus aktif agar dapat menerima perintah pengguna.
- Dashboard Flask harus aktif agar website dapat diakses.
- Jika seluruh program ingin dijalankan sekaligus di Windows, pengguna dapat menjalankan file `jalankan_crsl.bat`.

---

**CRSL Monitor**  
Project Praktik Scripting Language  
Developed using Python.
