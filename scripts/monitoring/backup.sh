#!/bin/bash

DATE=$(date +"%Y-%m-%d-%H-%M")

mkdir -p ~/devops-project/backups

tar -czf ~/devops-project/backups/apps-backup-$DATE.tar.gz \
~/devops-project/apps

echo "Backup completed at $DATE" >> ~/devops-project/logs/backup.log
