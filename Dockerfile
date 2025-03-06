# Menggunakan Debian sebagai base image
FROM debian:latest

# Install dependencies
RUN apt-get update && apt-get install -y     jellyfin     rclone     aria2     qbittorrent-nox     curl     python3     python3-pip     filebrowser     netdata     supervisor

# Install Uptime Kuma
RUN mkdir /app && cd /app &&     curl -fsSL https://github.com/louislam/uptime-kuma/releases/latest/download/kuma-app.tar.gz | tar -xz

# Install Prowlarr
RUN mkdir /prowlarr && cd /prowlarr &&     curl -fsSL https://github.com/Prowlarr/Prowlarr/releases/latest/download/prowlarr.tar.gz | tar -xz

# Install Organizr
RUN mkdir /organizr && cd /organizr &&     git clone https://github.com/causefx/Organizr.git .

# Install bot dependencies
WORKDIR /app/bot
COPY scripts/bot.py .
RUN pip3 install python-telegram-bot

# Copy config files
COPY config /config
COPY scripts/start.sh /scripts/start.sh
RUN chmod +x /scripts/start.sh

# Configure Supervisor
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose necessary ports
EXPOSE 8096 3001 6881 8112 80 19999

# Start Supervisor to manage services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
