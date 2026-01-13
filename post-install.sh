#!/usr/bin/env bash

set -euo pipefail

# Get script directory and source common library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# Initialize logging
init_logging "post-install.log"

# Check if NVIDIA GPU is present
has_nvidia_gpu() {
  if lspci | grep -i nvidia >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

# 🧠 Core system & firmware
core=(
  linux
  linux-headers
  sof-firmware
  acpid
)

# 🖥️ Graphics stack (NVIDIA + Wayland) - only if NVIDIA GPU detected
nvidia=(
  nvidia-dkms
  nvidia-utils
  lib32-nvidia-utils
  egl-wayland
)

# 🪟 Wayland, Hyprland & portals
hyprland=(
  hyprland
  xorg-xwayland
  xdg-desktop-portal
  xdg-desktop-portal-hyprland
  xdg-desktop-portal-gtk
  polkit
  hyprpolkitagent
)

# 🧩 Hyprland utilities
hypr_utils=(
  hypridle
  hyprlock
  hyprpaper
  brightnessctl
  power-profiles-daemon
)

# 📊 Bar, notifications & desktop UX
desktop_ui=(
  quickshell
  mako
  wl-clipboard
  cliphist
  grim
  slurp
  playerctl
)

# 🔊 Audio stack (PipeWire)
audio=(
  pipewire
  pipewire-pulse
  pipewire-jack
  wireplumber
  alsa-utils
  pamixer
  pavucontrol
)

# 🌐 Networking
network=(
  networkmanager
  network-manager-applet
)

# 🟦 Bluetooth
bluetooth=(
  bluez
  bluez-utils
  blueman
)

# 🖥️ Display manager
display_manager=(
  sddm
)

# 📁 File manager & storage integration
files=(
  nautilus
  gvfs
  gvfs-mtp
  gvfs-afc
  gvfs-smb
  file-roller
)

# 🔤 Fonts
fonts=(
  ttf-jetbrains-mono-nerd
  noto-fonts
  noto-fonts-emoji
  ttf-nerd-fonts-symbols
)

# 🐚 Shell & CLI productivity
cli=(
  kitty
  fish
  starship
  fzf
  zoxide
  eza
  bat
  fd
  neovim
)

# 🧰 Utilities & maintenance
utils=(
  reflector
  jq
)

# 🚀 Optional Qt support
qt=(
  qt6-wayland
  qt5-wayland
)

# Function to update system
update_system() {
  info "Updating system ..."
  sudo pacman -Syyyyu --noconfirm || error "Failed to update system"
}

# Function to install packages
install_packages() {
  local packages=("$@")
  if [[ ${#packages[@]} -eq 0 ]]; then
    return 0
  fi

  info "Installing packages: ${packages[*]}"
  sudo pacman -S --needed --noconfirm "${packages[@]}" || warn "Some packages failed to install"
}

# Main installation function
install_all_packages() {
  info "Installing core packages ..."

  # Always install core packages
  install_packages "${core[@]}"

  # Conditionally install NVIDIA packages
  if has_nvidia_gpu; then
    info "NVIDIA GPU detected, installing NVIDIA drivers ..."
    install_packages "${nvidia[@]}"
  else
    warn "No NVIDIA GPU detected, skipping NVIDIA drivers"
  fi

  # Install remaining packages
  install_packages "${hyprland[@]}"
  install_packages "${hypr_utils[@]}"
  install_packages "${desktop_ui[@]}"
  install_packages "${audio[@]}"
  install_packages "${network[@]}"
  install_packages "${bluetooth[@]}"
  install_packages "${display_manager[@]}"
  install_packages "${files[@]}"
  install_packages "${fonts[@]}"
  install_packages "${cli[@]}"
  install_packages "${utils[@]}"
  install_packages "${qt[@]}"
}

# Configure local pacman repository
configure_pacman_repo() {
  info "Configuring local pacman repository ..."
  backup_config "/etc/pacman.conf"

  # Check if repo already exists
  if grep -q "\[myrepo\]" /etc/pacman.conf 2>/dev/null; then
    warn "Local repository already configured, skipping ..."
    return 0
  fi

  sudo tee -a /etc/pacman.conf >/dev/null <<'EOF'

[myrepo]
SigLevel = Optional TrustAll
Server = file:///home/data/repo
EOF
  info "Local repository configured"
}

# Configure SDDM
configure_sddm() {
  info "Enabling and configuring SDDM service ..."
  install_packages sddm-eucalyptus-drop

  backup_config "/etc/sddm.conf"

  sudo tee /etc/sddm.conf >/dev/null <<'EOF'
[General]
DisplayServer=wayland

[Theme]
Current=eucalyptus-drop
EOF

  sudo systemctl enable sddm || warn "Failed to enable SDDM"
  info "SDDM configured and enabled"
}

# Configure reflector
configure_reflector() {
  info "Configuring and enabling reflector ..."
  sudo mkdir -p /etc/xdg/reflector
  backup_config "/etc/xdg/reflector/reflector.conf"

  sudo tee /etc/xdg/reflector/reflector.conf >/dev/null <<'EOF'
--country Germany,Armenia,Russia,Georgia
--age 12
--protocol https
--sort rate
--save /etc/pacman.d/mirrorlist
EOF

  sudo systemctl enable --now reflector.timer || warn "Failed to enable reflector timer"
  info "Reflector configured and enabled"
}

# Configure NVIDIA environment variables
configure_nvidia_env() {
  if ! has_nvidia_gpu; then
    warn "No NVIDIA GPU detected, skipping NVIDIA environment configuration"
    return 0
  fi

  info "Setting NVIDIA environment variables ..."
  mkdir -p ~/.config/environment.d/

  cat <<'EOF' >~/.config/environment.d/envvars.conf
WLR_NO_HARDWARE_CURSORS=1
LIBVA_DRIVER_NAME=nvidia
GBM_BACKEND=nvidia-drm
__GLX_VENDOR_LIBRARY_NAME=nvidia
WLR_RENDERER=vulkan
EOF

  info "NVIDIA environment variables configured"
}

# Configure UWSM
configure_uwsm() {
  info "Installing and setting up UWSM ..."
  install_packages uwsm

  sudo mkdir -p /usr/share/wayland-sessions
  backup_config "/usr/share/wayland-sessions/hyprland-uwsm.desktop"

  sudo tee /usr/share/wayland-sessions/hyprland-uwsm.desktop >/dev/null <<'EOF'
[Desktop Entry]
Name=Hyprland (UWSM)
Comment=Hyprland via Universal Wayland Session Manager
Exec=uwsm start start-hyprland
Type=Application
EOF

  info "UWSM configured"
}

# Change default shell
configure_shell() {
  info "Changing default shell to fish ..."
  if command -v fish >/dev/null 2>&1; then
    chsh -s /usr/bin/fish || warn "Failed to change shell (may require logout/login)"
    info "Default shell changed to fish"
  else
    warn "fish shell not found, skipping shell change"
  fi
}

# Main execution
main() {
  info "Starting post-install configuration ..."
  info "Log file: $LOG_FILE"

  update_system
  install_all_packages
  configure_pacman_repo
  configure_sddm
  configure_reflector
  configure_nvidia_env
  configure_uwsm
  configure_shell

  info "Post-install configuration completed successfully!"
  info "Please reboot your system to apply all changes."
}

# Run main function
main "$@"
