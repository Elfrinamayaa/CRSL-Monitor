import schedule
import time
from scraper import ambil_produk


# Fungsi scraping
def tugas_scraping():
    print("\n================================")
    print("SCRAPING OTOMATIS DIMULAI")
    print("================================")
    try:
        ambil_produk()
        print("\nScraping selesai!")
    except Exception as e:
        print("\nTerjadi kesalahan saat scraping:", e)

# Scraping langsung ketika scheduler dinyalakan
print("================================")
print("CRSL MONITOR SCHEDULER AKTIF")
print("================================")

print("\nMenjalankan scraping awal...")
tugas_scraping()

# Menjadwalkan scraping setiap hari pukul 09.00
schedule.every().day.at("09:00").do(tugas_scraping)
print("\nScraping berikutnya dijadwalkan pukul 09:00.")

# Menjalankan scheduler terus-menerus
while True:
    schedule.run_pending()
    time.sleep(30)