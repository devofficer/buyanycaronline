import configparser
import datetime


class ConfigFile:
    __instance = None

    @staticmethod
    def getInstance():
        if ConfigFile.__instance is None:
            ConfigFile()
        return ConfigFile.__instance

    def __init__(self, ):
        if ConfigFile.__instance is not None:
            raise Exception("This class is a DataBase!")
        else:
            parser = configparser.ConfigParser()
            parser.read("./app.conf")
            ConfigFile.__instance = parser


class IDGenerator:
    @staticmethod
    def generate_ID():
        now = str(datetime.datetime.now().timestamp()).split(".")
        return now[0]+"-"+now[1]
