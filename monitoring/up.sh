#!/bin/bash

# System Monitoring Dashboard Launcher
# Launches the Python HTTP server for the monitoring dashboard

echo "Starting System Monitoring Dashboard..."

# Change to the monitoring directory
cd "$(dirname "$0")"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found. Please install Python 3."
    exit 1
fi

# Check if required commands are available
REQUIRED_CMDS=("top" "free" "df" "uptime" "ps" "hostname" "uname" "date")
MISSING_CMDS=()

for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        MISSING_CMDS+=("$cmd")
    fi
done

if [ ${#MISSING_CMDS[@]} -ne 0 ]; then
    echo "Warning: The following commands are missing: ${MISSING_CMDS[*]}"
    echo "The dashboard may not work correctly without these utilities."
fi

# Launch the server
echo "Launching Python HTTP server on port 5050..."
echo "Dashboard will be available at: http://localhost:5050"
echo "API endpoints:"
echo "  - http://localhost:5050/api/metrics"
echo "  - http://localhost:5050/api/logs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------"

# Run the server in the foreground (can be stopped with Ctrl+C)
# To run in background, use: nohup python3 server.py > server.log 2>&1 &
python3 server.py