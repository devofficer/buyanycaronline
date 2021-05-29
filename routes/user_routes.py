from datetime import datetime, timedelta
from sanic import Blueprint
from decorators.Auth import *
from models.user_model import User
from database.user_collection import UserDB
from common.email import EmailClient

import jwt

user_blue_print = Blueprint("user_route_blueprint")


def generateJWT(user: User):
    exp = datetime.now() + timedelta(minutes=15)
    token = jwt.encode({"username": user.get_username(),
                        "role": user.get_role(),
                        "exp": exp.timestamp()},
                       ConfigFile.getInstance()['JWT']['SECRET'],
                       algorithm="HS256")
    return token


@user_blue_print.post("/user/create")
@AuthorizedAdmin()
async def create_user(request):
    body = request.json
    user = User(username=body["username"], role=body["role"], city=body["city"], country=body["country"],
                mobile=body["mobile"])
    user.set_hash(hashed=body["hashed"])
    return json(body={"Message": UserDB.create_user(user)})


@user_blue_print.post("/user/register")
async def register_user(request):
    body = request.json
    user = User(username=body["username"], city=body["city"], country=body["country"],
                mobile=body["mobile"])
    user.set_hash(hashed=body["hashed"])
    return json(body={"Message": UserDB.create_user(user)})


@user_blue_print.post("/user/login")
async def login_user(request):
    body = request.json
    user = UserDB.get_user_by_id(body["username"])
    if user.validate_hash(body["hashed"]):
        return json(body={"Message": "Logged in", "token": generateJWT(user)})
    else:
        return json(body={"Message": "Incorrect username or password"})


@user_blue_print.post("/user/update")
@Authenticated()
async def update_user(request):
    payload = await decode_jwt_and_get_payload(request)
    user = UserDB.get_user_by_id(payload['username'])
    for k, v in request.json['user'].items():
        if k == "username" or k == "role" or k == "hashed":
            continue
        if "_User__" + k in user.__dict__:
            user.__setattr__("_User__" + k, v)
    return json(body={"Message": UserDB.update_user(user)})


@user_blue_print.get("/user/reset-password-link")
async def reset_password(request: Request):
    conf = ConfigFile.getInstance()["SERVER"]
    username = request.args.get("username")
    user = UserDB.get_user_by_id(username)
    token = generateJWT(user)
    link = str(conf["PUBLIC_URI"])+"user/reset-password?token="+str(token)
    EmailClient.send_reset_password(link, username)
    return json(body={"Message": "Link sent"})
