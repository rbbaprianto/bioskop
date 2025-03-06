import os
import time
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
FLY_APP_NAME = os.environ["FLY_APP_NAME"]
FLY_VOLUME_ID = os.environ["FLY_VOLUME_ID"]
FLYCTL_PATH = "/home/runner/.fly/bin/flyctl"

def check_vm_status(update: Update, context: CallbackContext):
    update.message.reply_text("⏳ Mengecek status VM...")
    try:
        result = subprocess.run(
            [FLYCTL_PATH, "status", "--app", FLY_APP_NAME],
            capture_output=True, text=True
        )
        update.message.reply_text(f"📡 Status VM:\n\n{result.stdout}")
    except Exception as e:
        update.message.reply_text(f"❌ Gagal mengecek status VM: {str(e)}")

def start_vm(update: Update, context: CallbackContext):
    update.message.reply_text("⚡ Menyalakan VM...")
    try:
        result = subprocess.run(
            [FLYCTL_PATH, "machines", "start", "--app", FLY_APP_NAME],
            capture_output=True, text=True
        )
        update.message.reply_text(f"✅ VM berhasil dinyalakan.\n\n{result.stdout}")
    except Exception as e:
        update.message.reply_text(f"❌ Gagal menyalakan VM: {str(e)}")

def stop_vm(update: Update, context: CallbackContext):
    update.message.reply_text("🛑 Mematikan VM...")
    try:
        result = subprocess.run(
            [FLYCTL_PATH, "machines", "stop", "--app", FLY_APP_NAME],
            capture_output=True, text=True
        )
        update.message.reply_text(f"✅ VM berhasil dimatikan.\n\n{result.stdout}")
    except Exception as e:
        update.message.reply_text(f"❌ Gagal mematikan VM: {str(e)}")

def extend_yes(update: Update, context: CallbackContext):
    update.message.reply_text("📢 Memperbesar volume sebesar 10GB...")
    try:
        result = subprocess.run(
            [FLYCTL_PATH, "volumes", "extend", FLY_VOLUME_ID, "--size=+10"],
            capture_output=True, text=True
        )
        update.message.reply_text(f"✅ Volume diperbesar 10GB.\n\nOutput:\n{result.stdout}")
    except Exception as e:
        update.message.reply_text(f"❌ Gagal memperbesar volume: {str(e)}")

def extend_no(update: Update, context: CallbackContext):
    update.message.reply_text("❌ Perintah dibatalkan. Volume tidak diperbesar.")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("status_vm", check_vm_status))
    dp.add_handler(CommandHandler("start_vm", start_vm))
    dp.add_handler(CommandHandler("stop_vm", stop_vm))
    dp.add_handler(CommandHandler("extend_yes", extend_yes))
    dp.add_handler(CommandHandler("extend_no", extend_no))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    time.sleep(10)  # Tunggu 10 detik sebelum bot mulai
    main()
