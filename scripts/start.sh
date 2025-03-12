#!/bin/bash
# scripts/start.sh

# Start Docker services
docker-compose up -d

# Start Telegram bot
python3 scripts/bot.py &
