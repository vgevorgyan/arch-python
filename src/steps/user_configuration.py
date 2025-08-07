import os
from datetime import datetime

from ..config import config
from ..helpers.utils import run_chroot_command, run_command


def user_configuration():
    username = config["user"]["username"]
    home = config["user"]["home"]

    print("Configuring user ...")
    if os.path.isdir("/mnt" + home):
        print("Found old user home directory, backuping.")
        os.rename(
            "/mnt" + home, "/mnt" + home + "-" + datetime.now().strftime("%Y%m%d%H%M%S")
        )

    run_chroot_command(["groupadd", "-g", "1000", username])
    run_chroot_command(["useradd", "-m", "-g", "1000", "-u", "1000", username])
    run_chroot_command(["usermod", "-aG", "wheel,audio,optical,storage", username])
    run_command("genfstab -pU /mnt >> /mnt/etc/fstab", shell=True)
    print("+++++ Need to set passwords for root and new user.")
