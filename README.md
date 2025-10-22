<h1 align="center">🤖 Telegram Expired Notifier</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Excel-Automation-success?logo=microsoft-excel&logoColor=white" alt="Excel">
  <img src="https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram&logoColor=white" alt="Telegram">
  <img src="https://img.shields.io/github/license/DimasDarma11/telegram-expired-notifier?color=lightgrey" alt="License">
</p>

<p align="center">
  🔔 Bot otomatis untuk memantau tanggal expired VPS / RDP / Baremetal dari file Excel dan mengirimkan notifikasi ke Telegram!
</p>

---

## 🚀 Fitur Unggulan

✨ **Auto Scan Excel** — Membaca data dari file `Customer BareMetal.xlsx` secara otomatis  
🤖 **Auto Notify Telegram** — Mengirim pesan jika layanan akan expired dalam 3 hari  
💾 **Support Multi Sheet** — Bisa pakai sheet `VPSRDP`, `Baremetal`, dan lainnya  
📊 **Detail Lengkap** — Menampilkan IP, Region, Spesifikasi, Harga, Expired, Status  
🧠 **Smart Date Parser** — Format tanggal otomatis dikenali walau beda format  
💬 **Pesan Ramah Pelanggan** — Disertai ajakan konfirmasi perpanjangan layanan  
⚙️ **Dapat Dijadwalkan Otomatis** — Via GitHub Actions atau Cron Job  
💰 **Gratis 100%** — Tidak butuh server, cukup GitHub & Telegram Bot  

---


## 📁 Struktur Proyek

```bash
telegram-expired-notifier/
├── telegram_notifier.py       # Script utama
├── Customer BareMetal.xlsx    # File Excel data pelanggan
├── requirements.txt           # Dependency Python
└── .github/
    └── workflows/
        └── notifier.yml       # Scheduler GitHub Actions
```

---

## ⚙️ Konfigurasi Environment

Tambahkan **secrets** di GitHub repository:

| Variable | Deskripsi |
|-----------|------------|
| `BOT_TOKEN` | Token dari [@BotFather](https://t.me/BotFather) |
| `CHAT_ID` | Chat ID tujuan notifikasi (bisa pribadi atau grup) |

> 📍 Akses: **Settings → Secrets and variables → Actions → New repository secret**

---

## 📊 Format File Excel

### Sheet: `VPSRDP`
| NO | IP ADDRESS | REGION | SPESIFIKASI | EXPIRED DATE | HARGA | STATUS |
|----|-------------|---------|--------------|---------------|--------|--------|

### Sheet: `Baremetal`
| NO | IP ADDRESS | BATCH | SPESIFIKASI | EXPIRED DATE | HARGA | STATUS |
|----|-------------|--------|--------------|---------------|--------|--------|

📝 **Header ada di baris ke-3 (row Excel ke-3)**  
Contoh tanggal valid: `25/10/2025`, `2025-10-25`, atau `25-Oct-2025`

---

## ⚡ Cara Menjalankan

## 🔹 1️⃣ Jalankan Manual (Local)
```bash
pip install -r requirements.txt
python telegram_notifier.py
```

## 🔹 2️⃣ Jalankan Otomatis (GitHub Actions)
Buat file .github/workflows/notifier.yml seperti ini:

on:
  schedule:
    - cron: '0 0 * * *'  # Tiap hari jam 07:00 WIB
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Jalankan Notifier
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
        run: python telegram_notifier.py
🕒 Workflow ini otomatis berjalan setiap hari jam 07:00 WIB (00:00 UTC).

---

## 📩 Contoh Notifikasi Telegram

⚠️ **Pemberitahuan Server Mendekati Expired**
Berikut detail server yang akan segera berakhir:

━━━━━━━━━━━━━━━━━━━━━━━
💻 IP: 157.245.8.176
🌍 Region: Singapore
🧩 Spesifikasi: 4 CPU / 8GB RAM / 80GB SSD
💰 Harga: Rp 250.000
📅 Expired: 25-10-2025
📊 Status: Aktif
━━━━━━━━━━━━━━━━━━━━━━━

🙏 Mohon konfirmasi apakah ingin melakukan *perpanjangan layanan*.
Jika ya, segera hubungi admin untuk proses lanjut.
Terima kasih telah menggunakan layanan kami. 😊

---

## 🧠 Alur Kerja Script

1️⃣ Baca file Excel dengan Pandas
2️⃣ Normalisasi nama kolom → uppercase semua
3️⃣ Parsing kolom EXPIRED DATE jadi format tanggal
4️⃣ Filter data dengan tanggal yang akan habis ≤ 3 hari lagi
5️⃣ Generate pesan berformat Markdown
6️⃣ Kirim ke Telegram lewat API resmi Bot Telegram

---

## 🪄 Tips Tambahan

💡 Gunakan format tanggal konsisten di Excel
💡 Simpan file Excel dengan nama tetap (Customer BareMetal.xlsx)
💡 Bisa tambahkan sheet baru (tinggal ubah SHEET_NAME di script)
💡 Integrasikan ke Render, Railway, atau GitHub Actions untuk auto-run

---

## 🧑‍💻 Author
Dimas Darma — ARVOCLOUD
📬 Telegram Notifier Project © 2025
💻 Dibuat dengan Python, Pandas, dan cinta ❤️

<p align="center"> <img src="https://img.shields.io/badge/Made%20With-Python-3776AB?logo=python&logoColor=white" alt="Made with Python"> <img src="https://img.shields.io/badge/Status-Aktif-success?style=flat-square" alt="Status"> </p>

## ⚖️ Lisensi
Lisensi MIT — Bebas digunakan, dimodifikasi, dan dikembangkan.
Cukup sertakan atribusi ke repo ini jika digunakan secara publik.
Copyright (c) 2025 Dimas Darmawan
Permission is hereby granted, free of charge, to any person obtaining a copy...
<p align="center"> ⭐️ Jangan lupa kasih <b>Star</b> kalau kamu suka project ini 😄 </p>
