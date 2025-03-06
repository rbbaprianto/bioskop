import os
import time
import subprocess
import json
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Ambil environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FLY_APP_NAME = os.getenv("FLY_APP_NAME")
FLY_VOLUME_ID = os.getenv("FLY_VOLUME_ID")
FLYCTL_PATH = "/home/runner/.fly/bin/flyctl"

# Fungsi kirim notifikasi Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

# Cek status VM
def check_vm_status(update: Update, context: CallbackContext):
    update.message.reply_text("⏳ Mengecek status VM...")
    try:
        result = subprocess.run([FLYCTL_PATH, "status", "--app", FLY_APP_NAME], capture_output=True, text=True)
        update.message.reply_text(f"📡 Status VM:\n\n{result.stdout}")
    except Exception as e:
        update.message.reply_text(f"❌ Gagal mengecek status VM: {str(e)}")

# Start VM
def start_vm(update: Update, context: CallbackContext):
    update.message.reply_text("⚡ Menyalakan VM...")
    try:
        result = subprocess.run([FLYCTL_PATH, "machines", "start", "--app", FLY_APP_NAME], capture_output=True, text=True)
        update.message.reply_text(f"✅ VM berhasil dinyalakan.\n\n{result.stdout}")
        send_telegram_message("✅ VM telah dinyalakan!")
    except Exception as e:
        update.message.reply_text(f"❌ Gagal menyalakan VM: {str(e)}")

# Stop VM
def stop_vm(update: Update, context: CallbackContext):
    update.message.reply_text("🛑 Mematikan VM...")
    try:
        result = subprocess.run([FLYCTL_PATH, "machines", "stop", "--app", FLY_APP_NAME], capture_output=True, text=True)
        update.message.reply_text(f"✅ VM berhasil dimatikan.\n\n{result.stdout}")
        send_telegram_message("⚠️ VM telah dimatikan!")
    except Exception as e:
        update.message.reply_text(f"❌ Gagal mematikan VM: {str(e)}")

# Cek disk dan auto-extend jika < 20%
def check_disk_space(update: Update, context: CallbackContext):
    output = subprocess.run(["df", "-h", "/film"], capture_output=True, text=True).stdout
    lines = output.split("\n")
    if len(lines) > 1:
        usage_line = lines[1].split()
        percent_used = int(usage_line[4].replace("%", ""))
        
        if percent_used >= 80:
            update.message.reply_text(f"⚠️ Disk penuh {percent_used}%. Menambah 5GB...")
            extend_volume()
        else:
            update.message.reply_text(f"✅ Disk aman: {percent_used}% digunakan.")

# Extend volume secara manual
def extend_yes(update: Update, context: CallbackContext):
    update.message.reply_text("📢 Memperbesar volume sebesar 5GB...")
    try:
        result = subprocess.run([FLYCTL_PATH, "volumes", "extend", FLY_VOLUME_ID, "--size=+5"], capture_output=True, text=True)
        update.message.reply_text(f"✅ Volume diperbesar 5GB.\n\nOutput:\n{result.stdout}")
        send_telegram_message(f"✅ Volume diperbesar 5GB.\n{result.stdout}")
    except Exception as e:
        update.message.reply_text(f"❌ Gagal memperbesar volume: {str(e)}")

# Batalkan extend
def extend_no(update: Update, context: CallbackContext):
    update.message.reply_text("❌ Perintah dibatalkan. Volume tidak diperbesar.")

# Schedule auto-check disk
def schedule_disk_check():
    while True:
        output = subprocess.run(["df", "-h", "/film"], capture_output=True, text=True).stdout
        lines = output.split("\n")
        if len(lines) > 1:
            usage_line = lines[1].split()
            percent_used = int(usage_line[4].replace("%", ""))

            if percent_used >= 80:
                send_telegram_message(f"⚠️ Disk sudah {percent_used}% penuh. Menambah 5GB...")
                extend_volume()
        time.sleep(3600)  # Cek setiap 1 jam

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("status_vm", check_vm_status))
    dp.add_handler(CommandHandler("start_vm", start_vm))
    dp.add_handler(CommandHandler("stop_vm", stop_vm))
    dp.add_handler(CommandHandler("check_disk", check_disk_space))
    dp.add_handler(CommandHandler("extend_yes", extend_yes))
    dp.add_handler(CommandHandler("extend_no", extend_no))

    updater.start_polling()
    updater.job_queue.run_repeating(schedule_disk_check, interval=3600, first=10)
    updater.idle()

if __name__ == "__main__":
    time.sleep(5)
    main()
