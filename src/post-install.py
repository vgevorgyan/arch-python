#!/bin/env python

from .constants import (
    ADDITIONAL_PACKAGES,
    HYPRLAND_OPTIONAL_PACKAGES,
    HYPRLAND_PACKAGES,
    NVIDIA_OPEN_DRIVER,
    PIPEWIRE_PACKAGES,
)
from .helpers.utils import (
    install_packages_new_system,
    run_command,
    run_command_with_output,
)

print("+++++++ Updating system ...")
run_command_with_output(["sudo", "pacman", "-Syyyyu", "--noconfirm"])

print("+++++++ Installing core packages ...")
install_packages_new_system(
    NVIDIA_OPEN_DRIVER
    + HYPRLAND_PACKAGES
    + HYPRLAND_OPTIONAL_PACKAGES
    + PIPEWIRE_PACKAGES
    + ADDITIONAL_PACKAGES
)

print("+++++++ Installing paru ...")
run_command_with_output(
    [
        "sudo",
        "pacman",
        "-S",
        "--noconfirm",
        "--needed",
        "base-devel",
        "rust",
        "clang",
        "pkgconf",
        "cmake",
        "openssl",
        "zlib",
    ]
)
run_command("cd /tmp && git clone https://aur.archlinux.org/paru.git", shell=True)
run_command_with_output("cd /tmp/paru && makepkg -si", shell=True)

print("+++++++ Enabling PipeWire services ...")
run_command_with_output(
    [
        "systemctl",
        "--user",
        "enable",
        "--now",
        "pipewire",
        "pipewire-pulse",
        "wireplumber",
    ]
)

print("+++++++ Enabling SDDM service ...")
run_command_with_output(
    ["sudo", "paru", "-Sy", "--noconfirm", "sddm-theme-sugar-candy-git"]
)
run_command_with_output('echo "[General]" | sudo tee /etc/sddm.conf', shell=True)
run_command_with_output(
    'echo "DisplayServer=wayland" | sudo tee -a /etc/sddm.conf', shell=True
)
run_command_with_output('echo "" | sudo tee -a /etc/sddm.conf', shell=True)
run_command_with_output('echo "[Theme]" | sudo tee -a /etc/sddm.conf', shell=True)
run_command_with_output(
    'echo "Current=sugar-candy" | sudo tee -a /etc/sddm.conf', shell=True
)
run_command_with_output(
    [
        "sudo",
        "systemctl",
        "enable",
        "sddm",
    ]
)

print("+++++++ Setting NVIDIA env vars")
run_command_with_output("mkdir -p ~/.config/environment.d/", shell=True)
run_command_with_output(
    'echo "WLR_NO_HARDWARE_CURSORS=1" > ~/.config/environment.d/envvars.conf',
    shell=True,
)
run_command_with_output(
    'echo "LIBVA_DRIVER_NAME=nvidia" >> ~/.config/environment.d/envvars.conf',
    shell=True,
)
run_command_with_output(
    'echo "GBM_BACKEND=nvidia-drm" >> ~/.config/environment.d/envvars.conf',
    shell=True,
)
run_command_with_output(
    'echo "__GLX_VENDOR_LIBRARY_NAME=nvidia" >> ~/.config/environment.d/envvars.conf',
    shell=True,
)
run_command_with_output(
    'echo "WLR_RENDERER=vulkan" >> ~/.config/environment.d/envvars.conf',
    shell=True,
)

print("+++++++ Setting up UWSM ...")
run_command_with_output(
    'echo "[Desktop Entry]" | sudo tee /usr/share/wayland-sessions/hyprland-uwsm.desktop',
    shell=True,
)
run_command_with_output(
    'echo "Name=Hyprland (UWSM)" | sudo tee -a /usr/share/wayland-sessions/hyprland-uwsm.desktop',
    shell=True,
)
run_command_with_output(
    'echo "Comment=Hyprland via Universal Wayland Session Manager" | sudo tee -a /usr/share/wayland-sessions/hyprland-uwsm.desktop',
    shell=True,
)
run_command_with_output(
    'echo "Exec=uwsm start Hyprland" | sudo tee -a /usr/share/wayland-sessions/hyprland-uwsm.desktop',
    shell=True,
)
run_command_with_output(
    'echo "Type=Application" | sudo tee -a /usr/share/wayland-sessions/hyprland-uwsm.desktop',
    shell=True,
)

run_command_with_output("chsh -s /usr/bin/fish", shell=True)

print("The new system mainly installed and configured. Please reboot.")
