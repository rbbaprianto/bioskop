# Bioskop - Media Server dengan Jellyfin, Aria2, rclone, dan lainnya

Bioskop adalah sistem media server yang menggabungkan **Jellyfin, Aria2, rclone, qBittorrent, Uptime Kuma, File Browser, Prowlarr, Organizr, dan Netdata** dalam satu Docker container untuk pengalaman streaming dan manajemen unduhan yang optimal.

## Fitur Utama:
- **Jellyfin**: Streaming film dan serial favorit Anda.
- **Aria2 & rclone**: Mengunduh dan mengelola file film secara otomatis.
- **qBittorrent**: Klien torrent untuk mengunduh konten.
- **Uptime Kuma**: Monitoring uptime server.
- **File Browser**: Mengelola file yang sudah diunduh.
- **Prowlarr**: Manajemen indexer untuk torrent.
- **Organizr**: Panel kontrol untuk menyatukan semua layanan.
- **Netdata**: Monitoring kinerja server.

## Cara Install
1. Clone repository: `git clone https://github.com/rbbaprianto/bioskop.git`
2. Atur variabel lingkungan di `.env`.
3. Deploy ke Fly.io: `flyctl deploy --remote-only`.

## Start & Stop Server Lewat Telegram
Gunakan perintah ini di bot Telegram:
- `/start_vm` → Menyalakan server
- `/stop_vm` → Mematikan server
- `/status` → Mengecek status server

## Struktur Repository
```
/bioskop
│── Dockerfile
│── fly.toml
│── .gitignore
│── docker-compose.yml
│── .env.example
│── config/
│   ├── jellyfin/
│   ├── rclone/
│   ├── aria2/
│   ├── kuma/
│   ├── bot/
│── scripts/
│   ├── start.sh
│   ├── bot.py
│── .github/workflows/
│   ├── deploy.yml
│── README.md
```

## Lisensi
Proyek ini menggunakan lisensi MIT.
