# System Monitoring Dashboard

Docker-based system monitoring stack with real-time CPU, memory, disk, and network metrics.

## Features

- **Real-time Metrics**: Live CPU, memory, and disk usage with color-coded progress bars
- **System Information**: Hostname, kernel version, uptime, load average, process count
- **Log Viewer**: Recent log entries from monitoring scripts (CPU, memory, backup, disk-cleanup)
- **Auto-refresh**: Dashboard updates every 3 seconds
- **REST API**: JSON endpoints for metrics (`/api/metrics`) and logs (`/api/logs`)
- **Dockerized**: Multi-container orchestration with Docker Compose
- **Health Checks**: Automatic container health monitoring
- **Non-root User**: Security-hardened container execution
- **Responsive Design**: Works on desktop and mobile devices

## How to Run with Docker Compose

```bash
# Start the stack
docker compose up -d

# Dashboard available at
# http://localhost:5050

# View logs
docker compose logs -f

# Stop the stack
docker compose down
```

### Manual Docker Run

```bash
docker build -t monitoring-dashboard ./monitoring
docker run -d \
  --name monitoring-dashboard \
  -p 5050:5050 \
  -v $(pwd)/logs:/app/logs:ro \
  -v $(pwd)/apps:/app/apps:ro \
  monitoring-dashboard
```

### Direct Execution (no Docker)

```bash
chmod +x monitoring/up.sh
./monitoring/up.sh
```

## Architecture

```
┌──────────────┐
│   Browser    │
│ localhost:5050│
└──────┬───────┘
       │ HTTP
       ▼
┌──────────────────────────┐
│  monitoring-dashboard     │
│  (Python HTTP Server)     │
│  Port 5050                │
│                           │
│  ┌─────────────────────┐  │
│  │ / → index.html      │  │
│  │ /api/metrics → JSON │  │
│  │ /api/logs → JSON    │  │
│  └─────────────────────┘  │
└──────────────────────────┘
       │
       ├── reads logs/ (mounted volume)
       └── runs system commands (top, free, df, uptime)
```

## Project Structure

```
├── docker-compose.yml       # Docker Compose orchestration
├── monitoring/
│   ├── Dockerfile           # Container build
│   ├── server.py            # Python HTTP API server
│   ├── index.html           # Dashboard frontend
│   ├── up.sh                # Launcher script
│   ├── systeminfo.sh        # Diagnostics script
│   └── requirements.txt     # Python dependencies
├── apps/
│   └── app1/
│       ├── index.html       # Sample backend app
│       └── up_site.sh       # App launcher
├── scripts/
│   └── monitoring/
│       ├── cpu-monitor.sh   # CPU usage logger
│       ├── memory-monitor.sh# Memory usage logger
│       ├── backup.sh        # Backup automation
│       └── disk-cleanup.sh  # Disk cleanup
└── logs/                    # Log files (mounted volume)
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard UI |
| `/api/metrics` | GET | System metrics as JSON |
| `/api/logs` | GET | Recent log entries as JSON |

## Technologies

- **Python 3** — HTTP server & metrics collection
- **HTML/CSS/JS** — Frontend dashboard
- **Docker & Docker Compose** — Container orchestration
- **Bash** — Monitoring & automation scripts

## Author

**Mallikarjuna Kanal**

GitHub: [https://github.com/MKanal2003](https://github.com/MKanal2003)
