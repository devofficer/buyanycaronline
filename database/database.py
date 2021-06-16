from pymongo import MongoClient


class DataBase:
    __instance = None

    @staticmethod
    def getInstance():
        if DataBase.__instance is None:
            DataBase()
        return DataBase.__instance

    def __init__(self, ):
        if DataBase.__instance is not None:
            raise Exception("This class is a DataBase!")
        else:
            client = MongoClient("mongodb://localhost:27017")
            db = client['buyanycaronline']
            DataBase.__instance = db

    @staticmethod
    def user_collection():
        db = DataBase.getInstance()
        return db["users"]

    @staticmethod
    def advertisement_collection():
        db = DataBase.getInstance()
        return db["advertisements"]

    @staticmethod
    def image_collection():
        db = DataBase.getInstance()
        return db["images"]
