import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

# === Konfigurasi ===
BOT_TOKEN = os.getenv("BOT_TOKEN") 
SPREADSHEET_ID = "1ZvZHH-Nsh1noKOs9YQkgYLRjUgA_ZsSpfCHqc4GwsGo"

# === Setup logging ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# === Setup Google Sheets API ===
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# === Fungsi untuk menambahkan data ===
def add_customer(update: Update, context: CallbackContext):
    try:
        args = " ".join(context.args)
        parts = [x.strip() for x in args.split("|")]
        if len(parts) < 6:
            update.message.reply_text(
                "❌ Format salah!\nGunakan format:\n"
                "`/add VPSRDP | IP | Spesifikasi | Harga | 2025-10-30 | Aktif`\n"
                "Atau:\n"
                "`/add Baremetal | IP | Spesifikasi | Harga | 2025-10-30 | Aktif`",
                parse_mode='Markdown'
            )
            return

        sheet_name, ip, spesifikasi, harga, expired, status = parts

        # Cek nama sheet valid
        if sheet_name not in ["VPSRDP", "Baremetal"]:
            update.message.reply_text("⚠️ Nama sheet tidak valid! Gunakan `VPSRDP` atau `Baremetal`.")
            return

        # Buka sheet sesuai pilihan
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(sheet_name)

        # Validasi format tanggal
        try:
            expired_date = datetime.strptime(expired, "%Y-%m-%d").strftime("%d-%m-%Y")
        except ValueError:
            update.message.reply_text("⚠️ Format tanggal salah! Gunakan format YYYY-MM-DD.")
            return

        # Tambahkan ke sheet
        sheet.append_row([ip, spesifikasi, harga, expired_date, status])

        update.message.reply_text(
            f"✅ Data baru berhasil ditambahkan ke *{sheet_name}*.\n\n"
            f"💻 IP: `{ip}`\n📅 Expired: {expired_date}\n📦 Status: {status}",
            parse_mode='Markdown'
        )

    except Exception as e:
        update.message.reply_text(f"❌ Gagal menambahkan data:\n`{e}`", parse_mode='Markdown')

# === Fungsi start ===
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Halo! Kirim data pelanggan baru pakai format:\n\n"
        "`/add VPSRDP | IP | Spesifikasi | Harga | 2025-10-30 | Aktif`\n"
        "atau\n"
        "`/add Baremetal | IP | Spesifikasi | Harga | 2025-10-30 | Aktif`",
        parse_mode='Markdown'
    )

# === Jalankan bot ===
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add_customer))

    updater.start_polling()
    logging.info("🤖 Bot Telegram siap menerima input customer baru...")
    updater.idle()

if __name__ == "__main__":
    main()
