#!/bin/bash

THRESHOLD=80
VOLUME_ID=$(flyctl volumes list --json | jq -r '.[] | select(.name=="film_volume") | .id')

USAGE=$(df /film | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$USAGE" -ge "$THRESHOLD" ]; then
  echo "⚠️ Disk $USAGE% penuh. Menambah 5GB..."
  flyctl volumes extend $VOLUME_ID --size=+5 --yes
else
  echo "✅ Disk aman: $USAGE% digunakan."
fi
