# Gunakan Python 3.9 sebagai base image
FROM python:3.9

# Tentukan direktori kerja
WORKDIR /app

# Copy semua file ke dalam container
COPY . /app

# Pastikan requirements.txt tersedia sebelum menjalankan pip install
COPY scripts/requirements.txt /app/scripts/requirements.txt

# Buat virtual environment dan install dependencies
RUN python3 -m venv /app/venv \
    && /app/venv/bin/pip install --upgrade pip \
    && if [ -f "/app/scripts/requirements.txt" ]; then /app/venv/bin/pip install --no-cache-dir -r /app/scripts/requirements.txt; fi

# Berikan izin eksekusi pada semua script di dalam folder scripts
RUN chmod +x /app/scripts/*.sh

# Tentukan command untuk menjalankan bot
CMD ["/bin/sh", "/app/scripts/start.sh"]
