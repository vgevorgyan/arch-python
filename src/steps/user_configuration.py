import os

from ..config import config
from ..helpers.utils import run_chroot_command, run_command


def user_configuration():
    username = config["user"]["username"]
    home = config["user"]["home"]

    print("Configuring user ...")
    if os.path.isdir("/mnt" + home):
        print("Home dir exists")
    else:
        print("Home dir NOT exists")

    # run_chroot_command(["groupadd", "-g", "1000", username])
    # run_chroot_command(["useradd", "-m", "-g", "1000", "-u", "1000", username])
