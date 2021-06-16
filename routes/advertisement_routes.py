from sanic import Blueprint, Request, json

from common.enums import AdvertisementTypes
from database.advertisement_collection import AdvertisementDB
from decorators.Auth import *

advertisement_blue_print = Blueprint("advertisement_route_blueprint")


@advertisement_blue_print.get("/advertisement/unapproved")
@AuthorizedMod()
async def get_unapproved_ads(request: Request):
    pageNumber = request.args.get("pageNumber")
    nPerPage = request.args.get("nPerPage")
    return json(body=AdvertisementDB.get_unapproved_ads(int(pageNumber), int(nPerPage)))


@advertisement_blue_print.get("/advertisement/approve")
@AuthorizedMod()
async def get_unapproved_ads(request: Request):
    advertisementID = request.args.get("advertisementID")
    return json(body=AdvertisementDB.approve_advertisement(advertisementID))


@advertisement_blue_print.get("/advertisement/search")
async def search(request):
    page = int(request.args.get("page", "0"))
    advertisement_type = int(request.args.get('advertisementType', AdvertisementTypes.CAR.value))
    min_price = request.args.get('minPrice')
    max_price = request.args.get('maxPrice')

    if advertisement_type not in[AdvertisementTypes.CAR.value, AdvertisementTypes.BOAT.value, AdvertisementTypes.HEAVY.value,
                                 AdvertisementTypes.MOTORCYCLE.value]:
        return json({"Message": "Error, invalid advertisement type!"})

    result = AdvertisementDB.search(page, advertisement_type, min_price, max_price)

    return json(body=result)
