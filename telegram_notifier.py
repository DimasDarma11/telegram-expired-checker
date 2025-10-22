import pandas as pd
import requests
from datetime import datetime
import os
import openpyxl

# === Konfigurasi ===
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
EXCEL_PATH = "Customer BareMetal.xlsx"
SHEET_NAME = "VPSRDP" 

# === Fungsi kirim pesan Telegram ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("⚠️ Gagal kirim pesan Telegram:", response.text)

# === Baca data Excel ===
df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
df["EXPIRED DATE"] = pd.to_datetime(df["EXPIRED DATE"], errors="coerce")

# === Cek data yang expired dalam 3 hari ===
today = datetime.now().date()
soon_expired = df[df["EXPIRED DATE"].apply(
    lambda x: (x.date() - today).days <= 3 and (x.date() - today).days >= 0
)]

# === Format pesan Telegram ===
if not soon_expired.empty:
    message = (
        "⚠️ *Pemberitahuan Server Mendekati Expired*\n\n"
        "Berikut detail server yang akan segera berakhir:\n\n"
    )
    for _, row in soon_expired.iterrows():
        expired_date = row["EXPIRED DATE"].strftime('%d-%m-%Y')
        harga = str(row["HARGA"]).replace(".0", "").replace(",", ".")
        message += (
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💻 *IP:* `{row['IP ADDRESS']}`\n"
            f"🌍 *Region:* {row['REGION']}\n"
            f"🧩 *Spesifikasi:* {row['SPESIFIKASI']}\n"
            f"💰 *Harga:* Rp {harga}\n"
            f"📅 *Expired:* {expired_date}\n"
            f"📊 *Status:* {row['STATUS']}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

    # Tambahan pesan otomatis
    message += (
        "Mohon konfirmasi apakah ingin melakukan *perpanjangan layanan*.\n"
        "Jika ya, segera hubungi admin untuk proses lanjut.\n\n"
    )

    send_telegram_message(message)
    print("📨 Pesan terkirim ke Telegram.")
else:
    print("✅ Tidak ada server yang mendekati expired hari ini.")
