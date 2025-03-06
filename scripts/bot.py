import os
import time
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Ambil environment variables dengan fallback default
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FLY_APP_NAME = os.getenv("FLY_APP_NAME", "bioskop")
FLY_VOLUME_ID = os.getenv("FLY_VOLUME_ID")
FLYCTL_PATH = os.getenv("FLYCTL_PATH", "/home/runner/.fly/bin/flyctl")

# Cek apakah environment variable wajib sudah tersedia
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN atau TELEGRAM_CHAT_ID tidak ditemukan! Pastikan sudah diset di Fly.io secrets.")
    exit(1)

def run_flyctl_command(command, update: Update, success_msg: str, error_msg: str):
    """Helper function untuk menjalankan perintah flyctl dan mengirim hasilnya ke Telegram."""
    try:
        result = subprocess.run([FLYCTL_PATH] + command, capture_output=True, text=True)
        update.message.reply_text(f"{success_msg}\n\n{result.stdout}")
    except Exception as e:
        update.message.reply_text(f"{error_msg}\n❌ Error: {str(e)}")

async def check_vm_status(update: Update, context: CallbackContext):
    await update.message.reply_text("⏳ Mengecek status VM...")
    run_flyctl_command(["status", "--app", FLY_APP_NAME], update, "📡 Status VM:", "❌ Gagal mengecek status VM!")

async def start_vm(update: Update, context: CallbackContext):
    await update.message.reply_text("⚡ Menyalakan VM...")
    run_flyctl_command(["machines", "start", "--app", FLY_APP_NAME], update, "✅ VM berhasil dinyalakan!", "❌ Gagal menyalakan VM!")

async def stop_vm(update: Update, context: CallbackContext):
    await update.message.reply_text("🛑 Mematikan VM...")
    run_flyctl_command(["machines", "stop", "--app", FLY_APP_NAME], update, "✅ VM berhasil dimatikan!", "❌ Gagal mematikan VM!")

async def extend_yes(update: Update, context: CallbackContext):
    if not FLY_VOLUME_ID:
        await update.message.reply_text("❌ ERROR: FLY_VOLUME_ID tidak ditemukan! Pastikan sudah diset di Fly.io secrets.")
        return
    await update.message.reply_text("📢 Memperbesar volume sebesar 10GB...")
    run_flyctl_command(["volumes", "extend", FLY_VOLUME_ID, "--size=+10"], update, "✅ Volume diperbesar 10GB!", "❌ Gagal memperbesar volume!")

async def extend_no(update: Update, context: CallbackContext):
    await update.message.reply_text("❌ Perintah dibatalkan. Volume tidak diperbesar.")

async def main():
    """Fungsi utama untuk menjalankan bot Telegram."""
    print("⏳ Menunggu 10 detik sebelum memulai bot...")
    time.sleep(10)
    print("🚀 Bot Telegram dimulai!")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("status_vm", check_vm_status))
    app.add_handler(CommandHandler("start_vm", start_vm))
    app.add_handler(CommandHandler("stop_vm", stop_vm))
    app.add_handler(CommandHandler("extend_yes", extend_yes))
    app.add_handler(CommandHandler("extend_no", extend_no))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
