#!/bin/bash

THRESHOLD=20  # Jika disk tersisa 20%
USAGE=$(df /app | tail -1 | awk '{print $5}' | sed 's/%//')

if [ "$USAGE" -ge "$THRESHOLD" ]; then
  MESSAGE="🚨 Disk hampir penuh! Saat ini tersisa ${USAGE}%.\n\nKonfirmasi untuk extend volume:\n👉 /extend_yes untuk menambah 10GB\n❌ /extend_no untuk membatalkan"
  
  curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
       -d "chat_id=${TELEGRAM_CHAT_ID}" \
       -d "text=${MESSAGE}"
fi
