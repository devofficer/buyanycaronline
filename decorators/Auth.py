from functools import wraps
from sanic import Request
from sanic.response import json
import jwt
from database.user_collection import UserDB
from common.utils import ConfigFile


async def decode_jwt_and_get_payload(request):
    try:
        payload = jwt.decode(request.token, ConfigFile.getInstance()['JWT']['SECRET'], algorithms="HS256")
        return payload
    except jwt.PyJWTError:
        return False


async def check_request_for_authentication_status(request):
    try:
        jwt.decode(request.token, ConfigFile.getInstance()['JWT']['SECRET'], algorithms="HS256")
    except jwt.PyJWTError:
        return False

    return True


async def check_request_for_admin_authorization_status(request):
    try:
        payload = jwt.decode(request.token, ConfigFile.getInstance()['JWT']['SECRET'], algorithms="HS256")
        username = payload['username']
        user = UserDB.get_user_by_id(username)
        parser = ConfigFile.getInstance()
        role = int(parser['ROLES']['ADMIN'])
        user_role = user.get_role()
        if user_role == role:
            return True
    except jwt.PyJWTError:
        return False
    return False


async def check_request_for_moderator_authorization_status(request: Request):
    try:
        payload = jwt.decode(request.token, ConfigFile.getInstance()['JWT']['SECRET'], algorithms="HS256")
        username = payload['username']
        user = UserDB.get_user_by_id(username)
        parser = ConfigFile.getInstance()
        role = int(parser['ROLES']['ADMIN'])
        user_role = user.get_role()
        role_mod = int(parser['ROLES']['MOD'])
        if user_role == role or user_role == role_mod:
            return True
    except jwt.PyJWTError:
        return False
    return False


def Authenticated():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authenticated = await check_request_for_authentication_status(request)

            if is_authenticated:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({"status": "not authenticated"}, 403)

        return decorated_function

    return decorator


def AuthorizedAdmin():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = await check_request_for_admin_authorization_status(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({"status": "not authenticated"}, 403)

        return decorated_function

    return decorator


def AuthorizedMod():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = await check_request_for_moderator_authorization_status(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({"status": "not authenticated"}, 403)

        return decorated_function

    return decorator
