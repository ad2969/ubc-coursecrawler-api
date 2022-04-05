from rest_framework import status

from .db import redis_instance
from api.utils.response import ResponseError

def getAll(institution: str, dataType: str = None):
    try:
        queryString = institution
        if dataType != None: queryString += f":{dataType}"

        keys = redis_instance.scan_iter(match=f"{queryString}:*")
        items = redis_instance.mget(*keys)
        count = len(items)
        
        return {
            "status": "SUCCESS",
            "code": status.HTTP_200_OK,
            "count": count,
            "msg": f"found {count} items",
            "data": items,
        }

    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "REDUS ERROR: GET",
            f"problem with getting {dataType} from redis -- {str(e)}"
        )

def getOne(institution: str, dataType: str, key: str):
    try:
        queryString = f"{institution}:{dataType}:{key}"
        value = redis_instance.get(queryString)

        if not value:
            return {
                "status": "SUCCESS",
                "code": status.HTTP_204_NO_CONTENT,
                "msg": f"key {queryString} not found",
                "data": None,
            }

        return {
            "status": "SUCCESS",
            "code": status.HTTP_200_OK,
            "msg": f"key {queryString} found",
            "data": value,
        }

    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "REDUS ERROR: GET",
            f"problem with getting {queryString} from redis -- {str(e)}"
        )

def setMultiple(institution: str, dataType: str, data: dict):
    try:
        queryString = f"{institution}:{dataType}"
        count = len(data)
        redis_instance.mset(data)

        return {
            "status": "SUCCESS",
            "code": status.HTTP_201_CREATED,
            "count": count,
            "msg": f"found {count} items",
            "data": None,
        }
    
    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "REDIS ERROR: SET",
            f"problem with setting multiple {queryString} to redis -- {str(e)}"
        )

def setOne(institution: str, dataType: str, key: str, body: str):
    try:
        queryString = f"{institution}:{dataType}:{key}"
        redis_instance.set(key, body)
    
    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "REDIS ERROR: SET",
            f"problem with setting {queryString} to redis -- {str(e)}"
        )

def deleteAll(institution: str, dataType: str, override = False):
    try:
        queryString = f"{institution}:{dataType}"
        key = queryString if override else f"{queryString}:*"
        keys = redis_instance.keys(key)
        count = len(keys)
        if count: redis_instance.delete(*keys)
        
        return {
            "status": "SUCCESS",
            "code": status.HTTP_205_RESET_CONTENT,
            "count": count,
            "msg": f"deleted {count} items",
            "data": None,
        }

    except Exception as e:
        raise ResponseError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "REDUS ERROR: DELETE",
            f"problem with deleting all {queryString} from redis -- {str(e)}"
        )
