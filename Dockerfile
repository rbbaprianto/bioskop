# Gunakan Python sebagai base image
FROM python:3.9

# Set working directory dalam container
WORKDIR /app

# Salin hanya folder scripts ke dalam container
COPY scripts /app/scripts/

# Buat virtual environment (venv), aktifkan, dan instal dependensi
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    if [ -f "/app/scripts/requirements.txt" ]; then /app/venv/bin/pip install --no-cache-dir -r /app/scripts/requirements.txt; fi

# Pastikan semua script memiliki izin eksekusi
RUN chmod +x /app/scripts/*.sh /app/scripts/bot.py

# Gunakan venv untuk menjalankan bot.py
CMD ["/app/venv/bin/python3", "/app/scripts/bot.py"]
