FROM python:3.9-slim

# Mengatur direktori kerja dalam container
WORKDIR /app

# Salin semua file yang diperlukan, termasuk bot.py
COPY . /app/

# Pastikan bot.py memiliki izin eksekusi
RUN chmod +x /app/bot.py

# Menjalankan bot
CMD ["python3", "/app/bot.py"]
