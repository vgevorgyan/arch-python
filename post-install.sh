#!/usr/bin/env bash

NVIDIA_OPEN_DRIVER=("linux-headers" "nvidia-open-dkms" "nvidia-utils" "egl-wayland" "nvidia-settings")

HYPRLAND_PACKAGES=(
  "hyprland"
  "hyprpaper"
  "hyprlock"
  "xdg-desktop-portal-hyprland"
  "xorg-xwayland"
  "polkit"
  "wayland"
  "wayland-protocols"
  "mako"
  "waybar"
  "wofi"
  "wl-clipboard"
  "grim"
  "slurp"
  "brightnessctl"
  "power-profiles-daemon"
  "kitty"
  "sddm"
)

HYPRLAND_OPTIONAL_PACKAGES=(
  "xdg-desktop-portal"
  "xdg-desktop-portal-gtk"
  "ttf-jetbrains-mono-nerd"
  "noto-fonts"
  "noto-fonts-emoji"
  "nautilus"
  "gvfs"
  "gvfs-mtp"
  "gvfs-afc"
  "gvfs-smb"
  "sushi"
  "file-roller"
)

ADDITIONAL_PACKAGES=(
  "fish"
  "starship"
  "fzf"
  "zoxide"
  "eza"
  "bat"
  "fd"
  "neovim"
  "reflector"
)

PIPEWIRE_PACKAGES=(
  "pipewire"
  "pipewire-pulse"
  "wireplumber"
  "pipewire-jack"
  "pamixer"
  "pavucontrol"
)
ALL_PACKAGES=("${NVIDIA_OPEN_DRIVER[@]}" "${HYPRLAND_PACKAGES[@]}" "${HYPRLAND_OPTIONAL_PACKAGES[@]}" "${PIPEWIRE_PACKAGES[@]}" "${ADDITIONAL_PACKAGES[@]}")

echo "+++++++ Updating system ..."
sudo pacman -Syyyyu --noconfirm

echo "+++++++ Installing core packages ..."
sudo pacman -S --needed --noconfirm -- "${ALL_PACKAGES[@]}"

echo "+++++++ Configuring local pacman repository ..."
sudo tee -a /etc/pacman.conf >/dev/null <<'EOF'

[myrepo]
SigLevel = Optional TrustAll
Server = file:///home/data/repo
EOF

echo "+++++++ Enabling and configuring SDDM service ..."
sudo pacman -Sy --needed --noconfirm sddm-eucalyptus-drop
echo "[General]" | sudo tee /etc/sddm.conf
echo "DisplayServer=wayland" | sudo tee -a /etc/sddm.conf
echo "[Theme]" | sudo tee -a /etc/sddm.conf
echo "Current=eucalyptus-drop" | sudo tee -a /etc/sddm.conf
sudo systemctl enable sddm

echo "+++++++ Configure and enable reflector"
sudo tee /etc/xdg/reflector/reflector.conf >/dev/null <<'EOF'
--country Armenia,Russia,Georgia
--age 12
--protocol https
--sort rate
--save /etc/pacman.d/mirrorlist
EOF
sudo systemctl enable --now reflector.timer

echo "+++++++ Setting NVIDIA env vars"
mkdir -p ~/.config/environment.d/
cat <<'EOF' >~/.config/environment.d/envvars.conf
WLR_NO_HARDWARE_CURSORS=1
LIBVA_DRIVER_NAME=nvidia
GBM_BACKEND=nvidia-drm
__GLX_VENDOR_LIBRARY_NAME=nvidia
WLR_RENDERER=vulkan
EOF

sudo pacman -Sy --noconfirm uwsm

echo "+++++++ Setting up UWSM ..."
sudo tee /usr/share/wayland-sessions/hyprland-uwsm.desktop >/dev/null <<'EOF'
[Desktop Entry]
Name=Hyprland (UWSM)
Comment=Hyprland via Universal Wayland Session Manager
Exec=uwsm start Hyprland
Type=Application
EOF

chsh -s /usr/bin/fish

echo "The new system mainly installed and configured. Please reboot."
