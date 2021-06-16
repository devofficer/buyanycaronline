from sanic import json, Blueprint, response
from database.advertisement_collection import AdvertisementDB
from database.image_collection import ImageDB
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


@car_blue_print.post("/vehicle/car/<car_id>/image")
@Authenticated()
async def create_car_image(request, car_id):
    files = request.files['files']
    payload = await decode_jwt_and_get_payload(request)

    db_car = AdvertisementDB.get_advertisement_by_id(car_id)
    if db_car.get_adType() != AdvertisementTypes.CAR.value:
        return json({"Message": "Error, is not a car"})
    if db_car.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})

    car_images = db_car.get_images()

    for _file in files:
        if _file.type not in ['image/jpeg', 'image/png']:
            return json({"Message": "Error, image must be a JPEG file."})

    for _file in files:
        img_id = ImageDB.create_image(_file, "car", car_id)
        car_images.append({'_id': str(img_id)})

    db_car.set_images(car_images)

    message = AdvertisementDB.update_advertisement(db_car, car_id)

    return json({"Message": message})


@car_blue_print.delete("/vehicle/car/<car_id>/image/<image_id>")
@Authenticated()
async def remove_car_image(request, car_id, image_id):
    payload = await decode_jwt_and_get_payload(request)

    db_car = AdvertisementDB.get_advertisement_by_id(car_id)
    if db_car.get_adType() != AdvertisementTypes.CAR.value:
        return json({"Message": "Error, is not a car"})
    if db_car.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})

    car_images = db_car.get_images()
    new_list = []

    for car_image in car_images:
        if car_image['_id'] != image_id:
            new_list.append(car_image)

    db_car.set_images(new_list)

    message = AdvertisementDB.update_advertisement(db_car, car_id)

    return json({"Message": message})


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


@car_blue_print.post("/vehicle/heavy/<heavy_id>/image")
@Authenticated()
async def create_heavy_image(request, heavy_id):
    files = request.files['files']
    payload = await decode_jwt_and_get_payload(request)

    db_heavy = AdvertisementDB.get_advertisement_by_id(heavy_id)
    if db_heavy.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    if db_heavy.get_adType() != AdvertisementTypes.HEAVY.value:
        return json({"Message": "Error, is not a heavy vehicle"})

    images = db_heavy.get_images()

    for _file in files:
        if _file.type not in ['image/jpeg', 'image/png']:
            return json({"Message": "Error, image must be a JPEG file."})

    for _file in files:
        img_id = ImageDB.create_image(_file, "heavy", heavy_id)
        images.append({'_id': str(img_id)})

    db_heavy.set_images(images)

    message = AdvertisementDB.update_advertisement(db_heavy, heavy_id)

    return json({"Message": message})


@car_blue_print.delete("/vehicle/heavy/<heavy_id>/image/<image_id>")
@Authenticated()
async def remove_heavy_image(request, heavy_id, image_id):
    payload = await decode_jwt_and_get_payload(request)

    db_heavy = AdvertisementDB.get_advertisement_by_id(heavy_id)
    if db_heavy.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    if db_heavy.get_adType() != AdvertisementTypes.HEAVY.value:
        return json({"Message": "Error, is not a heavy vehicle"})

    images = db_heavy.get_images()
    new_list = []

    for _image in images:
        if _image['_id'] != image_id:
            new_list.append(_image)

    db_heavy.set_images(images)
    message = AdvertisementDB.update_advertisement(db_heavy, heavy_id)

    return json({"Message": message})


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


@car_blue_print.post("/vehicle/boat/<boat_id>/image")
@Authenticated()
async def create_boat_image(request, boat_id):
    files = request.files['files']
    payload = await decode_jwt_and_get_payload(request)

    db_boat = AdvertisementDB.get_advertisement_by_id(boat_id)
    if db_boat.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    if db_boat.get_adType() != AdvertisementTypes.BOAT.value:
        return json({"Message": "Error, is not a boat"})

    images = db_boat.get_images()

    for _file in files:
        if _file.type not in ['image/jpeg', 'image/png']:
            return json({"Message": "Error, image must be a JPEG file."})

    for _file in files:
        img_id = ImageDB.create_image(_file, "boat", boat_id)
        images.append({'_id': str(img_id)})

    db_boat.set_images(images)

    message = AdvertisementDB.update_advertisement(db_boat, boat_id)

    return json({"Message": message})


@car_blue_print.delete("/vehicle/boat/<boat_id>/image/<image_id>")
@Authenticated()
async def remove_boat_image(request, boat_id, image_id):
    payload = await decode_jwt_and_get_payload(request)

    db_boat = AdvertisementDB.get_advertisement_by_id(boat_id)
    if db_boat.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    if db_boat.get_adType() != AdvertisementTypes.BOAT.value:
        return json({"Message": "Error, is not a boat"})

    images = db_boat.get_images()
    new_list = []

    for _image in images:
        if _image['_id'] != image_id:
            new_list.append(_image)

    db_boat.set_images(images)
    message = AdvertisementDB.update_advertisement(db_boat, boat_id)

    return json({"Message": message})


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


@car_blue_print.post("/vehicle/motorcycle/<motorcycle_id>/image")
@Authenticated()
async def create_motorcycle_image(request, motorcycle_id):
    files = request.files['files']
    payload = await decode_jwt_and_get_payload(request)

    db_motorcycle = AdvertisementDB.get_advertisement_by_id(motorcycle_id)
    if db_motorcycle.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    if db_motorcycle.get_adType() != AdvertisementTypes.MOTORCYCLE.value:
        return json({"Message": "Error, is not a motorcycle"})

    images = db_motorcycle.get_images()

    for _file in files:
        if _file.type not in ['image/jpeg', 'image/png']:
            return json({"Message": "Error, image must be a JPEG file."})

    for _file in files:
        img_id = ImageDB.create_image(_file, "motorcycle", motorcycle_id)
        images.append({'_id': str(img_id)})

    db_motorcycle.set_images(images)

    message = AdvertisementDB.update_advertisement(db_motorcycle, motorcycle_id)

    return json({"Message": message})


@car_blue_print.delete("/vehicle/motorcycle/<motorcycle_id>/image/<image_id>")
@Authenticated()
async def remove_motorcycle_image(request, motorcycle_id, image_id):
    payload = await decode_jwt_and_get_payload(request)

    db_motorcycle = AdvertisementDB.get_advertisement_by_id(motorcycle_id)
    if db_motorcycle.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    if db_motorcycle.get_adType() != AdvertisementTypes.MOTORCYCLE.value:
        return json({"Message": "Error, is not a motorcycle"})

    images = db_motorcycle.get_images()
    new_list = []

    for _image in images:
        if _image['_id'] != image_id:
            new_list.append(_image)

    db_motorcycle.set_images(images)
    message = AdvertisementDB.update_advertisement(db_motorcycle, motorcycle_id)

    return json({"Message": message})


@car_blue_print.get("/vehicle/image/<image_id>")
async def get_vehicle_image(request, image_id):
    image_id = str(image_id).replace('.jpeg', '')
    image = ImageDB.get_image(image_id)

    if image:
        return response.raw(image, content_type='image/jpeg')

    return json({'Message': 'Image not found.'}, 404)



