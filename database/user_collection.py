from pymongo.errors import PyMongoError, DuplicateKeyError
from models.user_model import User
from database.database import DataBase
from models.class_to_dict import convert_to_dict


class UserDB:
    @staticmethod
    def create_user(user: User):
        try:
            col = DataBase.user_collection()
            json = convert_to_dict(user.__dict__)
            json["_id"] = user.get_username()
            col.insert_one(json)
        except DuplicateKeyError as e:
            return "User already registered"
        except PyMongoError as e:
            return "Error creating user"
        return "User have been successfully created"

    @staticmethod
    def get_user_by_id(username: str):
        record = None
        try:
            col = DataBase.user_collection()
            record = col.find_one({"_id": username})
        except PyMongoError as e:
            print(e)
        if record is not None:
            user = User()
            for k, v in record.items():
                user.__setattr__("_User__"+k, v)
            return user
        else:
            return User()

    @staticmethod
    def update_user(user: User):
        try:
            col = DataBase.user_collection()
            json = convert_to_dict(user.__dict__)
            if "id" in json:
                del json['id']
            col.update_one({"_id": user.get_username()}, {"$set": json})
        except PyMongoError as e:
            return "Error updating user"
        return "User have been successfully updated"
