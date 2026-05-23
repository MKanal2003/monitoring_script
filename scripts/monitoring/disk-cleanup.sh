#!/bin/bash

echo "Cleaning temporary files..."

find /tmp -type f -mtime +2 -delete

echo "Disk Usage After Cleanup:" >> ~/devops-project/logs/disk-cleanup.log

df -h >> ~/devops-project/logs/disk-cleanup.log
