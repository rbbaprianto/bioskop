#!/bin/bash
echo "Starting all services..."

# Start Jellyfin
service jellyfin start

# Start Aria2
aria2c --conf-path=/config/aria2/aria2.conf -D

# Start Rclone Mount
rclone mount mydrive: /film --config /config/rclone/rclone.conf --daemon

# Start Uptime Kuma
cd /app && node server/server.js &

# Start qBittorrent
qbittorrent-nox &

# Start File Browser
filebrowser -r /film &

# Start Prowlarr
cd /prowlarr && ./Prowlarr &

# Start Organizr
cd /organizr && php -S 0.0.0.0:80 &

# Start Netdata
service netdata start

# Start Telegram Bot
python3 /app/bot/bot.py &

# Keep container running
tail -f /dev/null
