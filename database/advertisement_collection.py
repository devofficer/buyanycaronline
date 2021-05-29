import json
from datetime import datetime

from pymongo.errors import PyMongoError, DuplicateKeyError

from common.enums import AdvertisementTypes, AdvertisementStatus
from models.vehicle_model import *
from database.database import DataBase
from models.class_to_dict import convert_to_dict
from common.utils import IDGenerator


class AdvertisementDB:
    @staticmethod
    def create_advertisement(advertisement: Advertisement):
        try:
            col = DataBase.advertisement_collection()
            data = convert_to_dict(advertisement.__dict__)
            data["_id"] = IDGenerator.generate_ID()
            data["last-modified-date"] = datetime.now().isoformat()
            col.insert_one(data)
        except DuplicateKeyError as e:
            return "Error duplicate key"
        except PyMongoError as e:
            return "Error creating advertisement"
        return "Car advertisement have been successfully created"

    @staticmethod
    def get_advertisement_by_id(id: str):
        record = None
        try:
            col = DataBase.advertisement_collection()
            record = col.find_one({"_id": id})
        except PyMongoError as e:
            print(e)
        if record is not None:
            vehicle = Vehicle(owner=record["owner"], title=record["title"], price=record["price"],
                              decription=record["description"], make=record["make"], model=record["model"],
                              features=record["features"], cylinder=record["cylinders"], color=record["color"],
                              year=record["year"], warranty=record["warranty"], fuel=record["fuelType"],
                              condition=record["condition"])
            if record["adType"] == AdvertisementTypes.CAR.value:
                car = Car(hp=record["hp"], body_type=record["bodyType"], trans=record["transmission"],
                          region=record["region"], doors=record["numOfDoors"], distance=record["distance"])
                for k, v in vehicle.__dict__.items():
                    car.__setattr__(k, v)
                car.set_adType(AdvertisementTypes.CAR.value)
                return car
            if record["adType"] == AdvertisementTypes.HEAVY.value:
                heavy = HeavyVehicle(distance=record["distance"], hours=record["hours"], heavyType=record["heavyType"])
                for k, v in vehicle.__dict__.items():
                    heavy.__setattr__(k, v)
                heavy.set_adType(AdvertisementTypes.HEAVY.value)
                return heavy
            if record["adType"] == AdvertisementTypes.BOAT.value:
                boat = Boat(length=record["length"], hours=record["hours"], typed=record["type"],
                            sub_type=record["subType"])
                for k, v in vehicle.__dict__.items():
                    boat.__setattr__(k, v)
                boat.set_adType(AdvertisementTypes.HEAVY.value)
                return boat
            if record["adType"] == AdvertisementTypes.MOTORCYCLE.value:
                motorcycle = MotorCycle(hours=record["hours"], engine_size=record["engineSize"])
                for k, v in vehicle.__dict__.items():
                    motorcycle.__setattr__(k, v)
                motorcycle.set_adType(AdvertisementTypes.HEAVY.value)
                return motorcycle
        else:
            raise Exception("Can't find an advertisement with that ID.")

    @staticmethod
    def update_advertisement(advertisement: Advertisement, id: str):
        try:
            col = DataBase.advertisement_collection()
            json = convert_to_dict(advertisement.__dict__)
            if "id" in json:
                del json['id']
            col.update_one({"_id": id}, {"$set": json})
        except PyMongoError as e:
            return "Error updating advertisement"
        return "Advertisement have been successfully updated"

    @staticmethod
    def get_unapproved_ads(pageNumber: int, nPerPage: int):
        return AdvertisementDB.get_advertisements({"status": AdvertisementStatus.UNDER_PROCESS.value},
                                                  pageNumber, nPerPage)

    @staticmethod
    def get_advertisements(query: json, pageNumber: int, nPerPage: int):
        data = list()
        try:
            col = DataBase.advertisement_collection()
            records = col.find(query).sort([("last-modified-date", 1)]).skip(
                (pageNumber - 1) * nPerPage if pageNumber > 0 else 0) \
                .limit(nPerPage)
            count = col.estimated_document_count()
            for record in records:
                data.append(record)
            return {"Message": "successfully found data", "data": data, "count": count}
        except PyMongoError as e:
            return {"Message": "Error finding data"}

    @staticmethod
    def approve_advertisement(advertisementID: str):
        try:
            col = DataBase.advertisement_collection()
            col.update_one({"_id": advertisementID}, {"$set": {"status": AdvertisementStatus.APPROVED.value}})
            return "Advertisement have been successfully updated"
        except PyMongoError as e:
            return "Error advertisement not updated"
