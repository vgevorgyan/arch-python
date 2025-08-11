from enum import Enum


class CPU(Enum):
    Intel = 1
    AMD = 2


class DiskAction:
    Create = 1
    Mount = 2


class PartitionType:
    Efi = 1
    Boot = 2
    Swap = 3
    LuksLvm2 = 4


NVIDIA_OPEN_DRIVER = [
    "linux-headers",
    "nvidia-open-dkms",
    "nvidia-utils",
    "egl-wayland",
    "nvidia-settings",
]

HYPRLAND_PACKAGES = [
    "hyprland",
    "hyprpaper",
    "hyprlock",
    "xdg-desktop-portal-hyprland",
    "xorg-xwayland",
    "polkit",
    "wayland",
    "wayland-protocols",
    "mako",
    "waybar",
    "wofi",
    "wl-clipboard",
    "grim",
    "slurp",
    "brightnessctl",
    "power-profiles-daemon",
    "kitty",
    "sddm",
    "uwsm",
]

HYPRLAND_OPTIONAL_PACKAGES = [
    "xdg-desktop-portal",
    "xdg-desktop-portal-gtk",
    "ttf-jetbrains-mono-nerd",
    "noto-fonts",
    "noto-fonts-emoji",
    "nautilus",
    "gvfs",
    "gvfs-mtp",
    "gvfs-afc",
    "gvfs-smb",
    "sushi",
    "file-roller",
    "paru",
]

ADDITIONAL_PACKAGES = [
    "fish",
    "starship",
    "fzf",
    "zoxide",
    "eza",
    "bat",
    "fd",
    "neovim",
]

PIPEWIRE_PACKAGES = [
    "pipewire",
    "pipewire-pulse",
    "wireplumber",
    "pipewire-jack",
    "pamixer",
    "pavucontrol",
]
