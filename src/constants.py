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
