#!/bin/bash

# ============================================================================
# Name        : system_diagnostics.sh
# Description : Linux system diagnostics and health check utility
# Author      : Mallikarjuna
# Version     : 1.0
# ============================================================================

set -o errexit
set -o nounset
set -o pipefail

# ============================================================================
# GLOBAL VARIABLES
# ============================================================================

readonly LOG_FILE="/var/log/system_diagnostics.log"
readonly DISK_THRESHOLD=80

readonly SERVICES=(
  "nginx"
  "ssh"
  "cron"
)

readonly API_ENDPOINTS=(
  "https://api.github.com"
  "https://google.com"
)

# ============================================================================
# LOGGING FUNCTIONS
# ============================================================================

log_info() {
  local message="$1"
  echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] ${message}" | tee -a "${LOG_FILE}"
}

log_warn() {
  local message="$1"
  echo "$(date '+%Y-%m-%d %H:%M:%S') [WARN] ${message}" | tee -a "${LOG_FILE}"
}

log_error() {
  local message="$1"
  echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] ${message}" | tee -a "${LOG_FILE}"
}

# ============================================================================
# ERROR HANDLING
# ============================================================================

handle_error() {
  local exit_code="$1"
  local line_number="$2"

  log_error "Script failed at line ${line_number} with exit code ${exit_code}"
  exit "${exit_code}"
}

trap 'handle_error $? $LINENO' ERR

# ============================================================================
# DISK UTILIZATION CHECK
# ============================================================================

check_disk_space() {
  log_info "Checking disk utilization..."

  local usage
  usage=$(df / | awk 'NR==2 {gsub("%",""); print $5}')

  log_info "Current disk utilization: ${usage}%"

  if [[ "${usage}" -ge "${DISK_THRESHOLD}" ]]; then
    log_warn "Disk utilization exceeded threshold (${DISK_THRESHOLD}%)"

    cleanup_logs_and_temp
  else
    log_info "Disk utilization within acceptable limit"
  fi
}

# ============================================================================
# CLEANUP FUNCTION
# ============================================================================

cleanup_logs_and_temp() {
  log_info "Starting cleanup of /var/log and /tmp"

  find /var/log -type f -name "*.log" -mtime +7 -exec truncate -s 0 {} \;
  find /tmp -type f -mtime +2 -delete

  log_info "Cleanup completed successfully"
}

# ============================================================================
# SYSTEMD SERVICE CHECK
# ============================================================================

check_services() {
  log_info "Checking systemd services..."

  for service in "${SERVICES[@]}"; do
    if systemctl is-active --quiet "${service}"; then
      log_info "Service '${service}' is running"
    else
      log_error "Service '${service}' is NOT running"
    fi
  done
}

# ============================================================================
# SYSLOG ERROR ANALYSIS
# ============================================================================

check_syslog_errors() {
  log_info "Checking syslog for ERROR entries in last hour..."

  local current_hour
  current_hour=$(date '+%b %e %H')

  local errors
  errors=$(grep "${current_hour}" /var/log/syslog | grep "ERROR" || true)

  if [[ -n "${errors}" ]]; then
    log_warn "Errors found in syslog:"
    echo "${errors}" | tee -a "${LOG_FILE}"
  else
    log_info "No ERROR entries found in syslog for the last hour"
  fi
}

# ============================================================================
# API CONNECTIVITY CHECK
# ============================================================================

check_api_connectivity() {
  log_info "Checking external API connectivity..."

  for api in "${API_ENDPOINTS[@]}"; do

    local http_code
    http_code=$(curl --silent \
      --output /dev/null \
      --write-out "%{http_code}" \
      --max-time 10 \
      "${api}")

    if [[ "${http_code}" == "200" ]]; then
      log_info "API reachable: ${api}"
    else
      log_error "API unreachable: ${api} (HTTP ${http_code})"
    fi
  done
}

# ============================================================================
# SYSTEM INFORMATION
# ============================================================================

print_system_info() {
  log_info "Collecting system information..."

  log_info "Hostname: $(hostname)"
  log_info "Kernel: $(uname -r)"
  log_info "Uptime: $(uptime -p)"
  log_info "Memory Usage:"
  free -h | tee -a "${LOG_FILE}"

  log_info "CPU Load:"
  uptime | tee -a "${LOG_FILE}"
}

# ============================================================================
# MAIN FUNCTION
# ============================================================================

main() {
  log_info "================================================="
  log_info "Starting system diagnostics"
  log_info "================================================="

  print_system_info
  check_disk_space
  check_services
  check_syslog_errors
  check_api_connectivity

  log_info "================================================="
  log_info "System diagnostics completed successfully"
  log_info "================================================="
}

main "$@"
