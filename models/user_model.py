import binascii
import hashlib
import os


class User:
    def __init__(self, username: str = "", role: int = 2, hashed: str = "", mobile: int = 0, city: str = "",
                 country: str = ""):
        self.__username = username
        self.__role = role
        self.__hashed = hashed
        self.__mobile = mobile
        self.__city = city
        self.__country = country
        self.__salt = ""

    def get_username(self):
        return self.__username

    def set_username(self, val: str):
        self.__username = val

    def get_role(self):
        return self.__role

    def set_role(self, val: int):
        self.__role = val

    def get_mobile(self):
        return self.__mobile

    def set_mobile(self, val: int):
        self.__mobile = val

    def get_hash(self):
        return self.__hashed

    def set_hash(self, hashed: str):
        self.__salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', hashed.encode('utf-8'), self.__salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        self.__hashed = pwdhash.decode('ascii')
        self.__salt = self.__salt.decode('ascii')

    def validate_hash(self, provided_password: str):
        """Verify a stored password against one provided by user"""
        salt = self.__salt.encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      self.__salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == self.__hashed

    def get_city(self):
        return self.__city

    def set_city(self, val: str):
        self.__city = val

    def get_country(self):
        return self.__country

    def set_country(self, val: str):
        self.__country = val

    def __str__(self) -> str:
        return self.__username + " " + str(self.__type) + " " + self.__hashed + " " \
               + self.__city + " " + self.__country + " " + str(self.__mobile)
