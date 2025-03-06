# Gunakan Debian sebagai base image
FROM debian:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    rclone \
    aria2 \
    qbittorrent-nox \
    curl \
    python3 \
    python3-pip \
    netdata \
    supervisor \
    git \
    npm && \
    apt-get clean

# Install Jellyfin
RUN curl -fsSL https://repo.jellyfin.org/jellyfin_team.gpg.key | tee /usr/share/keyrings/jellyfin.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/jellyfin.gpg] https://repo.jellyfin.org/debian bookworm main" | tee /etc/apt/sources.list.d/jellyfin.list && \
    apt-get update && apt-get install -y jellyfin && \
    apt-get clean

# Install Filebrowser
RUN curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash

# Install Tailscale
RUN curl -fsSL https://tailscale.com/install.sh | sh

# Install Uptime Kuma
RUN mkdir -p /app && cd /app && \
    curl -fsSL https://github.com/louislam/uptime-kuma/releases/latest/download/kuma-app.tar.gz | tar -xz

# Install Prowlarr
RUN mkdir -p /prowlarr && cd /prowlarr && \
    curl -fsSL https://github.com/Prowlarr/Prowlarr/releases/latest/download/prowlarr.tar.gz | tar -xz

# Install Organizr
RUN mkdir -p /organizr && cd /organizr && \
    git clone https://github.com/causefx/Organizr.git .

# Install Dashy
RUN mkdir -p /dashy && cd /dashy && \
    git clone https://github.com/Lissy93/dashy.git . && \
    npm install

# Pastikan folder konfigurasi ada sebelum COPY
RUN mkdir -p /config

# Copy config files
COPY config/ /config/
COPY scripts/start.sh /scripts/start.sh
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Berikan izin eksekusi ke start.sh
RUN chmod +x /scripts/start.sh

# Expose necessary ports
EXPOSE 8096 3001 6881 8112 80 19999 8989 7878 6767

# Jalankan start.sh sebagai entrypoint
CMD ["/bin/bash", "/scripts/start.sh"]
