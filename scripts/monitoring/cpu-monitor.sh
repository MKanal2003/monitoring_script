#!/bin/bash

DATE=$(date +"%Y-%m-%d %H:%M:%S")

CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')

echo "$DATE CPU Usage: $CPU%" >> ~/devops-project/logs/cpu.log

if (( $(echo "$CPU > 80" | bc -l) )); then
    echo "WARNING: High CPU Usage - $CPU%" >> ~/devops-project/logs/alerts.log
fi
