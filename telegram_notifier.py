import pandas as pd
import requests
from datetime import datetime
import os

# === Konfigurasi ===
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
EXCEL_PATH = "Customer BareMetal.xlsx"
SHEETS = ["VPSRDP", "Baremetal"]  # ← dua sheet sekaligus

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
    else:
        print("📨 Pesan terkirim ke Telegram.")

# === Fungsi baca dan proses tiap sheet ===
def process_sheet(sheet_name):
    print(f"✅ Membaca sheet: {sheet_name}")
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=sheet_name, header=2)
    except Exception as e:
        print(f"❌ Gagal membaca sheet '{sheet_name}': {e}")
        return None

    df.columns = [c.strip().upper() for c in df.columns]

    # Pastikan kolom EXPIRED DATE ada
    if "EXPIRED DATE" not in df.columns:
        print(f"⚠️ Sheet '{sheet_name}' tidak memiliki kolom 'EXPIRED DATE'")
        return None

    # Konversi kolom tanggal
    df["EXPIRED DATE"] = pd.to_datetime(df["EXPIRED DATE"], errors="coerce")

    # Filter yang expired dalam 3 hari
    today = datetime.now().date()
    soon_expired = df[df["EXPIRED DATE"].apply(
        lambda x: pd.notnull(x) and 0 <= (x.date() - today).days <= 3
    )]

    if soon_expired.empty:
        print(f"✅ Tidak ada data mendekati expired di sheet '{sheet_name}'.")
        return None

    # Format pesan
    message = (
        f"⚠️ *Pemberitahuan Server Mendekati Expired*\n"
        f"*Kategori:* {sheet_name}\n\n"
        f"Berikut detail server yang akan segera berakhir:\n\n"
    )

    for _, row in soon_expired.iterrows():
        expired_date = row["EXPIRED DATE"].strftime('%d-%m-%Y')
        harga = str(row.get("HARGA", "")).replace(".0", "").replace(",", ".")
        message += (
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💻 *IP:* `{row.get('IP ADDRESS', '-')}`\n"
            f"🧩 *Spesifikasi:* {row.get('SPESIFIKASI', '-')}\n"
            f"💰 *Harga:* Rp {harga}\n"
            f"📅 *Expired:* {expired_date}\n"
            f"📊 *Status:* {row.get('STATUS', '-')}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

    message += (
        "🙏 Mohon konfirmasi apakah ingin melakukan *perpanjangan layanan*.\n"
        "Jika ya, segera hubungi admin untuk proses lanjut.\n\n"
        "Terima kasih telah menggunakan layanan kami. 😊"
    )

    return message


# === Proses semua sheet ===
all_messages = []

print(f"📂 Membaca file Excel: {EXCEL_PATH}")
for sheet in SHEETS:
    msg = process_sheet(sheet)
    if msg:
        all_messages.append(msg)

# === Kirim ke Telegram ===
if all_messages:
    final_message = "\n\n".join(all_messages)
    send_telegram_message(final_message)
else:
    print("✅ Tidak ada server yang mendekati expired di semua sheet.")
