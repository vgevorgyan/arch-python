#!/usr/bin/env bash

USE_LAST_UWSM=0
UWSM_LINK="https://archive.archlinux.org/packages/u/uwsm/uwsm-0.23.0-1-any.pkg.tar.zst"
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

echo "+++++++ Installing paru ..."
cd /tmp && git clone https://aur.archlinux.org/paru-bin.git
cd /tmp/paru-bin && makepkg -si --noconfirm

cd
echo "+++++++ Enabling PipeWire services ..."
systemctl --user enable --now pipewire pipewire-pulse wireplumber

echo "+++++++ Enabling and configuring SDDM service ..."
paru -Sy --noconfirm sddm-theme-sugar-candy-git
echo "[General]" | sudo tee /etc/sddm.conf
echo "DisplayServer=wayland" | sudo tee -a /etc/sddm.conf
echo "[Theme]" | sudo tee -a /etc/sddm.conf
echo "Current=Sugar-Candy" | sudo tee -a /etc/sddm.conf
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

if ((USE_LAST_UWSM)); then
  sudo pacman -S --noconfirm uwsm
else
  sudo pacman -U --noconfirm $UWSM_LINK
fi

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
