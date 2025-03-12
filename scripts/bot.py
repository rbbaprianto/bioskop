# scripts/bot.py
import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FLY_API_TOKEN = os.getenv("FLY_API_TOKEN")
APP_NAME = "bioskop"

# Start VM
def start_vm(update: Update, context: CallbackContext):
    url = f"https://api.fly.io/v1/apps/{APP_NAME}/machines/start"
    headers = {"Authorization": f"Bearer {FLY_API_TOKEN}"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        update.message.reply_text("Server started successfully!")
    else:
        update.message.reply_text("Failed to start server.")

# Stop VM
def stop_vm(update: Update, context: CallbackContext):
    url = f"https://api.fly.io/v1/apps/{APP_NAME}/machines/stop"
    headers = {"Authorization": f"Bearer {FLY_API_TOKEN}"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        update.message.reply_text("Server stopped successfully!")
    else:
        update.message.reply_text("Failed to stop server.")

# Check status
def status(update: Update, context: CallbackContext):
    url = f"https://api.fly.io/v1/apps/{APP_NAME}/machines"
    headers = {"Authorization": f"Bearer {FLY_API_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        update.message.reply_text("Server is running.")
    else:
        update.message.reply_text("Server is not running.")

# Main function
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start_vm", start_vm))
    dispatcher.add_handler(CommandHandler("stop_vm", stop_vm))
    dispatcher.add_handler(CommandHandler("status", status))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
