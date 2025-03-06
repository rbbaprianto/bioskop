#!/bin/bash

# Mulai service utama
service jellyfin start
service qbittorrent-nox start
service tailscaled start
service supervisor start

# Jalankan pengecekan volume di background setiap 1 jam
echo "0 * * * * root /scripts/extend_volume.sh >> /var/log/extend_volume.log 2>&1" >> /etc/crontab

exec "$@"
