#!/bin/bash

DATE=$(date +"%Y-%m-%d %H:%M:%S")

MEMORY=$(free | awk '/Mem:/ {printf("%.2f"), $3/$2 * 100.0}')

echo "$DATE Memory Usage: $MEMORY%" >> ~/devops-project/logs/memory.log

if (( $(echo "$MEMORY > 80" | bc -l) )); then
    echo "WARNING: High Memory Usage - $MEMORY%" >> ~/devops-project/logs/alerts.log
fi
