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


## Layanan yang Ditambahkan:
- ✅ Bazarr
- ✅ Caddy (Reverse Proxy + HTTPS)
- ✅ Tailscale
- ✅ Sonarr & Radarr
- ✅ Notifikasi Telegram/Discord
- ✅ Dashy (UI Dashboard)


## Cara Install

### 1. Clone Repository
```sh
git clone https://github.com/rbbaprianto/bioskop.git
cd bioskop
```

### 2. Atur secret GitHub di repository:
   - `FLY_API_TOKEN`
   - `TELEGRAM_BOT_TOKEN`
   - `RPC_SECRET`
   - `SONARR_API_KEY`
   - `RADARR_API_KEY`
   - `BAZARR_API_KEY`
   - `QBITTORRENT_USERNAME`
   - `QBITTORRENT_PASSWORD`
   - `TAILSCALE_AUTHKEY`
   - `FLY_VOLUME_ID`
   
   
### 3. Deploy ke Fly.io
Pastikan sudah login ke Fly.io:
```sh
flyctl auth login
```

Deploy dengan perintah:
```sh
flyctl deploy --remote-only
```

### 4. Start & Stop Server Lewat Telegram
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
│   ├── jellyfin/      # Konfigurasi Jellyfin
│   ├── rclone/        # Konfigurasi rclone
│   ├── aria2/         # Konfigurasi aria2
│   ├── kuma/          # Konfigurasi Uptime Kuma
│   ├── bot/           # Script bot Telegram
│── scripts/
│   ├── start.sh       # Script inisialisasi
│   ├── bot.py         # Bot Telegram
│── .github/workflows/
│   ├── deploy.yml     # Workflow GitHub Actions
│── README.md          # Dokumentasi lengkap
```

## Lisensi
Proyek ini menggunakan lisensi MIT.
