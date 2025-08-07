# Create partitions

```bash

sgdisk --zap-all /dev/mapper/vda # Delete all
sgdisk -og /dev/vda # Create GPT partition table

sgdisk -n 1:0:+512MiB -t 1:ef00 -c 1:"EFI" /dev/vda
sgdisk -n 2:0:+1GiB -t 2:8300 -c 2:"boot" /dev/vda
sgdisk -n 3:0:+1GiB -t 3:8200 -c 3:"swap" /dev/vda
sgdisk -n 4:0:0 -t 4:8e00 -c 4:"LVM" /dev/vda

```

```bash
pvcreate /dev/mapper/cryptlvm
vgcreate system /dev/mapper/cryptlvm
lvcreate -L 4G -n data system
lvcreate -L 4G -n home system
lvcreate -l 100%FREE -n root system
```
