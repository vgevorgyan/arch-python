#!/usr/bin/env bash

set -euo pipefail

# Get script directory and source common library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# Initialize logging
init_logging "configure.log"

# Check if data directory exists
check_data_directory() {
  local data_dir="/home/data"
  if [[ ! -d "$data_dir" ]]; then
    error "Data directory $data_dir does not exist. Please ensure it is mounted."
  fi
  info "Data directory $data_dir found"
}

# Create symlink for a folder
create_symlink() {
  local folder="$1"
  local source_dir="/home/data/$folder"
  local target_dir="$HOME/$folder"
  
  # Check if source directory exists
  if [[ ! -d "$source_dir" ]]; then
    warn "Source directory $source_dir does not exist, creating it ..."
    mkdir -p "$source_dir" || error "Failed to create directory $source_dir"
  fi
  
  # Remove existing symlink or directory
  if [[ -L "$target_dir" ]]; then
    info "Removing existing symlink: $target_dir"
    rm -f "$target_dir" || error "Failed to remove symlink $target_dir"
  elif [[ -e "$target_dir" ]]; then
    warn "Removing existing directory/file: $target_dir"
    rm -rf "$target_dir" || error "Failed to remove $target_dir"
  fi
  
  # Create new symlink
  info "Creating symlink: $target_dir -> $source_dir"
  ln -s "$source_dir" "$target_dir" || error "Failed to create symlink from $target_dir to $source_dir"
  info "Successfully created symlink for $folder"
}

# Create all symlinks
create_symlinks() {
  local folders=("Documents" "Downloads" "Projects" "Pictures")
  
  info "Starting symlink creation ..."
  check_data_directory
  
  for folder in "${folders[@]}"; do
    create_symlink "$folder"
  done
  
  info "All symlinks created successfully!"
}

# Main execution
main() {
  info "Starting directory configuration ..."
  info "Log file: $LOG_FILE"
  
  cd "$HOME" || error "Failed to change to home directory"
  create_symlinks
  
  info "Directory configuration completed successfully!"
}

# Run main function
main "$@"
