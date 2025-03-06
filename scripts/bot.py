from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Selamat datang di Bioskop! Gunakan /help untuk melihat perintah.")

def status(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Semua layanan bioskop sedang berjalan dengan baik.")

def start_vm(update: Update, context: CallbackContext) -> None:
    os.system("flyctl machines start --all")
    update.message.reply_text("Server bioskop telah dinyalakan.")

def stop_vm(update: Update, context: CallbackContext) -> None:
    os.system("flyctl machines stop --all")
    update.message.reply_text("Server bioskop telah dimatikan.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("start_vm", start_vm))
    dp.add_handler(CommandHandler("stop_vm", stop_vm))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
