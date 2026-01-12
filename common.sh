#!/usr/bin/env bash

# Common library for installation scripts
# This file contains shared functions and utilities

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize logging
# Usage: init_logging "log_file_name.log"
init_logging() {
  local log_file="${1:-${HOME}/script.log}"
  LOG_FILE="${HOME}/${log_file}"
  exec > >(tee -a "$LOG_FILE") 2>&1
}

# Helper functions for colored output
error() {
  echo -e "${RED}ERROR:${NC} $1" >&2
  exit 1
}

info() {
  echo -e "${GREEN}INFO:${NC} $1"
}

warn() {
  echo -e "${YELLOW}WARN:${NC} $1"
}

# Check if running with sudo
check_sudo() {
  if ! sudo -n true 2>/dev/null; then
    error "This script requires sudo privileges. Please run with sudo or ensure passwordless sudo is configured."
  fi
}

# Backup configuration file
backup_config() {
  local file="$1"
  if [[ -f "$file" ]]; then
    sudo cp "$file" "${file}.bak.$(date +%Y%m%d_%H%M%S)"
  fi
}
