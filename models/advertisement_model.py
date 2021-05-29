from enum import Enum


class Advertisement():
    def __init__(self, adType: int = -1, title: str = "", price: int = 0, decription: str = "", owner: str = ""):
        self.__title = title
        self.__price = price
        self.__description = decription
        self.__status = 0
        self.__owner = owner
        self.__adType = adType

    def get_title(self):
        return self.__title

    def set_title(self, val: str):
        self.__title = val

    def get_price(self):
        return self.__price

    def set_price(self, val: int):
        self.__price = val

    def get_description(self):
        return self.__description

    def set_description(self, val: str):
        self.__description = val

    def get_status(self):
        return self.__status

    def set_status(self, val: int):
        self.__status = val

    def get_owner(self):
        return self.__owner

    def set_owner(self, val: str):
        self.__owner = val

    def get_adType(self):
        return self.__adType

    def set_adType(self, val: int):
        self.__adType = val
