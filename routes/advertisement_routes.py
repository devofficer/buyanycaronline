from sanic import Blueprint, Request, json
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
