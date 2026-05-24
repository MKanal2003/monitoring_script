# DevOps Linux Automation & Nginx Infrastructure Project

## Project Overview

This project is a hands-on DevOps infrastructure lab built using Linux, Bash scripting, Nginx, networking tools, Git/GitHub, SSH, SCP, and automation concepts.

The goal of this project is to simulate a real-world DevOps environment by building:

* Backend applications
* Nginx reverse proxy
* Load balancing
* Monitoring scripts (now with web dashboard!)
* Backup automation
* Cron jobs
* SSH remote administration
* Network troubleshooting
* GitHub integration
* Containerization with Docker & Docker Compose

---

## 🆕 NEW: System Monitoring Dashboard

A real-time web-based system monitoring dashboard has been added to visualize system metrics and logs!

### Features:
- **Real-time CPU, Memory, Disk usage** with progress bars
- **System information** (hostname, kernel, uptime, load average, process count)
- **Recent logs viewer** (integrates with existing log files)
- **Auto-refresh every 3 seconds**
- **Light, clean, responsive design**
- **Accessible at http://localhost:5050**

---

## Architecture Diagram

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

                  ↓
         Dockerized Monitoring Dashboard
                       Port 5050
```

---

## Technologies Used

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
| Python HTTP Server | Backend applications & Monitoring Dashboard |
| Docker             | Containerization               |
| Docker Compose     | Multi-container orchestration  |
| Networking Tools   | DNS/TCP troubleshooting        |
| HTML/CSS/JS        | Monitoring Dashboard UI        |

---

## Project Structure

```text
/devops-project
│
├── apps/
│   ├── app1/
│   │   ├── index.html
│   │   ├── up_site.sh
│   │   └── out.log
│   └── app2/
│       ├── index.html
│       ├── up_site.sh
│       └── out.log
│
├── scripts/
│   ├── monitoring/
│   │   ├── cpu-monitor.sh
│   │   ├── memory-monitor.sh
│   │   ├── backup.sh
│   │   ├── disk-cleanup.sh
│   │   ├── .cpu-monitor.sh.swp
│   │   └── .cpu-monitor.sh.swo
│   └── (other scripts...)
│
├── monitoring/
│   ├── server.py                 # Python HTTP server for dashboard
│   ├── index.html                # Dashboard HTML page
│   ├── up.sh                     # Launcher script
│   ├── Dockerfile                # Docker build file
│   ├── requirements.txt          # Python dependencies
│   ├── .system-info.sh.swp       # Vim swap (to be cleaned)
│   └── systeminfo.sh             # Standalone diagnostics script
│
├── backups/
│   └── apps-backup-2026-05-23-16-24.tar.gz
│
├── logs/
│   ├── cpu.log
│   ├── memory.log
│   ├── backup.log
│   └── disk-cleanup.log
│
├── docs/                         # (Intended for documentation)
│
├── ngnix/                        # (Note: typo - should be nginx/)
│
├── secure-data/                  # (Intended for sensitive data)
│
├── docker-compose.yml            # Docker Compose orchestration
├── Readme.md                     # This file (note: capital R)
└── .gitignore                    # (Currently minimal)
```

---

## 🚀 Features Implemented

### 1. Linux Administration
* File system management
* Permissions management
* Process monitoring
* Service management
* Environment variables

### 2. Backend Applications
Two backend applications created using Python HTTP server:
* **App 1**: Runs on `localhost:8081`
* **App 2**: Runs on `localhost:8082`

### 3. Nginx Reverse Proxy & Load Balancer
Nginx configured to:
* Accept traffic on port 80
* Route requests to backend applications
* Perform load balancing
* Act as reverse proxy

### 4. Monitoring & Automation Scripts
#### CPU Monitoring Script
* Tracks CPU usage
* Logs CPU utilization
* Generates alerts for high CPU usage

#### Memory Monitoring Script
* Tracks memory usage
* Stores logs
* Generates alert logs

#### Backup Automation Script
* Creates timestamp-based backups
* Compresses application files
* Stores backups automatically

#### Disk Cleanup Script
* Cleans temporary files
* Removes old files
* Logs disk usage

#### 🆕 System Monitoring Dashboard
* Real-time web interface at port 5050
* Displays CPU, memory, disk usage with progress bars
* Shows system information (hostname, kernel, uptime, etc.)
* Views recent logs from existing log files
* Auto-refreshes every 3 seconds
* Dockerized for easy deployment

### 5. Cron Job Automation
Configured cron jobs:
```cron
*/5 * * * * /home/$USER/devops-project/scripts/monitoring/cpu-monitor.sh
*/5 * * * * /home/$USER/devops-project/scripts/monitoring/memory-monitor.sh
0 */6 * * * /home/$USER/devops-project/scripts/monitoring/backup.sh
0 0 * * * /home/$USER/devops-project/scripts/monitoring/disk-cleanup.sh
```

### 6. SSH & SCP Setup
* SSH server setup
* Passwordless SSH authentication
* SSH key generation
* SCP file transfer
* GitHub SSH authentication

### 7. Networking & Packet Analysis
* DNS lookup
* TCP/IP analysis
* Port verification
* Network troubleshooting
* Wireshark packet capture
* HTTP traffic analysis
* TCP handshake analysis

### 8. Git & GitHub
* Git repository initialization
* Git commits
* GitHub remote repository
* SSH-based GitHub authentication
* Branch management

### 9. Containerization (NEW)
* Dockerfile for monitoring dashboard
* Docker Compose for orchestration
* Volume mounting for log persistence
* Health checks
* Non-root user for security

---

## 🐳 Docker & Docker Compose Setup

### Quick Start with Docker Compose
```bash
# From project root directory:
docker-compose up -d

# The dashboard will be available at:
# http://localhost:5050

# To stop:
docker-compose down
```

### Manual Docker Build & Run
```bash
# Build the image
docker build -t devops-monitoring ./monitoring

# Run the container
docker run -d \
  --name monitoring-dashboard \
  -p 5050:5050 \
  -v $(pwd)/logs:/app/logs:ro \
  -v $(pwd)/apps:/app/apps:ro \
  --restart unless-stopped \
  devops-monitoring
```

### Docker Compose Details
The `docker-compose.yml` file configures:
* **Service**: `monitoring-dashboard`
* **Build**: Uses Dockerfile in `./monitoring/` directory
* **Ports**: Maps container port 5050 to host port 5050
* **Volumes**: 
  * Mounts logs directory as read-only (for dashboard to read logs)
  * Mounts apps directory as read-only (optional)
* **Environment**: Sets timezone to UTC
* **Restart Policy**: `unless-stopped` (survives reboots)
* **Health Check**: Checks `/api/metrics` endpoint every 30 seconds
* **Network**: Uses bridge network for isolation

### Monitoring Dashboard Endpoints
When running, the dashboard provides:
* **Web Interface**: `http://localhost:5050`
* **Metrics API**: `http://localhost:5050/api/metrics` (JSON)
* **Logs API**: `http://localhost:5050/api/logs` (JSON)

---

## 📋 Setup & Usage Instructions

### Prerequisites
* Linux system (tested on Ubuntu/WSL2)
* Python 3.6+ (for direct execution)
* Docker & Docker Compose (for containerized version)
* Bash shell

### Option 1: Direct Execution (No Docker)
```bash
# Make the launcher script executable
chmod +x monitoring/up.sh

# Start the dashboard
./monitoring/up.sh

# Or manually:
cd monitoring
python3 server.py

# Dashboard available at: http://localhost:5050
```

### Option 2: Docker (Recommended for Production)
```bash
# Using Docker Compose (easiest)
docker-compose up -d

# Verify it's running
docker-compose ps

# View logs
docker-compose logs -f

# Stop and remove
docker-compose down
```

### Option 3: Manual Docker
```bash
# Build
docker build -t devops-monitoring ./monitoring

# Run
docker run -d -p 5050:5050 --name monitoring devops-monitoring

# Stop
docker stop monitoring && docker rm monitoring
```

### Accessing Existing Components
* **Backend App 1**: `http://localhost:8081`
* **Backend App 2**: `http://localhost:8082`
* **Nginx Load Balancer**: `http://localhost` (if configured)
* **Monitoring Dashboard**: `http://localhost:5050`

### Verification Commands
```bash
# Test backend apps
curl localhost:8081
curl localhost:8082

# Test monitoring dashboard API
curl localhost:5050/api/metrics
curl localhost:5050/api/logs

# Test if server is responding
curl -I localhost:5050
```

---

## 🔧 Configuration & Customization

### Changing Dashboard Port
To change the port (default: 5050):
1. Edit `monitoring/server.py` - change `PORT = 5050`
2. Update `docker-compose.yml` if using Docker
3. Update any firewall or proxy configurations

### Accessing Logs
The dashboard automatically reads from:
* `logs/cpu.log` - CPU monitoring logs
* `logs/memory.log` - Memory monitoring logs
* `logs/backup.log` - Backup job logs
* `logs/disk-cleanup.log` - Disk cleanup logs

### Security Notes
* The Docker container runs as a non-root user (`appuser`)
* Logs are mounted as read-only for safety
* Only port 5050 is exposed (when using Docker)
* No external dependencies - uses Python standard library only

### Extending the Dashboard
To add new metrics:
1. Edit `collect_system_metrics()` in `server.py`
2. Add new fields to the metrics dictionary
3. Update `index.html` to display the new metric
4. Add appropriate CSS/styling as needed

---

## 📈 Monitoring & Alerts

### Existing Alerting (via cron scripts)
The original monitoring scripts still generate alerts:
* CPU > 80% → logs to `logs/alerts.log`
* Memory > 80% → logs to `logs/alerts.log`

### Dashboard Visual Indicators
The dashboard uses color-coding for quick visual assessment:
* **Green**: < 50% usage
* **Yellow**: 50-79% usage  
* **Red**: ≥ 80% usage

---

## 🛠️ Maintenance & Troubleshooting

### Common Issues

#### "Address already in use" on port 5050
```bash
# Find and kill process using port 5050
lsof -ti:5050 | xargs kill -9
# Or
fuser -k 5050/tcp
```

#### Dashboard not updating
* Check browser console for JavaScript errors
* Verify API endpoints are accessible:
  * `http://localhost:5050/api/metrics`
  * `http://localhost:5050/api/logs`
* Check server logs: `docker-compose logs -f` or terminal output

#### Permission denied accessing logs
* Ensure the `logs/` directory is readable by the container/user
* When using Docker, verify volume mounting: `-v $(pwd)/logs:/app/logs:ro`

#### High resource usage by dashboard itself
* The dashboard is lightweight (< 10MB RAM, minimal CPU)
* If needed, increase refresh interval in `index.html` (change `REFRESH_INTERVAL`)

### Log Management
* Log files grow over time - consider log rotation
* The `disk-cleanup.sh` script can be extended to handle old logs
* Manual log truncation: `> logs/cpu.log` (use with caution)

---

## 📝 Notes & Known Issues

### Directory Naming
* **`ngnix/` directory**: Contains a typo (should be `nginx/`). The Nginx configuration is documented in README but no actual config file exists yet.
* **`Readme.md`**: Uses capital 'R' - conventional is lowercase `README.md`

### Temporary Files
* Vim swap files exist in repo (`.swp`, `.swo` files) - these should be added to `.gitignore`
* Consider adding `*.swp`, `*.swo`, `.DS_Store`, etc. to `.gitignore`

### Future Improvements
* Add actual Nginx configuration file to `nginx/` directory
* Fix the `ngnix/` → `nginx/` directory rename
* Enhance `.gitignore` with comprehensive patterns
* Add stop script for backend applications (`down_site.sh`)
* Integrate `systeminfo.sh` into monitoring dashboard
* Add authentication to dashboard (for production use)
* Add persistent storage for dashboard preferences
* Add alert notifications (email, Slack, webhook)

---

## ✅ Verification & Testing

### Quick Verification Checklist
1. [ ] Backend apps responding on ports 8081/8082
2. [ ] Monitoring dashboard accessible at port 5050
3. [ ] API endpoints returning JSON data
4. [ ] Dashboard auto-updating every few seconds
5. [ ] Logs visible in dashboard
6. [ ] Color-coded progress bars working correctly
7. [ ] Docker container starting successfully (if using Docker)
8. [ ] Health checks passing (if using Docker Compose)

### Test Commands
```bash
# All-in-one verification
echo "=== Testing Backend Apps ==="
curl -s localhost:8081 | grep -i backend || echo "App 1: FAIL"
curl -s localhost:8082 | grep -i backend || echo "App 2: FAIL"

echo -e "\n=== Testing Monitoring Dashboard ==="
curl -s http://localhost:5050/api/metrics | jq . >/dev/null 2>&1 && echo "Metrics API: PASS" || echo "Metrics API: FAIL"
curl -s http://localhost:5050/api/logs | jq . >/dev/null 2>&1 && echo "Logs API: PASS" || echo "Logs API: FAIL"
curl -s -o /dev/null -w "%{http_code}" http://localhost:5050/ | grep -q "200" && echo "Dashboard: PASS" || echo "Dashboard: FAIL"

echo -e "\n=== Testing Docker (if applicable) ==="
docker-compose ps | grep -q "Up" && echo "Docker Compose: PASS" || echo "Docker Compose: FAIL (or not running)"
```

---

## 📚 Learning Outcomes

By studying and extending this project, you will gain hands-on experience with:

1. **Linux System Administration**
   - Process monitoring (`top`, `ps`, `uptime`)
   - Memory and disk usage analysis (`free`, `df`)
   - Service management and automation

2. **Bash Scripting for DevOps**
   - Creating reusable automation scripts
   - Logging and alerting mechanisms
   - Cron job scheduling
   - Backup and cleanup automation

3. **Web Development & Monitoring**
   - Building real-time dashboards with HTML/CSS/JS
   - Creating RESTful APIs with Python
   - JSON data exchange and frontend consumption
   - Responsive web design principles

4. **Containerization & Orchestration**
   - Dockerfile best practices
   - Docker Compose for multi-container apps
   - Volume mounting for data persistence
   - Health checks and restart policies
   - Security considerations (non-root users)

5. **Infrastructure as Code Concepts**
   - Reproducible environments
   - Configuration management
   - Service discovery and load balancing
   - Monitoring and observability

6. **Professional DevOps Practices**
   - Logging and monitoring strategies
   - Alerting thresholds and notifications
   - Security hardening
   - Performance optimization
   - Documentation and knowledge sharing

---

## 👨‍💻 Author

**Mallikarjuna (MKanal2003)**  
DevOps | DevSecOps | Cloud Engineer

*Built as a comprehensive DevOps learning project demonstrating real-world infrastructure automation skills.*

---

> **Last Updated**: May 2026  
> **Project Status**: 🟢 Active & Functional  
> **Dashboard Port**: 5050  
> **Containerized**: ✅ Yes (Docker & Docker Compose ready)  
> **License**: MIT (feel free to fork and extend!)