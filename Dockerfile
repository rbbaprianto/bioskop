FROM debian:latest

# Install dependencies
RUN apt-get update && apt-get install -y     jellyfin     rclone     aria2     curl     python3     python3-pip     supervisor

# Install Uptime Kuma
RUN mkdir /app && cd /app &&     curl -fsSL https://github.com/louislam/uptime-kuma/releases/latest/download/kuma-app.tar.gz | tar -xz

# Install bot dependencies
WORKDIR /app/bot
COPY scripts/bot.py .
RUN pip3 install python-telegram-bot

# Create film directory and set volume
RUN mkdir -p /film
VOLUME /film

# Copy config files
COPY config /config
COPY scripts/start.sh /scripts/start.sh
RUN chmod +x /scripts/start.sh

# Configure Supervisor
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose necessary ports
EXPOSE 8096 3001

# Start Supervisor to manage services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
