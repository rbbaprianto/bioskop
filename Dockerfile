# Gunakan image Python sebagai base
FROM python:3.9

# Install dependencies bot
WORKDIR /app/bot
COPY scripts/bot.py /app/bot/bot.py
RUN pip3 install python-telegram-bot

# Jalankan bot sebagai entrypoint
CMD ["python3", "/app/bot/bot.py"]
