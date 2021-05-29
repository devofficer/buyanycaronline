from sanic import json, Blueprint
from database.advertisement_collection import AdvertisementDB
from database.user_collection import UserDB
from decorators.Auth import decode_jwt_and_get_payload, Authenticated
from common.enums import AdvertisementTypes
from models.vehicle_model import *

car_blue_print = Blueprint("car_blue_print")


async def create_vehicle(request):
    body = request.json
    vehicle_json = body["vehicle"]
    payload = await decode_jwt_and_get_payload(request)
    user = UserDB.get_user_by_id(payload['username'])
    vehicle = Vehicle(owner=user.get_username(), title=vehicle_json["title"],
                      price=vehicle_json["price"], decription=vehicle_json["description"],
                      make=vehicle_json["make"], model=vehicle_json["model"], features=vehicle_json["features"],
                      cylinder=vehicle_json["cylinders"],
                      color=vehicle_json["color"], year=vehicle_json["year"], warranty=vehicle_json["warranty"],
                      fuel=vehicle_json["fuel"],
                      condition=vehicle_json["condition"])
    return vehicle, vehicle_json


async def init_car(request):
    vehicle, vehicle_json = await create_vehicle(request)
    car = Car(hp=vehicle_json["hp"], body_type=vehicle_json["body_type"], trans=vehicle_json["transmission"],
              region=vehicle_json["region"], doors=vehicle_json["num_of_doors"], distance=vehicle_json["distance"])
    for k, v in vehicle.__dict__.items():
        if k not in car.__dict__:
            return json({"Message": "Error: " + str(k) + " is not found"})
        car.__setattr__(k, v)
    car.set_adType(AdvertisementTypes.CAR.value)
    return car


async def init_heavy(request):
    vehicle, vehicle_json = await create_vehicle(request)
    heavy = HeavyVehicle(distance=vehicle_json["distance"], hours=vehicle_json["hours"],
                         heavyType=vehicle_json["heavy_type"])
    for k, v in vehicle.__dict__.items():
        if k not in heavy.__dict__:
            return json({"Message": "Error: " + str(k) + " is not found"})
        heavy.__setattr__(k, v)
    heavy.set_adType(AdvertisementTypes.HEAVY.value)
    return heavy


async def init_boat(request):
    vehicle, vehicle_json = await create_vehicle(request)
    boat = Boat(length=vehicle_json["length"], typed=vehicle_json["typed"], sub_type=vehicle_json["subType"],
                hours=vehicle_json["hours"])
    for k, v in vehicle.__dict__.items():
        if k not in boat.__dict__:
            return json({"Message": "Error: " + str(k) + " is not found"})
        boat.__setattr__(k, v)
    boat.set_adType(AdvertisementTypes.BOAT.value)
    return boat


async def init_motorcycle(request):
    vehicle, vehicle_json = await create_vehicle(request)
    motorcycle = MotorCycle(engine_size=vehicle_json["engineSize"], hours=vehicle_json["hours"])
    for k, v in vehicle.__dict__.items():
        if k not in motorcycle.__dict__:
            return json({"Message": "Error: " + str(k) + " is not found"})
        motorcycle.__setattr__(k, v)
    motorcycle.set_adType(AdvertisementTypes.MOTORCYCLE.value)
    return motorcycle


@car_blue_print.post("/vehicle/car/create")
@Authenticated()
async def create_car(request):
    car = await init_car(request)
    return json({"Message": AdvertisementDB.create_advertisement(car)})


@car_blue_print.post("/vehicle/car/update")
@Authenticated()
async def update_car(request):
    body = request.json["vehicle"]
    payload = await decode_jwt_and_get_payload(request)
    car = await init_car(request)
    db_car = AdvertisementDB.get_advertisement_by_id(body["id"])
    if db_car.get_adType() != AdvertisementTypes.CAR.value:
        return json({"Message": "Error, is not a car"})
    if db_car.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    for k, v in car.__dict__.items():
        if "owner" in k or "status" in k or "id" in k:
            continue
        if isinstance(v, str):
            v.strip()
        db_car.__setattr__(k, v)
    return json({"Message": AdvertisementDB.update_advertisement(db_car, body["id"])})


@car_blue_print.post("/vehicle/heavy/create")
@Authenticated()
async def create_heavy(request):
    heavy = await init_heavy(request)
    return json({"Message": AdvertisementDB.create_advertisement(heavy)})


@car_blue_print.post("/vehicle/heavy/update")
@Authenticated()
async def update_heavy(request):
    body = request.json["vehicle"]
    heavy = await init_heavy(request)
    payload = await decode_jwt_and_get_payload(request)
    db_heavy = AdvertisementDB.get_advertisement_by_id(body["id"])
    if db_heavy.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    if db_heavy.get_adType() != AdvertisementTypes.HEAVY.value:
        return json({"Message": "Error, is not a heavy vehicle"})
    for k, v in heavy.__dict__.items():
        if "owner" in k or "status" in k or "id" in k:
            continue
        if isinstance(v, str):
            v.strip()
        db_heavy.__setattr__(k, v)
    return json({"Message": AdvertisementDB.update_advertisement(db_heavy, body["id"])})


@car_blue_print.post("/vehicle/boat/create")
@Authenticated()
async def create_boat(request):
    boat = await init_boat(request)
    return json({"Message": AdvertisementDB.create_advertisement(boat)})


@car_blue_print.post("/vehicle/boat/update")
@Authenticated()
async def update_boat(request):
    body = request.json["vehicle"]
    boat = await init_boat(request)
    payload = await decode_jwt_and_get_payload(request)
    db_boat = AdvertisementDB.get_advertisement_by_id(body["id"])
    if db_boat.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    if db_boat.get_adType() != AdvertisementTypes.BOAT.value:
        return json({"Message": "Error, is not a boat"})
    for k, v in boat.__dict__.items():
        if "owner" in k or "status" in k or "id" in k:
            continue
        if isinstance(v, str):
            v.strip()
        db_boat.__setattr__(k, v)
    return json({"Message": AdvertisementDB.update_advertisement(db_boat, body["id"])})


@car_blue_print.post("/vehicle/motorcycle/create")
@Authenticated()
async def create_motorcycle(request):
    motorcycle = await init_motorcycle(request)
    return json({"Message": AdvertisementDB.create_advertisement(motorcycle)})


@car_blue_print.post("/vehicle/motorcycle/update")
@Authenticated()
async def update_motorcycle(request):
    body = request.json["vehicle"]
    motorcycle = await init_motorcycle(request)
    payload = await decode_jwt_and_get_payload(request)
    db_motorcycle = AdvertisementDB.get_advertisement_by_id(body["id"])
    if db_motorcycle.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    if db_motorcycle.get_adType() != AdvertisementTypes.MOTORCYCLE.value:
        return json({"Message": "Error, is not a motorcycle"})
    for k, v in motorcycle.__dict__.items():
        if "owner" in k or "status" in k or "id" in k:
            continue
        if isinstance(v, str):
            v.strip()
        db_motorcycle.__setattr__(k, v)
    return json({"Message": AdvertisementDB.update_advertisement(db_motorcycle, body["id"])})
