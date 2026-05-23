# DevOps Linux Automation & Nginx Infrastructure Project

## Project Overview

This project is a hands-on DevOps infrastructure lab built using Linux, Bash scripting, Nginx, networking tools, Git/GitHub, SSH, SCP, and automation concepts.

The goal of this project is to simulate a real-world DevOps environment by building:

* Backend applications
* Nginx reverse proxy
* Load balancing
* Monitoring scripts
* Backup automation
* Cron jobs
* SSH remote administration
* Network troubleshooting
* GitHub integration

---

# Architecture Diagram

```text
                    User Request
                          ↓
                  Nginx Reverse Proxy
                          ↓
          ┌───────────────┴───────────────┐
          ↓                               ↓
      Backend App 1                  Backend App 2
          Port 8081                     Port 8082

          ↓                               ↓
      Monitoring                      Logging

                 ↓
        Automation Scripts

                 ↓
              Cron Jobs
```

---

# Technologies Used

| Technology         | Purpose                        |
| ------------------ | ------------------------------ |
| Linux              | Server administration          |
| Bash Scripting     | Automation                     |
| Nginx              | Reverse proxy & load balancing |
| Git/GitHub         | Version control                |
| SSH                | Secure remote access           |
| SCP                | Secure file transfer           |
| Cron               | Job scheduling                 |
| Wireshark          | Packet analysis                |
| Python HTTP Server | Backend applications           |
| Networking Tools   | DNS/TCP troubleshooting        |

---

# Project Structure

```text
/devops-project
│
├── apps/
│   ├── app1/
│   └── app2/
│
├── scripts/
│   ├── cpu-monitor.sh
│   ├── memory-monitor.sh
│   ├── backup.sh
│   └── disk-cleanup.sh
│
├── backups/
├── logs/
├── monitoring/
├── nginx/
├── docs/
└── README.md
```

---

# Features Implemented

## Linux Administration

* File system management
* Permissions management
* Process monitoring
* Service management
* Environment variables

---

## Backend Applications

Two backend applications were created using Python HTTP server.

### App 1

Runs on:

```text
localhost:8081
```

### App 2

Runs on:

```text
localhost:8082
```

---

# Nginx Reverse Proxy & Load Balancer

Nginx was configured to:

* Accept traffic on port 80
* Route requests to backend applications
* Perform load balancing
* Act as reverse proxy

---

# Nginx Configuration

```nginx
upstream backend_servers {

    server 127.0.0.1:8081;
    server 127.0.0.1:8082;

}

server {

    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location / {

        proxy_pass http://backend_servers;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    }

}
```

---

# Monitoring & Automation Scripts

## CPU Monitoring Script

Features:

* Tracks CPU usage
* Logs CPU utilization
* Generates alerts for high CPU usage

---

## Memory Monitoring Script

Features:

* Tracks memory usage
* Stores logs
* Generates alert logs

---

## Backup Automation Script

Features:

* Creates timestamp-based backups
* Compresses application files
* Stores backups automatically

---

## Disk Cleanup Script

Features:

* Cleans temporary files
* Removes old files
* Logs disk usage

---

# Cron Job Automation

Configured cron jobs:

```cron
*/5 * * * * /home/$USER/devops-project/scripts/cpu-monitor.sh
*/5 * * * * /home/$USER/devops-project/scripts/memory-monitor.sh
0 */6 * * * /home/$USER/devops-project/scripts/backup.sh
0 0 * * * /home/$USER/devops-project/scripts/disk-cleanup.sh
```

---

# SSH & SCP Setup

Implemented:

* SSH server setup
* Passwordless SSH authentication
* SSH key generation
* SCP file transfer
* GitHub SSH authentication

---

# Networking & Packet Analysis

Performed:

* DNS lookup
* TCP/IP analysis
* Port verification
* Network troubleshooting
* Wireshark packet capture
* HTTP traffic analysis
* TCP handshake analysis

---

# Git & GitHub

Implemented:

* Git repository initialization
* Git commits
* GitHub remote repository
* SSH-based GitHub authentication
* Branch management

---

# Commands Used

## Git Commands

```bash
git init
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

## Nginx Commands

```bash
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx
```

---

## Process Monitoring

```bash
ps aux
htop
ss -tulnp
```

---

# Verification Commands

## Test Backend Apps

```bash
curl localhost:8081
curl localhost:8082
```

---

## Test Load Balancer

```bash
curl localhost
```

Refresh multiple times to observe load balancing.

---

# Learning Outcomes

This project helped in understanding:

* Linux administration
* Bash scripting
* Nginx reverse proxy
* Load balancing
* Automation scripting
* Monitoring concepts
* Cron jobs
* SSH/SCP
* GitHub SSH authentication
* Networking fundamentals
* Packet analysis
* Production troubleshooting

---

# Future Enhancements

## Docker

Containerize:

* App1
* App2
* Nginx

---

## Monitoring Stack

Add:

* Prometheus
* Grafana
* Node Exporter

---

## CI/CD

Add:

* Jenkins
* GitHub Actions

---

## Kubernetes

Deploy applications on Kubernetes.

---

# Resume Project Description

## DevOps Linux Automation & Nginx Infrastructure Project

Built a complete DevOps infrastructure project using Linux, Bash scripting, Nginx reverse proxy, load balancing, monitoring automation, cron jobs, SSH/SCP, networking tools, and GitHub integration. Implemented backend application routing, backup automation, resource monitoring, and packet analysis using Wireshark.

---

# Screenshots To Add

Add screenshots for:

1. Nginx load balancing
2. CPU monitoring logs
3. Backup files
4. Cron jobs
5. Wireshark capture
6. SSH authentication
7. GitHub repository
8. Nginx access logs

---

# Author

Mallikarjuna

DevOps | DevSecOps | Cloud Engineer

