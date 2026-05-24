#!/usr/bin/env python3
"""
System Monitoring Dashboard Server
Serves static files and provides API endpoints for system metrics
"""

import http.server
import socketserver
import json
import subprocess
import os
import sys
from urllib.parse import urlparse, parse_qs
import threading
import time

PORT = 5050
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(PROJECT_ROOT, "..", "logs")

class MonitoringHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.serve_file('index.html', 'text/html')
        elif path == '/api/metrics':
            self.serve_metrics()
        elif path == '/api/logs':
            self.serve_logs()
        elif path.startswith('/static/'):
            # Serve static files if needed
            self.serve_static(path[1:])
        else:
            # Default to serving files from current directory
            super().do_GET()
    
    def serve_file(self, filename, content_type):
        """Serve a static file"""
        filepath = os.path.join(PROJECT_ROOT, filename)
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, f"File not found: {filename}")
    
    def serve_static(self, path):
        """Serve static files"""
        filepath = os.path.join(PROJECT_ROOT, path)
        if os.path.exists(filepath) and os.path.isfile(filepath):
            self.send_response(200)
            # Set content type based on extension
            if path.endswith('.css'):
                content_type = 'text/css'
            elif path.endswith('.js'):
                content_type = 'application/javascript'
            elif path.endswith('.png'):
                content_type = 'image/png'
            elif path.endswith('.jpg') or path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            else:
                content_type = 'application/octet-stream'
            self.send_header('Content-Type', content_type)
            self.end_headers()
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)
    
    def serve_metrics(self):
        """Serve system metrics as JSON"""
        try:
            metrics = self.collect_system_metrics()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(metrics).encode())
        except Exception as e:
            self.send_error(500, f"Error collecting metrics: {str(e)}")
    
    def serve_logs(self):
        """Serve recent log entries"""
        try:
            logs = self.collect_recent_logs()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(logs).encode())
        except Exception as e:
            self.send_error(500, f"Error reading logs: {str(e)}")
    
    def collect_system_metrics(self):
        """Collect system metrics using shell commands"""
        metrics = {}
        
        # Hostname
        try:
            metrics['hostname'] = subprocess.check_output(['hostname'], text=True).strip()
        except:
            metrics['hostname'] = 'unknown'
        
        # Kernel
        try:
            metrics['kernel'] = subprocess.check_output(['uname', '-r'], text=True).strip()
        except:
            metrics['kernel'] = 'unknown'
        
        # Uptime
        try:
            uptime_output = subprocess.check_output(['uptime', '-p'], text=True).strip()
            # Remove "up " prefix
            metrics['uptime'] = uptime_output.replace('up ', '') if uptime_output.startswith('up ') else uptime_output
        except:
            metrics['uptime'] = 'unknown'
        
        # CPU usage
        try:
            # Get CPU usage from top (percentage of CPU time spent in user and system modes)
            cpu_line = subprocess.check_output(['top', '-bn1'], text=True)
            # Extract the line with Cpu(s)
            for line in cpu_line.split('\n'):
                if line.strip().startswith('Cpu(s)'):
                    # Format: "Cpu(s):  5.2%us,  1.3%sy,  0.0%ni, 92.8%id,  0.0%wa,  0.3%hi,  0.2%si,  0.0%st"
                    parts = line.split(':')[1].strip().split(',')
                    user_part = parts[0].strip()  # e.g., "5.2%us"
                    system_part = parts[1].strip() # e.g., "1.3%sy"
                    user_pct = float(user_part.replace('%us', ''))
                    system_pct = float(system_part.replace('%sy', ''))
                    metrics['cpu_usage'] = round(user_pct + system_pct, 1)
                    break
            else:
                metrics['cpu_usage'] = 0.0
        except:
            metrics['cpu_usage'] = 0.0
        
        # Memory usage
        try:
            mem_info = subprocess.check_output(['free'], text=True)
            lines = mem_info.strip().split('\n')
            for line in lines:
                if line.startswith('Mem:'):
                    parts = line.split()
                    total_kb = int(parts[1])
                    used_kb = int(parts[2])
                    free_kb = int(parts[3])
                    
                    # Convert to human readable
                    def format_bytes(kb):
                        if kb >= 1024*1024:
                            return f"{kb/(1024*1024):.1f}G"
                        elif kb >= 1024:
                            return f"{kb/1024:.1f}M"
                        else:
                            return f"{kb}K"
                    
                    metrics['memory'] = {
                        'total': format_bytes(total_kb),
                        'used': format_bytes(used_kb),
                        'free': format_bytes(free_kb),
                        'percent': round((used_kb / total_kb) * 100, 1)
                    }
                    break
        except:
            metrics['memory'] = {'total': '0K', 'used': '0K', 'free': '0K', 'percent': 0}
        
        # Disk usage
        try:
            df_output = subprocess.check_output(['df', '/'], text=True)
            lines = df_output.strip().split('\n')
            for line in lines[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    total_kb = int(parts[1])
                    used_kb = int(parts[2])
                    free_kb = int(parts[3])
                    
                    # Convert to human readable
                    def format_bytes(kb):
                        if kb >= 1024*1024:
                            return f"{kb/(1024*1024):.1f}G"
                        elif kb >= 1024:
                            return f"{kb/1024:.1f}M"
                        else:
                            return f"{kb}K"
                    
                    metrics['disk'] = {
                        'total': format_bytes(total_kb),
                        'used': format_bytes(used_kb),
                        'free': format_bytes(free_kb),
                        'percent': round((used_kb / total_kb) * 100, 1)
                    }
                    break
        except:
            metrics['disk'] = {'total': '0K', 'used': '0K', 'free': '0K', 'percent': 0}
        
        # Load average
        try:
            load_avg = subprocess.check_output(['uptime'], text=True)
            # Extract load average from uptime output
            # Format: " 12:34:56 up 2 days,  3:45,  1 user,  load average: 0.50, 0.60, 0.70"
            if 'load average:' in load_avg:
                load_part = load_avg.split('load average:')[1].strip()
                loads = [float(x.strip()) for x in load_part.split(',')]
                metrics['load_avg'] = loads
            else:
                metrics['load_avg'] = [0.0, 0.0, 0.0]
        except:
            metrics['load_avg'] = [0.0, 0.0, 0.0]
        
        # Process count
        try:
            ps_output = subprocess.check_output(['ps', 'aux'], text=True)
            # Count lines minus header
            process_count = len(ps_output.strip().split('\n')) - 1
            metrics['process_count'] = process_count
        except:
            metrics['process_count'] = 0
        
        # Timestamp
        metrics['timestamp'] = subprocess.check_output(['date'], text=True).strip()
        
        return metrics
    
    def collect_recent_logs(self):
        """Collect recent log entries from log files"""
        logs = []
        log_files = ['cpu.log', 'memory.log', 'backup.log', 'disk-cleanup.log']
        
        for log_file in log_files:
            log_path = os.path.join(LOGS_DIR, log_file)
            if os.path.exists(log_path):
                try:
                    with open(log_path, 'r') as f:
                        lines = f.readlines()
                        # Get last 5 lines from each log file
                        for line in lines[-5:]:
                            if line.strip():
                                logs.append({
                                    'file': log_file,
                                    'line': line.strip(),
                                    'timestamp': self.extract_timestamp(line)
                                })
                except:
                    pass  # Skip if we can't read the file
        
        # Sort by timestamp (newest first) - simple approach: just reverse
        # For a more accurate sort, we'd need to parse timestamps properly
        logs.reverse()
        return logs[:20]  # Return last 20 entries total
    
    def extract_timestamp(self, log_line):
        """Try to extract timestamp from log line"""
        # Assuming format like: "2026-05-24 12:00:00 CPU Usage: 45.0%"
        parts = log_line.split(' ', 2)
        if len(parts) >= 2:
            return f"{parts[0]} {parts[1]}"
        return ""
    
    def log_message(self, format, *args):
        """Override to suppress default logging"""
        pass

if __name__ == "__main__":
    # Change to the monitoring directory
    os.chdir(PROJECT_ROOT)
    
    with socketserver.TCPServer(("", PORT), MonitoringHandler) as httpd:
        print(f"Monitoring dashboard serving at http://localhost:{PORT}")
        print(f"API metrics: http://localhost:{PORT}/api/metrics")
        print(f"API logs: http://localhost:{PORT}/api/logs")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()