from enum import Enum


class AdvertisementTypes(Enum):
    CAR = 0
    HEAVY = 1
    MOTORCYCLE = 2
    BOAT = 3


class AdvertisementStatus(Enum):
    UNDER_PROCESS = 0
    APPROVED = 1
    SOLD = 2

