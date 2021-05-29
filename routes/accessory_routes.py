from sanic import json, Blueprint
from database.advertisement_collection import AdvertisementDB
from database.user_collection import UserDB
from decorators.Auth import decode_jwt_and_get_payload, Authenticated
from common.enums import AdvertisementTypes
from models.accessory_model import *

acc_blue_print = Blueprint("acc_blue_print")

async def init_numberplate(request):
    body = request.json
    accessory_json = body["accessory"]
    payload = await decode_jwt_and_get_payload(request)
    user = UserDB.get_user_by_id(payload['username'])
    numberplate = NumberPlate(owner=user.get_username(), title=accessory_json["title"], 
                        price=accessory_json["price"], digits=accessory_json["digits"],
                        decription=accessory_json["description"], adType=AdvertisementTypes.NUMBERPLATE.value)

    return numberplate


@acc_blue_print.post("/accessory/numberplate/create")
@Authenticated()
async def create_numberplate(request):
    numberplate = await init_numberplate(request)
    return json({"Message": AdvertisementDB.create_advertisement(numberplate)})


@acc_blue_print.post("/accessory/numberplate/update")
@Authenticated()
async def update_numberplate(request):
    body = request.json["accessory"]
    numberplate = await init_numberplate(request)
    payload = await decode_jwt_and_get_payload(request)
    db_numberplate = AdvertisementDB.get_advertisement_by_id(body["id"])
    if db_numberplate.get_owner() != payload["username"]:
        return json({"Message": "You are not the owner of this ad"})
    if db_numberplate.get_adType() != AdvertisementTypes.NUMBERPLATE.value:
        return json({"Message": "Error, is not a numberplate"})
    for k, v in numberplate.__dict__.items():
        if "owner" in k or "status" in k or "id" in k:
            continue
        if isinstance(v, str):
            v.strip()
        db_numberplate.__setattr__(k, v)
    return json({"Message": AdvertisementDB.update_advertisement(db_numberplate, body["id"])})
